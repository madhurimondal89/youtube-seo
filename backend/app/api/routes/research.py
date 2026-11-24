import time
from fastapi import APIRouter, Query, HTTPException
from app.models.keyword import (
    KeywordResearchRequest,
    KeywordResearchResponse,
    KeywordMetricItem,
)
from app.models.common import DataProvenance
from app.youtube.factory import get_youtube_provider
from app.seo.keyword_engine import expand_keywords, calculate_specificity_score, normalize_keyword
from app.seo.intent import classify_search_intent
from app.seo.competition import calculate_estimated_competition
from app.seo.opportunity import calculate_relative_demand, calculate_opportunity_score
from app.seo.clustering import cluster_keywords
from app.core.cache import cache
from app.core.security import sanitize_keyword

router = APIRouter(prefix="/research", tags=["Research"])

@router.post("/keyword", response_model=KeywordResearchResponse)
async def research_keyword(req: KeywordResearchRequest):
    t0 = time.time()
    clean_seed = sanitize_keyword(req.seed)
    if not clean_seed:
        raise HTTPException(status_code=400, detail="Seed keyword cannot be empty.")

    cache_key = f"kw_res_{clean_seed}_{req.include_alphabet_expansion}_{req.max_keywords}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    provider = get_youtube_provider()

    # 1. Expand keywords
    expanded = await expand_keywords(
        seed=clean_seed,
        provider=provider,
        include_alphabet=req.include_alphabet_expansion,
        include_modifiers=req.include_modifiers,
        include_questions=req.include_questions,
        include_comparisons=req.include_comparisons,
        max_keywords=req.max_keywords
    )

    # 2. Get top SERP evidence for seed to inform overall landscape
    serp_evidence = await provider.search_videos(clean_seed, limit=15)

    # 3. Process each expanded keyword deterministically
    keyword_metrics: list[KeywordMetricItem] = []
    
    for idx, kw in enumerate(expanded):
        intents = classify_search_intent(kw)
        specificity = calculate_specificity_score(kw)
        
        # Rank in autocomplete for relative demand calculation
        auto_rank = idx + 1 if idx < 10 else None
        rel_demand = calculate_relative_demand(
            keyword=kw,
            root_query=clean_seed,
            autocomplete_rank=auto_rank,
            serp_results=serp_evidence
        )

        comp_score, comp_breakdown, comp_reasons = calculate_estimated_competition(kw, serp_evidence)
        opp_score, opp_breakdown, opp_reasons = calculate_opportunity_score(
            keyword=kw,
            relative_demand=rel_demand,
            estimated_competition=comp_score,
            specificity=specificity,
            intents=intents,
            serp_results=serp_evidence
        )

        all_breakdown = {**comp_breakdown, **opp_breakdown}
        all_reasons = list(dict.fromkeys(comp_reasons + opp_reasons))

        keyword_metrics.append(
            KeywordMetricItem(
                keyword=kw,
                intents=intents,
                search_surface="YouTube Autocomplete",
                relative_demand=rel_demand,
                estimated_competition=comp_score,
                opportunity_score=opp_score,
                freshness_score=int(opp_breakdown.get("freshness", 50)),
                specificity_score=specificity,
                word_count=len(kw.split()),
                char_count=len(kw),
                provenance=DataProvenance.CALCULATED,
                score_breakdown=all_breakdown,
                reasons=all_reasons,
            )
        )

    # 4. Generate Topic Clusters
    clusters = cluster_keywords(keyword_metrics)

    # 5. Top Opportunity ranking
    top_opp = sorted(keyword_metrics, key=lambda x: x.opportunity_score, reverse=True)[:10]

    elapsed = round((time.time() - t0) * 1000, 1)

    response = KeywordResearchResponse(
        seed=clean_seed,
        total_found=len(keyword_metrics),
        keywords=keyword_metrics,
        clusters=clusters,
        top_opportunity_keywords=top_opp,
        data_provenance=DataProvenance.CALCULATED,
        execution_time_ms=elapsed,
    )

    cache.set(cache_key, response, ttl_seconds=600)
    return response

@router.get("/suggest")
async def get_raw_suggestions(q: str = Query(..., min_length=1, max_length=100)):
    clean_q = sanitize_keyword(q)
    provider = get_youtube_provider()
    suggestions = await provider.get_autocomplete_suggestions(clean_q)
    return {
        "query": clean_q,
        "suggestions": suggestions,
        "count": len(suggestions),
        "provenance": DataProvenance.PUBLIC.value
    }
