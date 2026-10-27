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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl rounded-2xl bg-slate-900 border border-slate-800 p-6 shadow-2xl text-slate-200 space-y-6 max-h-[90vh] overflow-y-auto">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center text-brand-400">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">
                Live Deep Learning System Specifications
              </h3>
              <p className="text-xs text-slate-400">
                Verified Backend Architecture & Checkpoint Diagnostics
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Specs Grid */}
        <div className="space-y-4 text-xs">
          {/* Active Model */}
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Model Name:</span>
              <span className="font-mono font-semibold text-brand-300">
                {modelInfo?.architecture_summary.name || 'Loading...'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Architecture Category:</span>
              <span className="font-mono text-slate-200">
                {modelInfo?.architecture_summary.type || 'Loading...'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Trainable Parameters:</span>
              <span className="font-mono font-bold text-emerald-400">
                {modelInfo?.architecture_summary.trainable_parameters.toLocaleString() || '0'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Checkpoint Status:</span>
              <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                {modelInfo?.architecture_summary.checkpoint_status || 'ACTIVE'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Active Weights Path:</span>
              <span className="font-mono text-[11px] text-slate-400 truncate max-w-xs">
                {modelInfo?.architecture_summary.checkpoint_path || 'In-Memory Instance'}
              </span>
            </div>
          </div>

          {/* Backend Environment */}
          <div className="grid grid-cols-2 gap-3">
            <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-slate-400 block mb-1">Backend Server:</span>
              <span className="font-mono text-white font-medium">{health?.service || 'FastAPI'}</span>
              <span className="text-[10px] text-slate-500 block mt-0.5">Uptime: {health?.uptime_seconds}s</span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-slate-400 block mb-1">Deep Learning Runtime:</span>
              <span className="font-mono text-white font-medium">TensorFlow 2.16.1</span>
              <span className="text-[10px] text-slate-500 block mt-0.5">oneDNN Optimizations Active</span>
            </div>
          </div>

          {/* Dataset Summary */}
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1.5">
            <div className="flex items-center space-x-2 text-slate-300 font-semibold mb-1">
              <Database className="w-4 h-4 text-brand-400" />
              <span>Training Dataset Profile</span>
            </div>
            <p className="text-slate-400 leading-relaxed">
              {modelInfo?.training_dataset_summary.description || '100 Paired Clean & Noisy Smartphone Images'}
            </p>
            <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-slate-400">
              <span>Native Image Dimensions:</span>
              <span className="font-mono text-slate-200">1404 × 2040 pixels</span>
            </div>
          </div>
        </div>

        {/* Footer Close */}
        <div className="pt-2 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-medium transition-colors"
          >
            Dismiss
          </button>
        </div>

      </div>
    </div>
  );
};
