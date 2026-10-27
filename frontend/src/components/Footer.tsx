import React from 'react';
import { Shield, AlertTriangle } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-200/80 dark:border-slate-800/80 bg-slate-100/70 dark:bg-slate-950 py-12 text-slate-600 dark:text-slate-400 text-xs transition-colors duration-300">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Academic Citation & Title */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-8 border-b border-slate-200/80 dark:border-slate-800/80">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="font-bold text-slate-900 dark:text-white text-sm">
                Image Denoising Using Machine Learning for Smartphone Images
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] bg-slate-200 dark:bg-slate-900 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-mono font-medium">
                Academic Capstone
              </span>
            </div>
            <p className="text-slate-500 dark:text-slate-400 text-xs">
              Hybrid U-Net–DnCNN deep learning system for high-ISO and low-light smartphone photography restoration.
            </p>
          </div>

          <div className="flex items-center space-x-4 text-xs font-mono text-slate-500 dark:text-slate-400">
            <span>FastAPI Backend</span>
            <span>•</span>
            <span>TensorFlow 2.16</span>
            <span>•</span>
            <span>React + Vite</span>
          </div>
        </div>

        {/* Technical Disclaimer on Blurred vs Sensor Noise */}
        <div className="p-4 sm:p-5 rounded-2xl glass-panel bg-white/70 dark:bg-slate-900/60 border border-slate-200/80 dark:border-slate-800 flex items-start space-x-3 shadow-sm">
          <AlertTriangle className="w-4 h-4 text-amber-500 dark:text-amber-400 flex-shrink-0 mt-0.5" />
          <div className="space-y-1 leading-relaxed">
            <strong className="text-slate-900 dark:text-slate-200">Domain Scope & Academic Disclaimer:</strong>
            <p className="text-slate-600 dark:text-slate-400">
              This neural system is engineered specifically for stochastic sensor noise, photon shot noise, amplifier grain, and chromatic low-light artifacts in smartphone cameras. While fine photographic edges are preserved, the model does not guarantee reconstruction of severely out-of-focus optical blur, heavy motion streaks, or physically occluded details.
            </p>
          </div>
        </div>

        {/* Copyright & Security */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-slate-500 dark:text-slate-400 text-[11px]">
          <div>
            © {new Date().getFullYear()} Smartphone Image Denoising Project. All Rights Reserved.
          </div>
          <div className="flex items-center space-x-2 text-slate-500 dark:text-slate-400 font-medium">
            <Shield className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>Secure In-Memory Processing • No Permanent Image Storage</span>
          </div>
        </div>

      </div>
    </footer>
  );
};
