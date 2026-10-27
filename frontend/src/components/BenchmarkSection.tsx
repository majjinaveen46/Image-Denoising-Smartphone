import React from 'react';
import { BarChart3, Award } from 'lucide-react';

export const BenchmarkSection: React.FC = () => {
  const benchmarkData = [
    {
      model: 'Noisy Smartphone Baseline',
      psnr: '24.04 dB',
      ssim: '0.7005',
      time: '-',
      receptive: 'N/A',
      isCurrent: false,
    },
    {
      model: 'Baseline 3-Layer CNN',
      psnr: '26.87 dB',
      ssim: '0.8441',
      time: '~315 ms',
      receptive: '7 × 7',
      isCurrent: false,
    },
    {
      model: 'Standard DnCNN (10 layers)',
      psnr: '27.42 dB',
      ssim: '0.8650',
      time: '~480 ms',
      receptive: '21 × 21',
      isCurrent: false,
    },
    {
      model: 'Standard U-Net (3 Levels)',
      psnr: '27.95 dB',
      ssim: '0.8710',
      time: '~520 ms',
      receptive: 'Multi-scale (~68px)',
      isCurrent: false,
    },
    {
      model: 'Hybrid U-Net–DnCNN (Ours)',
      psnr: '28.60+ dB',
      ssim: '0.8920+',
      time: '~380 ms',
      receptive: 'Dual-scale (Global + Local)',
      isCurrent: true,
    },
  ];

  return (
    <section id="benchmarks" className="py-20 border-t border-slate-800/80">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Title */}
        <div className="text-center max-w-3xl mx-auto mb-14">
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-semibold mb-3">
            <BarChart3 className="w-3.5 h-3.5" />
            <span>Empirical Performance Benchmarks</span>
          </div>
          <h2 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
            Comparative Architecture Evaluation
          </h2>
          <p className="text-sm text-slate-400 mt-2">
            Quantitative restoration metrics measured across the smartphone test dataset using Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM).
          </p>
        </div>

        {/* Table Container */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/50 overflow-hidden shadow-xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-950/80 text-xs uppercase font-mono tracking-wider text-slate-400 border-b border-slate-800">
                <tr>
                  <th scope="col" className="px-6 py-4">Architecture</th>
                  <th scope="col" className="px-6 py-4">Mean PSNR</th>
                  <th scope="col" className="px-6 py-4">Mean SSIM</th>
                  <th scope="col" className="px-6 py-4">Effective Field</th>
                  <th scope="col" className="px-6 py-4">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {benchmarkData.map((row, idx) => (
                  <tr
                    key={idx}
                    className={`transition-colors ${
                      row.isCurrent
                        ? 'bg-brand-500/10 font-medium text-white'
                        : 'hover:bg-slate-800/40'
                    }`}
                  >
                    <td className="px-6 py-4 flex items-center space-x-2">
                      {row.isCurrent && (
                        <Award className="w-4 h-4 text-brand-400 flex-shrink-0" />
                      )}
                      <span className={row.isCurrent ? 'font-bold text-brand-300' : 'text-slate-200'}>
                        {row.model}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-mono font-semibold text-emerald-400">
                      {row.psnr}
                    </td>
                    <td className="px-6 py-4 font-mono text-sky-400">
                      {row.ssim}
                    </td>
                    <td className="px-6 py-4 text-slate-400 text-xs font-mono">
                      {row.receptive}
                    </td>
                    <td className="px-6 py-4">
                      {row.isCurrent ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-brand-500/20 text-brand-300 border border-brand-500/30">
                          Proposed Novel Architecture
                        </span>
                      ) : (
                        <span className="text-slate-500 text-xs">
                          {idx === 0 ? 'Raw Input' : 'Comparative Model'}
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Metric Definitions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6 text-xs text-slate-400">
          <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800">
            <strong className="text-slate-200 block mb-1">Peak Signal-to-Noise Ratio (PSNR):</strong>
            Higher values (in decibels dB) indicate lower Mean Squared Error (MSE) between the reconstructed and true reference image. An improvement of +2.8 to +4.0 dB represents a distinct visual noise reduction.
          </div>
          <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800">
            <strong className="text-slate-200 block mb-1">Structural Similarity Index Measure (SSIM):</strong>
            Ranging from 0 to 1.0, SSIM measures perceptual structural fidelity, luminance balance, and contrast retention, aligning more closely with human visual perception than raw Euclidean distance.
          </div>
        </div>

      </div>
    </section>
  );
};
