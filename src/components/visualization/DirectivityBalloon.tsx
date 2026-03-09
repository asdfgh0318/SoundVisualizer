/**
 * 3D Directivity Balloon — Three.js sphere colored by SPL at a given frequency.
 * AN69 style: radiation behavior over phi and theta.
 */

import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import type { DirectionalSpectrum } from '../../audio/spectrum.ts';
import { splAtFrequency } from '../../audio/spectrum.ts';

interface DirectivityBalloonProps {
  spectra: DirectionalSpectrum[];
  frequencyHz: number;
  size?: number;
}

function splToColor(spl: number, minSpl: number, maxSpl: number): THREE.Color {
  const range = maxSpl - minSpl;
  const t = range > 0 ? Math.max(0, Math.min(1, (spl - minSpl) / range)) : 0.5;
  // Blue -> Cyan -> Green -> Yellow -> Red
  const color = new THREE.Color();
  color.setHSL((1 - t) * 0.65, 1, 0.5);
  return color;
}

/**
 * Interpolate SPL at arbitrary (az, el) from sparse measurements using
 * inverse-distance weighting on the sphere.
 */
function interpolateSpl(
  azDeg: number,
  elDeg: number,
  points: { az: number; el: number; spl: number }[],
): number {
  const toRad = Math.PI / 180;

  // Convert to unit sphere coordinates
  const x0 = Math.cos(elDeg * toRad) * Math.cos(azDeg * toRad);
  const y0 = Math.sin(elDeg * toRad);
  const z0 = Math.cos(elDeg * toRad) * Math.sin(azDeg * toRad);

  let weightSum = 0;
  let valueSum = 0;

  for (const p of points) {
    const x1 = Math.cos(p.el * toRad) * Math.cos(p.az * toRad);
    const y1 = Math.sin(p.el * toRad);
    const z1 = Math.cos(p.el * toRad) * Math.sin(p.az * toRad);

    const dot = x0 * x1 + y0 * y1 + z0 * z1;
    const angle = Math.acos(Math.min(1, Math.max(-1, dot)));

    if (angle < 0.001) return p.spl; // exact match

    const w = 1 / (angle * angle + 0.01); // IDW with regularization
    weightSum += w;
    valueSum += w * p.spl;
  }

  return weightSum > 0 ? valueSum / weightSum : -Infinity;
}

export function DirectivityBalloon({
  spectra,
  frequencyHz,
  size = 450,
}: DirectivityBalloonProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<{
    renderer: THREE.WebGLRenderer;
    controls: OrbitControls;
    animId: number;
  } | null>(null);

  useEffect(() => {
    if (!containerRef.current || spectra.length === 0) return;

    // Extract SPL data at the target frequency
    const points = spectra
      .map((s) => ({
        az: s.azimuthDeg,
        el: s.elevationDeg,
        spl: splAtFrequency(s.spectrum, frequencyHz),
      }))
      .filter((p) => isFinite(p.spl));

    if (points.length === 0) return;

    const minSpl = Math.min(...points.map((p) => p.spl));
    const maxSpl = Math.max(...points.map((p) => p.spl));

    // Three.js setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color('#111827');

    const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 100);
    camera.position.set(2.5, 1.5, 2.5);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(size, size);
    renderer.setPixelRatio(window.devicePixelRatio);
    containerRef.current.innerHTML = '';
    containerRef.current.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Build balloon mesh — deform sphere radius by SPL
    const phiSegments = 36;   // azimuth
    const thetaSegments = 18; // elevation
    const geometry = new THREE.SphereGeometry(1, phiSegments, thetaSegments);
    const positions = geometry.attributes.position;
    const colors = new Float32Array(positions.count * 3);

    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i);
      const y = positions.getY(i);
      const z = positions.getZ(i);

      // Convert vertex to spherical (az, el)
      const r = Math.sqrt(x * x + y * y + z * z);
      const elRad = Math.asin(y / r);
      const azRad = Math.atan2(z, x);
      const elDeg = (elRad * 180) / Math.PI;
      const azDeg = ((azRad * 180) / Math.PI + 360) % 360;

      const spl = interpolateSpl(azDeg, elDeg, points);
      const splRange = maxSpl - minSpl;
      const normalizedSpl = splRange > 0 ? (spl - minSpl) / splRange : 0.5;

      // Deform radius: 0.3 to 1.5 based on SPL
      const newR = 0.3 + normalizedSpl * 1.2;
      positions.setXYZ(i, (x / r) * newR, (y / r) * newR, (z / r) * newR);

      const color = splToColor(spl, minSpl, maxSpl);
      colors[i * 3] = color.r;
      colors[i * 3 + 1] = color.g;
      colors[i * 3 + 2] = color.b;
    }

    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.computeVertexNormals();

    const material = new THREE.MeshPhongMaterial({
      vertexColors: true,
      side: THREE.DoubleSide,
      shininess: 30,
      transparent: true,
      opacity: 0.85,
    });

    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    // Wireframe overlay
    const wireMat = new THREE.MeshBasicMaterial({
      color: 0x444444,
      wireframe: true,
      transparent: true,
      opacity: 0.15,
    });
    scene.add(new THREE.Mesh(geometry.clone(), wireMat));

    // Axes helper
    const axes = new THREE.AxesHelper(1.8);
    scene.add(axes);

    // Reference sphere (unit)
    const refGeo = new THREE.SphereGeometry(0.02, 8, 8);
    const refMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    scene.add(new THREE.Mesh(refGeo, refMat)); // origin dot

    // Lighting
    scene.add(new THREE.AmbientLight(0xffffff, 0.5));
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(3, 3, 3);
    scene.add(dirLight);

    // Animate
    let animId = 0;
    const animate = () => {
      animId = requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    sceneRef.current = { renderer, controls, animId };

    return () => {
      cancelAnimationFrame(animId);
      renderer.dispose();
      geometry.dispose();
      material.dispose();
      wireMat.dispose();
      controls.dispose();
    };
  }, [spectra, frequencyHz, size]);

  if (spectra.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8 text-sm">
        No spectral data — capture measurements first
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="mx-auto"
      style={{ width: size, height: size }}
      aria-label={`3D directivity balloon at ${frequencyHz} Hz`}
    />
  );
}
