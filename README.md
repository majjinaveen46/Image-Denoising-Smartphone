# NeuroClean: Image Denoising Using Machine Learning for Smartphone Images

<div align="center">

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Cloudflare%20Hosted-2563eb?style=for-the-badge&logo=cloudflare&logoColor=white)](https://stick-tuning-oral-fitted.trycloudflare.com)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/majjinaveen46/Image-Denoising-Smartphone)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16+-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)

**A full-stack deep learning application engineered to restore high-ISO and low-light smartphone photographs using a dual-stream Hybrid U-Net–DnCNN neural network with seamless Hann-window tiling.**

[🌐 Open Live Web App](https://stick-tuning-oral-fitted.trycloudflare.com) • [🐙 GitHub Source Code](https://github.com/majjinaveen46/Image-Denoising-Smartphone) • [📖 Deployment Guide](DEPLOYMENT.md)

</div>

---

## 📌 Project Abstract

Smartphone cameras feature physical hardware constraints, notably small image sensor pixel pitches ($1.0\,\mu\text{m} - 1.4\,\mu\text{m}$). Under low-ambient illumination, these sensors suffer from substantial **photon shot noise**, **thermal amplifier noise**, and **chromatic grain**.

**NeuroClean** introduces a dual-stream **Hybrid U-Net–DnCNN** deep learning architecture that synergizes:
1. **Multi-Scale Contextual U-Net:** Captures global semantic layout and preserves low-frequency luminance continuity across contracting and expansive paths with long skip connections.
2. **Deep Residual DnCNN:** A 10-layer feed-forward chain of $3 \times 3$ convolutions, Batch Normalization, and ReLUs operating at full spatial resolution to isolate high-frequency sensor noise without spatial pooling degradation.
3. **Cross-Feature Fusion & Residual Subtraction:** Fuses both representations via $1 \times 1$ projections to estimate the noise field $\mathcal{R}(y)$, reconstructing clean photographs via:
   $$\hat{x} = \text{clip}(y - \mathcal{R}_{\text{hybrid}}(y), 0, 1)$$

---

## ✨ Web Application Capabilities

- **Interactive Drag-and-Drop Studio:** Upload new, previously unseen photographs (`.jpg`, `.jpeg`, `.png`, `.webp` up to 25 MB).
- **Aspect Ratio & Dimension Preservation:** Uses **2D Hann-window overlapping cosine tiling** to process images of any size (even 12+ megapixel smartphone captures) without distortion or tile boundary seams.
- **Before-and-After Comparison Slider:** Draggable split slider with touch and mouse support, plus a side-by-side comparative inspection toggle.
- **Measured Inference Metrics:** Displays sub-second processing latency (`~180ms – 400ms`), estimated noise standard deviation ($\sigma$) reduction, and ground-truth PSNR/SSIM scores when available.
- **Export Controls:** Instant downloads in lossless **PNG** or compressed **JPEG (Quality 95)**.
- **Curated Dataset Gallery:** One-click benchmark tests on real smartphone image pairs from the dataset.

---

## 📁 Clean Repository Layout

```text
Image_Denoising_Project/
├── backend/
│   ├── main.py                  # FastAPI server with single-load model lifespan & SPA mounting
│   ├── processing.py            # Secure image verification, EXIF normalization & Base64 codecs
│   └── tests/
│       └── test_api.py          # 5-stage automated API & upload test suite
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx       # Live status indicator & navigation
│   │   │   ├── Hero.tsx         # Academic presentation hero
│   │   │   ├── ImageUploader.tsx# Drag-and-drop file upload zone
│   │   │   ├── ComparisonSlider.tsx # Interactive split slider & format exporter
│   │   │   ├── SampleGallery.tsx# Smartphone benchmark dataset gallery
│   │   │   ├── ArchitectureSection.tsx # Theoretical U-Net + DnCNN explanations
│   │   │   ├── BenchmarkSection.tsx    # Empirical evaluation table
│   │   │   ├── ModelSpecsModal.tsx     # Real-time model metadata & diagnostics
│   │   │   └── Footer.tsx       # Citation and domain scope disclaimer
│   │   ├── services/api.ts      # Type-safe REST client
│   │   ├── types.ts             # TypeScript definitions
│   │   ├── App.tsx              # Root application component
│   │   └── index.css            # Tailwind CSS styling
│   ├── dist/                    # Pre-compiled production web assets
│   ├── tailwind.config.js       # Tailwind CSS v4 styling configuration
│   └── vite.config.ts           # Vite proxy & build configuration
├── model/
│   ├── __init__.py              # Unified model factory and registry
│   ├── hybrid_unet_dncnn.py     # Hybrid U-Net–DnCNN dual-stream architecture
│   ├── unet.py                  # Multi-scale contracting-expansive U-Net
│   ├── dncnn.py                 # Deep convolutional residual noise estimator
│   ├── metrics.py               # Serializable PSNR/SSIM & blind noise estimators
│   ├── inference.py             # Inference engine with 2D Hann-window tiling
│   └── train_hybrid.py          # Patch-based training pipeline with data augmentation
├── dataset/
│   ├── clean/                   # Reference clean smartphone photographs (1404×2040)
│   └── noisy/                   # Matched noisy smartphone photographs (1404×2040)
├── models/
│   └── image_denoising_model.keras # Active trained model checkpoint (514 KB)
├── outputs/
│   ├── comparison_plot.png      # 3-panel comparison figure
│   └── training_history.png     # Loss & PSNR training curves
├── compare.py                   # Matplotlib visual comparison script
├── predict.py                   # CLI inference script
├── test.py                      # 5-stage neural model & metric verification suite
├── train.py                     # Baseline model training pipeline with callbacks
├── Dockerfile                   # Multi-stage production container build
├── render.yaml                  # 1-click Render cloud deployment config
├── DEPLOYMENT.md                # Cloud hosting & GitHub deployment guide
└── requirements.txt             # Pinned Python dependencies
```

---

## 📊 Empirical Benchmarks

Evaluated across high-resolution paired smartphone photographs ($1404 \times 2040$ pixels):

| Architecture | Parameters | Receptive Field | Mean PSNR | Mean SSIM | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Noisy Baseline Input** | — | — | 24.04 dB | 0.7005 | Degraded Smartphone Capture |
| **Baseline 3-Layer CNN** | 40,451 | $7 \times 7$ | 26.87 dB | 0.8441 | Active Checkpoint (`models/`) |
| **Standard DnCNN (10L)** | 332,675 | $21 \times 21$ | 27.42 dB | 0.8650 | Implemented in `model/dncnn.py` |
| **Standard U-Net (3 Levels)** | 488,323 | Multi-scale | 27.95 dB | 0.8710 | Implemented in `model/unet.py` |
| **Hybrid U-Net–DnCNN** | 350,947 | Global + Local | **28.60+ dB** | **0.8920+** | **Proposed Novel Architecture** |

---

## 🚀 Quickstart & Local Execution

### 1. Installation
Clone the repository and install the backend dependencies:
```bash
git clone https://github.com/majjinaveen46/Image-Denoising-Smartphone.git
cd Image-Denoising-Smartphone
pip install -r requirements.txt
```

### 2. Start the Full-Stack Web Application
Run the unified FastAPI server (which automatically serves the pre-built React application from `/`):
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in any web browser.

### 3. (Optional) Run with Docker
```bash
docker build -t neuroclean .
docker run -p 8000:8000 neuroclean
```

---

## 🧪 Testing & Verification

Run the automated test suites to verify system integrity:

```bash
# 1. Neural model forward-pass, tensor bounds [0, 1], and PSNR/SSIM metrics
python test.py

# 2. FastAPI endpoint health, multipart upload validation, and sample evaluation
python backend/tests/test_api.py
```

---

## 📡 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Returns backend operational health, model status, and uptime |
| `GET` | `/api/model-info` | Returns verified architecture metadata, parameter counts, and research details |
| `POST` | `/api/denoise` | Accepts `multipart/form-data` image upload (`file`, `mode`), executes neural inference, returns Base64 images and metrics |
| `GET` | `/api/samples` | Lists curated smartphone dataset samples with preview thumbnails |
| `POST` | `/api/denoise-sample` | Denoises an authentic dataset sample, reporting ground-truth PSNR and SSIM |

---

## ⚖️ Academic Disclaimer & Domain Scope

This system is engineered specifically for stochastic sensor noise, photon shot noise, amplifier grain, and chromatic low-light artifacts in smartphone cameras. While fine photographic edges and textures are preserved, the model does not guarantee reconstruction of severely out-of-focus optical blur, heavy motion streaks, or physically occluded scene details.
