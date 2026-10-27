import React from 'react';
import { X, Cpu, Database } from 'lucide-react';
import type { ModelInfo, HealthStatus } from '../types';

interface ModelSpecsModalProps {
  isOpen: boolean;
  onClose: () => void;
  modelInfo: ModelInfo | null;
  health: HealthStatus | null;
}

export const ModelSpecsModal: React.FC<ModelSpecsModalProps> = ({
  isOpen,
  onClose,
  modelInfo,
  health,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 dark:bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl rounded-3xl glass-panel bg-white/95 dark:bg-slate-900/95 border border-slate-200/80 dark:border-white/10 p-6 sm:p-7 shadow-2xl text-slate-800 dark:text-slate-200 space-y-6 max-h-[90vh] overflow-y-auto">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-200/80 dark:border-slate-800">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center text-brand-600 dark:text-brand-400 shadow-sm">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white">
                Live Deep Learning System Specifications
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Verified Backend Architecture & Checkpoint Diagnostics
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-700 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Specs Grid */}
        <div className="space-y-4 text-xs">
          {/* Active Model */}
          <div className="p-4 sm:p-5 rounded-2xl bg-slate-50 dark:bg-slate-950/80 border border-slate-200/80 dark:border-slate-800/80 space-y-2.5">
            <div className="flex items-center justify-between">
              <span className="text-slate-500 dark:text-slate-400">Model Name:</span>
              <span className="font-mono font-semibold text-brand-600 dark:text-brand-300">
                {modelInfo?.architecture_summary.name || 'Loading...'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-500 dark:text-slate-400">Architecture Category:</span>
              <span className="font-mono text-slate-800 dark:text-slate-200">
                {modelInfo?.architecture_summary.type || 'Loading...'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-500 dark:text-slate-400">Trainable Parameters:</span>
              <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">
                {modelInfo?.architecture_summary.trainable_parameters.toLocaleString() || '0'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-500 dark:text-slate-400">Checkpoint Status:</span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-mono bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
                {modelInfo?.architecture_summary.checkpoint_status || 'ACTIVE'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-500 dark:text-slate-400">Active Weights Path:</span>
              <span className="font-mono text-[11px] text-slate-500 dark:text-slate-400 truncate max-w-xs">
                {modelInfo?.architecture_summary.checkpoint_path || 'In-Memory Instance'}
              </span>
            </div>
          </div>

          {/* Backend Environment */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-950/80 border border-slate-200/80 dark:border-slate-800">
              <span className="text-slate-500 dark:text-slate-400 block mb-1">Backend Server:</span>
              <span className="font-mono text-slate-900 dark:text-white font-medium">{health?.service || 'FastAPI'}</span>
              <span className="text-[10px] text-slate-400 dark:text-slate-500 block mt-0.5">Uptime: {health?.uptime_seconds}s</span>
            </div>

            <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-950/80 border border-slate-200/80 dark:border-slate-800">
              <span className="text-slate-500 dark:text-slate-400 block mb-1">Deep Learning Runtime:</span>
              <span className="font-mono text-slate-900 dark:text-white font-medium">TensorFlow 2.16.1</span>
              <span className="text-[10px] text-slate-400 dark:text-slate-500 block mt-0.5">oneDNN Optimizations Active</span>
            </div>
          </div>

          {/* Dataset Summary */}
          <div className="p-4 sm:p-5 rounded-2xl bg-slate-50 dark:bg-slate-950/80 border border-slate-200/80 dark:border-slate-800/80 space-y-2">
            <div className="flex items-center space-x-2 text-slate-900 dark:text-slate-200 font-semibold mb-1">
              <Database className="w-4 h-4 text-brand-600 dark:text-brand-400" />
              <span>Training Dataset Profile</span>
            </div>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
              {modelInfo?.training_dataset_summary.description || '100 Paired Clean & Noisy Smartphone Images'}
            </p>
            <div className="flex items-center justify-between pt-2 border-t border-slate-200/80 dark:border-slate-800/60 text-slate-500 dark:text-slate-400">
              <span>Native Image Dimensions:</span>
              <span className="font-mono text-slate-800 dark:text-slate-200">1404 × 2040 pixels</span>
            </div>
          </div>
        </div>

        {/* Footer Close */}
        <div className="pt-2 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2.5 rounded-xl bg-slate-200 hover:bg-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-white text-xs font-semibold transition-colors shadow-sm"
          >
            Dismiss
          </button>
        </div>

      </div>
    </div>
  );
};
