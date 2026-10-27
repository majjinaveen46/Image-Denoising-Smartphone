# Deployment & GitHub Guide: NeuroClean

This guide provides simple, step-by-step instructions to push your project to **GitHub** and deploy it to a free cloud hosting service (**Render**, **Hugging Face Spaces**, or **Railway**).

---

## 🐙 Step 1: Push to GitHub

The local Git repository is already initialized and all project files have been committed to the `main` branch.

### Option A: Using GitHub CLI (`gh`) (Easiest)
In your terminal / PowerShell:
```bash
# 1. Log in to your GitHub account (opens browser authentication)
gh auth login

# 2. Create the remote repository on GitHub and push in one command:
gh repo create Image-Denoising-Smartphone --public --source=. --remote=origin --push
```

### Option B: Using Standard Git (Web UI)
1. Go to [github.com/new](https://github.com/new) and create a new repository named `Image-Denoising-Smartphone`.
2. Do **not** check "Initialize with README" (we already have a complete one).
3. Copy your repository URL and run the following in your terminal:
```bash
# Set your GitHub remote (replace <YOUR_USERNAME> with your GitHub username)
git remote add origin https://github.com/<YOUR_USERNAME>/Image-Denoising-Smartphone.git

# Push the main branch
git push -u origin main
```

---

## 🚀 Step 2: Deploy to the Cloud (Free Hosting)

Because this application includes both a **React 18 frontend** and a **Python/FastAPI/TensorFlow deep learning backend**, we have included a production-ready, multi-stage [`Dockerfile`](./Dockerfile) and [`render.yaml`](./render.yaml).

### Method 1: Deploy on Render (Recommended • 1-Click Free Web Service)
1. Go to **[render.com](https://render.com)** and sign in with your GitHub account.
2. Click **New +** → **Web Service**.
3. Select your newly created `Image-Denoising-Smartphone` repository.
4. Render will detect the [`Dockerfile`](./Dockerfile) automatically:
   - **Environment**: `Docker`
   - **Region**: Closest to you (e.g. Frankfurt, Oregon, Singapore)
   - **Branch**: `main`
5. Click **Deploy Web Service**.
6. Render will build the React frontend and Python backend, providing you with a free live public URL (e.g., `https://neuroclean-smartphone-denoising.onrender.com`).

---

### Method 2: Deploy on Hugging Face Spaces (Free 16GB RAM for Machine Learning)
Hugging Face Spaces provides generous free RAM (16 GB) specifically tailored for Deep Learning models:
1. Go to **[huggingface.co/spaces](https://huggingface.co/spaces)** and click **Create new Space**.
2. Name your space (e.g. `smartphone-image-denoising`).
3. Select **Space SDK** → **Docker** → **Blank**.
4. Set visibility to **Public** and click **Create Space**.
5. Push your code directly to the Hugging Face Space remote:
   ```bash
   git remote add space https://huggingface.co/spaces/<YOUR_HF_USERNAME>/smartphone-image-denoising
   git push space main
   ```
6. Your deep learning website will build and be live instantly on Hugging Face!

---

### Method 3: Deploy on Railway
1. Go to **[railway.app](https://railway.app)** and click **New Project** → **Deploy from GitHub repo**.
2. Select `Image-Denoising-Smartphone`.
3. Railway automatically detects the Dockerfile, builds the container, and assigns a live HTTPS public domain.

---

## 🛠️ Continuous Integration (CI)
A GitHub Actions workflow is pre-configured in [`.github/workflows/ci.yml`](./.github/workflows/ci.yml). Every time you push changes to GitHub, GitHub Actions will automatically:
- Set up Python 3.11 and Node.js 20.
- Execute unit and neural architecture tests (`python test.py`).
- Run FastAPI endpoint and file upload validation tests (`python backend/tests/test_api.py`).
- Compile the React TypeScript bundle (`npm run build`).
