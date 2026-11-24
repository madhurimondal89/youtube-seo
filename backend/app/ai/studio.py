import re
from typing import Optional
from app.models.ai_dtos import (
    TitleIdea,
    DescriptionResponse,
    TagGenerationResponse,
    VideoHookItem,
    ContentCalendarDay,
    ContentCalendarResponse,
)
from app.seo.title_analyzer import analyze_title_heuristics
from app.ai.base import AIProvider

class AIStudioEngine:
    """
    Creator studio generation engine.
    Works seamlessly with local/cloud LLMs or with full deterministic heuristic fallbacks
    when AI is disabled or offline.
    """

    TITLE_TEMPLATES = [
        # How-to
        ("How to Master {keyword} (Step-by-Step for Beginners)", "How-to"),
        ("How I Scaled With {keyword} in 30 Days", "Case Study"),
        ("How to Do {keyword} Without Complicated Setups", "How-to"),
        # Contrarian
        ("Stop Doing {keyword} Like This! (Do This Instead)", "Contrarian"),
        ("The Harsh Truth About {keyword} in 2026", "Contrarian"),
        ("Why 95% of Creators Fail at {keyword}", "Contrarian"),
        # Numbered List
        ("7 Powerful {keyword} Strategies You Should Know", "Numbered List"),
        ("5 Costly {keyword} Mistakes to Avoid", "Numbered List"),
        ("3 Simple {keyword} Tweaks for Massive Results", "Numbered List"),
        # Blueprint / Authority
        ("The Ultimate {keyword} Blueprint (Zero to Mastery)", "Case Study"),
        ("{keyword}: The Only Guide You Need in 2026", "How-to"),
        ("The Secret to Fast {keyword} Growth Revealed", "Case Study"),
        # Comparison
        ("{keyword} vs Traditional Methods: Honest Verdict", "Contrarian"),
        ("Is {keyword} Still Worth It in 2026?", "Contrarian"),
    ]

    async def generate_title_ideas(
        self,
        topic: str,
        keyword: str,
        ai_provider: Optional[AIProvider] = None,
        count: int = 12
    ) -> list[TitleIdea]:
        k_clean = keyword.title().strip()
        t_clean = topic.title().strip()
        kw = k_clean if k_clean else t_clean
        
        titles: list[tuple[str, str]] = []

        # Check if AI provider is active
        ai_used = False
        if ai_provider and await ai_provider.is_available():
            prompt = (
                f"Generate {count} high-performing YouTube video title ideas for the topic '{t_clean}' "
                f"and keyword '{kw}'. Provide one title per line. Do not include numbering or quotes."
            )
            response = await ai_provider.generate_text(prompt, max_tokens=400)
            if response and not response.startswith("Ollama Error"):
                lines = [l.strip().lstrip("-*0123456789. ") for l in response.split("\n") if l.strip()]
                for line in lines[:count]:
                    if len(line) > 15:
                        titles.append((line, "AI Generated"))
                        ai_used = True

        if not ai_used or len(titles) < 5:
            # Deterministic heuristic template generation
            for t_pattern, style in self.TITLE_TEMPLATES[:count]:
                formatted = t_pattern.format(keyword=kw)
                titles.append((formatted, style))

        # Score every title deterministically
        results: list[TitleIdea] = []
        for raw_title, style in titles[:count]:
            h = analyze_title_heuristics(raw_title, target_keyword=kw)
            
            # Determine SEO relevance heuristic
            seo_rel = 90 if kw.lower() in raw_title.lower() else 65
            if h["frontloaded_keyword"]:
                seo_rel = min(100, seo_rel + 10)

            results.append(
                TitleIdea(
                    title=raw_title,
                    seo_relevance_heuristic=seo_rel,
                    curiosity_heuristic=h["curiosity_score"],
                    character_count=h["character_count"],
                    has_number=h["has_number"],
                    frontloaded_keyword=h["frontloaded_keyword"],
                    style=style,
                )
            )

        # Sort by combination of curiosity and SEO relevance
        results.sort(key=lambda x: (x.seo_relevance_heuristic * 0.5 + x.curiosity_heuristic * 0.5), reverse=True)
        return results

    async def generate_description(
        self,
        topic: str,
        target_keywords: list[str],
        call_to_action: str = "Subscribe for more practical creator guides",
        chapters_requested: bool = True
    ) -> DescriptionResponse:
        t_clean = topic.title().strip()
        kw_primary = target_keywords[0].title() if target_keywords else t_clean
        
        hook = f"Want to master {kw_primary.lower()} and get better results on YouTube? In this complete walkthrough, we break down actionable steps to build authority, save time, and avoid common pitfalls."
        
        chapters = ""
        if chapters_requested:
            chapters = (
                "📌 TIMESTAMPS / CHAPTERS:\n"
                "00:00 - Introduction to " + kw_primary + "\n"
                "01:45 - Key Foundations & Concepts\n"
                "04:20 - Step-by-Step Implementation Walkthrough\n"
                "08:10 - Common Mistakes to Avoid\n"
                "11:35 - Advanced Optimization & Best Practices\n"
                "14:00 - Summary & Next Steps"
            )

        cta_block = f"🔔 {call_to_action}\n💬 Let me know your biggest question in the comments below!"
        
        hashtags = [
            f"#{re.sub(r'[^a-zA-Z0-9]', '', kw_primary)}",
            "#YouTubeSEO",
            "#ContentCreator"
        ]
        
        full_desc = (
            f"{hook}\n\n"
            f"We dive deep into {t_clean}, covering practical frameworks that deliver real-world outcomes without unnecessary complexity.\n\n"
            f"{chapters}\n\n"
            f"{cta_block}\n\n"
            f"{' '.join(hashtags)}"
        )

        return DescriptionResponse(
            full_description=full_desc,
            hook_first_lines=hook,
            chapters_placeholder=chapters,
            suggested_hashtags=hashtags,
            keyword_coverage=[k for k in target_keywords if k.lower() in full_desc.lower()] or [kw_primary],
        )

    def generate_tags(self, title: str, topic: str, target_keyword: Optional[str] = None) -> TagGenerationResponse:
        primary = []
        secondary = []
        long_tail = []

        kw = (target_keyword or topic).lower().strip()
        primary.append(kw)
        
        words = [w.lower() for w in title.split() if len(w) > 3 and w.lower() not in ["with", "from", "that", "this"]]
        for w in words[:4]:
            if w != kw:
                secondary.append(f"{kw} {w}")

        secondary.extend([
            f"{kw} 2026",
            f"{kw} tutorial",
            f"{kw} guide",
            f"how to do {kw}"
        ])

        long_tail.extend([
            f"{kw} for beginners",
            f"best {kw} tips and tricks",
            f"{kw} step by step tutorial",
            f"how to get started with {kw}",
            f"{kw} mistakes to avoid"
        ])

        # Deduplicate
        all_tags = list(dict.fromkeys(primary + secondary + long_tail))
        char_count = sum(len(t) for t in all_tags) + len(all_tags)

        return TagGenerationResponse(
            primary_tags=primary[:3],
            secondary_tags=secondary[:6],
            long_tail_tags=long_tail[:6],
            total_tags=len(all_tags),
            char_count=char_count,
        )

    def generate_hooks(self, topic: str, target_audience: str) -> list[VideoHookItem]:
        t = topic.title().strip()
        return [
            VideoHookItem(
                hook_type="Contrarian / Pattern Interrupt",
                first_3_seconds=f"Most creators are doing {t} completely wrong.",
                next_15_seconds=f"They spend hours optimizing the wrong things, only to wonder why their videos get zero traction. In the next 8 minutes, I'll show you the exact system that actually works.",
                open_loop="And make sure to watch until the end, because the third tweak made the biggest difference in my tests."
            ),
            VideoHookItem(
                hook_type="Direct Promise / Problem First",
                first_3_seconds=f"If you're struggling with {t}, watch this first.",
                next_15_seconds=f"Today I'm sharing the exact step-by-step blueprint to master {t} without burning out or wasting weeks on trial and error.",
                open_loop="I'm even sharing the free template we used so you can implement this in 10 minutes."
            ),
            VideoHookItem(
                hook_type="Story / Case Study",
                first_3_seconds=f"This single change transformed our results with {t}.",
                next_15_seconds=f"Just 30 days ago, we tested an unconventional approach to {t}. The result was a 4x increase in viewer retention and search ranking.",
                open_loop="Here is the breakdown, starting with the counter-intuitive foundation."
            )
        ]

    def generate_content_calendar(self, topic: str, duration_days: int = 30) -> ContentCalendarResponse:
        t = topic.title().strip()
        items: list[ContentCalendarDay] = []
        
        cadence = 7 if duration_days <= 30 else 14
        num_videos = max(4, duration_days // cadence)

        types = ["Hero Pillar", "Evergreen Guide", "Trend / New Features", "Quick Win / Fix", "Comparison / Review"]
        intents = ["Tutorial", "Informational", "Problem/Fix", "Commercial", "Comparison"]

        for i in range(num_videos):
            day_num = (i * cadence) + 3
            c_type = types[i % len(types)]
            intent = intents[i % len(intents)]
            
            if c_type == "Hero Pillar":
                title = f"The Complete Guide to {t} (Zero to Hero Blueprint)"
                kw = f"{t.lower()} complete guide"
            elif c_type == "Quick Win / Fix":
                title = f"3 Simple {t} Fixes That Save 10 Hours a Week"
                kw = f"{t.lower()} tips"
            elif c_type == "Comparison / Review":
                title = f"Top 5 {t} Methods Ranked (Honest Comparison)"
                kw = f"best {t.lower()} tools"
            elif c_type == "Trend / New Features":
                title = f"{t} in 2026: What Changed and What Works Now"
                kw = f"{t.lower()} 2026"
            else:
                title = f"How to Build a Consistent System for {t}"
                kw = f"how to do {t.lower()}"

            items.append(
                ContentCalendarDay(
                    day=day_num,
                    title=title,
                    target_keyword=kw,
                    intent=intent,
                    content_type=c_type,
                    production_effort="High" if c_type == "Hero Pillar" else "Medium"
                )
            )

        return ContentCalendarResponse(
            duration_days=duration_days,
            schedule=items,
            strategy_summary=f"Balanced {duration_days}-day editorial calendar for '{t}' combining authority pillar content with frequent high-intent long-tail tutorials."
        )

ai_studio = AIStudioEngine()
