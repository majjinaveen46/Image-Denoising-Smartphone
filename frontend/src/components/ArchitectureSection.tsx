import React from 'react';
import { Cpu, GitFork, Minimize2, Sparkles, CheckCircle2 } from 'lucide-react';
import { Sensor3DVisualizer } from './Sensor3DVisualizer';

interface ArchitectureSectionProps {
  theme: 'dark' | 'light';
}

export const ArchitectureSection: React.FC<ArchitectureSectionProps> = ({ theme }) => {
  return (
    <section id="architecture" className="py-20 border-t border-slate-200/80 dark:border-slate-800/80 bg-slate-50/50 dark:bg-slate-950/40 transition-colors duration-300">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-14">
        
        {/* Section Title */}
        <div className="text-center max-w-3xl mx-auto">
          <div className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-full bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 text-xs font-bold mb-3 shadow-sm border border-indigo-500/20">
            <Cpu className="w-3.5 h-3.5 text-indigo-500" />
            <span>Research Methodology & Theory</span>
          </div>
          <h2 className="text-2xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            How the Hybrid U-Net–DnCNN Model Works
          </h2>
          <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 mt-3 leading-relaxed">
            Smartphone camera sensors are physically restricted by small pixel pitch (1.0µm–1.4µm), yielding heavy photon shot noise in low ambient light. Our architecture addresses this through dual-stream synergistic feature extraction.
          </p>
        </div>

        {/* 3D Animated Interactive Sensor Lattice */}
        <div className="w-full">
          <Sensor3DVisualizer theme={theme} />
        </div>

        {/* Mathematical Formulation Callout with Glassmorphism */}
        <div className="p-7 rounded-3xl glass-panel bg-white/70 dark:bg-gradient-to-r dark:from-slate-900/80 dark:to-indigo-950/40 border border-slate-200/80 dark:border-white/10 shadow-xl">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
            <div className="space-y-2 max-w-xl">
              <span className="text-xs uppercase font-mono font-bold tracking-wider text-brand-600 dark:text-brand-400">
                Mathematical Problem Formulation
              </span>
              <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white">
                Deep Residual Noise Learning
              </h3>
              <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                Rather than forcing a neural network to reconstruct the entire clean photograph from scratch, our model learns a mapping from the degraded input <span className="font-mono text-brand-600 dark:text-brand-300 font-bold">y</span> to the underlying noise field <span className="font-mono text-brand-600 dark:text-brand-300 font-bold">R(y)</span>:
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-slate-900 dark:bg-slate-950/95 border border-slate-700/80 font-mono text-xs sm:text-sm text-slate-200 space-y-2 flex-shrink-0 w-full md:w-auto shadow-inner">
              <div className="text-slate-400">// Observation model:</div>
              <div className="text-brand-300 font-bold">y = x + v</div>
              <div className="text-slate-400">// Deep Residual Subtraction:</div>
              <div className="text-emerald-400 font-bold">x̂ = clip( y - R_hybrid(y), 0, 1 )</div>
            </div>
          </div>
        </div>

        {/* Dual Branch Architecture Diagram Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          {/* Branch 1: U-Net */}
          <div className="rounded-3xl glass-panel bg-white/60 dark:bg-slate-900/60 border border-slate-200/80 dark:border-slate-800 p-7 space-y-4 shadow-lg hover:shadow-xl transition-all">
            <div className="flex items-center space-x-3">
              <div className="w-11 h-11 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-600 dark:text-indigo-400 shadow-sm">
                <GitFork className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">
                  Stream 1: Multi-Scale Contextual U-Net
                </h3>
                <span className="text-xs text-indigo-600 dark:text-indigo-400 font-mono font-medium">Contracting-Expansive Flow</span>
              </div>
            </div>

            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              Consists of successive convolution blocks coupled with pooling operations and expansive upsampling. Long skip connections bridge high-resolution spatial feature maps across layers, ensuring that uniform smooth regions and lighting gradients are consistently maintained.
            </p>

            <ul className="space-y-2.5 text-xs text-slate-600 dark:text-slate-400 pt-3 border-t border-slate-200 dark:border-slate-800">
              <li className="flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-indigo-500 flex-shrink-0" />
                <span>Captures global context and scene luminance variations</span>
              </li>
              <li className="flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-indigo-500 flex-shrink-0" />
                <span>Skip connections prevent gradient vanishing across deep layers</span>
              </li>
            </ul>
          </div>

          {/* Branch 2: DnCNN */}
          <div className="rounded-3xl glass-panel bg-white/60 dark:bg-slate-900/60 border border-slate-200/80 dark:border-slate-800 p-7 space-y-4 shadow-lg hover:shadow-xl transition-all">
            <div className="flex items-center space-x-3">
              <div className="w-11 h-11 rounded-2xl bg-sky-500/10 border border-sky-500/20 flex items-center justify-center text-sky-600 dark:text-sky-400 shadow-sm">
                <Minimize2 className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">
                  Stream 2: Deep Residual DnCNN
                </h3>
                <span className="text-xs text-sky-600 dark:text-sky-400 font-mono font-medium">Feed-forward Convolutional Chain</span>
              </div>
            </div>

            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              Features a deep stack of 3×3 convolutions with Batch Normalization and ReLU activations operating directly at full spatial resolution (no pooling). It specializes exclusively in detecting fine sensor grain, salt-and-pepper spikes, and micro-textures without softening edges.
            </p>

            <ul className="space-y-2.5 text-xs text-slate-600 dark:text-slate-400 pt-3 border-t border-slate-200 dark:border-slate-800">
              <li className="flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-sky-500 flex-shrink-0" />
                <span>Operates without spatial pooling to preserve edge sharpness</span>
              </li>
              <li className="flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-sky-500 flex-shrink-0" />
                <span>Batch Normalization accelerates internal covariate shift</span>
              </li>
            </ul>
          </div>

        </div>

        {/* Cross-Feature Fusion Unit */}
        <div className="rounded-3xl glass-panel bg-white/60 dark:bg-slate-900/40 border border-brand-500/30 p-7 text-center space-y-3 shadow-lg">
          <div className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-full bg-brand-500/10 text-brand-600 dark:text-brand-300 text-xs font-bold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Cross-Stream Feature Fusion Layer</span>
          </div>
          <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white">
            1×1 Projection & Hann-Window Tiling Engine
          </h3>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed">
            Feature representations from the U-Net and DnCNN streams are concatenated at native resolution and fused through 1×1 channel-mixing kernels. During inference, arbitrary dimensions are processed via 2D Hann-window overlapping tiles, eliminating tile seam boundaries and memory bottlenecks.
          </p>
        </div>

      </div>
    </section>
  );
};
