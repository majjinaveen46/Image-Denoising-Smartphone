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
      {/* Upload Box Container with Frosted Glassmorphism */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`relative rounded-3xl border-2 border-dashed p-6 sm:p-10 transition-all text-center glass-panel shadow-xl ${
          dragActive
            ? 'border-brand-500 bg-brand-500/10 scale-[1.01] shadow-brand-500/10'
            : 'border-slate-300 dark:border-slate-800 bg-white/50 dark:bg-slate-900/40 hover:border-brand-400 dark:hover:border-slate-700'
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
            <div className="w-16 h-16 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center text-brand-600 dark:text-brand-400 mb-4 transform hover:scale-110 transition-transform shadow-md">
              <Upload className="w-7 h-7" />
            </div>

            <h3 className="text-lg font-bold text-slate-900 dark:text-white">
              Drag & drop your smartphone photograph here
            </h3>
            <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1.5 max-w-md">
              Supports real low-light and noisy smartphone photos.
              Formats: <strong className="text-slate-800 dark:text-slate-300 font-semibold">JPG, JPEG, PNG, WEBP</strong> (up to 25 MB).
            </p>

            <button
              type="button"
              onClick={triggerUpload}
              className="mt-6 inline-flex items-center px-6 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 dark:bg-slate-800 dark:hover:bg-slate-700 text-white text-xs sm:text-sm font-semibold border border-slate-700 shadow-md transition-all transform hover:-translate-y-0.5"
            >
              <ImageIcon className="w-4 h-4 mr-2 text-brand-400" />
              Browse Local Device
            </button>
          </div>
        ) : (
          /* Image Selected / Preview State */
          <div className="flex flex-col md:flex-row items-center gap-6 text-left">
            {/* Image Thumbnail with Glass Frame */}
            <div className="relative group w-48 h-48 sm:w-56 sm:h-56 rounded-2xl overflow-hidden bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 flex-shrink-0 shadow-lg">
              <img
                src={previewUrl}
                alt="Uploaded preview"
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <button
                  type="button"
                  onClick={triggerUpload}
                  className="px-3 py-1.5 rounded-lg bg-black/80 text-xs text-white border border-white/20 hover:bg-black font-medium"
                >
                  Change Photo
                </button>
              </div>
            </div>

            {/* Meta and Action Configuration */}
            <div className="flex-1 w-full space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 dark:text-emerald-400 flex-shrink-0" />
                    <h4 className="text-sm sm:text-base font-bold text-slate-900 dark:text-white truncate max-w-xs sm:max-w-md">
                      {selectedFile?.name}
                    </h4>
                  </div>
                  {imageMeta && (
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                      Resolution: <span className="text-slate-900 dark:text-slate-200 font-mono font-semibold">{imageMeta.width} × {imageMeta.height} px</span> • Size: <span className="text-slate-900 dark:text-slate-200 font-mono font-semibold">{imageMeta.sizeKb} KB</span>
                    </p>
                  )}
                </div>

                <button
                  onClick={() => {
                    setSelectedFile(null);
                    setPreviewUrl(null);
                    setImageMeta(null);
                  }}
                  className="text-xs text-slate-400 hover:text-rose-500 dark:hover:text-rose-400 transition-colors font-medium"
                >
                  Remove
                </button>
              </div>

              {/* Processing Mode Selection with Glass Tiles */}
              <div className="p-3.5 rounded-2xl bg-slate-100/70 dark:bg-slate-950/80 border border-slate-200/80 dark:border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-1.5">
                    <SlidersHorizontal className="w-3.5 h-3.5 text-brand-600 dark:text-brand-400" />
                    <span className="text-xs font-bold text-slate-800 dark:text-slate-200">Processing Engine Mode</span>
                  </div>
                  <span className="text-[10px] text-slate-500 dark:text-slate-400 flex items-center gap-1 font-medium">
                    <Info className="w-3 h-3" />
                    {processingMode === 'tiled' ? 'Preserves 100% Dimensions' : 'Fast 128x128 Preview'}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs">
                  <button
                    type="button"
                    onClick={() => setProcessingMode('tiled')}
                    className={`py-2 px-3 rounded-xl border text-left transition-all ${
                      processingMode === 'tiled'
                        ? 'bg-brand-500/15 border-brand-500/50 text-brand-700 dark:text-brand-300 font-semibold shadow-sm'
                        : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
                    }`}
                  >
                    <div className="font-bold text-slate-900 dark:text-white">Full-Res Tiled</div>
                    <div className="text-[10px] text-slate-500 dark:text-slate-400">Hann-window blending, sharp</div>
                  </button>

                  <button
                    type="button"
                    onClick={() => setProcessingMode('resize')}
                    className={`py-2 px-3 rounded-xl border text-left transition-all ${
                      processingMode === 'resize'
                        ? 'bg-brand-500/15 border-brand-500/50 text-brand-700 dark:text-brand-300 font-semibold shadow-sm'
                        : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
                    }`}
                  >
                    <div className="font-bold text-slate-900 dark:text-white">Rapid Preview</div>
                    <div className="text-[10px] text-slate-500 dark:text-slate-400">Sub-second inference test</div>
                  </button>
                </div>
              </div>

              {/* Action Button */}
              <button
                type="button"
                onClick={handleProcess}
                disabled={isLoading}
                className="w-full sm:w-auto inline-flex items-center justify-center px-7 py-3 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white font-bold text-sm shadow-lg shadow-brand-500/25 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform active:scale-95"
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
        <div className="mt-3.5 p-4 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-700 dark:text-rose-300 text-xs sm:text-sm flex items-start space-x-2.5 shadow-sm">
          <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-rose-500" />
          <span>{errorMsg}</span>
        </div>
      )}
    </div>
  );
};
