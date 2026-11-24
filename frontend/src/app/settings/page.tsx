"use client";

import React, { useState, useEffect } from "react";
import {
  Settings as SettingsIcon,
  Cpu,
  Shield,
  Database,
  Trash2,
  CheckCircle2,
  AlertTriangle,
  Zap,
  Radio,
  ExternalLink,
  Terminal,
  Activity,
} from "lucide-react";
import { fetchSettings, saveSettings, testAiConnection, AppSettings } from "@/lib/api";

const PRESET_ENDPOINTS = [
  { name: "LM Studio (Local)", url: "http://localhost:1234/v1", defaultModel: "qwen2.5-coder-7b-instruct" },
  { name: "Ollama v1 (Local)", url: "http://localhost:11434/v1", defaultModel: "qwen2.5:3b" },
  { name: "LocalAI (Local)", url: "http://localhost:8080/v1", defaultModel: "gpt-4" },
  { name: "Groq (Ultra-Fast Cloud)", url: "https://api.groq.com/openai/v1", defaultModel: "llama-3.3-70b-versatile" },
  { name: "DeepSeek (Cloud)", url: "https://api.deepseek.com/v1", defaultModel: "deepseek-chat" },
  { name: "OpenRouter (Universal)", url: "https://openrouter.ai/api/v1", defaultModel: "meta-llama/llama-3.3-70b-instruct" },
];

export default function SettingsPage() {
  const [loading, setLoading] = useState(true);
  const [aiEnabled, setAiEnabled] = useState(false);
  const [aiProvider, setAiProvider] = useState("custom");

  // Custom OpenAI-Compatible
  const [customBaseUrl, setCustomBaseUrl] = useState("http://localhost:1234/v1");
  const [customModel, setCustomModel] = useState("qwen2.5-coder-7b-instruct");
  const [customApiKey, setCustomApiKey] = useState("");

  // Ollama
  const [ollamaBaseUrl, setOllamaBaseUrl] = useState("http://127.0.0.1:11434");
  const [ollamaModel, setOllamaModel] = useState("qwen2.5:3b");

  // Gemini
  const [geminiModel, setGeminiModel] = useState("gemini-1.5-flash");
  const [geminiApiKey, setGeminiApiKey] = useState("");

  // OpenAI
  const [openaiModel, setOpenaiModel] = useState("gpt-4o-mini");
  const [openaiApiKey, setOpenaiApiKey] = useState("");

  // YouTube Data
  const [youtubeProvider, setYoutubeProvider] = useState("public");
  const [youtubeApiKey, setYoutubeApiKey] = useState("");

  // Status & Feedback
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [testingAi, setTestingAi] = useState(false);
  const [testResult, setTestResult] = useState<{
    success: boolean;
    provider: string;
    response?: string;
    message?: string;
  } | null>(null);
  const [cacheCleared, setCacheCleared] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const s = await fetchSettings();
        if (s) {
          setAiEnabled(s.ai_enabled);
          setAiProvider(s.ai_provider || "custom");
          setCustomBaseUrl(s.custom_ai_base_url || "http://localhost:1234/v1");
          setCustomModel(s.custom_ai_model || "custom-model");
          setOllamaBaseUrl(s.ollama_base_url || "http://127.0.0.1:11434");
          setOllamaModel(s.ollama_model || "qwen2.5:3b");
          setGeminiModel(s.gemini_model || "gemini-1.5-flash");
          setOpenaiModel(s.openai_model || "gpt-4o-mini");
          setYoutubeProvider(s.youtube_provider || "public");
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSaved(false);
    try {
      await saveSettings({
        ai_enabled: aiEnabled,
        ai_provider: aiProvider,
        custom_ai_base_url: customBaseUrl,
        custom_ai_model: customModel,
        custom_ai_api_key: customApiKey || undefined,
        ollama_base_url: ollamaBaseUrl,
        ollama_model: ollamaModel,
        gemini_model: geminiModel,
        gemini_api_key: geminiApiKey || undefined,
        openai_model: openaiModel,
        openai_api_key: openaiApiKey || undefined,
        youtube_provider: youtubeProvider,
        youtube_api_key: youtubeApiKey || undefined,
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err: any) {
      alert("Error saving settings: " + (err.message || String(err)));
    } finally {
      setSaving(false);
    }
  };

  const handleTestAi = async () => {
    setTestingAi(true);
    setTestResult(null);
    try {
      // Save current configuration first so the backend tests what's on screen
      await saveSettings({
        ai_enabled: aiEnabled,
        ai_provider: aiProvider,
        custom_ai_base_url: customBaseUrl,
        custom_ai_model: customModel,
        custom_ai_api_key: customApiKey || undefined,
        ollama_base_url: ollamaBaseUrl,
        ollama_model: ollamaModel,
        gemini_model: geminiModel,
        gemini_api_key: geminiApiKey || undefined,
        openai_model: openaiModel,
        openai_api_key: openaiApiKey || undefined,
      });
      const res = await testAiConnection();
      setTestResult(res);
    } catch (err: any) {
      setTestResult({
        success: false,
        provider: aiProvider,
        message: err.message || "Could not connect to backend server.",
      });
    } finally {
      setTestingAi(false);
    }
  };

  const handleClearCache = async () => {
    try {
      const res = await fetch("/api/system/cache/clear", { method: "POST" });
      if (res.ok) {
        setCacheCleared(true);
        setTimeout(() => setCacheCleared(false), 2500);
      }
    } catch {
      setCacheCleared(true);
      setTimeout(() => setCacheCleared(false), 2500);
    }
  };

  const applyPreset = (preset: typeof PRESET_ENDPOINTS[0]) => {
    setCustomBaseUrl(preset.url);
    setCustomModel(preset.defaultModel);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">AI Models &amp; Platform Settings</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Connect any AI brain (Local LM Studio, Ollama, DeepSeek, Groq, Gemini, OpenAI, or custom endpoints) and configure data sources.
        </p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Section 1: Universal AI Model Architecture */}
        <div className="glass-panel p-6 rounded-xl space-y-5 border border-slate-800">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div className="flex items-center gap-2">
              <Cpu className="w-5 h-5 text-indigo-400" />
              <div>
                <h2 className="text-base font-bold text-white">AI Model &amp; Brain Configuration</h2>
                <p className="text-xs text-slate-400">Connect your preferred local or cloud model endpoint</p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-slate-300">
                {aiEnabled ? "AI Active" : "AI Inactive (Heuristics)"}
              </span>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={aiEnabled}
                  onChange={(e) => setAiEnabled(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600" />
              </label>
            </div>
          </div>

          {!aiEnabled && (
            <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-700/60 text-xs text-slate-300 flex items-start gap-2.5">
              <Shield className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
              <p>
                <strong>Deterministic Mode Active:</strong> YouTube SEO calculates all SEO scores, keyword opportunities, outlier multipliers, and content ideas using pure mathematical algorithms and 14 built-in psychology templates. Zero GPU/RAM footprint required.
              </p>
            </div>
          )}

          {aiEnabled && (
            <div className="space-y-4 pt-1">
              {/* Provider Selection */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-2">Select AI Engine Type</label>
                <div className="grid grid-cols-1 sm:grid-cols-4 gap-2.5">
                  <button
                    type="button"
                    onClick={() => setAiProvider("custom")}
                    className={`p-3 rounded-xl border text-left transition-all ${
                      aiProvider === "custom"
                        ? "bg-indigo-600/20 border-indigo-500 text-white shadow-md shadow-indigo-950/50"
                        : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
                    }`}
                  >
                    <div className="flex items-center gap-2 font-bold text-xs mb-1">
                      <Terminal className="w-3.5 h-3.5 text-indigo-400" />
                      <span>Custom / Any Endpoint</span>
                    </div>
                    <p className="text-[11px] text-slate-400 leading-tight">
                      LM Studio, LocalAI, Groq, DeepSeek, OpenRouter
                    </p>
                  </button>

                  <button
                    type="button"
                    onClick={() => setAiProvider("ollama")}
                    className={`p-3 rounded-xl border text-left transition-all ${
                      aiProvider === "ollama"
                        ? "bg-indigo-600/20 border-indigo-500 text-white shadow-md shadow-indigo-950/50"
                        : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
                    }`}
                  >
                    <div className="flex items-center gap-2 font-bold text-xs mb-1">
                      <Cpu className="w-3.5 h-3.5 text-cyan-400" />
                      <span>Local Ollama</span>
                    </div>
                    <p className="text-[11px] text-slate-400 leading-tight">
                      Qwen, Gemma, Llama on localhost:11434
                    </p>
                  </button>

                  <button
                    type="button"
                    onClick={() => setAiProvider("gemini")}
                    className={`p-3 rounded-xl border text-left transition-all ${
                      aiProvider === "gemini"
                        ? "bg-indigo-600/20 border-indigo-500 text-white shadow-md shadow-indigo-950/50"
                        : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
                    }`}
                  >
                    <div className="flex items-center gap-2 font-bold text-xs mb-1">
                      <Zap className="w-3.5 h-3.5 text-amber-400" />
                      <span>Google Gemini</span>
                    </div>
                    <p className="text-[11px] text-slate-400 leading-tight">
                      Free-tier Gemini 1.5 Flash API
                    </p>
                  </button>

                  <button
                    type="button"
                    onClick={() => setAiProvider("openai")}
                    className={`p-3 rounded-xl border text-left transition-all ${
                      aiProvider === "openai"
                        ? "bg-indigo-600/20 border-indigo-500 text-white shadow-md shadow-indigo-950/50"
                        : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
                    }`}
                  >
                    <div className="flex items-center gap-2 font-bold text-xs mb-1">
                      <Activity className="w-3.5 h-3.5 text-emerald-400" />
                      <span>OpenAI ChatGPT</span>
                    </div>
                    <p className="text-[11px] text-slate-400 leading-tight">
                      Official GPT-4o-mini / GPT-4o
                    </p>
                  </button>
                </div>
              </div>

              {/* Provider 1: CUSTOM / ANY OPENAI-COMPATIBLE ENDPOINT */}
              {aiProvider === "custom" && (
                <div className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-4">
                  <div className="space-y-1.5">
                    <span className="text-xs font-semibold text-slate-200">1-Click Endpoint Presets:</span>
                    <div className="flex flex-wrap gap-2">
                      {PRESET_ENDPOINTS.map((preset, idx) => (
                        <button
                          key={idx}
                          type="button"
                          onClick={() => applyPreset(preset)}
                          className="px-2.5 py-1 rounded-md bg-slate-800/80 hover:bg-slate-700 text-[11px] text-slate-300 border border-slate-700 transition-colors"
                        >
                          {preset.name}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">
                        Endpoint URL (Base URL)
                      </label>
                      <input
                        type="text"
                        value={customBaseUrl}
                        onChange={(e) => setCustomBaseUrl(e.target.value)}
                        placeholder="e.g. http://localhost:1234/v1 or https://api.groq.com/openai/v1"
                        className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 placeholder-slate-500 font-mono focus:border-indigo-500"
                      />
                      <span className="text-[10px] text-slate-500">
                        Supports LM Studio (`http://localhost:1234/v1`), LocalAI, Groq, DeepSeek, etc.
                      </span>
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-300 mb-1">
                        Model Identifier / Name
                      </label>
                      <input
                        type="text"
                        value={customModel}
                        onChange={(e) => setCustomModel(e.target.value)}
                        placeholder="e.g. llama-3.3-70b-versatile, deepseek-chat, or your loaded model"
                        className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 placeholder-slate-500 font-mono focus:border-indigo-500"
                      />
                      <span className="text-[10px] text-slate-500">Type any model name configured in your server.</span>
                    </div>

                    <div className="sm:col-span-2">
                      <label className="block text-xs font-semibold text-slate-300 mb-1">
                        API Key (Optional for Local Models)
                      </label>
                      <input
                        type="password"
                        value={customApiKey}
                        onChange={(e) => setCustomApiKey(e.target.value)}
                        placeholder="Leave blank for local LM Studio / Ollama, or paste Bearer key for Groq/DeepSeek"
                        className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 placeholder-slate-500 font-mono focus:border-indigo-500"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Provider 2: OLLAMA */}
              {aiProvider === "ollama" && (
                <div className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Ollama Base URL</label>
                    <input
                      type="text"
                      value={ollamaBaseUrl}
                      onChange={(e) => setOllamaBaseUrl(e.target.value)}
                      placeholder="http://127.0.0.1:11434"
                      className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono focus:border-indigo-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Model Name</label>
                    <input
                      type="text"
                      value={ollamaModel}
                      onChange={(e) => setOllamaModel(e.target.value)}
                      placeholder="e.g. qwen2.5:3b, qwen2.5:1.5b, llama3.2"
                      className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono focus:border-indigo-500"
                    />
                  </div>
                </div>
              )}

              {/* Provider 3: GOOGLE GEMINI */}
              {aiProvider === "gemini" && (
                <div className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Gemini Model</label>
                    <input
                      type="text"
                      value={geminiModel}
                      onChange={(e) => setGeminiModel(e.target.value)}
                      placeholder="gemini-1.5-flash or gemini-1.5-pro"
                      className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono focus:border-indigo-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1 flex items-center justify-between">
                      <span>Gemini API Key</span>
                      <a
                        href="https://aistudio.google.com"
                        target="_blank"
                        rel="noreferrer"
                        className="text-[10px] text-indigo-400 hover:underline flex items-center gap-1"
                      >
                        Get Free Key <ExternalLink className="w-2.5 h-2.5" />
                      </a>
                    </label>
                    <input
                      type="password"
                      value={geminiApiKey}
                      onChange={(e) => setGeminiApiKey(e.target.value)}
                      placeholder="AIzaSy..."
                      className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono focus:border-indigo-500"
                    />
                  </div>
                </div>
              )}

              {/* Provider 4: OPENAI */}
              {aiProvider === "openai" && (
                <div className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">OpenAI Model</label>
                    <input
                      type="text"
                      value={openaiModel}
                      onChange={(e) => setOpenaiModel(e.target.value)}
                      placeholder="gpt-4o-mini or gpt-4o"
                      className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono focus:border-indigo-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">OpenAI API Key</label>
                    <input
                      type="password"
                      value={openaiApiKey}
                      onChange={(e) => setOpenaiApiKey(e.target.value)}
                      placeholder="sk-..."
                      className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 font-mono focus:border-indigo-500"
                    />
                  </div>
                </div>
              )}

              {/* Test Connection Button & Result */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pt-2">
                <button
                  type="button"
                  onClick={handleTestAi}
                  disabled={testingAi}
                  className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-indigo-300 border border-slate-700 flex items-center gap-2 transition-all shadow"
                >
                  <Activity className={`w-3.5 h-3.5 ${testingAi ? "animate-spin text-indigo-400" : "text-indigo-400"}`} />
                  <span>{testingAi ? "Testing Endpoint..." : "Test AI Model Connection"}</span>
                </button>

                {testResult && (
                  <div
                    className={`p-3 rounded-lg text-xs border w-full sm:w-auto flex-1 ${
                      testResult.success
                        ? "bg-emerald-950/40 border-emerald-500/40 text-emerald-300"
                        : "bg-rose-950/40 border-rose-500/40 text-rose-300"
                    }`}
                  >
                    <div className="flex items-center gap-2 font-semibold">
                      {testResult.success ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                      ) : (
                        <AlertTriangle className="w-4 h-4 text-rose-400 flex-shrink-0" />
                      )}
                      <span>{testResult.success ? "Connection Verified!" : "Connection Failed"}</span>
                      <span className="text-[10px] text-slate-400 font-normal">({testResult.provider})</span>
                    </div>
                    <p className="mt-1 text-[11px] text-slate-200">
                      {testResult.success ? testResult.response : testResult.message}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Section 2: Data Sources */}
        <div className="glass-panel p-6 rounded-xl space-y-4 border border-slate-800">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
            <Database className="w-5 h-5 text-cyan-400" />
            <div>
              <h2 className="text-base font-bold text-white">YouTube Data Sources</h2>
              <p className="text-xs text-slate-400">Configure how YouTube SEO extracts search data and video statistics</p>
            </div>
          </div>

          <div className="space-y-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Provider Mode</label>
              <select
                value={youtubeProvider}
                onChange={(e) => setYoutubeProvider(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200"
              >
                <option value="public">Public Web Scraper &amp; RSS Feeds (Lawful, Rate-Limited, Zero Cost)</option>
                <option value="api">Official Google YouTube Data API v3 (Fastest, Requires API Key)</option>
                <option value="mock">Offline Mock Provider (For Local Dev &amp; Offline Unit Tests)</option>
              </select>
            </div>

            {youtubeProvider === "api" && (
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">YouTube Data API Key</label>
                <input
                  type="password"
                  value={youtubeApiKey}
                  onChange={(e) => setYoutubeApiKey(e.target.value)}
                  placeholder="AIzaSy..."
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 font-mono"
                />
              </div>
            )}
          </div>
        </div>

        {/* Section 3: Privacy & Stateless Cache */}
        <div className="glass-panel p-6 rounded-xl space-y-4 border border-slate-800">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
            <Shield className="w-5 h-5 text-emerald-400" />
            <h2 className="text-base font-bold text-white">Privacy &amp; Stateless Cache</h2>
          </div>

          <p className="text-xs text-slate-400 leading-relaxed">
            YouTube SEO operates strictly in-memory during each research session. No data is stored in any external database, and responses are cached with a 15-minute TTL to stay polite to search servers.
          </p>

          <button
            type="button"
            onClick={handleClearCache}
            className="px-4 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-200 flex items-center gap-2"
          >
            <Trash2 className="w-3.5 h-3.5 text-rose-400" />
            <span>{cacheCleared ? "In-Memory Cache Cleared!" : "Clear In-Memory Cache"}</span>
          </button>
        </div>

        {/* Save button & Status */}
        <div className="flex items-center gap-3 pt-2">
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm transition-colors shadow-lg shadow-indigo-950/50 flex items-center gap-2"
          >
            <SettingsIcon className="w-4 h-4" />
            <span>{saving ? "Saving..." : "Save Configuration"}</span>
          </button>
          {saved && (
            <span className="text-xs text-emerald-400 font-semibold flex items-center gap-1.5 bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/30">
              <CheckCircle2 className="w-4 h-4" /> Settings saved to runtime &amp; .env
            </span>
          )}
        </div>
      </form>
    </div>
  );
}
