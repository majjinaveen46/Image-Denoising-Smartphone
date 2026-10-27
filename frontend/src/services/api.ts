import type { DenoiseResponse, HealthStatus, ModelInfo, SampleItem } from "../types";

const API_BASE = "/api";

export async function fetchHealth(): Promise<HealthStatus> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) {
    throw new Error(`Health check failed with status ${res.status}`);
  }
  return res.json();
}

export async function fetchModelInfo(): Promise<ModelInfo> {
  const res = await fetch(`${API_BASE}/model-info`);
  if (!res.ok) {
    throw new Error(`Failed to fetch model info (status ${res.status})`);
  }
  return res.json();
}

export async function fetchSamples(): Promise<SampleItem[]> {
  const res = await fetch(`${API_BASE}/samples`);
  if (!res.ok) {
    throw new Error("Failed to load demonstration samples");
  }
  const data = await res.json();
  return data.samples || [];
}

export async function denoiseImageUpload(
  file: File,
  mode: "tiled" | "resize" = "tiled"
): Promise<DenoiseResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("mode", mode);

  const res = await fetch(`${API_BASE}/denoise`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "Unknown server error" }));
    throw new Error(errorData.detail || `Server returned error status ${res.status}`);
  }

  return res.json();
}

export async function denoiseSampleImage(
  sampleId: string,
  mode: "tiled" | "resize" = "resize"
): Promise<DenoiseResponse> {
  const formData = new FormData();
  formData.append("sample_id", sampleId);
  formData.append("mode", mode);

  const res = await fetch(`${API_BASE}/denoise-sample`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "Sample denoising failed" }));
    throw new Error(errorData.detail || `Server returned error status ${res.status}`);
  }

  return res.json();
}
