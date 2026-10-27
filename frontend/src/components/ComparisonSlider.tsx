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
      {/* Top Controls Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-xl bg-slate-900/90 border border-slate-800">
        
        {/* View Mode Toggle */}
        <div className="flex items-center space-x-1.5 p-1 rounded-lg bg-slate-950 border border-slate-800 text-xs">
          <button
            onClick={() => setViewMode('slider')}
            className={`px-3 py-1.5 rounded-md font-medium flex items-center gap-1.5 transition-all ${
              viewMode === 'slider'
                ? 'bg-brand-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Sliders className="w-3.5 h-3.5" />
            Interactive Split
          </button>
          <button
            onClick={() => setViewMode('side-by-side')}
            className={`px-3 py-1.5 rounded-md font-medium flex items-center gap-1.5 transition-all ${
              viewMode === 'side-by-side'
                ? 'bg-brand-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Columns className="w-3.5 h-3.5" />
            Side-by-Side
          </button>
        </div>

        {/* Action Controls & Download */}
        <div className="flex items-center space-x-2">
          {/* Format Selector */}
          <div className="flex items-center rounded-lg bg-slate-950 border border-slate-800 text-xs overflow-hidden">
            <button
              onClick={() => setDownloadFormat('png')}
              className={`px-2.5 py-1.5 font-mono ${
                downloadFormat === 'png' ? 'bg-slate-800 text-brand-300 font-bold' : 'text-slate-400'
              }`}
            >
              PNG
            </button>
            <button
              onClick={() => setDownloadFormat('jpeg')}
              className={`px-2.5 py-1.5 font-mono ${
                downloadFormat === 'jpeg' ? 'bg-slate-800 text-brand-300 font-bold' : 'text-slate-400'
              }`}
            >
              JPG
            </button>
          </div>

          <button
            onClick={handleDownload}
            className="inline-flex items-center px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-sm transition-all"
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
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 text-xs transition-colors"
          >
            New Upload
          </button>
        </div>

      </div>

      {/* Main Visualizer Area */}
      {viewMode === 'slider' ? (
        /* Interactive Split Slider */
        <div
          ref={containerRef}
          onMouseMove={handleMouseMove}
          onTouchMove={handleTouchMove}
          className="relative w-full rounded-2xl overflow-hidden bg-slate-950 border border-slate-800 select-none shadow-2xl cursor-ew-resize min-h-[360px] max-h-[640px] flex items-center justify-center"
        >
          {/* Denoised Image (Full background / Right side) */}
          <img
            src={data.denoised_image}
            alt="Denoised Output"
            className="w-full h-full object-contain pointer-events-none"
          />

          {/* Label Right: Denoised */}
          <div className="absolute top-4 right-4 z-20 px-2.5 py-1 rounded-md bg-slate-950/80 backdrop-blur-md border border-emerald-500/30 text-emerald-300 font-mono text-xs font-semibold shadow-md pointer-events-none">
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
          <div className="absolute top-4 left-4 z-20 px-2.5 py-1 rounded-md bg-slate-950/80 backdrop-blur-md border border-rose-500/30 text-rose-300 font-mono text-xs font-semibold shadow-md pointer-events-none">
            Original Noisy Input
          </div>

          {/* Draggable Divider Line and Knob */}
          <div
            className="absolute top-0 bottom-0 z-30 w-1 bg-white cursor-ew-resize shadow-[0_0_12px_rgba(0,0,0,0.8)]"
            style={{ left: `${sliderPosition}%` }}
            onMouseDown={handleMouseDown}
          >
            <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-9 h-9 rounded-full bg-white text-slate-900 border-2 border-brand-500 shadow-xl flex items-center justify-center pointer-events-none">
              <Sliders className="w-4 h-4 text-brand-600 rotate-90" />
            </div>
          </div>
        </div>
      ) : (
        /* Side-by-Side Dual View */
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Original */}
          <div className="rounded-2xl overflow-hidden bg-slate-950 border border-slate-800 p-2 space-y-2">
            <div className="flex items-center justify-between px-2 py-1 text-xs">
              <span className="font-semibold text-rose-400">Original Photograph</span>
              <span className="text-slate-500 font-mono">Input</span>
            </div>
            <div className="rounded-xl overflow-hidden bg-black flex items-center justify-center max-h-[460px]">
              <img
                src={data.original_image}
                alt="Original Photograph"
                className="w-full h-auto object-contain"
              />
            </div>
          </div>

          {/* Denoised */}
          <div className="rounded-2xl overflow-hidden bg-slate-950 border border-slate-800 p-2 space-y-2">
            <div className="flex items-center justify-between px-2 py-1 text-xs">
              <span className="font-semibold text-emerald-400">Denoised Photograph</span>
              <span className="text-slate-500 font-mono">Neural Reconstruction</span>
            </div>
            <div className="rounded-xl overflow-hidden bg-black flex items-center justify-center max-h-[460px]">
              <img
                src={data.denoised_image}
                alt="Denoised Photograph"
                className="w-full h-auto object-contain"
              />
            </div>
          </div>
        </div>
      )}

      {/* Quantitative Metadata and Metrics Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {/* Processing Time */}
        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center space-x-1.5 text-slate-400 text-xs mb-1">
            <Clock className="w-3.5 h-3.5 text-amber-400" />
            <span>Processing Time</span>
          </div>
          <div className="text-base sm:text-lg font-bold font-mono text-white">
            {data.metadata.processing_time_ms} ms
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">
            {data.metadata.processing_mode === 'tiled' ? 'High-Fidelity Tiled' : 'Fast Resize'}
          </div>
        </div>

        {/* Resolution & Dimensions */}
        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center space-x-1.5 text-slate-400 text-xs mb-1">
            <Zap className="w-3.5 h-3.5 text-brand-400" />
            <span>Image Dimensions</span>
          </div>
          <div className="text-base sm:text-lg font-bold font-mono text-white">
            {data.metadata.width} × {data.metadata.height}
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5 truncate">
            Ratio: {data.metadata.aspect_ratio}
          </div>
        </div>

        {/* Estimated Noise Reduction */}
        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center space-x-1.5 text-slate-400 text-xs mb-1">
            <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
            <span>Noise Suppression</span>
          </div>
          <div className="text-base sm:text-lg font-bold font-mono text-emerald-400">
            {data.metrics.noise_reduction_percentage > 0 ? `-${data.metrics.noise_reduction_percentage}%` : 'Clean'}
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">
            σ: {data.metrics.estimated_input_noise_sigma} → {data.metrics.estimated_output_noise_sigma}
          </div>
        </div>

        {/* Quantitative PSNR / Model */}
        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center space-x-1.5 text-slate-400 text-xs mb-1">
            <ShieldAlert className="w-3.5 h-3.5 text-indigo-400" />
            <span>Restoration Quality</span>
          </div>
          {data.metrics.psnr_db !== null ? (
            <>
              <div className="text-base sm:text-lg font-bold font-mono text-white">
                {data.metrics.psnr_db} dB
              </div>
              <div className="text-[10px] text-slate-500 mt-0.5">
                SSIM: {data.metrics.ssim ?? 'N/A'}
              </div>
            </>
          ) : (
            <>
              <div className="text-sm font-semibold text-slate-200 truncate">
                Blind Real Photo
              </div>
              <div className="text-[10px] text-slate-500 mt-0.5 truncate">
                {data.metadata.model_name}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
