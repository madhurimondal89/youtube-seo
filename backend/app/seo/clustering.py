from collections import defaultdict
from app.models.keyword import KeywordMetricItem, TopicCluster

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
    "to", "was", "were", "will", "with", "youtube"
}

def cluster_keywords(keywords: list[KeywordMetricItem]) -> list[TopicCluster]:
    """
    Groups keywords into semantic clusters based on shared core nouns and qualifiers.
    Generates recommended pillar title, supporting videos, and playlist titles.
    """
    if not keywords:
        return []

    # Map core token -> list of keywords
    token_groups: dict[str, list[KeywordMetricItem]] = defaultdict(list)
    
    for item in keywords:
        tokens = [w for w in item.keyword.lower().split() if w not in STOP_WORDS and len(w) > 2]
        if not tokens:
            token_groups["general"].append(item)
            continue
        
        # Pick the most specific secondary token or primary token
        assigned = False
        for tok in tokens:
            if tok not in ["video", "channel", "how", "best", "2026", "guide"]:
                token_groups[tok].append(item)
                assigned = True
                break
        if not assigned:
            token_groups[tokens[0]].append(item)

    clusters: list[TopicCluster] = []

    for core_tok, items in token_groups.items():
        if len(items) < 2 and len(token_groups) > 3:
            # Skip tiny isolated clusters if we have enough groups
            continue

        # Sort by opportunity score descending
        sorted_items = sorted(items, key=lambda x: x.opportunity_score, reverse=True)
        main_kw = sorted_items[0].keyword
        supporting = [it.keyword for it in sorted_items[1:8]]
        avg_opp = int(sum(it.opportunity_score for it in sorted_items) / len(sorted_items))

        cluster_name = f"{core_tok.title()} Mastery"
        pillar_title = f"The Ultimate Guide to {core_tok.title()} (Complete Blueprint)"
        
        supporting_ideas = [
            f"How to Get Started with {main_kw.title()}",
            f"5 Costly Mistakes When Doing {core_tok.title()}",
            f"Top Tools for {main_kw.title()} in 2026",
            f"{main_kw.title()} vs Alternatives: Full Breakdown"
        ]

        clusters.append(
            TopicCluster(
                cluster_name=cluster_name,
                main_keyword=main_kw,
                supporting_keywords=supporting,
                related_entities=[core_tok, "YouTube Growth", "Workflow Optimization"],
                recommended_pillar_title=pillar_title,
                supporting_video_ideas=supporting_ideas,
                playlist_suggestion=f"{core_tok.title()} Step-by-Step Series",
                avg_opportunity_score=avg_opp,
            )
        )

    # Sort clusters by average opportunity score
    clusters.sort(key=lambda c: c.avg_opportunity_score, reverse=True)
    return clusters[:6]
