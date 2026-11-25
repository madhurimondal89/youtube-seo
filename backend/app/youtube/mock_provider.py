import hashlib
from typing import Optional
from app.youtube.base import YouTubeProvider
from app.models.video import VideoSearchResult, VideoMetadata
from app.models.channel import ChannelMetadata
from app.models.common import DataProvenance

class MockYouTubeProvider(YouTubeProvider):
    """
    Zero-network mock provider delivering realistic, deterministic data
    for unit testing, local development, and offline operation.
    """

    MODIFIERS = [
        "tutorial", "for beginners", "2026", "how to", "best tools",
        "vs code", "automation", "without code", "step by step", "tips and tricks",
        "case study", "review", "free course", "setup guide"
    ]

    async def get_autocomplete_suggestions(self, query: str, hl: str = "en", gl: str = "US") -> list[str]:
        q = query.strip().lower()
        results = [q]
        for mod in self.MODIFIERS:
            results.append(f"{q} {mod}")
        # Add alphabet expansion hints
        for char in ["ai", "app", "pro", "workflow"]:
            results.append(f"{q} {char}")
        return results[:15]

    async def search_videos(self, query: str, limit: int = 20) -> list[VideoSearchResult]:
        q = query.strip()
        seed_hash = int(hashlib.md5(q.encode()).hexdigest()[:8], 16)
        results: list[VideoSearchResult] = []

        channels = [
            ("TechPilot Academy", "UCmock_01", 340000),
            ("Creator Lab Pro", "UCmock_02", 125000),
            ("Code & Scale", "UCmock_03", 45000),
            ("Growth Hacks 2026", "UCmock_04", 12000),
            ("Indie Builder", "UCmock_05", 3500),
            ("AI Video Mastery", "UCmock_06", 89000),
            ("Automate Everything", "UCmock_07", 520000),
            ("The Solo Creator", "UCmock_08", 18500),
        ]

        for i in range(limit):
            chan_name, chan_id, subs = channels[i % len(channels)]
            vid_id = f"mock_{seed_hash % 10000}_{i:02d}"
            
            # Create a realistic view distribution with small creator breakout (outlier)
            if i == 3:
                views = 485000  # breakout video for small channel
            elif i == 0:
                views = 1200000 # top authority
            else:
                views = max(1200, (seed_hash * (i + 3) * 7919) % 350000)

            title_templates = [
                f"{q.title()}: Complete Step-by-Step Guide",
                f"How I Scaled With {q.title()} (Full Breakdown)",
                f"Top 7 {q.title()} Tools You Must Know in 2026",
                f"{q.title()} For Beginners: Do Not Make These Mistakes",
                f"Why Most People Fail at {q.title()} (And How to Fix It)",
                f"Stop Doing {q.title()} Like This! Better Alternative",
                f"{q.title()} vs Traditional Methods: Honest Comparison",
                f"Building a $10k System with {q.title()}",
            ]
            title = title_templates[i % len(title_templates)]
            
            results.append(
                VideoSearchResult(
                    video_id=vid_id,
                    title=title,
                    channel_name=chan_name,
                    channel_id=chan_id,
                    published_time_text=f"{(i * 5) + 2} days ago",
                    published_timestamp=1726000000 - (i * 86400 * 5),
                    views_count=views,
                    views_text=f"{views:,} views",
                    duration_text=f"{10 + (i % 15)}:{20 + (i * 3) % 40:02d}",
                    duration_seconds=(10 + (i % 15)) * 60 + 20,
                    thumbnail_url=f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg",
                    description_snippet=f"Everything you need to master {q}. In this video we cover key principles, actionable setups, and mistakes to avoid.",
                    rank_position=i + 1,
                    provenance=DataProvenance.PUBLIC,
                )
            )
        return results

    async def get_video_details(self, video_id: str) -> Optional[VideoMetadata]:
        vid_num = sum(ord(c) for c in video_id)
        views = 145000 + (vid_num * 123) % 400000
        likes = int(views * 0.042)
        comments = int(views * 0.0035)

        return VideoMetadata(
            video_id=video_id,
            url=f"https://www.youtube.com/watch?v={video_id}",
            title="Complete YouTube SEO Mastery Guide (Ranking Step-by-Step)",
            description=(
                "Master YouTube SEO in 2026 with proven keyword research, title psychology, and metadata strategies.\n\n"
                "📌 In this video:\n"
                "00:00 - Introduction to YouTube SEO\n"
                "02:15 - Keyword Research & Expansion\n"
                "05:40 - Title & Thumbnail Psychology\n"
                "09:12 - Description & Tag Best Practices\n"
                "12:50 - Measuring CTR and Audience Retention\n\n"
                "🔔 Subscribe for weekly actionable guides!\n"
                "#YouTubeSEO #ContentCreator #VideoMarketing"
            ),
            channel_id="UCmock_creator_01",
            channel_name="Creator Studio Pro",
            channel_subscribers=85000,
            published_date="2026-03-15",
            views_count=views,
            likes_count=likes,
            comments_count=comments,
            duration_seconds=925,
            tags=[
                "youtube seo", "youtube seo 2026", "keyword research",
                "how to rank youtube videos", "video marketing",
                "youtube algorithm", "creator studio"
            ],
            thumbnail_url=f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            has_chapters=True,
            provenance=DataProvenance.PUBLIC,
        )

    async def get_channel_details(self, channel_id_or_handle: str) -> Optional[ChannelMetadata]:
        return ChannelMetadata(
            channel_id=channel_id_or_handle if channel_id_or_handle.startswith("UC") else "UCmock_channel_888",
            channel_title="Authority Tech Creator",
            handle="@authoritytech" if not channel_id_or_handle.startswith("@") else channel_id_or_handle,
            description="Helping creators scale high-impact channels using automation, data-driven SEO, and workflow intelligence.",
            subscriber_count=145000,
            video_count=180,
            view_count=12400000,
            avatar_url="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=120&h=120&fit=crop",
            banner_url="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200&h=300&fit=crop",
            provenance=DataProvenance.PUBLIC,
        )

    async def get_channel_recent_videos(self, channel_id: str, limit: int = 30) -> list[VideoMetadata]:
        videos: list[VideoMetadata] = []
        base_views = [
            18000, 22000, 19500, 24000, 21000, 17500, 23000,
            580000, # viral outlier (28x baseline)
            20500, 25000, 19000, 22500, 18500, 21500, 85000, # moderate outlier (4x)
            20000, 19800, 23500, 21200, 18900
        ]
        
        for i in range(min(limit, len(base_views))):
            v_views = base_views[i]
            vid_id = f"mock_chan_{i:03d}"
            videos.append(
                VideoMetadata(
                    video_id=vid_id,
                    url=f"https://www.youtube.com/watch?v={vid_id}",
                    title=f"Video #{i+1}: Advanced Topic Optimization and Case Study {i+1}",
                    description=f"Detailed walkthrough of technique #{i+1} covering practical application and metrics.",
                    channel_id=channel_id,
                    channel_name="Authority Tech Creator",
                    channel_subscribers=145000,
                    published_date=f"2026-0{(i % 6) + 1}-10",
                    views_count=v_views,
                    likes_count=int(v_views * 0.045),
                    comments_count=int(v_views * 0.004),
                    duration_seconds=600 + (i * 35),
                    tags=["tutorial", "guide", "creator tools", "seo"],
                    thumbnail_url=f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg",
                    has_chapters=True,
                    provenance=DataProvenance.PUBLIC,
                )
            )
        return videos
