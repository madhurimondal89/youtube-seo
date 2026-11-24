# Mathematical Specification for TubePilot AI Deterministic Scoring Engines

All scores in TubePilot AI are **100% reproducible, deterministic, and statistical**.
**LLMs NEVER generate, calculate, or hallucinate numerical scores.**
If an input signal is missing or unavailable, it is recorded as `null` / `Unavailable` with clear data provenance, rather than being substituted with fake zeros or synthetic assumptions.

---

## 1. Data Provenance Classification
Every signal and output is categorized under one of the following provenance types:
- `Official`: Directly from YouTube Data API v3 (e.g. video views, upload timestamp).
- `Public`: Publicly observable on YouTube web surface (e.g. search suggestions, public watch page metadata).
- `Calculated`: Deterministically derived via mathematical formulas from public/official signals.
- `Estimated`: Heuristic approximation based on transparent observable indicators (e.g., Estimated Competition).
- `Relative`: Comparative ordinal/normalized scale (e.g. Relative Demand Index 0–100, where 100 is peak observed suggestion velocity).
- `Unavailable`: Explicitly absent signal; omitted from formula denominators to prevent distortion.

---

## 2. Relative Demand Index ($D_{rel}$)
### Purpose
YouTube does not disclose private monthly search volumes. TubePilot AI measures **Relative Demand** by analyzing search suggestion presence, suggestion rank order, modifier breadth, and keyword character length.

### Formula
$$D_{rel} = \min\left(100, \max\left(0, w_r \cdot S_{rank} + w_m \cdot S_{mod} + w_s \cdot S_{exact} + w_p \cdot S_{presence}\right)\right)$$

Where:
- $S_{rank} \in [0, 100]$: Suggestion Position Score.
  If the keyword appears at position $k \in [1, 10]$ in root autocomplete:
  $$S_{rank} = \max(0, 100 - (k - 1) \cdot 10)$$
  If not present in root autocomplete, $S_{rank} = 20$.
- $S_{mod} \in [0, 100]$: Modifier Breadth.
  Percentage of standard search intents (how, what, best, vs, tutorial, 2026) yielding this query in autocomplete.
  $$S_{mod} = \left(\frac{N_{\text{active modifiers}}}{N_{\text{tested modifiers}}}\right) \times 100$$
- $S_{exact} \in [0, 100]$: Exact Match Ratio in top SERP titles.
  $$S_{exact} = \left(\frac{\sum_{i=1}^{M} \mathbb{I}(\text{keyword in Title}_i)}{M}\right) \times 100 \quad (M \le 20)$$
- $S_{presence} \in [0, 100]$: Character brevity bonus (shorter root queries generally indicate broader search volume):
  $$S_{presence} = \max\left(0, 100 - 2 \cdot \max(0, \text{len(query)} - 10)\right)$$

### Default Weights
- $w_r = 0.40$ (Suggestion Rank)
- $w_m = 0.30$ (Modifier Breadth)
- $w_s = 0.20$ (SERP Title Match)
- $w_p = 0.10$ (Search Surface Brevity)

---

## 3. Estimated Competition Score ($C_{est}$)
### Purpose
Evaluates how difficult it is for a new or average creator to rank on the first page of search results for a given query.
Scale: `0` (Zero competition / wide open) to `100` (Extremely saturated by massive authoritative channels).

### Formula
$$C_{est} = \sum_{j=1}^{5} w_j \cdot C_j$$

Where:
1. **$C_{\text{authority}}$ (Channel Authority Saturation, weight $w_1 = 0.30$):**
   Proportion of top 20 ranking videos belonging to channels with $> 100,000$ subscribers (or $> 500,000$ median views).
   $$C_{\text{authority}} = \left(\frac{\sum_{i=1}^{N} \mathbb{I}(\text{Subs}_i \ge 100k)}{N}\right) \times 100$$
2. **$C_{\text{views}}$ (Median Views Density, weight $w_2 = 0.25$):**
   Logarithmic scaling of median views $V_{\text{med}}$ among top results:
   $$C_{\text{views}} = \min\left(100, \max\left(0, \frac{\log_{10}(V_{\text{med}} + 1) - 2.0}{4.0} \times 100\right)\right)$$
   *(Maps 100 views $\to 0$, 10,000 views $\to 50$, 1,000,000+ views $\to 100$)*
3. **$C_{\text{density}}$ (Exact Keyword Match in Top 10 Titles, weight $w_3 = 0.20$):**
   $$C_{\text{density}} = \left(\frac{\sum_{i=1}^{10} \mathbb{I}(\text{token\_overlap} \ge 0.8)}{10}\right) \times 100$$
4. **$C_{\text{age}}$ (SERP Incumbency / Age Barrier, weight $w_4 = 0.15$):**
   Median age of top 10 ranking videos $A_{\text{med}}$ in days:
   $$C_{\text{age}} = \min\left(100, \frac{A_{\text{med}}}{1095} \times 100\right) \quad (1095 \text{ days} \approx 3 \text{ years})$$
5. **$C_{\text{saturation}}$ (Direct Video Count in SERP, weight $w_5 = 0.10$):**
   Degree to which search results offer direct answers vs. unrelated fallbacks.

---

## 4. Opportunity Score ($O_{\text{score}}$)
### Purpose
A unified 0–100 index indicating whether a creator should make a video on this topic.
High demand + low competition + high small creator success + freshness = **High Opportunity**.

### Component Breakdown (Specification 18)
| Component | Metric | Weight | Mathematical Definition |
|---|---|---|---|
| 1. Demand Signal | $S_{\text{demand}}$ | 15% | $D_{rel}$ (Relative Demand Index) |
| 2. Competition Opportunity | $S_{\text{comp\_opp}}$ | 15% | $100 - C_{est}$ (Inverted competition score) |
| 3. Small Creator Success | $S_{\text{small\_creator}}$ | 10% | $\frac{\sum \mathbb{I}(\text{Subs}_i < 25k \land \text{Views}_i > 10k)}{N_{\text{small}}} \times 100$ |
| 4. Freshness Signal | $S_{\text{fresh}}$ | 10% | Top videos published within last 90 days: $\frac{N_{\le 90\text{d}}}{N} \times 100$ |
| 5. Content Gap Signal | $S_{\text{gap}}$ | 10% | Weak title/description optimization in top 10 ranking videos |
| 6. Search Intent Specificity | $S_{\text{intent}}$ | 10% | Clear intent (Tutorial/Comparison/Problem) vs ambiguous |
| 7. Long-Tail Specificity | $S_{\text{longtail}}$ | 10% | Word count metric: $\min(100, (\text{word\_count} - 1) \times 25)$ |
| 8. Channel Fit | $S_{\text{fit}}$ | 10% | Semantic cosine similarity between topic & user channel profile |
| 9. Outlier Evidence | $S_{\text{outlier}}$ | 5% | Presence of $\ge 3\times$ multiplier outliers among ranking videos |
| 10. Trend Persistence | $S_{\text{trend}}$ | 5% | Growth in autocomplete variants over time |

### Aggregate Score Formula
$$O_{\text{score}} = \sum_{k=1}^{10} W_k \cdot S_k \quad \text{where } \sum W_k = 1.0$$

---

## 5. Statistical Outlier Detection ($M_{\text{outlier}}$)
### Purpose
Identifies videos that dramatically out-perform their channel's typical baseline, proving that topic appeal / packaging overrides channel subscriber size.

### Baseline Metrics
Given channel's last $K$ videos ($K \in [15, 50]$) with view counts $V = [v_1, v_2, \dots, v_K]$:
- Channel Median Views: $\tilde{V} = \text{median}(V)$
- Median Absolute Deviation (MAD):
  $$\text{MAD} = \text{median}\left(|v_i - \tilde{V}|\right)$$
- Robust Z-score:
  $$Z_{\text{robust}} = \frac{0.6745 \cdot (v_{\text{target}} - \tilde{V})}{\max(1, \text{MAD})}$$

### Outlier Multiplier
$$\text{Multiplier} = \frac{v_{\text{target}}}{\max(1, \tilde{V})}$$

### Classification Thresholds
- **Viral Outlier**: $\text{Multiplier} \ge 10.0\times$ (or $Z_{\text{robust}} \ge 5.0$)
- **High Outlier**: $5.0\times \le \text{Multiplier} < 10.0\times$
- **Solid Outlier**: $2.5\times \le \text{Multiplier} < 5.0\times$
- **Expected Range**: $0.5\times \le \text{Multiplier} < 2.5\times$
- **Underperforming**: $\text{Multiplier} < 0.5\times$

---

## 6. Video SEO Audit Score ($SEO_{\text{video}}$)
### Transparent Category Breakdown (0–100)
1. **Title Optimization (25 points)**:
   - Length between 45 and 70 characters (8 pts)
   - Primary keyword within first 35 characters (8 pts)
   - Readability and clear structure (contains curiosity/power word, no all-caps spam) (5 pts)
   - No keyword stuffing or duplicate words (4 pts)
2. **Description Optimization (20 points)**:
   - First 2–3 lines contain primary keyword naturally (6 pts)
   - Description length $\ge 250$ words with clear context (5 pts)
   - Timestamp chapters present (4 pts)
   - Call to action (CTA) and social links present (3 pts)
   - Hashtags present ($\le 3$ relevant tags) (2 pts)
3. **Keyword Relevance (20 points)**:
   - Primary keyword matched in Title AND Description (10 pts)
   - Supporting semantic keywords distributed across metadata (10 pts)
4. **Tags Optimization (10 points)**:
   - 5 to 15 focused tags provided (4 pts)
   - Includes primary keyword, variations, and brand tag (4 pts)
   - No single-character or spam tags (2 pts)
5. **Search Intent Alignment (10 points)**:
   - Title phrasing matches detected intent (e.g. "How to..." for Tutorial intent) (10 pts)
6. **Readability & Formatting (5 points)**:
   - Flesch Reading Ease score $\ge 60$ or clean phrasing, clean punctuation (5 pts)
7. **Context & Engagement Signals (10 points)**:
   - Thumbnail text clarity heuristic, engagement ratio (likes/views) if available (10 pts)

$$SEO_{\text{video}} = \sum \text{Earned Category Points} \in [0, 100]$$

---

## 7. Content Gap Matrix Score ($G_{\text{tier}}$)
Given user channel topics $T_{\text{user}}$ and competitor channel topics $T_{\text{comp}}$:
- **Topic Discrepancy**: Topic $t \in T_{\text{comp}}$ where $t \notin T_{\text{user}}$
- **Performance Multiplier**: $\text{Avg Multiplier of topic } t \text{ across competitors}$
- **Tier Assignment**:
  - **HIGH OPPORTUNITY**: Competitor multiplier $\ge 3.0\times$ AND search intent is tutorial/commercial AND topic absent in user channel.
  - **MEDIUM OPPORTUNITY**: Competitor multiplier $\ge 1.5\times$ AND topic absent or published $> 18$ months ago.
  - **LOW OPPORTUNITY**: Competitor multiplier $< 1.5\times$ or saturated by dominant channels.
