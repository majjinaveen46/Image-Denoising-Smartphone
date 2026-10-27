import { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { ImageUploader } from './components/ImageUploader';
import { ComparisonSlider } from './components/ComparisonSlider';
import { SampleGallery } from './components/SampleGallery';
import { ArchitectureSection } from './components/ArchitectureSection';
import { BenchmarkSection } from './components/BenchmarkSection';
import { Footer } from './components/Footer';
import { ModelSpecsModal } from './components/ModelSpecsModal';
import { fetchHealth, fetchModelInfo } from './services/api';
import type { HealthStatus, ModelInfo, DenoiseResponse } from './types';
import { Sliders, CheckCircle2 } from 'lucide-react';

export function App() {
  const [theme, setTheme] = useState<'dark' | 'light'>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('neuroclean_theme');
      if (saved === 'light' || saved === 'dark') return saved;
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return 'dark';
  });

  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [isSpecsOpen, setIsSpecsOpen] = useState<boolean>(false);
  const [denoiseResult, setDenoiseResult] = useState<DenoiseResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    localStorage.setItem('neuroclean_theme', theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  useEffect(() => {
    // Initial health and model-info checks
    fetchHealth()
      .then((h) => setHealth(h))
      .catch((err) => console.warn('Health check issue:', err));

    fetchModelInfo()
      .then((m) => setModelInfo(m))
      .catch((err) => console.warn('Model info issue:', err));

    // Periodic light polling for live status
    const interval = setInterval(() => {
      fetchHealth()
        .then((h) => setHealth(h))
        .catch(() => setHealth(null));
    }, 15000);

    return () => clearInterval(interval);
  }, []);

  const handleScrollToUpload = () => {
    const el = document.getElementById('studio');
    el?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'dark bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-900'} flex flex-col font-sans selection:bg-brand-500/30 selection:text-brand-500 transition-colors duration-300`}>
      {/* Top Navigation */}
      <Navbar
        theme={theme}
        onToggleTheme={toggleTheme}
        health={health}
        modelInfo={modelInfo}
        onOpenSpecs={() => setIsSpecsOpen(true)}
      />

      <main className="flex-1">
        {/* Hero Section */}
        <Hero onScrollToUpload={handleScrollToUpload} />

        {/* Interactive Denoise Studio Section */}
        <section id="studio" className="py-16 md:py-24 relative">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
            
            {/* Studio Header */}
            <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 pb-6 border-b border-slate-200/80 dark:border-slate-800/80">
              <div>
                <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-brand-500/10 text-brand-600 dark:text-brand-400 text-xs font-semibold mb-2 border border-brand-500/20 shadow-sm">
                  <Sliders className="w-3.5 h-3.5" />
                  <span>Real-Time Inference Workspace</span>
                </div>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
                  Smartphone Photograph Denoising Studio
                </h2>
                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
                  Upload any raw or compressed smartphone image to execute deep neural denoising. Our system preserves 100% of the image's original dimensions and aspect ratio.
                </p>
              </div>

              {denoiseResult && (
                <div className="flex items-center space-x-2 text-xs text-emerald-600 dark:text-emerald-400 font-medium bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-lg flex-shrink-0">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Restoration Completed</span>
                </div>
              )}
            </div>

            {/* Denoise Result or Uploader */}
            {denoiseResult ? (
              <ComparisonSlider
                data={denoiseResult}
                onReset={() => setDenoiseResult(null)}
              />
            ) : (
              <ImageUploader
                onDenoiseSuccess={(res) => setDenoiseResult(res)}
                isLoading={isLoading}
                setIsLoading={setIsLoading}
              />
            )}

          </div>
        </section>

        {/* Authentic Smartphone Dataset Gallery */}
        <SampleGallery
          onSelectSample={(res) => setDenoiseResult(res)}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
        />

        {/* Methodology & Theoretical Architecture with 3D Visualizer */}
        <ArchitectureSection theme={theme} />

        {/* Benchmark Comparisons */}
        <BenchmarkSection />
      </main>

      {/* Footer */}
      <Footer />

      {/* System Specifications Modal */}
      <ModelSpecsModal
        isOpen={isSpecsOpen}
        onClose={() => setIsSpecsOpen(false)}
        modelInfo={modelInfo}
        health={health}
      />
    </div>
  );
}

export default App;
