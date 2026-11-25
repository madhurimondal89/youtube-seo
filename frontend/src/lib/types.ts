export type DataProvenance = "Official" | "Public" | "Calculated" | "Estimated" | "Relative" | "Sample Data" | "AI Recommendation" | "Unavailable";

export type SearchIntent =
  | "Informational"
  | "Tutorial"
  | "Commercial"
  | "Transactional"
  | "Navigational"
  | "Entertainment"
  | "News/Trending"
  | "Comparison"
  | "Problem/Fix";

export interface KeywordMetricItem {
  keyword: str;
  intents: SearchIntent[];
  search_surface: string;
  relative_demand: number;
  estimated_competition: number;
  opportunity_score: number;
  freshness_score: number;
  specificity_score: number;
  word_count: number;
  char_count: number;
  provenance: DataProvenance;
  score_breakdown: Record<string, number>;
  reasons: string[];
}

type str = string;

export interface TopicCluster {
  cluster_name: string;
  main_keyword: string;
  supporting_keywords: string[];
  related_entities: string[];
  recommended_pillar_title: string;
  supporting_video_ideas: string[];
  playlist_suggestion: string;
  avg_opportunity_score: number;
}

export interface KeywordResearchResponse {
  seed: string;
  total_found: number;
  keywords: KeywordMetricItem[];
  clusters: TopicCluster[];
  top_opportunity_keywords: KeywordMetricItem[];
  data_provenance: DataProvenance;
  execution_time_ms: number;
}

export interface VideoSearchResult {
  video_id: string;
  title: string;
  channel_name: string;
  channel_id?: string;
  published_time_text?: string;
  views_count?: number;
  views_text?: string;
  duration_text?: string;
  duration_seconds?: number;
  thumbnail_url?: string;
  description_snippet?: string;
  rank_position: number;
  provenance: DataProvenance;
}

export interface OutlierVideoItem {
  video_id: string;
  title: string;
  channel_name: string;
  views: number;
  channel_median_views: number;
  multiplier: number;
  multiplier_text: string;
  tier: string;
  z_score: number;
  published_date?: string;
  thumbnail_url?: string;
  primary_topic?: string;
  provenance: DataProvenance;
}

export interface AuditChecklistItem {
  id: string;
  title: string;
  passed: boolean;
  score_earned: number;
  max_score: number;
  feedback: string;
  actionable_fix?: string;
  severity: "critical" | "warning" | "optimal";
}

export interface AuditCategoryScore {
  category_name: string;
  earned_score: number;
  max_score: number;
  percentage: number;
  items: AuditChecklistItem[];
}

export interface VideoAuditResult {
  video_id?: string;
  title: string;
  overall_score: number;
  verdict: string;
  categories: AuditCategoryScore[];
  action_plan: string[];
  keywords_detected: string[];
  estimated_readability: string;
  curiosity_score: number;
  provenance: DataProvenance;
}

export interface ChannelAuditResult {
  channel_id: string;
  channel_title: string;
  overall_health_score: number;
  topic_consistency_score: number;
  title_quality_score: number;
  upload_cadence_score: number;
  outlier_ratio: number;
  recommendations: string[];
  next_best_video_topics: string[];
  provenance: DataProvenance;
}

export interface ChannelPerformanceMetrics {
  median_views: number;
  mean_views: number;
  mad_views: number;
  upload_frequency_per_month: number;
  average_duration_seconds: number;
  outlier_count: number;
  top_performing_topics: string[];
  recent_videos: any[];
  outliers: OutlierVideoItem[];
  provenance: DataProvenance;
}

export interface CompetitorComparisonResult {
  channels: any[];
  metrics_by_channel: Record<string, ChannelPerformanceMetrics>;
  shared_topics: string[];
  unique_topics_by_channel: Record<string, string[]>;
  content_gaps: any[];
  provenance: DataProvenance;
}

export interface TitleIdea {
  title: string;
  seo_relevance_heuristic: number;
  curiosity_heuristic: number;
  character_count: number;
  has_number: boolean;
  frontloaded_keyword: boolean;
  style: string;
}

export interface SystemStatus {
  app_name: string;
  version: string;
  environment: string;
  ai_enabled: boolean;
  ai_provider: string;
  ai_status: string;
  ai_mode?: string;
  active_model?: string;
  youtube_provider: string;
  cache_size: number;
  uptime_seconds: number;
  timestamp: string;
}

export interface VisualScoreBreakdown {
  visual_hierarchy_score: number;
  text_readability_score: number;
  subject_visibility_score: number;
  contrast_score: number;
  mobile_readability_score: number;
  composition_score: number;
  background_complexity_score: number;
  aspect_ratio_score?: number;
  clarity_score?: number;
  focal_hierarchy_score?: number;
}

export interface VisualIssue {
  severity: "critical" | "warning" | "info";
  category: string;
  issue: string;
  suggestion: string;
}

export interface ThumbnailAnalysisResponse {
  filename: string;
  width: number;
  height: number;
  aspect_ratio_label: string;
  is_standard_hd: bool;
  overall_score: number;
  breakdown: VisualScoreBreakdown;
  dominant_colors: string[];
  average_brightness: number;
  contrast_ratio: number;
  issues: VisualIssue[];
  recommendations: string[];
  mobile_preview_advisory: string;
  data_provenance: string;
  ctr_disclaimer?: string;
  vision_ai_status?: string;
  vision_ai_insights?: string[];
}

type bool = boolean;

export interface CoachVideoPlan {
  day: number;
  format: string;
  title: string;
  target_keyword: string;
  hook_script: string;
  thumbnail_concept: string;
  script_structure: string[];
}

export interface CoachWeekPlan {
  week_number: number;
  theme: string;
  milestone_objective: string;
  videos: CoachVideoPlan[];
}

export interface GrowthStrategyResponse {
  niche: string;
  channel_name?: string;
  language: string;
  executive_summary: string;
  target_audience_profile: string;
  weeks: CoachWeekPlan[];
  publishing_checklist: string[];
  weekly_review_metrics: string[];
  data_provenance: string;
}

