import React from 'react';
import { ArrowDown, Cpu, Sparkles, ShieldCheck, Zap } from 'lucide-react';

interface HeroProps {
  onScrollToUpload: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onScrollToUpload }) => {
  return (
    <section className="relative overflow-hidden pt-12 pb-16 md:pt-20 md:pb-24 border-b border-slate-800/60">
      {/* Subtle Ambient Background Gradients */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-brand-500/10 blur-[120px] rounded-full pointer-events-none -z-10" />
      <div className="absolute top-1/3 left-1/3 w-[300px] h-[300px] bg-indigo-500/10 blur-[100px] rounded-full pointer-events-none -z-10" />

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        {/* Research Pill */}
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-900/90 border border-brand-500/30 text-brand-300 text-xs font-medium mb-6 shadow-sm">
          <Sparkles className="w-3.5 h-3.5 text-brand-400" />
          <span>Academic Project • Deep Learning Computer Vision</span>
        </div>

        {/* Hero Title */}
        <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight sm:leading-none">
          Image Denoising Using Machine Learning for{' '}
          <span className="bg-gradient-to-r from-brand-400 via-sky-300 to-indigo-400 bg-clip-text text-transparent">
            Smartphone Images
          </span>
        </h1>

        {/* Clear Explanation of AI Denoising */}
        <p className="mt-6 text-base sm:text-lg text-slate-300 max-w-3xl mx-auto leading-relaxed">
          Smartphone photography often suffers from sensor noise, photon shot noise, and chromatic grain under low-light conditions.
          Our dual-stream <strong className="text-white font-semibold">Hybrid U-Net–DnCNN</strong> model fuses multi-scale contextual representations with deep residual noise estimation to restore photographic clarity while preserving critical edges and fine textures.
        </p>

        {/* Action Button */}
        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
          <button
            onClick={onScrollToUpload}
            className="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3.5 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white font-semibold text-sm shadow-lg shadow-brand-500/25 transition-all transform hover:-translate-y-0.5"
          >
            <Sparkles className="w-4 h-4 mr-2" />
            Upload Your Image
            <ArrowDown className="w-4 h-4 ml-2 animate-bounce" />
          </button>

          <a
            href="#samples"
            className="w-full sm:w-auto inline-flex items-center justify-center px-5 py-3.5 rounded-xl bg-slate-900/80 hover:bg-slate-800 border border-slate-700/80 text-slate-200 font-medium text-sm transition-all"
          >
            Explore Dataset Demos
          </a>
        </div>

        {/* Feature Highlights Grid */}
        <div className="mt-14 grid grid-cols-1 sm:grid-cols-3 gap-4 text-left max-w-4xl mx-auto">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
            <div className="w-8 h-8 rounded-lg bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mb-3">
              <Cpu className="w-4 h-4 text-brand-400" />
            </div>
            <h3 className="text-sm font-semibold text-white">Hybrid U-Net–DnCNN</h3>
            <p className="text-xs text-slate-400 mt-1">
              Combines contracting-expansive multi-scale context with deep feed-forward residual noise subtraction.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
            <div className="w-8 h-8 rounded-lg bg-sky-500/10 border border-sky-500/20 flex items-center justify-center mb-3">
              <Zap className="w-4 h-4 text-sky-400" />
            </div>
            <h3 className="text-sm font-semibold text-white">Hann-Window Tiling</h3>
            <p className="text-xs text-slate-400 mt-1">
              Supports full smartphone resolution with 0% distortion and seamless cosine boundary blending.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mb-3">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
            </div>
            <h3 className="text-sm font-semibold text-white">Privacy & Security</h3>
            <p className="text-xs text-slate-400 mt-1">
              In-memory inference only; no persistent retention of user uploads, and EXIF orientation preserved.
            </p>
          </div>
        </div>

      </div>
    </section>
  );
};
