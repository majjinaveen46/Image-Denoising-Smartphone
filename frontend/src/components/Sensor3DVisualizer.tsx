import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { Activity } from 'lucide-react';

interface Sensor3DProps {
  theme: 'dark' | 'light';
}

export const Sensor3DVisualizer: React.FC<Sensor3DProps> = ({ theme }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [denoiseState, setDenoiseState] = useState<'both' | 'noisy' | 'clean'>('both');

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // Scene & Camera setup
    const scene = new THREE.Scene();
    const width = container.clientWidth || 600;
    const height = container.clientHeight || 340;

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 18, 28);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    // Grid Dimensions
    const size = 28;
    const segments = 32;
    const geometry = new THREE.PlaneGeometry(size, size, segments, segments);
    geometry.rotateX(-Math.PI / 2);

    // Keep initial positions for procedural wave & noise displacement
    const pos = geometry.attributes.position;
    const initialY = new Float32Array(pos.count);
    for (let i = 0; i < pos.count; i++) {
      initialY[i] = pos.getY(i);
    }

    // Material (wireframe terrain mesh)
    const wireframeColor = theme === 'dark' ? 0x0284c7 : 0x0369a1;
    const wireframeMaterial = new THREE.MeshBasicMaterial({
      color: wireframeColor,
      wireframe: true,
      transparent: true,
      opacity: theme === 'dark' ? 0.35 : 0.45,
    });
    const terrainMesh = new THREE.Mesh(geometry, wireframeMaterial);
    scene.add(terrainMesh);

    // 3D Photon Particle Cloud (representing photon shot noise)
    const particleCount = 450;
    const particleGeometry = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleVels = new Float32Array(particleCount);

    for (let i = 0; i < particleCount; i++) {
      particlePositions[i * 3] = (Math.random() - 0.5) * size;
      particlePositions[i * 3 + 1] = Math.random() * 5 + 0.5;
      particlePositions[i * 3 + 2] = (Math.random() - 0.5) * size;
      particleVels[i] = Math.random() * 0.04 + 0.01;
    }
    particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

    const particleColor = theme === 'dark' ? 0x38bdf8 : 0x0284c7;
    const particleMaterial = new THREE.PointsMaterial({
      color: particleColor,
      size: 0.35,
      transparent: true,
      opacity: theme === 'dark' ? 0.8 : 0.9,
    });
    const particleSystem = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particleSystem);

    // Mouse Parallax Interaction
    let targetRotY = 0;
    let targetRotX = 0;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      targetRotY = x * 0.4;
      targetRotX = y * 0.2;
    };

    container.addEventListener('mousemove', handleMouseMove);

    // Animation Loop
    let animationFrameId: number;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const time = clock.getElapsedTime();

      // Smooth terrain rotation following mouse
      terrainMesh.rotation.y += (targetRotY - terrainMesh.rotation.y) * 0.05;
      terrainMesh.rotation.z += (targetRotX - terrainMesh.rotation.z) * 0.05;
      particleSystem.rotation.y = terrainMesh.rotation.y;

      // Update Plane Vertices (Procedural 3D Noise vs Smooth Signal)
      const positions = geometry.attributes.position;
      for (let i = 0; i < positions.count; i++) {
        const x = positions.getX(i);
        const z = positions.getZ(i);

        // Smooth underlying photographic signal (sine ripple)
        const cleanSignal = Math.sin(x * 0.3 + time * 1.2) * Math.cos(z * 0.3 + time * 0.8) * 0.8;

        // High-frequency stochastic sensor noise
        const noiseSpike = (Math.sin(x * 5.0 + time * 6.0) * Math.cos(z * 4.0 + time * 5.0)) * 1.4;

        let finalY = cleanSignal;
        if (denoiseState === 'noisy') {
          finalY = cleanSignal + noiseSpike;
        } else if (denoiseState === 'clean') {
          finalY = cleanSignal * 0.4;
        } else {
          // 'both': Split down the middle (Left = Noisy Sensor, Right = Denoised Neural Surface)
          const blendFactor = THREE.MathUtils.smoothstep(x, -4, 4);
          finalY = THREE.MathUtils.lerp(cleanSignal + noiseSpike, cleanSignal * 0.3, blendFactor);
        }

        positions.setY(i, finalY);
      }
      positions.needsUpdate = true;

      // Update Particles (Photon shot noise hovering and falling)
      const pPositions = particleGeometry.attributes.position;
      for (let i = 0; i < particleCount; i++) {
        let py = pPositions.getY(i) - particleVels[i];
        if (py < 0.2) py = 5.0;
        pPositions.setY(i, py);
      }
      pPositions.needsUpdate = true;

      renderer.render(scene, camera);
    };

    animate();

    // Resize Handler
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      container.removeEventListener('mousemove', handleMouseMove);
      renderer.dispose();
      geometry.dispose();
      wireframeMaterial.dispose();
      particleGeometry.dispose();
      particleMaterial.dispose();
    };
  }, [theme, denoiseState]);

  return (
    <div className="relative w-full rounded-2xl overflow-hidden glass-panel border border-white/10 dark:border-white/10 dark:bg-slate-900/50 bg-white/60 shadow-2xl p-4 sm:p-6 transition-colors duration-300">
      
      {/* 3D Canvas Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-2 z-10 relative">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-lg bg-brand-500/10 border border-brand-500/20 flex items-center justify-center text-brand-500 dark:text-brand-400">
            <Activity className="w-4 h-4 animate-pulse" />
          </div>
          <div>
            <h4 className="text-xs sm:text-sm font-bold tracking-tight text-slate-800 dark:text-white flex items-center gap-1.5">
              Interactive 3D Sensor & Noise Lattice
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-600 dark:text-brand-300 border border-brand-500/20">
                WebGL
              </span>
            </h4>
            <p className="text-[11px] text-slate-500 dark:text-slate-400">
              Interactive 3D simulation of smartphone photodiode noise and neural surface smoothing.
            </p>
          </div>
        </div>

        {/* 3D State Mode Controls */}
        <div className="flex items-center space-x-1 p-1 rounded-xl bg-slate-200/80 dark:bg-slate-950/80 border border-slate-300 dark:border-slate-800 text-xs">
          <button
            type="button"
            onClick={() => setDenoiseState('both')}
            className={`px-2.5 py-1 rounded-lg font-medium transition-all ${
              denoiseState === 'both'
                ? 'bg-brand-600 text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            Split (Noisy vs Clean)
          </button>
          <button
            type="button"
            onClick={() => setDenoiseState('noisy')}
            className={`px-2.5 py-1 rounded-lg font-medium transition-all ${
              denoiseState === 'noisy'
                ? 'bg-rose-600 text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            Raw Noise
          </button>
          <button
            type="button"
            onClick={() => setDenoiseState('clean')}
            className={`px-2.5 py-1 rounded-lg font-medium transition-all ${
              denoiseState === 'clean'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            Denoised Surface
          </button>
        </div>
      </div>

      {/* 3D WebGL Canvas Container */}
      <div
        ref={mountRef}
        className="w-full h-[280px] sm:h-[320px] rounded-xl overflow-hidden cursor-grab active:cursor-grabbing relative"
      />

      {/* Footer Simulation Legend */}
      <div className="flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400 pt-2 border-t border-slate-200/80 dark:border-slate-800/80">
        <div className="flex items-center space-x-4">
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
            <span>Left: Raw Poisson Photon Fluctuation</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span>Right: Reconstructed Manifold</span>
          </span>
        </div>
        <span className="hidden sm:inline font-mono text-[10px]">
          Hover & move cursor to rotate in 3D
        </span>
      </div>

    </div>
  );
};
