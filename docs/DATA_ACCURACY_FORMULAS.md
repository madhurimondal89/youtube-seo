# Data Accuracy & Mathematical Scoring Formulas
### YouTube SEO & Creator Intelligence Platform (`seo.freeyoutubetools.com`)

This document defines the mathematical models, formulas, data classification, and signal provenances used throughout the platform.

---

## 1. Data Classification & Provenance Standard

Every metric displayed to users is tagged with an immutable provenance label:

| Provenance Label | Meaning | Example |
|---|---|---|
| **Official** | Direct from YouTube Data API v3 or authorized YouTube Analytics OAuth | Channel Upload Date, Verified Subscriber count, Official Video ID |
| **Public** | Publicly accessible HTML / RSS / Autocomplete network response | Autocomplete Suggestion Matrix, Public View Count, Video Duration |
| **Calculated** | Transparent statistical or mathematical derivation with zero AI hallucination | 0-100 Opportunity Score, MAD Outlier Multiplier, Tag Character Count |
| **Estimated** | Heuristic approximation where exact platform numbers are proprietary | Estimated Competition Index, Mobile Scale Legibility |
| **AI-Generated** | Output produced by large or small language models, labeled as guidance | 30-Day Growth Strategy, Title Variations, Hook Scripts |

> **Ethical Principle:** The platform NEVER fabricates exact monthly search volumes (e.g. "82,410 monthly searches"), fake channel revenue, or confidential competitor click-through rates.

---

## 2. Mathematical Scoring Formulas

### A. Relative Demand Index (0–100)
Measures the search velocity and relative popularity of a keyword compared to its root query.

$$\text{RDI} = 0.40 \cdot S_{\text{rank}} + 0.25 \cdot S_{\text{brevity}} + 0.20 \cdot S_{\text{root}} + 0.15 \cdot S_{\text{views}}$$

Where:
- $S_{\text{rank}}$: Autocomplete Rank Score:
  $$S_{\text{rank}} = \max(10, 105 - (\text{rank} \cdot 10)) \quad (\text{Rank 1} = 95, \text{Rank 10} = 10, \text{Unranked} = 30)$$
- $S_{\text{brevity}}$: Word brevity bonus (shorter search queries generally reflect broader aggregate demand):
  - $\le 2$ words: 90
  - $3-4$ words: 75
  - $> 4$ words: $\max(30, 75 - (\text{words} - 4) \cdot 8)$
- $S_{\text{root}}$: Exact root query token containment (90 if root contained, else 50).
- $S_{\text{views}}$: Observable SERP view presence benchmark (Log scale distribution).

---

### B. Estimated Competition Index (0–100)
Evaluates how difficult it is for a non-celebrity creator to rank in search results for a given query.

$$\text{Competition} = 0.30 \cdot C_{\text{authority}} + 0.25 \cdot C_{\text{views}} + 0.20 \cdot C_{\text{density}} + 0.15 \cdot C_{\text{age}} + 0.10 \cdot C_{\text{sat}}$$

Where:
1. **$C_{\text{authority}}$ (Channel Authority Saturation - 30%):** Ratio of top 15 SERP results held by channels with $>500,000$ views or official artist/brand verification.
2. **$C_{\text{views}}$ (Median View Density - 25%):** Median view count mapped on a logarithmic curve:
   $$C_{\text{views}} = \min\left(100, \max\left(0, \frac{\log_{10}(\text{Median Views}) - 2}{4} \cdot 100\right)\right)$$
3. **$C_{\text{density}}$ (Exact Keyword Density - 20%):** Percentage of top 10 video titles matching $\ge 75\%$ of query tokens.
4. **$C_{\text{age}}$ (Incumbency Age Barrier - 15%):** Ratio of videos published over 1 year ago maintaining ranking vs fresh videos published in the last 30 days.
5. **$C_{\text{sat}}$ (SERP Result Saturation - 10%):** Breadth of unique competing videos indexed for the phrase.

---

### C. 10-Component Opportunity Score (0–100)
A balanced composite determining whether creating content on this topic is strategically viable.

$$\text{Opportunity} = \sum_{i=1}^{10} w_i \cdot S_i$$

| Component | Weight ($w_i$) | Calculation |
|---|---|---|
| **Demand** | 15% | Relative Demand Index ($0-100$) |
| **Competition Opportunity** | 15% | $100 - \text{Estimated Competition}$ |
| **Small Creator Success** | 10% | Proportion of non-mega channels getting $>15,000$ views in SERP |
| **Freshness Signal** | 10% | Presence of videos ranked within the last 30 days |
| **Content Gap Signal** | 10% | Search volume exists but top titles have weak keyword alignment |
| **Search Intent Specificity** | 10% | High intent types (Tutorial, Problem/Fix, Comparison = 90, Broad = 40) |
| **Long-Tail Specificity** | 10% | Word count & modifier depth ($1-2$ words = 30, $4-5+$ words = 90) |
| **Channel Fit / Broad Applicability**| 10% | Token overlap with channel topical clusters |
| **Outlier Evidence** | 5% | Presence of outlier videos ($>3\text{x}$ channel average) on this topic |
| **Trend Persistence** | 5% | Evergreen durability indicator |

---

### D. Outlier Detection (Median Absolute Deviation)
Identifies breakout videos while preventing extreme multi-million-view anomalies from distorting baseline channel averages.

Unlike arithmetic mean ($\mu$), which is heavily distorted by one viral video, we compute:

1. **Channel Median Views ($\tilde{X}$):**
   $$\tilde{X} = \text{median}(x_1, x_2, \dots, x_n)$$

2. **Median Absolute Deviation (MAD):**
   $$\text{MAD} = \text{median}(|x_i - \tilde{X}|)$$

3. **Performance Multiplier:**
   $$\text{Multiplier} = \frac{\text{Video Views}}{\max(1, \tilde{X})}$$

4. **Robust Modified Z-Score ($M_i$):**
   $$M_i = \frac{0.6745 \cdot (x_i - \tilde{X})}{\max(1, \text{MAD})}$$

**Outlier Tiers:**
- **Viral Outlier:** $\ge 10\text{x}$ median views OR $M_i \ge 5.0$
- **High Outlier:** $\ge 5.0\text{x}$ median views OR $M_i \ge 3.0$
- **Solid Outlier:** $\ge 2.5\text{x}$ median views
- **Expected:** $0.5\text{x} - 2.49\text{x}$ median views
- **Underperforming:** $< 0.5\text{x}$ median views

---

### E. Thumbnail Vision & Readability Scoring (0–100)
Evaluates optical clarity and clickability on mobile search feeds.

$$\text{Vision Score} = 0.20 \cdot S_{\text{aspect}} + 0.30 \cdot S_{\text{contrast}} + 0.20 \cdot S_{\text{clarity}} + 0.15 \cdot S_{\text{mobile}} + 0.15 \cdot S_{\text{hierarchy}}$$

1. **Aspect Ratio ($S_{\text{aspect}}$ - 20%):** Standard 16:9 ($1280 \times 720$) = 100. Non-standard aspect ratios penalized to prevent black pillarboxing.
2. **Luminance & Contrast ($S_{\text{contrast}}$ - 30%):** ITU-R BT.709 perceived luminance ($Y = 0.299R + 0.587G + 0.114B$) and standard deviation of luminance across pixels. High-contrast foreground/background separation scores 80–100.
3. **Safety Zone Check:** Evaluates whether critical faces/text overlap with the bottom-right timestamp badge ($70\%-100\%$ X, $70\%-100\%$ Y).
4. **Mobile Scaled Readability ($S_{\text{mobile}}$ - 15%):** Simulated downsampling to 120px width checking legibility against dark and light YouTube themes.
