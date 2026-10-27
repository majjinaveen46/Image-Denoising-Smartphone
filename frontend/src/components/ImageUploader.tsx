import React, { useState, useRef } from 'react';
import type { DragEvent, ChangeEvent } from 'react';
import { Upload, Image as ImageIcon, AlertCircle, Sparkles, Loader2, CheckCircle2, SlidersHorizontal, Info } from 'lucide-react';
import { denoiseImageUpload } from '../services/api';
import type { DenoiseResponse } from '../types';

interface ImageUploaderProps {
  onDenoiseSuccess: (result: DenoiseResponse) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({
  onDenoiseSuccess,
  isLoading,
  setIsLoading,
}) => {
  const [dragActive, setDragActive] = useState<boolean>(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [imageMeta, setImageMeta] = useState<{ width: number; height: number; sizeKb: number } | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [processingMode, setProcessingMode] = useState<'tiled' | 'resize'>('tiled');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateAndSetFile = (file: File) => {
    setErrorMsg(null);

    const validExtensions = ['image/jpeg', 'image/png', 'image/webp'];
    const hasValidExt = validExtensions.includes(file.type) || 
      /\.(jpe?g|png|webp)$/i.test(file.name);

    if (!hasValidExt) {
      setErrorMsg('Unsupported format. Please upload a JPG, JPEG, or PNG photograph.');
      return;
    }

    if (file.size > 25 * 1024 * 1024) {
      setErrorMsg('File exceeds 25 MB limit. Please select a smaller photograph.');
      return;
    }

    setSelectedFile(file);

    // Read image preview and dimensions
    const reader = new FileReader();
    reader.onload = (e) => {
      const url = e.target?.result as string;
      setPreviewUrl(url);

      const img = new Image();
      img.onload = () => {
        setImageMeta({
          width: img.naturalWidth,
          height: img.naturalHeight,
          sizeKb: Math.round(file.size / 1024),
        });
      };
      img.src = url;
    };
    reader.readAsDataURL(file);
  };

  const handleDrag = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const triggerUpload = () => {
    fileInputRef.current?.click();
  };

  const handleProcess = async () => {
    if (!selectedFile) return;
    setIsLoading(true);
    setErrorMsg(null);

    try {
      const response = await denoiseImageUpload(selectedFile, processingMode);
      onDenoiseSuccess(response);
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to process image. Please check backend connection.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full">
      {/* Upload Box Container */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`relative rounded-2xl border-2 border-dashed p-6 sm:p-10 transition-all text-center ${
          dragActive
            ? 'border-brand-500 bg-brand-500/10 shadow-lg shadow-brand-500/10 scale-[1.01]'
            : 'border-slate-800 bg-slate-900/40 hover:border-slate-700/80 hover:bg-slate-900/60'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/jpg,image/png,image/webp"
          onChange={handleFileChange}
          className="hidden"
        />

        {!previewUrl ? (
          /* Empty Upload State */
          <div className="flex flex-col items-center justify-center py-6">
            <div className="w-16 h-16 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center text-brand-400 mb-4 group-hover:scale-110 transition-transform">
              <Upload className="w-7 h-7" />
            </div>

            <h3 className="text-lg font-semibold text-white">
              Drag & drop your smartphone photograph here
            </h3>
            <p className="text-xs sm:text-sm text-slate-400 mt-1.5 max-w-md">
              Supports real low-light and noisy smartphone photos.
              Formats: <strong className="text-slate-300 font-medium">JPG, JPEG, PNG, WEBP</strong> (up to 25 MB).
            </p>

            <button
              type="button"
              onClick={triggerUpload}
              className="mt-6 inline-flex items-center px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs sm:text-sm font-medium border border-slate-700 shadow-sm transition-all"
            >
              <ImageIcon className="w-4 h-4 mr-2 text-brand-400" />
              Browse Local Device
            </button>
          </div>
        ) : (
          /* Image Selected / Preview State */
          <div className="flex flex-col md:flex-row items-center gap-6 text-left">
            {/* Image Thumbnail */}
            <div className="relative group w-48 h-48 sm:w-56 sm:h-56 rounded-xl overflow-hidden bg-slate-950 border border-slate-800 flex-shrink-0 shadow-md">
              <img
                src={previewUrl}
                alt="Uploaded preview"
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <button
                  type="button"
                  onClick={triggerUpload}
                  className="px-3 py-1.5 rounded-lg bg-black/70 text-xs text-white border border-white/20 hover:bg-black"
                >
                  Change File
                </button>
              </div>
            </div>

            {/* Meta and Action Configuration */}
            <div className="flex-1 w-full space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    <h4 className="text-sm sm:text-base font-semibold text-white truncate max-w-xs sm:max-w-md">
                      {selectedFile?.name}
                    </h4>
                  </div>
                  {imageMeta && (
                    <p className="text-xs text-slate-400 mt-1">
                      Resolution: <span className="text-slate-200 font-mono">{imageMeta.width} × {imageMeta.height} px</span> • Size: <span className="text-slate-200 font-mono">{imageMeta.sizeKb} KB</span>
                    </p>
                  )}
                </div>

                <button
                  onClick={() => {
                    setSelectedFile(null);
                    setPreviewUrl(null);
                    setImageMeta(null);
                  }}
                  className="text-xs text-slate-500 hover:text-rose-400 transition-colors"
                >
                  Remove
                </button>
              </div>

              {/* Processing Mode Selection */}
              <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-1.5">
                    <SlidersHorizontal className="w-3.5 h-3.5 text-brand-400" />
                    <span className="text-xs font-semibold text-slate-300">Processing Mode</span>
                  </div>
                  <span className="text-[10px] text-slate-500 flex items-center gap-1">
                    <Info className="w-3 h-3" />
                    {processingMode === 'tiled' ? 'Preserves 100% Dimensions' : 'Fast 128x128 Preview'}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs">
                  <button
                    type="button"
                    onClick={() => setProcessingMode('tiled')}
                    className={`py-2 px-3 rounded-lg border text-left transition-all ${
                      processingMode === 'tiled'
                        ? 'bg-brand-500/10 border-brand-500/40 text-brand-300 font-medium'
                        : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    <div className="font-semibold text-white">Full-Res Tiled</div>
                    <div className="text-[10px] text-slate-400">Hann-window blending, sharp</div>
                  </button>

                  <button
                    type="button"
                    onClick={() => setProcessingMode('resize')}
                    className={`py-2 px-3 rounded-lg border text-left transition-all ${
                      processingMode === 'resize'
                        ? 'bg-brand-500/10 border-brand-500/40 text-brand-300 font-medium'
                        : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    <div className="font-semibold text-white">Rapid Preview</div>
                    <div className="text-[10px] text-slate-400">Sub-second inference test</div>
                  </button>
                </div>
              </div>

              {/* Action Button */}
              <button
                type="button"
                onClick={handleProcess}
                disabled={isLoading}
                className="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white font-semibold text-sm shadow-md shadow-brand-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    <span>Executing Deep Neural Denoising...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 mr-2" />
                    <span>Remove Noise</span>
                  </>
                )}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Error Alert Message */}
      {errorMsg && (
        <div className="mt-3 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs sm:text-sm flex items-start space-x-2.5">
          <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-rose-400" />
          <span>{errorMsg}</span>
        </div>
      )}
    </div>
  );
};
