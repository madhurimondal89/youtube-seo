from pydantic import BaseModel
from typing import List, Optional
import json

class CoachVideoPlan(BaseModel):
    day: int
    format: str  # "Long-form Pillar" or "YouTube Short"
    title: str
    target_keyword: str
    hook_script: str
    thumbnail_concept: str
    script_structure: List[str]

class CoachWeekPlan(BaseModel):
    week_number: int
    theme: str
    milestone_objective: str
    videos: List[CoachVideoPlan]

class GrowthStrategyResponse(BaseModel):
    niche: str
    channel_name: Optional[str] = None
    language: str
    executive_summary: str
    target_audience_profile: str
    weeks: List[CoachWeekPlan]
    publishing_checklist: List[str]
    weekly_review_metrics: List[str]
    data_provenance: str = "Deterministic Framework"

async def generate_growth_strategy(
    niche: str,
    channel_name: Optional[str] = None,
    language: str = "English",
    ai_provider=None
) -> GrowthStrategyResponse:
    # 1. Check if AI Provider is active
    if ai_provider and await ai_provider.is_available():
        system_prompt = (
            "You are a world-class YouTube Growth Coach & Algorithm Strategist. "
            "Generate a hyper-practical, high-retention 30-day YouTube growth plan in JSON format. "
            "Never invent fake analytics. Return pure JSON matching the requested schema."
        )
        prompt = f"""
Create a 30-day YouTube growth roadmap for:
- Niche: {niche}
- Channel Name: {channel_name or 'Creator Channel'}
- Language/Region: {language}

Return a valid JSON object with:
{{
  "executive_summary": "...",
  "target_audience_profile": "...",
  "weeks": [
    {{
      "week_number": 1,
      "theme": "...",
      "milestone_objective": "...",
      "videos": [
        {{
          "day": 3,
          "format": "Long-form Pillar",
          "title": "...",
          "target_keyword": "...",
          "hook_script": "First 10s retention hook...",
          "thumbnail_concept": "Visual description...",
          "script_structure": ["Hook", "Setup", "Revelation", "CTA"]
        }}
      ]
    }}
  ],
  "publishing_checklist": ["..."],
  "weekly_review_metrics": ["..."]
}}
"""
        try:
            raw = await ai_provider.generate_text(prompt, system_prompt=system_prompt, max_tokens=1500)
            clean_json = raw.strip()
            if clean_json.startswith("```"):
                clean_json = clean_json.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            data = json.loads(clean_json)
            
            weeks_parsed = []
            for w in data.get("weeks", []):
                vids = [CoachVideoPlan(**v) for v in w.get("videos", [])]
                weeks_parsed.append(CoachWeekPlan(
                    week_number=w.get("week_number", 1),
                    theme=w.get("theme", ""),
                    milestone_objective=w.get("milestone_objective", ""),
                    videos=vids
                ))
                
            return GrowthStrategyResponse(
                niche=niche,
                channel_name=channel_name,
                language=language,
                executive_summary=data.get("executive_summary", f"30-Day Growth Plan for {niche}"),
                target_audience_profile=data.get("target_audience_profile", "Target viewers seeking deep value & engaging storytelling."),
                weeks=weeks_parsed,
                publishing_checklist=data.get("publishing_checklist", []),
                weekly_review_metrics=data.get("weekly_review_metrics", []),
                data_provenance="AI-Generated (Verified Framework)"
            )
        except Exception:
            # Fall back to algorithmic engine if parsing or API fails
            pass

    # 2. High-Fidelity Deterministic Algorithmic Generator
    is_bengali = "bengali" in language.lower() or "bangla" in language.lower()
    
    # Contextual tailoring for Mystery/History
    is_mystery = any(w in niche.lower() for w in ["mystery", "history", "rahasya", "crime", "unsolved", "itihas"])
    
    if is_bengali and is_mystery:
        summary = (
            f"বাংলায় {niche} বিষয়ক চ্যানেলের জন্য ৩০ দিনের শ্রোতা-আকর্ষণ স্ট্র্যাটেজি। "
            "প্রথম ২ সপ্তাহে উচ্চ সার্চ চাহিদাসম্পন্ন ঐতিহাসিক রহস্য দিয়ে অডিয়েন্স বেস তৈরি করা হবে এবং শেষ ২ সপ্তাহে অরিজিনাল থিওরি ও শর্টস হুক দিয়ে এভারেজ পার্সেন্টেজ ভিউড (APV) বাড়ানো হবে।"
        )
        audience = (
            "১৮-৩৪ বছর বয়সী বাঙালি দর্শক যারা ইতিহাস, লোককথা, অমীমাংসিত রহস্য এবং বাস্তব তদন্তমূলক তথ্যচিত্র পছন্দ করেন। "
            "এদের জন্য মূল ফ্যাক্টর হলো: গভীর আবহ সঙ্গীত, আকস্মিক প্রশ্নের হুক এবং প্রামাণ্য তথ্যের রেফারেন্স।"
        )
        w1_v1 = CoachVideoPlan(
            day=3,
            format="Long-form Pillar (12-18 min)",
            title=f"{niche}: ইতিহাসের সবচেয়ে গোপন অমীমাংসিত সত্য যা কেউ বলেনি",
            target_keyword=f"{niche.lower()} documentary bangla",
            hook_script="আজ থেকে ঠিক ১২০ বছর আগে যা ঘটেছিল, তা জানলে আপনি কোনোদিন রাতের অন্ধকারে একা থাকতে পারবেন না...",
            thumbnail_concept="কালো-ধূসর ব্যাকগ্রাউন্ডে ঐতিহাসিক পুরনো দলিলের ওপর লাল রক্তের ছাপ, একপাশে আঁধার ঘেরা মুখের সিলুয়েট। বড় বোল্ড ফন্টে: 'অমিমাংসিত সত্য' (হলুদ ও সাদা রঙে)।",
            script_structure=["০-১৫ সেকেন্ড: কোল্ড ওপেনিং হুক", "১৫-৪৫ সেকেন্ড: ঐতিহাসিক প্রেক্ষাপট", "১-৮ মিনিট: প্রথম ৩টি অদ্ভুত প্রমাণ", "৮-১৫ মিনিট: গোপন নথির অমীমাংসিত ক্লাইম্যাক্স", "১৫-১৮ মিনিট: দর্শকের মতামত আহ্বান ও সিটিএ"]
        )
        w1_v2 = CoachVideoPlan(
            day=6,
            format="YouTube Short (45s Hook)",
            title="এই গোপন নথিটি ব্রিটিশরা কেন লুকিয়ে ফেলেছিল? #shorts",
            target_keyword="bangla history mystery shorts",
            hook_script="একটি ফাইল যা কোনো ইতিহাস বইয়ে নেই—কেন এটা মুছে ফেলা হয়েছিল?",
            thumbnail_concept="পুরনো লাল সিলমোহর লাগানো ব্রিটিশ ফাইল, সেন্টারে প্রশ্নচিহ্ন।",
            script_structure=["০-৩ সেকেন্ড: দ্রুত প্রশ্ন", "৩-৩০ সেকেন্ড: ৩টি অদ্ভুত সত্য", "৩০-৪৫ সেকেন্ড: লং ভিডিওর রেফারেন্স ও সাবস্ক্রাইব"]
        )
        w2_v1 = CoachVideoPlan(
            day=10,
            format="Long-form Pillar (15 min)",
            title="রহস্যময় প্রাচীন দুর্গের নিচে লুকিয়ে থাকা সত্য: তদন্তমূলক রিপোর্ট",
            target_keyword="bangla historical mystery report",
            hook_script="আজ আমরা এমন এক জায়গায় প্রবেশ করছি যেখানে গত ৫০ বছর ধরে সাধারণ মানুষের প্রবেশ নিষিদ্ধ...",
            thumbnail_concept="ভাঙা প্রাচীন দুর্গের গেটে টর্চের আলো ফেলা, কোনায় লাল সতর্কবার্তা বাতি। বোল্ড টেক্সট: 'নিষিদ্ধ এলাকা'।",
            script_structure=["০-২০ সেকেন্ড: অন-লোকেশন বা ভিজ্যুয়াল হুক", "২০ সেকেন্ড-৩ মিনিট: দুর্গের ইতিহাস ও ট্র্যাজেডি", "৩-১০ মিনিট: প্রত্যক্ষদর্শীদের বিবরণ ও আর্কিওলজিক্যাল তথ্য", "১০-১৫ মিনিট: শেষ সিদ্ধান্ত ও প্রশ্ন"]
        )
        w2_v2 = CoachVideoPlan(
            day=13,
            format="YouTube Short (50s Fact)",
            title="এই প্রাচীন দুর্গের ৩টি ভয়ঙ্কর রহস্য! #shorts",
            target_keyword="historical facts shorts",
            hook_script="আপনি কি জানেন এই দুর্গের নিচে কী আবিষ্কৃত হয়েছিল?",
            thumbnail_concept="উজ্জ্বল আলোয় দুর্গের গোপন সুড়ঙ্গ।",
            script_structure=["০-৫ সেকেন্ড: হুক", "৫-৪০ সেকেন্ড: দ্রুত ৩টি ফ্যাক্ট", "৪০-৫০ সেকেন্ড: পিন কমেন্ট ও লিঙ্ক"]
        )
        w3_v1 = CoachVideoPlan(
            day=17,
            format="Long-form Investigation (14 min)",
            title="হারিয়ে যাওয়া কাফেলার রহস্য: আসল সত্য কী ছিল?",
            target_keyword="unsolved mysteries in bengali",
            hook_script="১০০ জন মানুষ এক রাতে মরুভূমির বুক থেকে কোথায় মিলিয়ে গেল? আজ সব ফাইল উন্মুক্ত...",
            thumbnail_concept="মরুভূমির বালির ওপর পড়ে থাকা পুরনো কম্পাস ও মানচিত্র। বোল্ড টেক্সট: 'কোথায় গেল তারা?'",
            script_structure=["০-১৫ সেকেন্ড: আকস্মিক উধাও হওয়ার গল্প", "১৫-৬০ সেকেন্ড: মানচিত্র ও টাইমলাইন", "১-১১ মিনিট: ৪টি সম্ভাব্য থিওরি বিশ্লেষণ", "১১-১৪ মিনিট: সবচেয়ে নির্ভরযোগ্য থিওরি ও কনক্লুশন"]
        )
        w3_v2 = CoachVideoPlan(
            day=20,
            format="YouTube Short (40s)",
            title="১০০ জন মানুষ এক রাতে কোথায় মিলিয়ে গেল? #shorts",
            target_keyword="mystery shorts bangla",
            hook_script="এই ঘটনাটি শতাব্দীর সবচেয়ে বড় বিস্ময়...",
            thumbnail_concept="মানচিত্রের ওপর লাল ক্রস দাগ।",
            script_structure=["০-৩ সেকেন্ড: প্রশ্ন", "৩-৩৫ সেকেন্ড: ঘটনার চমক", "৩৫-৪০ সেকেন্ড: সাবস্ক্রাইব"]
        )
        w4_v1 = CoachVideoPlan(
            day=24,
            format="Series Finale / Mega Documentary (20 min)",
            title=f"বাংলার সবচেয়ে রোমাঞ্চকর রহস্য: পূর্ণাঙ্গ তথ্যচিত্র | {niche}",
            target_keyword="bangla full documentary mystery",
            hook_script="আজকের ভিডিওটি কোনো গল্প নয়—এটি বহু বছরের গবেষণার নির্যাস...",
            thumbnail_concept="সিনেমাটিক মুভি পোস্টার স্টাইল: তিনটি ঐতিহাসিক ঘটনার কোলাজ, নিচে বড় ফন্টে 'চূড়ান্ত সত্য'।",
            script_structure=["০-৩০ সেকেন্ড: মেগা প্রিভিউ ট্রেলার", "৩০ সেকেন্ড-৫ মিনিট: পার্ট ১ - প্রথম অধ্যায়", "৫-১৫ মিনিট: পার্ট ২ - লুকানো সত্য ও প্রমাণ", "১৫-২০ মিনিট: পার্ট ৩ - ভবিষ্যৎ রহস্য ও কমিউনিটি ডিসকাশন"]
        )
        w4_v2 = CoachVideoPlan(
            day=28,
            format="Community Q&A / Behind the Scenes",
            title="দর্শকদের সেরা ৫টি রহস্য থিওরি যাচাই করলাম!",
            target_keyword="mystery theories breakdown",
            hook_script="গত এক মাসে আপনারা যে প্রশ্নগুলো পাঠিয়েছেন, তার উত্তর খুঁজতে গিয়ে আমরা অবাক হয়ে গেছি...",
            thumbnail_concept="দর্শকদের স্ক্রিনশট কমেন্ট ও পাশে প্রশ্নচিহ্ন।",
            script_structure=["০-১৫ সেকেন্ড: দর্শকদের কমেন্ট দেখানো", "১৫ সেকেন্ড-৮ মিনিট: ৫টি থিওরি এক্সপ্লেইন", "৮-১০ মিনিট: আগামী মাসের মেগা প্রজেক্টের ঘোষণা"]
        )
    else:
        # Universal English / Multi-niche template
        summary = (
            f"30-day algorithmic audience building strategy for {niche}. "
            "Weeks 1-2 build search authority through high-intent problem-solving pillars. "
            "Weeks 3-4 leverage browse feed curiosity hooks and short-form funneling to maximize subscriber conversion."
        )
        audience = (
            f"Active viewers interested in {niche}. Core drivers: actionable insights, "
            "compelling visual pacing (new cut every 4-6 seconds), high contrast thumbnails, and fast value delivery."
        )
        w1_v1 = CoachVideoPlan(
            day=3,
            format="Long-form Pillar (10-15 min)",
            title=f"The Complete Guide to {niche} (What Nobody Tells You)",
            target_keyword=f"best guide {niche.lower()}",
            hook_script="If you want to master this in 2026, stop making these 3 mistakes immediately...",
            thumbnail_concept="Split-screen contrast: 'Wrong Way' (dim with red X) vs 'Right Way' (sharp with green tick). 3-4 bold words.",
            script_structure=["0-15s: High-stakes hook", "15-60s: Roadmap overview", "1-8m: Step-by-step breakdown", "8-12m: Advanced nuances", "12-15m: Summary & lead magnet CTA"]
        )
        w1_v2 = CoachVideoPlan(
            day=6,
            format="YouTube Short (45s)",
            title=f"Never Do This in {niche}! #shorts",
            target_keyword=f"{niche.lower()} tips shorts",
            hook_script="Stop doing this right now if you want fast results...",
            thumbnail_concept="Close-up emotional expression with a warning icon.",
            script_structure=["0-3s: Immediate action stop", "3-35s: 1 game-changing tip", "35-45s: Watch full video link"]
        )
        w2_v1 = CoachVideoPlan(
            day=10,
            format="Long-form Comparison (12 min)",
            title=f"Top 5 {niche} Strategies Tested (Which One Actually Works?)",
            target_keyword=f"{niche.lower()} comparison review",
            hook_script="I tested all 5 popular methods for 14 days so you don't have to waste time...",
            thumbnail_concept="Tier list or side-by-side battle card with bold score overlay.",
            script_structure=["0-20s: Challenge context", "20s-2m: Method 1 & 2 test", "2-8m: Surprising results", "8-12m: The definitive winner"]
        )
        w2_v2 = CoachVideoPlan(
            day=13,
            format="YouTube Short (35s)",
            title=f"The #1 Secret in {niche} You Missed #shorts",
            target_keyword=f"{niche.lower()} hacks",
            hook_script="Here is the one setting 90% of creators ignore...",
            thumbnail_concept="Pointer arrow pointing to a hidden setting.",
            script_structure=["0-3s: Hook", "3-25s: Direct reveal", "25-35s: CTA"]
        )
        w3_v1 = CoachVideoPlan(
            day=17,
            format="Deep-Dive Case Study (14 min)",
            title=f"How One Simple Tweak Changed Everything in {niche}",
            target_keyword=f"{niche.lower()} case study",
            hook_script="This single insight doubled performance in less than 30 days...",
            thumbnail_concept="Growth graph climbing steeply with an annotated breakout circle.",
            script_structure=["0-15s: Before vs After snapshot", "15s-3m: The breakthrough moment", "3-10m: Replication guide", "10-14m: Actionable checklist"]
        )
        w3_v2 = CoachVideoPlan(
            day=20,
            format="YouTube Short (40s)",
            title="3 Things I Wish I Knew Sooner! #shorts",
            target_keyword=f"{niche.lower()} mistakes",
            hook_script="If I had to start over again, here are 3 things I'd change...",
            thumbnail_concept="Bold numbers 1, 2, 3 highlighted in neon.",
            script_structure=["0-3s: Hook", "3-30s: 3 quick points", "30-40s: Subscribe callout"]
        )
        w4_v1 = CoachVideoPlan(
            day=24,
            format="Ultimate Blueprint (18 min)",
            title=f"The 2026 {niche} Masterclass: Zero to Pro",
            target_keyword=f"{niche.lower()} masterclass complete",
            hook_script="Everything you need to succeed in one definitive documentary-style guide...",
            thumbnail_concept="Cinematic studio lighting with bold gold title: 'MASTERCLASS 2026'.",
            script_structure=["0-30s: Cinematic sizzle reel", "30s-6m: Pillar 1 Foundation", "6-12m: Pillar 2 Execution", "12-18m: Pillar 3 Mastery"]
        )
        w4_v2 = CoachVideoPlan(
            day=28,
            format="Community Q&A / Review (10 min)",
            title=f"Audience Q&A: Answering Your Hardest {niche} Questions",
            target_keyword=f"{niche.lower()} questions answered",
            hook_script="You asked, I'm answering raw and unfiltered...",
            thumbnail_concept="Viewer comment cards floating with live reaction.",
            script_structure=["0-15s: Intro", "15s-8m: Top 5 community questions", "8-10m: Next month roadmap preview"]
        )

    weeks = [
        CoachWeekPlan(week_number=1, theme="Foundation & High-Demand Pillar Launch", milestone_objective="Establish search baseline & capture intent traffic", videos=[w1_v1, w1_v2]),
        CoachWeekPlan(week_number=2, theme="Curiosity & Retention Deep-Dive", milestone_objective="Boost Average View Duration (AVD) above 45%", videos=[w2_v1, w2_v2]),
        CoachWeekPlan(week_number=3, theme="Trending Angles & Audience Exploration", milestone_objective="Break into YouTube Suggested & Browse algorithms", videos=[w3_v1, w3_v2]),
        CoachWeekPlan(week_number=4, theme="Authority Anchor & Community Retention", milestone_objective="Convert casual search viewers into loyal subscribers", videos=[w4_v1, w4_v2]),
    ]
    
    checklist = [
        "First 10 Seconds: Never start with an animated channel intro. Deliver the hook immediately.",
        "Thumbnail Safety: Keep faces and critical text out of the bottom-right corner (timestamp zone).",
        "Description Link Structure: Put the primary call-to-action link in lines 1-2 above the 'Show more' fold.",
        "Pinned Comment: Post an engaging open-ended question in the pinned comment within 10 minutes of upload.",
        "Shorts Funnel: In every YouTube Short, use the 'Related video' feature to route mobile viewers directly to your long-form pillar.",
        "Sound Design: Maintain background music at -24dB to -28dB so narration stays crisp and legible on phone speakers."
    ]
    
    metrics = [
        "CTR Benchmark: Target 6.0% - 10.0% Click-Through Rate within the first 48 hours.",
        "Average Percentage Viewed (APV): Strive for >40% on 12-minute+ videos and >55% on videos under 8 minutes.",
        "End Screen CTR: Target >3.5% clicks on your recommended next video.",
        "Browse / Suggested Ratio: Aim for Browse Features to exceed Search traffic by Week 4 as audience authority builds."
    ]
    
    return GrowthStrategyResponse(
        niche=niche,
        channel_name=channel_name,
        language=language,
        executive_summary=summary,
        target_audience_profile=audience,
        weeks=weeks,
        publishing_checklist=checklist,
        weekly_review_metrics=metrics,
        data_provenance="Deterministic Algorithmic Framework"
    )
