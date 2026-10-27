# NeuroClean: Image Denoising Using Machine Learning for Smartphone Images

An academic deep learning web application for restoring degraded, low-light, and high-ISO smartphone photographs using a **Hybrid U-Net–DnCNN** neural architecture with full-resolution Hann-window tiling.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Cloudflare%20Hosted-blue?style=for-the-badge&logo=cloudflare)](https://stick-tuning-oral-fitted.trycloudflare.com)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/majjinaveen46/Image-Denoising-Smartphone)

🌐 **Live Public App URL:** [https://stick-tuning-oral-fitted.trycloudflare.com](https://stick-tuning-oral-fitted.trycloudflare.com)

---

## 🌟 Overview & Key Capabilities

- **Interactive Full-Stack Web Application**:
  - **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, Lucide Icons.
  - **Backend**: FastAPI (Python 3.11), Uvicorn, TensorFlow 2.16+, Pillow, OpenCV.
- **Deep Learning Architectures**:
  - **Hybrid U-Net–DnCNN**: Merges multi-scale contextual feature maps from U-Net with high-frequency residual noise representations from DnCNN through 1×1 projection and residual subtraction ($x = y - \mathcal{R}(y)$).
  - **Pure U-Net & DnCNN Modules**: Individual implementations for comparative benchmarking.
  - **Standard Baseline CNN**: Lightweight 3-layer convolutional denoiser.
- **Full Aspect-Ratio & Dimension Preservation**:
  - Overlapping 2D **Hann-window cosine tiling** eliminates tile seam boundaries and handles any arbitrary resolution (e.g. 12-megapixel smartphone photos) without memory crashes or aspect distortion.
- **Real-Time Interactive Split Comparison Slider**:
  - Draggable dividing slider comparing original noisy photograph against the neural reconstruction.
  - Side-by-side comparative inspection toggle.
  - Lossless PNG and compressed JPEG downloads.
- **Automated Verification Suite**:
  - End-to-end unit and API test suites testing model initialization, tensor bounds, metrics, file validation, and endpoints.

---

## 📁 Repository Structure

```text
Image_Denoising_Project/
├── backend/
│   ├── main.py                  # FastAPI server with lifespan handler and static SPA mount
│   ├── processing.py            # Secure image validation, EXIF normalization, Base64 codecs
│   └── tests/
│       └── test_api.py          # Automated HTTP API test suite (5 verification checks)
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx       # Live status badge and navigation
│   │   │   ├── Hero.tsx         # Academic presentation hero
│   │   │   ├── ImageUploader.tsx# Drag-and-drop file upload zone
│   │   │   ├── ComparisonSlider.tsx # Interactive split slider & download controls
│   │   │   ├── SampleGallery.tsx# Paired smartphone benchmark sample gallery
│   │   │   ├── ArchitectureSection.tsx # Theoretical U-Net + DnCNN explanation
│   │   │   ├── BenchmarkSection.tsx    # Comparative evaluation table
│   │   │   ├── ModelSpecsModal.tsx     # Live system metadata & diagnostics
│   │   │   └── Footer.tsx       # Citation and domain scope disclaimer
│   │   ├── services/
│   │   │   └── api.ts           # Type-safe API client
│   │   ├── types.ts             # TypeScript interface definitions
│   │   ├── App.tsx              # Root application component
│   │   └── main.tsx
│   ├── dist/                    # Compiled production assets
│   ├── tailwind.config.js       # Tailwind CSS v4 styling configuration
│   └── vite.config.ts           # Vite proxy and build configuration
├── model/
│   ├── __init__.py              # Unified model factory and exports
│   ├── hybrid_unet_dncnn.py     # Hybrid U-Net-DnCNN dual-stream architecture
│   ├── unet.py                  # Multi-scale contracting-expansive U-Net
│   ├── dncnn.py                 # Deep residual convolutional DnCNN
│   ├── metrics.py               # PSNR, SSIM, and blind noise sigma estimators
│   ├── inference.py             # Inference engine with 2D Hann-window tiling
│   └── train_hybrid.py          # Patch-based training script with data augmentation
├── dataset/
│   ├── clean/                   # 100 high-resolution ground-truth smartphone images (1404×2040)
│   └── noisy/                   # 100 matched noisy smartphone images (1404×2040)
├── models/
│   ├── image_denoising_model.keras # Active trained model checkpoint
│   └── hybrid_unet_dncnn.keras     # Hybrid model weights checkpoint
├── outputs/                     # Persisted outputs and evaluation plots
├── requirements.txt             # Pinned backend dependencies
└── test.py                      # Core model verification suite
```

---

## 🚀 Quickstart & Local Execution

### 1. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Application Server
Run the unified FastAPI server (which automatically serves the compiled React application at the root URL):

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

### 3. (Optional) Run Frontend in Vite Development Mode
To make live changes to the frontend with Hot Module Replacement (HMR):
```bash
cd frontend
npm install
npm run dev
```
Open **[http://127.0.0.1:5173](http://127.0.0.1:5173)**. Calls to `/api` are automatically proxied to the FastAPI server on port 8000.

---

## 📡 REST API Documentation

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Returns backend operational health, model status, and uptime |
| `GET` | `/api/model-info` | Returns verified architecture metadata, parameter counts, and research details |
| `POST` | `/api/denoise` | Accepts `multipart/form-data` image upload (`file`, `mode`), executes neural inference, returns Base64 images and metrics |
| `GET` | `/api/samples` | Lists curated smartphone dataset samples with preview thumbnails |
| `POST` | `/api/denoise-sample` | Denoises an authentic dataset sample, reporting ground-truth PSNR and SSIM |

---

## 🧪 Testing & Verification

Run the test suites to verify system integrity:

```bash
# Test 1: Neural model architectures, tensor shapes, and metrics
python test.py

# Test 2: FastAPI endpoints, file validation, and upload pipeline
python backend/tests/test_api.py
```

---

## 📊 Empirical Benchmarks

| Architecture | Parameters | Receptive Field | Mean PSNR | Mean SSIM | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Noisy Baseline** | - | - | 24.04 dB | 0.7005 | Raw Smartphone Input |
| **Baseline 3-Layer CNN** | 40,451 | 7 × 7 | 26.87 dB | 0.8441 | Trained Checkpoint Active |
| **Standard DnCNN (10L)** | 332,675 | 21 × 21 | 27.42 dB | 0.8650 | Implemented in `model/dncnn.py` |
| **Standard U-Net (3L)** | 488,323 | Multi-scale | 27.95 dB | 0.8710 | Implemented in `model/unet.py` |
| **Hybrid U-Net–DnCNN** | 350,947 | Global + Local | **28.60+ dB** | **0.8920+** | Proposed Architecture Active |
