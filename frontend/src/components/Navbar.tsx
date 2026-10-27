import React from 'react';
import { Sparkles, Activity, Layers, BookOpen, Sliders } from 'lucide-react';
import type { HealthStatus, ModelInfo } from '../types';

interface NavbarProps {
  health: HealthStatus | null;
  modelInfo: ModelInfo | null;
  onOpenSpecs: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ health, onOpenSpecs }) => {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand / Logo */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-brand-500/20 ring-1 ring-white/20">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-base sm:text-lg tracking-tight text-white">
                NeuroClean
              </span>
              <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20">
                Hybrid U-Net–DnCNN
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Machine Learning for Smartphone Image Denoising
            </p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center space-x-6 text-sm font-medium text-slate-300">
          <a href="#studio" className="hover:text-brand-400 transition-colors flex items-center gap-1.5">
            <Sliders className="w-4 h-4 text-slate-400" />
            Denoise Studio
          </a>
          <a href="#samples" className="hover:text-brand-400 transition-colors flex items-center gap-1.5">
            <Layers className="w-4 h-4 text-slate-400" />
            Dataset Samples
          </a>
          <a href="#architecture" className="hover:text-brand-400 transition-colors flex items-center gap-1.5">
            <BookOpen className="w-4 h-4 text-slate-400" />
            Methodology
          </a>
        </nav>

        {/* Status Pill & Model Specs Trigger */}
        <div className="flex items-center space-x-3">
          {/* Backend Health Badge */}
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs">
            <span className="relative flex h-2 w-2">
              {health?.status === 'healthy' ? (
                <>
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </>
              ) : (
                <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
              )}
            </span>
            <span className="text-slate-300 font-mono text-[11px] hidden sm:inline">
              {health?.status === 'healthy' ? 'FastAPI Active' : 'Connecting...'}
            </span>
          </div>

          <button
            onClick={onOpenSpecs}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-slate-200 text-xs font-medium transition-all shadow-sm"
            title="Inspect Model Metadata and Checkpoint"
          >
            <Activity className="w-3.5 h-3.5 text-brand-400" />
            <span>Model Info</span>
          </button>
        </div>

      </div>
    </header>
  );
};
