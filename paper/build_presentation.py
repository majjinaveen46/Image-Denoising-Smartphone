import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    template_path = r"C:/Users/User/.gemini/antigravity/brain/429251bf-9f93-43de-8a54-81c01ce993e0/.user_uploaded/media_1793125668679_f7816a57.pptx"
    output_path = r"c:/Users/User/OneDrive/Documents/Image_Denoising_Project/paper/Project_Review_3_Image_Denoising.pptx"
    
    prs = pptx.Presentation(template_path)
    
    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides[0]
    for shape in s1.shapes:
        if shape.name == "Title 6" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            p1 = tf.paragraphs[0]
            p1.text = "B.Tech Computer Science and Engineering • Project Review 3"
            p1.font.name = "Arial"
            p1.font.size = Pt(15)
            p1.font.bold = True
            p1.font.color.rgb = RGBColor(0, 98, 155)
            p1.alignment = PP_ALIGN.CENTER
            
            p2 = tf.add_paragraph()
            p2.text = "Image Denoising Using Machine Learning for Smartphone Images"
            p2.font.name = "Arial"
            p2.font.size = Pt(22)
            p2.font.bold = True
            p2.font.color.rgb = RGBColor(20, 40, 80)
            p2.alignment = PP_ALIGN.CENTER

            p3 = tf.add_paragraph()
            p3.text = "(NeuroClean: Hybrid U-Net–DnCNN Dual-Stream Deep Learning Framework)"
            p3.font.name = "Arial"
            p3.font.size = Pt(13)
            p3.font.italic = True
            p3.font.color.rgb = RGBColor(100, 100, 100)
            p3.alignment = PP_ALIGN.CENTER

        elif shape.name == "object 3" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            p_t = tf.paragraphs[0]
            p_t.text = "Team Members:"
            p_t.font.name = "Arial"
            p_t.font.size = Pt(13)
            p_t.font.bold = True
            p_t.font.color.rgb = RGBColor(0, 98, 155)

            members = [
                ("MAJJI NAVEEN", "23BCI0131"),
                ("PARRI HARI CHANDAN", "23BCT0153"),
                ("M. SIVA CHARAN REDDY", "23BDS0156")
            ]
            for name, regno in members:
                p_m = tf.add_paragraph()
                p_m.text = f"• {name.ljust(26)} ({regno})"
                p_m.font.name = "Arial"
                p_m.font.size = Pt(12)
                p_m.font.bold = True
                p_m.font.color.rgb = RGBColor(30, 30, 30)

            p_g_lbl = tf.add_paragraph()
            p_g_lbl.text = "\nFaculty Guide / Supervisor:"
            p_g_lbl.font.name = "Arial"
            p_g_lbl.font.size = Pt(13)
            p_g_lbl.font.bold = True
            p_g_lbl.font.color.rgb = RGBColor(0, 98, 155)

            p_g = tf.add_paragraph()
            p_g.text = "Dr. JAYALAKSHMI M (Associate Professor, SCOPE)"
            p_g.font.name = "Arial"
            p_g.font.size = Pt(12)
            p_g.font.bold = True
            p_g.font.color.rgb = RGBColor(30, 30, 30)

    # -------------------------------------------------------------
    # SLIDE 2: Approval Mail From Guide
    # -------------------------------------------------------------
    s2 = prs.slides[1]
    for shape in s2.shapes:
        if shape.name == "Content Placeholder 2" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            p = tf.paragraphs[0]
            p.text = "Project Review Approval Status:"
            p.font.name = "Arial"
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = RGBColor(0, 98, 155)
            
            p_meta = tf.add_paragraph()
            p_meta.text = "• Project ID: 11790UG05   |   Semester: Fall Semester   |   Review: Project Review 3\n"
            p_meta.font.name = "Arial"
            p_meta.font.size = Pt(12)
            p_meta.font.bold = True
            p_meta.font.color.rgb = RGBColor(40, 40, 40)

            p_email_hdr = tf.add_paragraph()
            p_email_hdr.text = "Guide Approval Confirmation (Sample Record):"
            p_email_hdr.font.name = "Arial"
            p_email_hdr.font.size = Pt(12.5)
            p_email_hdr.font.bold = True
            p_email_hdr.font.color.rgb = RGBColor(0, 98, 155)

            p_conf = tf.add_paragraph()
            p_conf.text = "\"The Fall Semester Project Review 3 for Project ID 11790UG05 has been approved.\""
            p_conf.font.name = "Arial"
            p_conf.font.size = Pt(13)
            p_conf.font.bold = True
            p_conf.font.italic = True
            p_conf.font.color.rgb = RGBColor(20, 80, 20)

            approval_items = [
                ("Meeting with Guide Frequently", "Satisfied"),
                ("PowerPoint Presentation", "Approved"),
                ("Project Demonstration", "Approved"),
                ("Final Project Report", "Satisfied"),
                ("Project Outcome", "Completed"),
                ("Turnitin Plagiarism Percentage", "13%"),
                ("Turnitin AI Score", "Nil % (Requirement: <= 25%)")
            ]
            for k, v in approval_items:
                p_item = tf.add_paragraph()
                p_item.text = f"   [APPROVED]  {k}:  {v}"
                p_item.font.name = "Arial"
                p_item.font.size = Pt(11.5)
                p_item.font.bold = (k in ["Project Outcome", "Turnitin Plagiarism Percentage", "Turnitin AI Score"])
                if k in ["Project Outcome", "Turnitin Plagiarism Percentage", "Turnitin AI Score"]:
                    p_item.font.color.rgb = RGBColor(0, 100, 50)
                else:
                    p_item.font.color.rgb = RGBColor(40, 40, 40)

            p_end = tf.add_paragraph()
            p_end.text = "\nAll the above aspects are addressed, implemented, and updated by the project team."
            p_end.font.name = "Arial"
            p_end.font.size = Pt(11.5)
            p_end.font.italic = True
            p_end.font.color.rgb = RGBColor(70, 70, 70)

    # -------------------------------------------------------------
    # SLIDE 3: Aim
    # -------------------------------------------------------------
    s3 = prs.slides[2]
    for shape in s3.shapes:
        if shape.name == "Content Placeholder 2" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            p = tf.paragraphs[0]
            p.text = "Primary Aim:"
            p.font.name = "Arial"
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = RGBColor(0, 98, 155)

            p_aim = tf.add_paragraph()
            p_aim.text = (
                "To design, develop, and deploy a robust deep-learning-based computational photography system "
                "(NeuroClean) that effectively removes stochastic Poisson photon shot noise, amplifier read noise, "
                "and chromatic grain from high-ISO and low-light smartphone photographs, while rigorously preserving "
                "100% of native image dimensions, aspect ratios, and fine textural fidelity."
            )
            p_aim.font.name = "Arial"
            p_aim.font.size = Pt(13)
            p_aim.font.color.rgb = RGBColor(30, 30, 30)

            p_core = tf.add_paragraph()
            p_core.text = "\nKey Sub-Aims:"
            p_core.font.name = "Arial"
            p_core.font.size = Pt(13)
            p_core.font.bold = True
            p_core.font.color.rgb = RGBColor(0, 98, 155)

            sub_aims = [
                "Dual-Stream Neural Modeling: Formulate a hybrid U-Net–DnCNN architecture to extract macro contextual illumination while preserving micro-scale spatial edge details.",
                "Deep Residual Subtraction: Train the model to isolate the underlying noise field R(y) rather than direct clean image generation: x̂ = clip(y - R_hybrid(y), 0, 1).",
                "Artifact-Free Full-Resolution Tiling: Implement a 2D Hann-window overlapping cosine tiling engine with exact partition of unity to eliminate border stitching seams and GPU memory faults.",
                "End-to-End Web-Based Deployment: Deploy an asynchronous FastAPI microservice paired with a responsive React/TypeScript studio featuring real-time before/after split sliders and Three.js 3D sensor simulation."
            ]
            for sa in sub_aims:
                p_sa = tf.add_paragraph()
                p_sa.text = f"• {sa}"
                p_sa.font.name = "Arial"
                p_sa.font.size = Pt(11.5)
                p_sa.font.color.rgb = RGBColor(40, 40, 40)

    # -------------------------------------------------------------
    # SLIDE 4: Abstract
    # -------------------------------------------------------------
    s4 = prs.slides[3]
    for shape in s4.shapes:
        if shape.name == "Content Placeholder 2" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            p1 = tf.paragraphs[0]
            p1.text = "Problem Statement & Context:"
            p1.font.name = "Arial"
            p1.font.size = Pt(13)
            p1.font.bold = True
            p1.font.color.rgb = RGBColor(0, 98, 155)

            p1_b = tf.add_paragraph()
            p1_b.text = (
                "Smartphone camera sensors are physically restricted by sub-micron to micron pixel pitches (1.0–1.4 μm) "
                "and micro-apertures. Under low-light settings, severe Poisson photon shot noise and chromatic mottling degrade "
                "image fidelity. Standard multi-scale autoencoders (U-Net) oversmooth high-frequency textures through spatial pooling, "
                "whereas feed-forward networks (DnCNN) have strictly limited receptive fields (21×21 pixels), failing to remove wide-area chroma blotches."
            )
            p1_b.font.name = "Arial"
            p1_b.font.size = Pt(11)
            p1_b.font.color.rgb = RGBColor(40, 40, 40)

            p2 = tf.add_paragraph()
            p2.text = "\nProposed Hybrid Methodology & Tiling Engine:"
            p2.font.name = "Arial"
            p2.font.size = Pt(13)
            p2.font.bold = True
            p2.font.color.rgb = RGBColor(0, 98, 155)

            p2_b = tf.add_paragraph()
            p2_b.text = (
                "We propose NeuroClean, introducing a dual-stream Hybrid U-Net–DnCNN architecture that combines multi-scale context flow "
                "with non-pooling residual grain modeling joined by 1×1 cross-channel fusion. To process arbitrary megapixel photographs "
                "without memory bloat or boundary seams, we engineer a 2D Hann-window overlapping cosine tiling engine satisfying the mathematical "
                "partition of unity (Σ w = 1.0)."
            )
            p2_b.font.name = "Arial"
            p2_b.font.size = Pt(11)
            p2_b.font.color.rgb = RGBColor(40, 40, 40)

            p3 = tf.add_paragraph()
            p3.text = "\nKey Results & Outcomes:"
            p3.font.name = "Arial"
            p3.font.size = Pt(13)
            p3.font.bold = True
            p3.font.color.rgb = RGBColor(0, 98, 155)

            p3_b = tf.add_paragraph()
            p3_b.text = (
                "Evaluated on paired real-world smartphone photographs (1404×2040 native resolution), our model achieves 28.60+ dB PSNR "
                "and 0.8920+ SSIM (+4.56 dB and +0.1915 over raw noisy baseline, p < 0.001). The system is deployed online via an asynchronous "
                "FastAPI backend and React glassmorphic UI, with a full-length manuscript prepared for Springer Nature (MTAP)."
            )
            p3_b.font.name = "Arial"
            p3_b.font.size = Pt(11)
            p3_b.font.color.rgb = RGBColor(40, 40, 40)

    # -------------------------------------------------------------
    # SLIDE 5: Literature Review
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    # In slide 5, add a structured table
    table_shape = s5.shapes.add_table(rows=6, cols=5, left=Inches(0.6), top=Inches(1.8), width=Inches(12.1), height=Inches(4.5))
    tbl = table_shape.table
    
    headers = ["Paper / Author", "Objective", "Methodology", "Pros / Cons", "Findings / Limitations"]
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0, 98, 155)
        for p in cell.text_frame.paragraphs:
            p.font.name = "Arial"
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.alignment = PP_ALIGN.CENTER

    lit_data = [
        (
            "BM3D\n(Dabov et al., 2007)",
            "Image denoising using transform domain sparsity",
            "Block-matching and 3D collaborative Wiener filtering in transform domain",
            "Pros: Strong benchmark on Gaussian noise\nCons: O(N²) search complexity, blurs real camera grain",
            "Introduces watercolor-like smearing on real smartphone noise patterns."
        ),
        (
            "DnCNN\n(Zhang et al., 2017)",
            "Deep CNN for residual noise estimation",
            "17-20 convolutional layers with Batch Normalization & ReLU operating at full resolution",
            "Pros: Fast convergence, preserves fine grain\nCons: Receptive field strictly limited to 21×21 pixels",
            "Cannot resolve wide-area chroma blotches due to depth-bounded receptive field."
        ),
        (
            "U-Net\n(Ronneberger et al., 2015)",
            "Contextual feature preservation for image restoration",
            "Contracting-expansive encoder-decoder with pooling and long skip connections",
            "Pros: Captures global context and luminance\nCons: Spatial pooling destroys micro-textures",
            "Causes edge softening and phase artifacts upon bilinear/transposed upsampling."
        ),
        (
            "CBDNet\n(Guo et al., 2019)",
            "Blind denoising for real camera photographs",
            "Noise estimation subnetwork coupled with asymmetric loss and U-Net backbone",
            "Pros: Realistic noise modeling\nCons: High compute cost, complex multi-network training",
            "Effective on synthetic-real blend, but heavy latency for interactive web inference."
        ),
        (
            "Restormer\n(Zamir et al., 2022)",
            "Transformer-based high-resolution restoration",
            "Multi-Dconv head transposed attention with gated feed-forward networks",
            "Pros: High benchmark scores on crop datasets\nCons: Prohibitive compute requirements for edge",
            "Too memory-intensive for direct full-resolution processing on mobile/standard GPUs."
        )
    ]

    for r_idx, row in enumerate(lit_data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            if r_idx % 2 == 0:
                cell.fill.fore_color.rgb = RGBColor(245, 248, 250)
            else:
                cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
            for p in cell.text_frame.paragraphs:
                p.font.name = "Arial"
                p.font.size = Pt(9)
                p.font.color.rgb = RGBColor(30, 30, 30)

    # -------------------------------------------------------------
    # SLIDE 6: Research Gap
    # -------------------------------------------------------------
    s6 = prs.slides[5]
    for shape in s6.shapes:
        if shape.name == "Content Placeholder 2" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            gaps = [
                (
                    "Gap 1: The Context vs. Texture Grain Dilemma",
                    "Existing deep restoration networks force a compromise: deep feed-forward models (DnCNN) maintain native resolution and capture fine pixel grain but have a mathematically bounded receptive field (21×21 pixels), making them blind to wide-area chroma mottling. Conversely, multi-scale encoder-decoder networks (U-Net) capture global luminance context through pooling but destroy organic high-frequency textures."
                ),
                (
                    "Gap 2: High-Resolution Tiling & Boundary Discontinuity Barrier",
                    "Real smartphone photographs regularly exceed 12 to 48 megapixels (3000×4000 to 6000×8000). Direct whole-image tensor processing triggers fatal GPU Out-Of-Memory (OOM) allocation faults. Naive non-overlapping block tiling creates severe orthogonal grid-line boundary stitching discontinuities due to truncated receptive fields at patch edges."
                ),
                (
                    "Gap 3: The Prototype-to-Production Deployment Disconnect",
                    "The overwhelming majority of image denoising research terminates with isolated offline Python or MATLAB scripts tested on downsampled crops. There is a lack of accessible, full-stack, privacy-preserving web services supporting arbitrary dimensions, aspect ratios, live quality metrics, and interactive client-side before/after split sliders."
                )
            ]
            for idx, (title, desc) in enumerate(gaps):
                p_t = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                p_t.text = f"{title}:"
                p_t.font.name = "Arial"
                p_t.font.size = Pt(13)
                p_t.font.bold = True
                p_t.font.color.rgb = RGBColor(0, 98, 155)

                p_d = tf.add_paragraph()
                p_d.text = desc + "\n"
                p_d.font.name = "Arial"
                p_d.font.size = Pt(11)
                p_d.font.color.rgb = RGBColor(40, 40, 40)

    # -------------------------------------------------------------
    # SLIDE 7: Objectives, SDG & TRL
    # -------------------------------------------------------------
    s7 = prs.slides[6]
    for shape in s7.shapes:
        if shape.name == "Content Placeholder 2" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            objs = [
                "1. Dual-Stream Synergy: Design a Hybrid U-Net–DnCNN architecture combining multi-scale context flow with non-pooling residual grain modeling via 1×1 cross-channel fusion.",
                "2. Deep Residual Learning: Formulate the network objective as residual noise estimation R(y), recovering clean images via x̂ = clip(y - R_hybrid(y), 0, 1).",
                "3. Seamless Tiling Engine: Formulate and implement a 2D Hann-window overlapping cosine tiling engine with partition-of-unity proof (Σ w = 1.0) to process arbitrary dimensions without boundary artifacts.",
                "4. Empirical Validation: Benchmark the model against classical and deep learning baselines on 100 paired real-world smartphone captures (1404×2040) with Holm-corrected statistical tests.",
                "5. Full-Stack Cloud Deployment: Deliver an open-source, asynchronous web studio (FastAPI + React 18) featuring live noise estimation (σ̂) and a 3D Three.js photodiode visualizer."
            ]
            for idx, ob in enumerate(objs):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                p.text = ob
                p.font.name = "Arial"
                p.font.size = Pt(10.5)
                p.font.color.rgb = RGBColor(30, 30, 30)

        elif shape.name == "TextBox 6" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            p1 = tf.paragraphs[0]
            p1.text = "Identified Sustainable Development Goals (SDG):"
            p1.font.name = "Arial"
            p1.font.size = Pt(11)
            p1.font.bold = True
            p1.font.color.rgb = RGBColor(0, 98, 155)

            p2 = tf.add_paragraph()
            p2.text = "• SDG 9: Industry, Innovation and Infrastructure (Edge AI for Mobile ISPs)\n• SDG 12: Responsible Consumption (Extending smartphone hardware lifespan via AI)"
            p2.font.name = "Arial"
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = RGBColor(40, 40, 40)

            p3 = tf.add_paragraph()
            p3.text = "\nTechnology Readiness Level (TRL) & Outcomes:"
            p3.font.name = "Arial"
            p3.font.size = Pt(11)
            p3.font.bold = True
            p3.font.color.rgb = RGBColor(0, 98, 155)

            p4 = tf.add_paragraph()
            p4.text = "• TRL Level: TRL 7 / 8 (System Prototype in Operational Environment - Live Web Application)\n• Outcome Achieved: Full Research Manuscript prepared for Springer Nature (MTAP) / IEEE Access (Turnitin: 13%, Nil% AI)"
            p4.font.name = "Arial"
            p4.font.size = Pt(9.5)
            p4.font.bold = True
            p4.font.color.rgb = RGBColor(0, 100, 50)

    # -------------------------------------------------------------
    # SLIDE 8: Framework / Architecture / Block Diagram
    # -------------------------------------------------------------
    s8 = prs.slides[7]
    for shape in s8.shapes:
        if shape.name == "Content Placeholder 2" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            p1 = tf.paragraphs[0]
            p1.text = "End-to-End System Architecture Pipeline:"
            p1.font.name = "Arial"
            p1.font.size = Pt(13)
            p1.font.bold = True
            p1.font.color.rgb = RGBColor(0, 98, 155)

            steps = [
                ("1. Input Capture (y = x + v):", "Accepts arbitrary resolution RGB smartphone images degraded by Poisson-Gaussian noise."),
                ("2. 2D Hann-Window Tiling:", "Decomposes input into 256×256 patches with 50% overlap (stride 128) and symmetric reflection padding."),
                ("3. Stream 1 (Contextual U-Net):", "Two contracting conv blocks (32/64 filters) with max-pooling, 128-filter bottleneck, expansive decoder with skip connections (captures macro-luminance)."),
                ("4. Stream 2 (High-Frequency DnCNN):", "10 non-pooling convolutional layers with Batch Normalization & ReLU (isolates micro-grain without pooling loss)."),
                ("5. Cross-Stream Feature Fusion:", "Concatenates representations (64 channels) followed by a 1×1 convolution with BatchNorm to learn inter-branch non-linear dependencies."),
                ("6. Deep Residual Estimation & Subtraction:", "Estimates 3-channel noise field R_hybrid(y), recovering clean image: x̂ = clip(y - R_hybrid(y), 0, 1)."),
                ("7. Weighted Overlap-Add Reassembly:", "Blends predicted patches using 2D separable Hann cosine weights; normalizes by accumulated window weights to guarantee seamless output.")
            ]
            for title, desc in steps:
                p_s = tf.add_paragraph()
                p_s.text = f"• {title} {desc}"
                p_s.font.name = "Arial"
                p_s.font.size = Pt(10)
                p_s.font.color.rgb = RGBColor(40, 40, 40)

    # -------------------------------------------------------------
    # SLIDE 9: Functional Requirements
    # -------------------------------------------------------------
    s9 = prs.slides[8]
    for shape in s9.shapes:
        if shape.name == "Content Placeholder 2" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            reqs = [
                ("FR1: Multi-Format Image Ingestion & Validation", "Support JPEG, JPG, PNG, and WebP up to 25 MB with strict magic-byte validation and anti-path-traversal protection."),
                ("FR2: EXIF Orientation & Dimension Preservation", "Automatically correct orientation flags (ImageOps.exif_transpose) and preserve 100% of native pixel dimensions without forced resizing."),
                ("FR3: Asynchronous Deep Learning Execution", "Execute model inference in sub-second latency through single-load model caching in GPU/CPU memory (no per-request re-initialization)."),
                ("FR4: Memory-Bounded Full-Resolution Tiling", "Support multi-megapixel smartphone captures (12+ to 48 MP) via 2D Hann-window overlapping tiling with a constant memory footprint under 620 MB."),
                ("FR5: Interactive Before/After Split Inspection", "Provide a touch/pointer-enabled interactive comparison slider with a side-by-side inspection toggle for instant visual verification."),
                ("FR6: Real-Time Quality Metrics & Noise Variance", "Display measured processing latency (ms), ground-truth PSNR/SSIM, and Immerkaer Laplacian blind noise standard deviation estimation (σ̂)."),
                ("FR7: Secure Export & In-Memory Privacy", "Stream processed images directly to the client via Base64/Blob data URIs with zero permanent server-side file retention.")
            ]
            for idx, (title, desc) in enumerate(reqs):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                p.text = f"• {title}: {desc}"
                p.font.name = "Arial"
                p.font.size = Pt(10)
                p.font.color.rgb = RGBColor(30, 30, 30)

    # -------------------------------------------------------------
    # SLIDE 10: Modules
    # -------------------------------------------------------------
    s10 = prs.slides[9]
    for shape in s10.shapes:
        if shape.name == "Content Placeholder 2" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            mods = [
                (
                    "Module 1: Preprocessing & Ingestion Engine",
                    "Performs secure image decoding, EXIF orientation correction, float32 normalization to [0, 1], and boundary reflection padding."
                ),
                (
                    "Module 2: Hybrid U-Net–DnCNN Deep Learning Core",
                    "Implements the dual-stream feature extraction network in TensorFlow/Keras, combining contracting-expansive U-Net with non-pooling residual DnCNN and 1×1 fusion."
                ),
                (
                    "Module 3: 2D Hann-Window Tiling & Blending Engine",
                    "Executes 256×256 patch extraction at 50% stride (S=128), batched neural forward passes, and weighted overlap-add synthesis satisfying partition of unity."
                ),
                (
                    "Module 4: Asynchronous REST Microservice (FastAPI)",
                    "Provides high-throughput endpoints (POST /api/denoise, GET /api/health, GET /api/model-info) with single-load model lifespan and memory-safe streaming."
                ),
                (
                    "Module 5: Interactive Glassmorphic Web UI & 3D WebGL Visualizer",
                    "Built with React 18, TypeScript, and Tailwind CSS v4, featuring Dark/Light mode, before/after split sliders, and a Three.js 3D photodiode sensor simulation."
                )
            ]
            for idx, (title, desc) in enumerate(mods):
                p_t = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                p_t.text = f"{title}:"
                p_t.font.name = "Arial"
                p_t.font.size = Pt(12)
                p_t.font.bold = True
                p_t.font.color.rgb = RGBColor(0, 98, 155)

                p_d = tf.add_paragraph()
                p_d.text = desc + "\n"
                p_d.font.name = "Arial"
                p_d.font.size = Pt(10.5)
                p_d.font.color.rgb = RGBColor(40, 40, 40)

    # -------------------------------------------------------------
    # SLIDE 11: Experiments and Results
    # -------------------------------------------------------------
    s11 = prs.slides[10]
    for shape in s11.shapes:
        if shape.name == "Content Placeholder 2" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            p1 = tf.paragraphs[0]
            p1.text = "Quantitative Restoration Benchmarks on Smartphone Dataset (1404×2040 native resolution):"
            p1.font.name = "Arial"
            p1.font.size = Pt(11)
            p1.font.bold = True
            p1.font.color.rgb = RGBColor(0, 98, 155)

    # Add results table on slide 11
    t11_shape = s11.shapes.add_table(rows=6, cols=5, left=Inches(0.6), top=Inches(2.2), width=Inches(12.1), height=Inches(2.2))
    tbl11 = t11_shape.table
    
    t11_hdrs = ["Architecture / Model", "Parameters", "Receptive Field", "Mean PSNR (dB)", "Mean SSIM"]
    for i, h in enumerate(t11_hdrs):
        c = tbl11.cell(0, i)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = RGBColor(0, 98, 155)
        for p in c.text_frame.paragraphs:
            p.font.name = "Arial"
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.alignment = PP_ALIGN.CENTER

    results_data = [
        ("Noisy Baseline Input", "—", "—", "24.04 ± 0.42 dB", "0.7005"),
        ("Baseline 3-Layer CNN", "40,451", "7 × 7", "26.87 ± 0.31 dB", "0.8441"),
        ("Standard DnCNN (10 Layers)", "332,675", "21 × 21", "27.42 ± 0.28 dB", "0.8650"),
        ("Standard U-Net (3 Levels)", "488,323", "Multi-Scale (~68px)", "27.95 ± 0.25 dB", "0.8710"),
        ("Proposed Hybrid U-Net–DnCNN", "350,947", "Dual-Scale (Global+Local)", "28.60 ± 0.22 dB", "0.8920")
    ]
    for r_idx, row in enumerate(results_data):
        for c_idx, val in enumerate(row):
            c = tbl11.cell(r_idx + 1, c_idx)
            c.text = val
            c.fill.solid()
            if r_idx == 4:
                c.fill.fore_color.rgb = RGBColor(230, 245, 255)
            elif r_idx % 2 == 0:
                c.fill.fore_color.rgb = RGBColor(248, 250, 252)
            else:
                c.fill.fore_color.rgb = RGBColor(255, 255, 255)
            for p in c.text_frame.paragraphs:
                p.font.name = "Arial"
                p.font.size = Pt(9.5)
                if r_idx == 4:
                    p.font.bold = True
                    p.font.color.rgb = RGBColor(0, 98, 155)
                else:
                    p.font.color.rgb = RGBColor(30, 30, 30)

    # Add text summary below table
    tx_box = s11.shapes.add_textbox(left=Inches(0.6), top=Inches(4.6), width=Inches(12.1), height=Inches(2.0))
    tf_b = tx_box.text_frame
    p_b1 = tf_b.paragraphs[0]
    p_b1.text = "Key Experimental Findings:"
    p_b1.font.name = "Arial"
    p_b1.font.size = Pt(11)
    p_b1.font.bold = True
    p_b1.font.color.rgb = RGBColor(0, 98, 155)

    res_findings = [
        "Restoration Gain: Proposed Hybrid model achieves +4.56 dB PSNR and +0.1915 SSIM over raw capture, outperforming U-Net by +0.65 dB and DnCNN by +1.18 dB (Wilcoxon signed-rank test p < 0.001).",
        "Ablation Proof: Removing DnCNN drops SSIM by 0.0210 (texture blurring); removing U-Net drops PSNR by 1.18 dB (chroma blotches). 1×1 cross-channel fusion adds +0.42 dB over simple concatenation.",
        "Tiling Seam Elimination: Naive tiling causes severe boundary grid lines (Mean Boundary Discontinuity MBGD = 0.0842), whereas 2D Hann-window tiling suppresses seams to an imperceptible MBGD = 0.0012 within 620 MB VRAM."
    ]
    for rf in res_findings:
        p_rf = tf_b.add_paragraph()
        p_rf.text = f"• {rf}"
        p_rf.font.name = "Arial"
        p_rf.font.size = Pt(10)
        p_rf.font.color.rgb = RGBColor(40, 40, 40)

    # -------------------------------------------------------------
    # SLIDE 12: Conclusion and Future Work
    # -------------------------------------------------------------
    s12 = prs.slides[11]
    for shape in s12.shapes:
        if shape.name == "Content Placeholder 2" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            p1 = tf.paragraphs[0]
            p1.text = "Conclusion:"
            p1.font.name = "Arial"
            p1.font.size = Pt(13)
            p1.font.bold = True
            p1.font.color.rgb = RGBColor(0, 98, 155)

            concl_points = [
                "Developed NeuroClean, a dual-stream Hybrid U-Net–DnCNN neural network that simultaneously resolves large-scale luminance mottling and isolates fine stochastic sensor grain in smartphone photography.",
                "Formulated deep residual noise learning, establishing superior convergence stability and structural edge preservation compared to direct clean image synthesis.",
                "Engineered a 2D Hann-window overlapping cosine tiling engine with partition of unity, completely eliminating boundary seam discontinuities while preserving 100% of native image dimensions.",
                "Validated statistically significant improvements across paired smartphone captures (28.60+ dB PSNR, 0.8920+ SSIM, p < 0.001) and delivered an open-source, full-stack cloud web studio."
            ]
            for cp in concl_points:
                p_c = tf.add_paragraph()
                p_c.text = f"• {cp}"
                p_c.font.name = "Arial"
                p_c.font.size = Pt(10.5)
                p_c.font.color.rgb = RGBColor(40, 40, 40)

            p2 = tf.add_paragraph()
            p2.text = "\nFuture Work & Roadmap:"
            p2.font.name = "Arial"
            p2.font.size = Pt(13)
            p2.font.bold = True
            p2.font.color.rgb = RGBColor(0, 98, 155)

            fw_points = [
                "1. RAW Bayer-Pattern Sensor Denoising: Extend the hybrid model to raw sensor data prior to ISP demosaicing and non-linear tone-curve mapping.",
                "2. Temporal Multi-Frame Video Fusion: Incorporate temporal recurrent connections for low-light smartphone video restoration.",
                "3. Hardware Quantization: Quantize the network to 8-bit integer (INT8) precision using TensorRT and CoreML for on-device mobile NPU deployment."
            ]
            for fp in fw_points:
                p_f = tf.add_paragraph()
                p_f.text = f"• {fp}"
                p_f.font.name = "Arial"
                p_f.font.size = Pt(10.5)
                p_f.font.color.rgb = RGBColor(40, 40, 40)

    # -------------------------------------------------------------
    # SLIDE 13: Outcome Achieved
    # -------------------------------------------------------------
    s13 = prs.slides[12]
    for shape in s13.shapes:
        if shape.name == "Content Placeholder 2" and shape.has_text_frame:
            tf = shape.text_frame
            tf.clear()
            
            p1 = tf.paragraphs[0]
            p1.text = "1. Research Journal Publication (Prepared & Submitted):"
            p1.font.name = "Arial"
            p1.font.size = Pt(13)
            p1.font.bold = True
            p1.font.color.rgb = RGBColor(0, 98, 155)

            p1_b = tf.add_paragraph()
            p1_b.text = (
                "• Manuscript Title: \"NeuroClean: High-Fidelity Smartphone Image Denoising via Hybrid U-Net–DnCNN Dual-Stream Deep Learning and Overlapping Hann-Window Tiling\"\n"
                "• Target Journal: Multimedia Tools and Applications (Springer Nature) / IEEE Access\n"
                "• Plagiarism & AI Verification: Turnitin Plagiarism: 13%   |   Turnitin AI Score: Nil %\n"
                "• Authors: Majji Naveen, Parri Hari Chandan, M. Siva Charan Reddy, under the Supervision of Dr. Jayalakshmi M"
            )
            p1_b.font.name = "Arial"
            p1_b.font.size = Pt(10.5)
            p1_b.font.color.rgb = RGBColor(30, 30, 30)

            p2 = tf.add_paragraph()
            p2.text = "\n2. Live Production Cloud Deployment:"
            p2.font.name = "Arial"
            p2.font.size = Pt(13)
            p2.font.bold = True
            p2.font.color.rgb = RGBColor(0, 98, 155)

            p2_b = tf.add_paragraph()
            p2_b.text = (
                "• Live Public URL: https://majjinaveen46.github.io/Image-Denoising-Smartphone/\n"
                "• Deployed with FastAPI asynchronous backend, React glassmorphic UI, live noise metrics, and 3D WebGL sensor visualizer."
            )
            p2_b.font.name = "Arial"
            p2_b.font.size = Pt(10.5)
            p2_b.font.color.rgb = RGBColor(30, 30, 30)

            p3 = tf.add_paragraph()
            p3.text = "\n3. Open-Source Codebase & Artifacts:"
            p3.font.name = "Arial"
            p3.font.size = Pt(13)
            p3.font.bold = True
            p3.font.color.rgb = RGBColor(0, 98, 155)

            p3_b = tf.add_paragraph()
            p3_b.text = (
                "• GitHub Repository: https://github.com/majjinaveen46/Image-Denoising-Smartphone\n"
                "• Includes model weights, Hann-window tiling pipeline, automated test suite, Docker container, and documentation."
            )
            p3_b.font.name = "Arial"
            p3_b.font.size = Pt(10.5)
            p3_b.font.color.rgb = RGBColor(30, 30, 30)

    # -------------------------------------------------------------
    # SLIDE 14: References
    # -------------------------------------------------------------
    s14 = prs.slides[13]
    # Remove existing text frames or placeholders on Slide 14 to provide clean 2-column layout
    shapes_to_remove = [s for s in s14.shapes if s.name in ["Rectangle 3", "Content Placeholder 2"]]
    for shp in shapes_to_remove:
        # Clear text frame content
        if shp.has_text_frame:
            shp.text_frame.clear()
            shp.width = Inches(0.1)
            shp.height = Inches(0.1)
            shp.left = Inches(14.0) # Move out of view

    refs_data = [
        (1, "A. Dudhane, S. W. Zamir, S. Khan, and F. S. Khan, \"Burst Image Restoration and Enhancement,\" in Proc. CVPR / arXiv:2110.03680, 2022.", "https://arxiv.org/abs/2110.03680"),
        (2, "R. Flepp, A. Ignatov, R. Timofte, and L. Van Gool, \"Real-World Mobile Image Denoising Dataset with Efficient Baselines,\" in Proc. IEEE/CVF CVPR, pp. 2596–2606, 2024.", "https://paperswithcode.com/paper/real-world-mobile-image-denoising-dataset"),
        (3, "S. Guo, \"Toward effective image restoration from raw domain,\" Ph.D. Dissertation, Dept. of Computing, The Hong Kong Polytechnic University, 2024.", "https://theses.lib.polyu.edu.hk/handle/200/12922"),
        (4, "Z. Li, H. Liu, L. Cheng, and X. Jia, \"Image Denoising Algorithm Based on Gradient Domain Guided Filtering and NSST,\" IEEE Access, vol. 11, pp. 11923–11933, 2023.", "https://ieeexplore.ieee.org/document/10035968"),
        (5, "L. Kumari, N. Mittal, and M. Modi, \"Comparative Analysis of Noise Reduction Filters for Medical Images,\" ResearchGate / Signal & Image Processing, 2024.", "https://www.researchgate.net/publication/379162688_Comparative_Analysis_of_Noise_Reduction_Filters_for_Medical_Images"),
        (6, "J. Lee, \"Development of Alternative Filters to Enhance the Quality of Digital Images,\" ResearchGate / Digital Imaging Systems, 2024.", "https://www.researchgate.net/publication/379091587_Development_of_Alternative_Filters_to_Enhance_the_Quality_of_Digital_Images"),
        (7, "R. S. Jebur, M. H. Bin Mohamed Zabil, D. A. Hammood, and L. K. Cheng, \"A comprehensive review of image denoising in deep learning,\" Multimedia Tools and Applications, Springer, 2023.", "https://link.springer.com/article/10.1007/s11042-023-17468-2"),
        (8, "S. Mittal et al., \"LIVENet: A Novel Network for Real-World Low-Light Image Denoising and Enhancement,\" in Proc. IEEE/CVF WACV, pp. 2960–2970, 2024.", "https://ieeexplore.ieee.org/document/10483686"),
        (9, "Z. Zhou, Y. Chen, and Y. Zhou, \"Deep Dynamic Memory Augmented Attentional Dictionary Learning for Image Denoising,\" IEEE Trans. Circuits Syst. Video Technol., vol. 33, no. 9, pp. 4668–4682, 2023.", "https://ieeexplore.ieee.org/abstract/document/10054440"),
        (10, "O. Gupta, I. N. Kalapala, and K. M. Bhurchandi, \"Enhancing Image Denoising Performance through a Family of Algorithms,\" in Proc. IEEE ISCON, pp. 1–6, 2023.", "https://ieeexplore.ieee.org/abstract/document/10136117"),
        (11, "L. Zhou, D. Zhou, H. Yang, S. Yang, and L. Nie, \"Multi-scale network toward real-world image denoising,\" Int. J. Machine Learning & Cybernetics, Springer, vol. 14, pp. 1109–1123, 2023.", "https://link.springer.com/article/10.1007/s13042-022-01694-5"),
        (12, "A. Ulu, G. Yildiz, and B. Dizdaroğlu, \"MLFAN: Multilevel Feature Attention Network With Texture Prior for Image Denoising,\" IEEE Access, vol. 11, pp. 35647–35661, 2023.", "https://ieeexplore.ieee.org/abstract/document/10092851"),
        (13, "G. Zhang, G. Zhang, Q. Lu, Y. Bo, and X. Zhou, \"Application of Improved Canny Algorithm in Image Edge Detection of Transmission Lines,\" in Proc. IEEE ICICML, pp. 312–316, 2024.", "https://ieeexplore.ieee.org/abstract/document/10424911"),
        (14, "A. Ranganath, F. Santiago, O. DeGuchy, M. Singhal, and R. F. Marcia, \"Recurrent Neural Imaging: An Evolutionary Approach for Mixed Poisson-Gaussian Image Denoising,\" in Proc. IEEE DISCOVERY, pp. 1–6, 2023.", "https://ieeexplore.ieee.org/abstract/document/10069162/"),
        (15, "T. Direk, \"Image denoising by linear regression on non-local means algorithm,\" Signal, Image and Video Processing, Springer, vol. 18, pp. 3185–3194, 2024.", "https://link.springer.com/article/10.1007/s11760-024-03086-4")
    ]

    col1_refs = refs_data[:8]
    col2_refs = refs_data[8:]

    def populate_ref_box(left, top, width, height, refs_slice):
        box = s14.shapes.add_textbox(left, top, width, height)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.05)
        tf.margin_right = Inches(0.05)
        tf.margin_top = Inches(0.05)
        tf.margin_bottom = Inches(0.05)
        for idx, (num, cit, url) in enumerate(refs_slice):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.space_after = Pt(4)
            p.line_spacing = 1.05
            
            # Number & Citation
            r_num = p.add_run()
            r_num.text = f"[{num}] "
            r_num.font.name = "Arial"
            r_num.font.size = Pt(8.5)
            r_num.font.bold = True
            r_num.font.color.rgb = RGBColor(0, 98, 155)

            r_cit = p.add_run()
            r_cit.text = f"{cit} "
            r_cit.font.name = "Arial"
            r_cit.font.size = Pt(8.0)
            r_cit.font.color.rgb = RGBColor(40, 40, 40)

            # Hyperlink
            r_link = p.add_run()
            r_link.text = "[Link]"
            r_link.font.name = "Arial"
            r_link.font.size = Pt(8.0)
            r_link.font.bold = True
            r_link.font.underline = True
            r_link.font.color.rgb = RGBColor(0, 102, 204)
            r_link.hyperlink.address = url

    populate_ref_box(Inches(0.6), Inches(1.45), Inches(5.8), Inches(5.3), col1_refs)
    populate_ref_box(Inches(6.7), Inches(1.45), Inches(5.8), Inches(5.3), col2_refs)

    prs.save(output_path)
    print(f"[SUCCESS] Presentation generated successfully at: {output_path}")

if __name__ == "__main__":
    build_presentation()
