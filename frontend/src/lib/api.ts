import {
  KeywordResearchResponse,
  VideoAuditResult,
  ChannelAuditResult,
  ChannelPerformanceMetrics,
  CompetitorComparisonResult,
  OutlierVideoItem,
  TitleIdea,
  SystemStatus,
  ThumbnailAnalysisResponse,
  GrowthStrategyResponse,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function fetchSystemStatus(): Promise<SystemStatus | null> {
  try {
    const res = await fetch(`${API_BASE}/system/status`, { cache: "no-store" });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

export interface AppSettings {
  ai_enabled: boolean;
  ai_provider: string;
  ollama_base_url: string;
  ollama_model: string;
  custom_ai_base_url: string;
  custom_ai_model: string;
  custom_ai_api_key_masked: string;
  has_custom_ai_api_key: boolean;
  gemini_model: string;
  gemini_api_key_masked: string;
  has_gemini_api_key: boolean;
  openai_model: string;
  openai_api_key_masked: string;
  has_openai_api_key: boolean;
  youtube_provider: string;
  youtube_api_key_masked: string;
  has_youtube_api_key: boolean;
}

export async function fetchSettings(): Promise<AppSettings | null> {
  try {
    const res = await fetch(`${API_BASE}/system/settings`, { cache: "no-store" });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

export async function saveSettings(payload: Record<string, any>): Promise<{ status: string; message: string }> {
  const res = await fetch(`${API_BASE}/system/settings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to save settings");
  return await res.json();
}

export async function testAiConnection(): Promise<{ success: boolean; provider: string; response?: string; message?: string }> {
  const res = await fetch(`${API_BASE}/system/test-ai`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error("AI test endpoint unreachable");
  return await res.json();
}

export async function researchKeyword(
  seed: string,
  includeAlphabet: boolean = true,
  includeModifiers: boolean = true,
  maxKeywords: number = 40,
  includeQuestions: boolean = true,
  includeComparisons: boolean = true
): Promise<KeywordResearchResponse> {
  const res = await fetch(`${API_BASE}/research/keyword`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      seed,
      include_alphabet_expansion: includeAlphabet,
      include_modifiers: includeModifiers,
      include_questions: includeQuestions,
      include_comparisons: includeComparisons,
      max_keywords: maxKeywords,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Research request failed" }));
    throw new Error(err.detail || "Failed to research keyword");
  }
  return await res.json();
}

export async function auditVideo(
  videoUrlOrId?: string,
  title?: string,
  description?: string,
  tags: string[] = [],
  targetKeyword?: string,
  hasCaptions: boolean = false
): Promise<VideoAuditResult> {
  const res = await fetch(`${API_BASE}/audit/video`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      video_url_or_id: videoUrlOrId,
      title,
      description,
      tags,
      target_keyword: targetKeyword,
      has_captions: hasCaptions,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Video audit failed" }));
    throw new Error(err.detail || "Failed to audit video");
  }
  return await res.json();
}

export async function auditChannel(channelUrlOrHandle: string): Promise<ChannelAuditResult> {
  const res = await fetch(`${API_BASE}/audit/channel`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ channel_url_or_handle: channelUrlOrHandle }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Channel audit failed" }));
    throw new Error(err.detail || "Failed to audit channel");
  }
  return await res.json();
}

export async function analyzeChannel(channelUrlOrHandle: string): Promise<ChannelPerformanceMetrics> {
  const res = await fetch(`${API_BASE}/competitor/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ channel_url_or_handle: channelUrlOrHandle }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Channel analysis failed" }));
    throw new Error(err.detail || "Failed to analyze channel");
  }
  return await res.json();
}

export async function compareCompetitors(
  userChannel: string,
  competitorChannels: string[]
): Promise<CompetitorComparisonResult> {
  const res = await fetch(`${API_BASE}/competitor/compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_channel: userChannel,
      competitor_channels: competitorChannels,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Competitor comparison failed" }));
    throw new Error(err.detail || "Failed to compare competitors");
  }
  return await res.json();
}

export async function getOutliers(channel: string): Promise<OutlierVideoItem[]> {
  const res = await fetch(`${API_BASE}/competitor/outliers?channel=${encodeURIComponent(channel)}`);
  if (!res.ok) throw new Error("Failed to load outliers");
  return await res.json();
}

export async function generateTitleIdeas(
  topic: string,
  targetKeyword?: string,
  count: number = 12
): Promise<TitleIdea[]> {
  const res = await fetch(`${API_BASE}/ai/title`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      topic,
      target_keyword: targetKeyword,
      count,
    }),
  });
  if (!res.ok) throw new Error("Failed to generate title ideas");
  return await res.json();
}

export async function generateDescription(
  topic: string,
  targetKeywords: string[],
  callToAction?: string,
  chaptersRequested: boolean = true
) {
  const res = await fetch(`${API_BASE}/ai/description`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      topic,
      target_keywords: targetKeywords,
      call_to_action: callToAction,
      chapters_requested: chaptersRequested,
    }),
  });
  if (!res.ok) throw new Error("Failed to generate description");
  return await res.json();
}

export async function generateTags(title: string, topic: string, targetKeyword?: string) {
  const res = await fetch(`${API_BASE}/ai/tags`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, topic, target_keyword: targetKeyword }),
  });
  if (!res.ok) throw new Error("Failed to generate tags");
  return await res.json();
}

export async function generateHooks(topic: string, targetAudience: string = "Creators") {
  const res = await fetch(`${API_BASE}/ai/hooks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic, target_audience: targetAudience }),
  });
  if (!res.ok) throw new Error("Failed to generate hooks");
  return await res.json();
}

export async function generateCalendar(topic: string, durationDays: number = 30) {
  const res = await fetch(`${API_BASE}/ai/calendar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic, duration_days: durationDays }),
  });
  if (!res.ok) throw new Error("Failed to generate calendar");
  return await res.json();
}

export async function analyzeThumbnailUpload(file: File): Promise<ThumbnailAnalysisResponse> {
  const base64 = await new Promise<string>((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
  const res = await fetch(`${API_BASE}/ai/thumbnail/analyze-upload`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image_base64: base64, filename: file.name }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Thumbnail analysis failed" }));
    throw new Error(err.detail || "Failed to analyze thumbnail upload");
  }
  return await res.json();
}

export async function analyzeThumbnailUrl(url: string): Promise<ThumbnailAnalysisResponse> {
  const res = await fetch(`${API_BASE}/ai/thumbnail/analyze-url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Failed to analyze thumbnail from URL" }));
    throw new Error(err.detail || "Failed to analyze thumbnail from URL");
  }
  return await res.json();
}

export async function fetchGrowthStrategy(
  niche: string,
  channelName?: string,
  language: string = "English",
  savedKeywords?: string[],
  topPerformingTopics?: string[],
  channelMetricsSummary?: string
): Promise<GrowthStrategyResponse> {
  const res = await fetch(`${API_BASE}/ai/growth-coach`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      niche,
      channel_name: channelName,
      language,
      saved_keywords: savedKeywords,
      top_performing_topics: topPerformingTopics,
      channel_metrics_summary: channelMetricsSummary,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Growth strategy generation failed" }));
    throw new Error(err.detail || "Failed to generate growth strategy");
  }
  return await res.json();
}

// --- Workspace Persistence API ---
export async function saveWorkspaceKeywordProject(seed: string, data: any, title?: string) {
  const res = await fetch(`${API_BASE}/workspace/keywords`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ seed, data, title }),
  });
  if (!res.ok) throw new Error("Failed to save keyword project");
  return await res.json();
}

export async function fetchWorkspaceKeywordProjects() {
  const res = await fetch(`${API_BASE}/workspace/keywords`, { cache: "no-store" });
  if (!res.ok) return [];
  return await res.json();
}

export async function saveWorkspaceCompetitor(channelId: string, channelName: string, medianViews: number = 0, subscriberCount: string = "N/A", notes: string = "") {
  const res = await fetch(`${API_BASE}/workspace/competitors`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      channel_id: channelId,
      channel_name: channelName,
      median_views: medianViews,
      subscriber_count: subscriberCount,
      notes,
    }),
  });
  if (!res.ok) throw new Error("Failed to save competitor to watchlist");
  return await res.json();
}

export async function fetchWorkspaceCompetitors() {
  const res = await fetch(`${API_BASE}/workspace/competitors`, { cache: "no-store" });
  if (!res.ok) return [];
  return await res.json();
}

export async function saveWorkspaceAudit(videoTitle: string, overallScore: number, auditData: any, videoUrl?: string) {
  const res = await fetch(`${API_BASE}/workspace/audits`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      video_title: videoTitle,
      overall_score: overallScore,
      audit_data: auditData,
      video_url: videoUrl,
    }),
  });
  if (!res.ok) throw new Error("Failed to save audit report");
  return await res.json();
}

export async function fetchWorkspaceAudits() {
  const res = await fetch(`${API_BASE}/workspace/audits`, { cache: "no-store" });
  if (!res.ok) return [];
  return await res.json();
}


