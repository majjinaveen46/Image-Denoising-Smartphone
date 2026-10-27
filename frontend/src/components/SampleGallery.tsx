import React, { useEffect, useState } from 'react';
import { Layers, Play, CheckCircle, Loader2 } from 'lucide-react';
import { fetchSamples, denoiseSampleImage } from '../services/api';
import type { SampleItem, DenoiseResponse } from '../types';

interface SampleGalleryProps {
  onSelectSample: (result: DenoiseResponse) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const SampleGallery: React.FC<SampleGalleryProps> = ({
  onSelectSample,
  isLoading,
  setIsLoading,
}) => {
  const [samples, setSamples] = useState<SampleItem[]>([]);
  const [activeSampleId, setActiveSampleId] = useState<string | null>(null);
  const [loadingSampleId, setLoadingSampleId] = useState<string | null>(null);

  useEffect(() => {
    fetchSamples()
      .then((data) => setSamples(data))
      .catch((err) => console.error("Error fetching samples:", err));
  }, []);

  const handleTestSample = async (id: string) => {
    setLoadingSampleId(id);
    setIsLoading(true);
    try {
      const response = await denoiseSampleImage(id, "resize");
      setActiveSampleId(id);
      onSelectSample(response);
      const el = document.getElementById("studio");
      el?.scrollIntoView({ behavior: "smooth" });
    } catch (err) {
      console.error("Failed to denoise sample:", err);
    } finally {
      setLoadingSampleId(null);
      setIsLoading(false);
    }
  };

  if (samples.length === 0) {
    return null;
  }

  return (
    <section id="samples" className="py-16 border-t border-slate-800/80">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Heading */}
        <div className="text-center max-w-3xl mx-auto mb-10">
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-brand-500/10 text-brand-400 text-xs font-semibold mb-3">
            <Layers className="w-3.5 h-3.5" />
            <span>Smartphone Dataset Verification</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Curated Smartphone Benchmark Samples
          </h2>
          <p className="text-sm text-slate-400 mt-2">
            Click any test pair below from our paired smartphone dataset (1404×2040) to instantly run inference and benchmark ground-truth restoration metrics.
          </p>
        </div>

        {/* Samples Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {samples.map((sample) => (
            <div
              key={sample.id}
              className={`rounded-2xl bg-slate-900/60 border p-4 transition-all ${
                activeSampleId === sample.id
                  ? 'border-brand-500 ring-2 ring-brand-500/20 shadow-lg shadow-brand-500/10'
                  : 'border-slate-800 hover:border-slate-700'
              }`}
            >
              {/* Dual Thumbnail Comparison */}
              <div className="grid grid-cols-2 gap-2 mb-3">
                <div className="space-y-1">
                  <div className="text-[10px] uppercase font-semibold text-rose-400 tracking-wider">
                    Noisy
                  </div>
                  <div className="rounded-lg overflow-hidden bg-black aspect-[4/3] border border-slate-800">
                    <img
                      src={sample.noisy_thumbnail}
                      alt={`Noisy ${sample.id}`}
                      className="w-full h-full object-cover"
                    />
                  </div>
                </div>

                <div className="space-y-1">
                  <div className="text-[10px] uppercase font-semibold text-emerald-400 tracking-wider">
                    Clean Target
                  </div>
                  <div className="rounded-lg overflow-hidden bg-black aspect-[4/3] border border-slate-800">
                    <img
                      src={sample.clean_thumbnail}
                      alt={`Clean ${sample.id}`}
                      className="w-full h-full object-cover"
                    />
                  </div>
                </div>
              </div>

              {/* Title & Action */}
              <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-800/80">
                <div>
                  <h4 className="text-sm font-semibold text-white">
                    {sample.title}
                  </h4>
                  <span className="text-[11px] text-slate-500 font-mono">
                    ID: {sample.id}.png
                  </span>
                </div>

                <button
                  type="button"
                  onClick={() => handleTestSample(sample.id)}
                  disabled={isLoading}
                  className="inline-flex items-center px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-brand-600 text-slate-200 hover:text-white text-xs font-medium border border-slate-700 hover:border-brand-500 transition-all disabled:opacity-50"
                >
                  {loadingSampleId === sample.id ? (
                    <>
                      <Loader2 className="w-3.5 h-3.5 mr-1.5 animate-spin text-brand-400" />
                      Testing...
                    </>
                  ) : activeSampleId === sample.id ? (
                    <>
                      <CheckCircle className="w-3.5 h-3.5 mr-1.5 text-emerald-400" />
                      Loaded
                    </>
                  ) : (
                    <>
                      <Play className="w-3.5 h-3.5 mr-1.5 text-brand-400" />
                      Test Sample
                    </>
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
};
