export interface ModelInfo {
  project_title: string;
  academic_context: string;
  architecture_summary: {
    name: string;
    type: string;
    total_parameters: number;
    trainable_parameters: number;
    receptive_field: string;
    input_channels: number;
    checkpoint_path: string | null;
    checkpoint_status: string;
  };
  technologies: {
    deep_learning: string;
    computer_vision: string;
    api_server: string;
    frontend_stack: string;
  };
  supported_features: {
    arbitrary_dimensions: boolean;
    full_resolution_tiling: boolean;
    hann_window_blending: boolean;
    exif_orientation_correction: boolean;
    formats: string[];
  };
  training_dataset_summary: {
    description: string;
    native_resolution: string;
    noise_profile: string;
  };
}

export interface DenoiseResponse {
  success: boolean;
  filename?: string;
  sample_id?: string;
  original_image: string; // Base64 data URI
  denoised_image: string; // Base64 data URI
  metadata: {
    width: number;
    height: number;
    aspect_ratio: string;
    processing_time_ms: number;
    model_name: string;
    processing_mode: string;
  };
  metrics: {
    estimated_input_noise_sigma: number;
    estimated_output_noise_sigma: number;
    noise_reduction_percentage: number;
    psnr_db: number | null;
    ssim: number | null;
  };
}

export interface SampleItem {
  id: string;
  title: string;
  noisy_thumbnail: string;
  clean_thumbnail: string;
  noisy_path: string;
  clean_path: string;
}

export interface HealthStatus {
  status: string;
  service: string;
  version: string;
  uptime_seconds: number;
  model_loaded: boolean;
  model_name: string | null;
  backend_framework: string;
}
