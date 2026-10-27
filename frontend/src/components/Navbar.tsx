import React from 'react';
import { Sparkles, Activity, Layers, BookOpen, Sliders, Moon, Sun } from 'lucide-react';
import type { HealthStatus, ModelInfo } from '../types';

interface NavbarProps {
  theme: 'dark' | 'light';
  onToggleTheme: () => void;
  health: HealthStatus | null;
  modelInfo: ModelInfo | null;
  onOpenSpecs: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  theme,
  onToggleTheme,
  health,
  onOpenSpecs,
}) => {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-200/80 dark:border-slate-800/80 bg-white/70 dark:bg-slate-950/75 backdrop-blur-xl transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand / Logo */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 via-indigo-600 to-sky-400 flex items-center justify-center shadow-lg shadow-brand-500/25 ring-1 ring-white/30 transform hover:scale-105 transition-transform">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-base sm:text-lg tracking-tight text-slate-900 dark:text-white">
                NeuroClean
              </span>
              <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-600 dark:text-brand-300 border border-brand-500/20 shadow-sm">
                Hybrid U-Net–DnCNN
              </span>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 hidden sm:block">
              Machine Learning for Smartphone Image Denoising
            </p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center space-x-6 text-sm font-semibold text-slate-600 dark:text-slate-300">
          <a href="#studio" className="hover:text-brand-600 dark:hover:text-brand-400 transition-colors flex items-center gap-1.5">
            <Sliders className="w-4 h-4 text-brand-500" />
            Denoise Studio
          </a>
          <a href="#samples" className="hover:text-brand-600 dark:hover:text-brand-400 transition-colors flex items-center gap-1.5">
            <Layers className="w-4 h-4 text-indigo-500" />
            Dataset Demos
          </a>
          <a href="#architecture" className="hover:text-brand-600 dark:hover:text-brand-400 transition-colors flex items-center gap-1.5">
            <BookOpen className="w-4 h-4 text-sky-500" />
            Methodology
          </a>
        </nav>

        {/* Controls: Theme Toggle & Backend Status */}
        <div className="flex items-center space-x-2.5">
          {/* Light / Dark Mode Toggle Button */}
          <button
            onClick={onToggleTheme}
            aria-label="Toggle theme"
            className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-900 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-200 transition-all shadow-sm flex items-center justify-center transform active:scale-95"
            title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
          >
            {theme === 'dark' ? (
              <Sun className="w-4 h-4 text-amber-400 rotate-0 transition-transform hover:rotate-45" />
            ) : (
              <Moon className="w-4 h-4 text-indigo-600 transition-transform hover:-rotate-12" />
            )}
          </button>

          {/* Backend Status Pill */}
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-xs">
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
            <span className="text-slate-700 dark:text-slate-300 font-mono text-[11px] hidden sm:inline font-medium">
              {health?.status === 'healthy' ? 'FastAPI Active' : 'Connecting...'}
            </span>
          </div>

          {/* Model Specs Trigger */}
          <button
            onClick={onOpenSpecs}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800/80 dark:hover:bg-slate-700/80 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 text-xs font-semibold transition-all shadow-sm"
            title="Inspect Model Metadata and Checkpoint"
          >
            <Activity className="w-3.5 h-3.5 text-brand-600 dark:text-brand-400" />
            <span>Model Info</span>
          </button>
        </div>

      </div>
    </header>
  );
};
