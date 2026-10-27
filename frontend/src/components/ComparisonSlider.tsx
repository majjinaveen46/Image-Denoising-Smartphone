import React, { useState, useRef, useCallback, useEffect } from 'react';
import { Download, Sliders, Columns, Zap, Clock, ShieldAlert, Sparkles, Check } from 'lucide-react';
import type { DenoiseResponse } from '../types';

interface ComparisonSliderProps {
  data: DenoiseResponse;
  onReset: () => void;
}

export const ComparisonSlider: React.FC<ComparisonSliderProps> = ({ data, onReset }) => {
  const [sliderPosition, setSliderPosition] = useState<number>(50);
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [viewMode, setViewMode] = useState<'slider' | 'side-by-side'>('slider');
  const [downloadFormat, setDownloadFormat] = useState<'png' | 'jpeg'>('png');
  const [copiedNotification, setCopiedNotification] = useState<boolean>(false);

  const containerRef = useRef<HTMLDivElement>(null);

  const handleMove = useCallback(
    (clientX: number) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const x = clientX - rect.left;
      const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100));
      setSliderPosition(percentage);
    },
    []
  );

  const handleMouseDown = () => setIsDragging(true);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (isDragging) {
      handleMove(e.clientX);
    }
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (e.touches && e.touches[0]) {
      handleMove(e.touches[0].clientX);
    }
  };

  useEffect(() => {
    const onGlobalMouseUp = () => setIsDragging(false);
    window.addEventListener('mouseup', onGlobalMouseUp);
    return () => window.removeEventListener('mouseup', onGlobalMouseUp);
  }, []);

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = data.denoised_image;
    const baseName = (data.filename || 'smartphone_denoised').replace(/\.[^/.]+$/, '');
    link.download = `${baseName}_denoised.${downloadFormat}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    setCopiedNotification(true);
    setTimeout(() => setCopiedNotification(false), 2500);
  };

  return (
    <div className="w-full space-y-6">
      {/* Top Glass Controls Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-2xl glass-panel bg-white/70 dark:bg-slate-900/80 border border-slate-200/80 dark:border-slate-800 shadow-md">
        
        {/* View Mode Toggle */}
        <div className="flex items-center space-x-1.5 p-1 rounded-xl bg-slate-200/70 dark:bg-slate-950/80 border border-slate-300 dark:border-slate-800 text-xs">
          <button
            onClick={() => setViewMode('slider')}
            className={`px-3 py-1.5 rounded-lg font-semibold flex items-center gap-1.5 transition-all ${
              viewMode === 'slider'
                ? 'bg-brand-600 text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <Sliders className="w-3.5 h-3.5" />
            Interactive Split
          </button>
          <button
            onClick={() => setViewMode('side-by-side')}
            className={`px-3 py-1.5 rounded-lg font-semibold flex items-center gap-1.5 transition-all ${
              viewMode === 'side-by-side'
                ? 'bg-brand-600 text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <Columns className="w-3.5 h-3.5" />
            Side-by-Side
          </button>
        </div>

        {/* Action Controls & Download */}
        <div className="flex items-center space-x-2">
          {/* Format Selector */}
          <div className="flex items-center rounded-xl bg-slate-200/70 dark:bg-slate-950/80 border border-slate-300 dark:border-slate-800 text-xs overflow-hidden">
            <button
              onClick={() => setDownloadFormat('png')}
              className={`px-3 py-1.5 font-mono text-xs font-bold transition-colors ${
                downloadFormat === 'png' ? 'bg-white dark:bg-slate-800 text-brand-600 dark:text-brand-300 shadow-sm' : 'text-slate-600 dark:text-slate-400'
              }`}
            >
              PNG
            </button>
            <button
              onClick={() => setDownloadFormat('jpeg')}
              className={`px-3 py-1.5 font-mono text-xs font-bold transition-colors ${
                downloadFormat === 'jpeg' ? 'bg-white dark:bg-slate-800 text-brand-600 dark:text-brand-300 shadow-sm' : 'text-slate-600 dark:text-slate-400'
              }`}
            >
              JPG
            </button>
          </div>

          <button
            onClick={handleDownload}
            className="inline-flex items-center px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-md shadow-emerald-500/20 transition-all transform active:scale-95"
          >
            {copiedNotification ? (
              <>
                <Check className="w-3.5 h-3.5 mr-1.5" />
                Downloaded!
              </>
            ) : (
              <>
                <Download className="w-3.5 h-3.5 mr-1.5" />
                Download Denoised
              </>
            )}
          </button>

          <button
            onClick={onReset}
            className="px-3.5 py-2 rounded-xl bg-slate-200/80 hover:bg-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-xs font-semibold transition-colors shadow-sm"
          >
            New Upload
          </button>
        </div>

      </div>

      {/* Main Visualizer Area */}
      {viewMode === 'slider' ? (
        /* Interactive Split Slider with 3D Border Glow */
        <div
          ref={containerRef}
          onMouseMove={handleMouseMove}
          onTouchMove={handleTouchMove}
          className="relative w-full rounded-3xl overflow-hidden bg-slate-900 border border-slate-300/80 dark:border-white/10 select-none shadow-2xl cursor-ew-resize min-h-[380px] max-h-[640px] flex items-center justify-center transition-all"
        >
          {/* Denoised Image (Full background / Right side) */}
          <img
            src={data.denoised_image}
            alt="Denoised Output"
            className="w-full h-full object-contain pointer-events-none"
          />

          {/* Label Right: Denoised */}
          <div className="absolute top-4 right-4 z-20 px-3 py-1.5 rounded-xl bg-black/75 backdrop-blur-md border border-emerald-500/40 text-emerald-300 font-mono text-xs font-bold shadow-lg pointer-events-none">
            Denoised (AI Model)
          </div>

          {/* Original Noisy Image (Clipped Left side) */}
          <div
            className="absolute inset-0 overflow-hidden pointer-events-none"
            style={{ width: `${sliderPosition}%` }}
          >
            <img
              src={data.original_image}
              alt="Original Input"
              className="absolute inset-0 w-full h-full object-contain pointer-events-none"
              style={{
                width: containerRef.current ? `${containerRef.current.clientWidth}px` : '100%',
                maxWidth: 'none',
              }}
            />
          </div>

          {/* Label Left: Original */}
          <div className="absolute top-4 left-4 z-20 px-3 py-1.5 rounded-xl bg-black/75 backdrop-blur-md border border-rose-500/40 text-rose-300 font-mono text-xs font-bold shadow-lg pointer-events-none">
            Original Noisy Input
          </div>

          {/* Draggable Divider Line and 3D Knob */}
          <div
            className="absolute top-0 bottom-0 z-30 w-1 bg-white cursor-ew-resize shadow-[0_0_15px_rgba(0,0,0,0.9)]"
            style={{ left: `${sliderPosition}%` }}
            onMouseDown={handleMouseDown}
          >
            <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-10 h-10 rounded-full bg-white text-slate-900 border-2 border-brand-500 shadow-2xl flex items-center justify-center pointer-events-none transform transition-transform hover:scale-110">
              <Sliders className="w-4 h-4 text-brand-600 rotate-90" />
            </div>
          </div>
        </div>
      ) : (
        /* Side-by-Side Dual View with Glass Cards */
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Original */}
          <div className="rounded-3xl overflow-hidden glass-panel bg-white/60 dark:bg-slate-900/60 border border-slate-200/80 dark:border-slate-800 p-3 space-y-2 shadow-lg">
            <div className="flex items-center justify-between px-2 py-1 text-xs">
              <span className="font-bold text-rose-500 dark:text-rose-400">Original Photograph</span>
              <span className="text-slate-500 font-mono font-medium">Input</span>
            </div>
            <div className="rounded-2xl overflow-hidden bg-black flex items-center justify-center max-h-[460px]">
              <img
                src={data.original_image}
                alt="Original Photograph"
                className="w-full h-auto object-contain"
              />
            </div>
          </div>

          {/* Denoised */}
          <div className="rounded-3xl overflow-hidden glass-panel bg-white/60 dark:bg-slate-900/60 border border-slate-200/80 dark:border-slate-800 p-3 space-y-2 shadow-lg">
            <div className="flex items-center justify-between px-2 py-1 text-xs">
              <span className="font-bold text-emerald-600 dark:text-emerald-400">Denoised Photograph</span>
              <span className="text-slate-500 font-mono font-medium">Neural Reconstruction</span>
            </div>
            <div className="rounded-2xl overflow-hidden bg-black flex items-center justify-center max-h-[460px]">
              <img
                src={data.denoised_image}
                alt="Denoised Photograph"
                className="w-full h-auto object-contain"
              />
            </div>
          </div>
        </div>
      )}

      {/* Quantitative Metadata and Metrics Cards with Glassmorphism */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
        {/* Processing Time */}
        <div className="p-4 rounded-2xl glass-panel bg-white/60 dark:bg-slate-900/50 border border-slate-200/80 dark:border-slate-800 shadow-md">
          <div className="flex items-center space-x-1.5 text-slate-500 dark:text-slate-400 text-xs mb-1">
            <Clock className="w-3.5 h-3.5 text-amber-500" />
            <span className="font-semibold">Processing Time</span>
          </div>
          <div className="text-base sm:text-lg font-bold font-mono text-slate-900 dark:text-white">
            {data.metadata.processing_time_ms} ms
          </div>
          <div className="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">
            {data.metadata.processing_mode === 'tiled' ? 'High-Fidelity Tiled' : 'Fast Resize'}
          </div>
        </div>

        {/* Resolution & Dimensions */}
        <div className="p-4 rounded-2xl glass-panel bg-white/60 dark:bg-slate-900/50 border border-slate-200/80 dark:border-slate-800 shadow-md">
          <div className="flex items-center space-x-1.5 text-slate-500 dark:text-slate-400 text-xs mb-1">
            <Zap className="w-3.5 h-3.5 text-brand-500" />
            <span className="font-semibold">Image Dimensions</span>
          </div>
          <div className="text-base sm:text-lg font-bold font-mono text-slate-900 dark:text-white">
            {data.metadata.width} × {data.metadata.height}
          </div>
          <div className="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5 truncate">
            Ratio: {data.metadata.aspect_ratio}
          </div>
        </div>

        {/* Estimated Noise Reduction */}
        <div className="p-4 rounded-2xl glass-panel bg-white/60 dark:bg-slate-900/50 border border-slate-200/80 dark:border-slate-800 shadow-md">
          <div className="flex items-center space-x-1.5 text-slate-500 dark:text-slate-400 text-xs mb-1">
            <Sparkles className="w-3.5 h-3.5 text-emerald-500" />
            <span className="font-semibold">Noise Suppression</span>
          </div>
          <div className="text-base sm:text-lg font-bold font-mono text-emerald-600 dark:text-emerald-400">
            {data.metrics.noise_reduction_percentage > 0 ? `-${data.metrics.noise_reduction_percentage}%` : 'Clean'}
          </div>
          <div className="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">
            σ: {data.metrics.estimated_input_noise_sigma} → {data.metrics.estimated_output_noise_sigma}
          </div>
        </div>

        {/* Quantitative PSNR / Model */}
        <div className="p-4 rounded-2xl glass-panel bg-white/60 dark:bg-slate-900/50 border border-slate-200/80 dark:border-slate-800 shadow-md">
          <div className="flex items-center space-x-1.5 text-slate-500 dark:text-slate-400 text-xs mb-1">
            <ShieldAlert className="w-3.5 h-3.5 text-indigo-500" />
            <span className="font-semibold">Restoration Quality</span>
          </div>
          {data.metrics.psnr_db !== null ? (
            <>
              <div className="text-base sm:text-lg font-bold font-mono text-slate-900 dark:text-white">
                {data.metrics.psnr_db} dB
              </div>
              <div className="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">
                SSIM: {data.metrics.ssim ?? 'N/A'}
              </div>
            </>
          ) : (
            <>
              <div className="text-sm font-bold text-slate-800 dark:text-slate-200 truncate">
                Blind Real Photo
              </div>
              <div className="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5 truncate">
                {data.metadata.model_name}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
