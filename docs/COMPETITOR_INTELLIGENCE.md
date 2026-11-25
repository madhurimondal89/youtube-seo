# Competitor Intelligence Methodology & Limitations
### YouTube SEO & Creator Intelligence Platform (`seo.freeyoutubetools.com`)

This document outlines the techniques, permitted data sources, and analytical limitations used by the Competitor Intelligence and Outlier Discovery engines.

---

## 1. Permitted Data Sources

1. **YouTube Public RSS Feeds:**
   - Endpoint: `https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}`
   - Data extracted: Video ID, Title, Publication Timestamp, Media Description.
   - Zero authentication required, lawful and strictly read-only.

2. **Public HTML & Microformat Parser:**
   - Public view counts, channel subscriber counts, avatar and banner assets.
   - Paced requests with in-memory TTL caching to prevent server flooding.

3. **Official YouTube Data API v3 (Optional):**
   - Endpoints: `playlistItems.list(playlistId="UU...")` and `videos.list(part="statistics,snippet,contentDetails")`.
   - Used when the user configures their own Google API key.

---

## 2. Statistical Metrics & Algorithms

### A. Median Absolute Deviation (MAD) Outlier Engine
Why not use standard deviation or arithmetic mean?
- Traditional mean views ($\mu$) is distorted by a single viral video. If a channel averages 5,000 views per video but one hit 2,000,000 views, the mean is artificially skewed to 150,000 views.
- Our engine computes the **median baseline** ($\tilde{X}$) and **MAD**:
  $$\text{MAD} = \text{median}(|x_i - \tilde{X}|)$$
- Multipliers:
  - $\ge 10.0\text{x}$ median: **Viral Outlier** (Algorithmic browse breakout)
  - $\ge 5.0\text{x}$ median: **High Outlier** (Strong external or search driver)
  - $\ge 2.5\text{x}$ median: **Solid Outlier** (Reliable above-average topic)

### B. Content Gap Analysis
Identifies high-opportunity topics where:
1. Competitors receive high search traffic on a phrase.
2. The user's channel has not published a video covering that keyword.
3. The competition density in top results has weak exact-match title alignment.

### C. Publishing Pattern Analysis
- **Cadence & Day-of-Week Distribution:** Tracks publishing regularity (Monday–Sunday) to identify competitor upload schedules.
- **Shorts vs Long-form Ratio:** Distinguishes channels relying primarily on short-form discovery (<60s) from long-form depth channels.

---

## 3. Explicit Limitations & Non-Claims

- **No Private Competitor Analytics:** The platform NEVER claims access to competitor YouTube Studio dashboards, private CTR, average watch time, or RPM.
- **Estimated Upload Frequency:** Based on observable public video uploads within the sample window.
- **Directional Signals:** All outlier ratios and content gaps are directional research aids, not guarantees of algorithmic distribution.
