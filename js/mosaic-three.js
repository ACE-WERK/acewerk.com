/**
 * Three.js Mosaic Renderer — AceWerk Hero
 *
 * Renders the 130×130 tile mosaic with glass-like materials (fresnel,
 * thin-film iridescence, transmission hint), rise-on-hover physics,
 * and responsive layout — all driven by Three.js InstancedMesh.
 *
 * Consumes the tile asset map extracted from the landing page hero image
 * (16,900 tiles, RGB data in data/tile-data.b64).
 *
 * Usage:
 *   import { MosaicRenderer } from './js/mosaic-three.js';
 *   const mosaic = new MosaicRenderer(canvas, { cols: 130, rows: 130 });
 *   await mosaic.loadTileData('/data/tile-data.b64');
 *   mosaic.start();
 */

import * as THREE from 'three';

// ── Custom Shaders ──────────────────────────────────────────────
const VERTEX_SHADER = /* glsl */ `
  varying vec2 vUv;
  varying vec3 vWorldPos;
  varying vec3 vWorldNormal;
  varying vec3 vViewPos;
  varying vec3 vInstanceColor;

  // Per-instance color attribute (custom, added via InstancedBufferAttribute)
  attribute vec3 aInstanceColor;

  // Instance matrix (managed by Three.js InstancedMesh)
  // Must be explicitly declared for ShaderMaterial on InstancedMesh
  attribute mat4 instanceMatrix;

  void main() {
    vUv = uv;

    // Instance transform
    vec4 worldPos = instanceMatrix * vec4(position, 1.0);

    // Normal in world space (approximate — assumes uniform scaling)
    vec3 worldNormal = normalize(mat3(instanceMatrix) * normal);

    vWorldPos = worldPos.xyz;
    vWorldNormal = worldNormal;
    vInstanceColor = aInstanceColor;

    vec4 mvPosition = modelViewMatrix * worldPos;
    vViewPos = -mvPosition.xyz; // view-space position (camera at origin)

    gl_Position = projectionMatrix * mvPosition;
  }
`;

const FRAGMENT_SHADER = /* glsl */ `
  varying vec2 vUv;
  varying vec3 vWorldPos;
  varying vec3 vWorldNormal;
  varying vec3 vViewPos;
  varying vec3 vInstanceColor;

  uniform vec3 uCameraPos;
  uniform float uTime;
  uniform float uIridescence;
  uniform float uRoughness;
  uniform float uTransmission;
  uniform float uFresnelPower;

  // ── Helpers ──

  // Rounded rectangle SDF
  float rbox(vec2 p, vec2 b, float r) {
    vec2 q = abs(p) - b + r;
    return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r;
  }

  // Schlick Fresnel
  float fresnelSchlick(float cosTheta, float f0) {
    return f0 + (1.0 - f0) * pow(1.0 - cosTheta, 5.0);
  }

  // Thin-film iridescence — angle-dependent color shift
  vec3 thinFilm(float cosTheta, float strength) {
    // Simulate thin-film interference: phase shift depends on angle
    float phase = (1.0 - cosTheta) * 3.0 + uTime * 0.15;

    // Base interference colors (soap-bubble palette)
    vec3 c1 = vec3(1.0, 0.3, 0.2);  // warm
    vec3 c2 = vec3(0.2, 0.6, 1.0);  // cool
    vec3 c3 = vec3(0.3, 1.0, 0.4);  // green
    vec3 c4 = vec3(0.8, 0.2, 1.0);  // purple

    float t = fract(phase);
    vec3 iri = mix(mix(c1, c2, smoothstep(0.0, 0.33, t)),
                   mix(c3, c4, smoothstep(0.33, 0.66, t)),
                   smoothstep(0.33, 0.66, t));

    return iri * strength;
  }

  void main() {
    // ── Tile shape mask ──
    vec2 p = vUv - 0.5;
    float d = rbox(p, vec2(0.5), 0.14);
    float aa = fwidth(d) * 1.25;
    float mask = smoothstep(aa, -aa, d);
    if (mask <= 0.002) discard;

    // ── View direction ──
    vec3 V = normalize(vViewPos);
    vec3 N = normalize(vWorldNormal);

    // ── Edge distance for glass effects ──
    float edgeDist = -d; // positive inside, near edge = near 0
    float edgeFactor = smoothstep(0.0, 0.12, edgeDist);

    // ── Fresnel (glassy edge sheen) ──
    float cosTheta = abs(dot(N, V));
    float fresnel = fresnelSchlick(cosTheta, 0.04);

    // ── Iridescence ──
    vec3 iridescence = thinFilm(cosTheta, uIridescence);

    // ── Base color ──
    vec3 baseColor = vInstanceColor;

    // ── Compose the glass look ──
    // Core: the base color
    vec3 col = baseColor;

    // Transmission hint: edges are slightly brighter/clearer
    float transmission = uTransmission * (1.0 - edgeFactor);
    col = mix(col, col * 1.3, transmission * 0.35);

    // Iridescence overlay — strongest at glancing angles
    float iriMask = fresnel * (1.0 - uRoughness);
    col = mix(col, col + iridescence * 0.25, iriMask);

    // Fresnel edge glow — bright rim like glass
    float rim = fresnel * pow(1.0 - edgeFactor, 1.5) * 0.55;
    col += rim * mix(vec3(0.8, 0.85, 1.0), baseColor * 1.5, 0.5);

    // Specular highlight (crisp top-left sparkle)
    vec3 H = normalize(V + vec3(0.3, 0.5, 1.0)); // fake light direction
    float spec = pow(max(dot(N, H), 0.0), 128.0);
    col += spec * 0.18 * mix(vec3(1.0), baseColor, 0.6);

    // Top sheen
    col += smoothstep(0.5, -0.5, p.y) * 0.04;

    // Subtle depth darkening toward center
    col *= 0.85 + 0.15 * edgeFactor;

    // Clamp and output
    col = clamp(col, 0.0, 1.3);

    float alpha = (0.88 + fresnel * 0.12) * mask;
    gl_FragColor = vec4(col, alpha);
  }
`;

// ── MosaicRenderer ──────────────────────────────────────────────
export class MosaicRenderer {
  /**
   * @param {HTMLCanvasElement} canvas
   * @param {Object} config
   * @param {number} config.cols - Grid columns (130)
   * @param {number} config.rows - Grid rows (130)
   * @param {number} [config.tileGap=0.13] - Gap between tiles as fraction
   * @param {number} [config.riseHeight=0.35] - Max rise in tile units
   * @param {number} [config.hoverRadius=8] - Hover radius in tile units
   * @param {number} [config.iridescence=0.45] - Iridescence strength
   * @param {number} [config.roughness=0.15] - Surface roughness
   * @param {number} [config.transmission=0.35] - Transmission amount
   * @param {number} [config.fresnelPower=3.5] - Fresnel exponent
   */
  constructor(canvas, config = {}) {
    this.canvas = canvas;
    this.cols = config.cols || 130;
    this.rows = config.rows || 130;
    this.tileGap = config.tileGap ?? 0.13;
    this.riseHeight = config.riseHeight ?? 0.35;
    this.hoverRadius = config.hoverRadius ?? 8;
    this.N = this.cols * this.rows;

    // Material params
    this._iridescence = config.iridescence ?? 0.45;
    this._roughness = config.roughness ?? 0.15;
    this._transmission = config.transmission ?? 0.35;
    this._fresnelPower = config.fresnelPower ?? 3.5;

    // State
    this.tileData = null;
    this.instancedMesh = null;
    this.riseTargets = null;
    this.riseValues = null;
    this.riseVelocities = null;
    this.mouseTile = null;
    this.mouse = { x: -999, y: -999 };
    this.running = false;
    this.rafId = 0;
    this.lastTime = 0;
    this.dpr = 1;
    this.reduceMotion = false;

    // Three.js objects
    this.renderer = null;
    this.scene = null;
    this.camera = null;
    this.raycaster = null;
    this.mouseNDC = new THREE.Vector2();

    this._init();
  }

  // ── Initialization ──
  _init() {
    this.reduceMotion = window.matchMedia(
      '(prefers-reduced-motion: reduce)'
    ).matches;

    // ── Renderer ──
    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      alpha: true,
      premultipliedAlpha: false,
      antialias: true,
    });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    this.renderer.setClearColor(0x000000, 0);
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;

    // ── Scene ──
    this.scene = new THREE.Scene();

    // ── Camera (orthographic, looking down) ──
    // We position the camera looking down at the mosaic grid.
    // The grid spans from (0,0) to (cols, rows) in tile units.
    this.camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 100);
    this.camera.position.set(this.cols / 2, this.rows / 2, 50);
    this.camera.lookAt(this.cols / 2, this.rows / 2, 0);

    // ── Raycaster ──
    this.raycaster = new THREE.Raycaster();
    this.raycaster.far = 60;

    // ── Ambient light (for the scene, though shader is self-lit) ──
    // No external lights needed — our custom shader is self-illuminating.

    // ── Resize ──
    this._onResize = this._onResize.bind(this);
    this._onPointerMove = this._onPointerMove.bind(this);
    this._onPointerLeave = this._onPointerLeave.bind(this);
    this._onTouchStart = this._onTouchStart.bind(this);
    this._onTouchMove = this._onTouchMove.bind(this);
    this._onTouchEnd = this._onTouchEnd.bind(this);
    this._onVisibility = this._onVisibility.bind(this);

    window.addEventListener('resize', this._onResize);
    this._onResize();

    // ── Context loss handling ──
    this.canvas.addEventListener(
      'webglcontextlost',
      (e) => {
        e.preventDefault();
        this.stop();
      },
      false
    );
    this.canvas.addEventListener(
      'webglcontextrestored',
      () => {
        if (this.tileData) this.start();
      },
      false
    );
  }

  // ── Load tile data ──
  /**
   * Load tile RGB data from a base64-encoded file.
   * @param {string} url - URL to the base64 tile data file
   * @returns {Promise<void>}
   */
  async loadTileData(url) {
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`Failed to load tile data: ${resp.status}`);
    const b64 = await resp.text();
    const raw = atob(b64.trim());
    this.tileData = new Uint8Array(raw.length);
    for (let i = 0; i < raw.length; i++) {
      this.tileData[i] = raw.charCodeAt(i);
    }
    this._buildMesh();
  }

  /**
   * Load tile data from an inline base64 string.
   * @param {string} b64 - Base64-encoded RGB data
   */
  loadTileDataInline(b64) {
    const raw = atob(b64.trim());
    this.tileData = new Uint8Array(raw.length);
    for (let i = 0; i < raw.length; i++) {
      this.tileData[i] = raw.charCodeAt(i);
    }
    this._buildMesh();
  }

  // ── Build instanced mesh ──
  _buildMesh() {
    if (!this.tileData) return;

    const N = this.N;
    const cols = this.cols;
    const rows = this.rows;
    const gap = this.tileGap;

    // ── Geometry: a unit plane ──
    const geo = new THREE.PlaneGeometry(1.0 - gap, 1.0 - gap);

    // ── Custom shader material ──
    const material = new THREE.ShaderMaterial({
      vertexShader: VERTEX_SHADER,
      fragmentShader: FRAGMENT_SHADER,
      uniforms: {
        uCameraPos: { value: new THREE.Vector3() },
        uTime: { value: 0 },
        uIridescence: { value: this._iridescence },
        uRoughness: { value: this._roughness },
        uTransmission: { value: this._transmission },
        uFresnelPower: { value: this._fresnelPower },
      },
      transparent: true,
      depthWrite: true,
      depthTest: true,
    });

    // ── Create InstancedMesh ──
    // Note: Three.js InstancedMesh requires MeshStandardMaterial or
    // ShaderMaterial if we handle instanceMatrix ourselves.
    // We'll extend InstancedMesh to work with ShaderMaterial.
    const mesh = new THREE.InstancedMesh(geo, material, N);
    mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    mesh.castShadow = false;
    mesh.receiveShadow = false;
    mesh.frustumCulled = false; // Always visible in orthographic view

    // ── Add per-instance color attribute ──
    const colors = new Float32Array(N * 3);
    const colorAttr = new THREE.InstancedBufferAttribute(colors, 3);
    mesh.geometry.setAttribute('aInstanceColor', colorAttr);

    // ── Set initial instance transforms and colors ──
    const dummy = new THREE.Object3D();
    const matrix = new THREE.Matrix4();

    for (let i = 0; i < N; i++) {
      const col = i % cols;
      const row = Math.floor(i / cols);

      // Position: center of each grid cell, at z=0
      dummy.position.set(col + 0.5, row + 0.5, 0);
      dummy.rotation.set(0, 0, 0);
      dummy.scale.set(1, 1, 1);
      dummy.updateMatrix();

      mesh.setMatrixAt(i, dummy.matrix);

      // Color from tile data
      const o = i * 3;
      colors[o] = this.tileData[o] / 255;
      colors[o + 1] = this.tileData[o + 1] / 255;
      colors[o + 2] = this.tileData[o + 2] / 255;
    }

    colorAttr.needsUpdate = true;
    mesh.instanceMatrix.needsUpdate = true;

    // ── Animation state ──
    this.riseTargets = new Float32Array(N);
    this.riseValues = new Float32Array(N);
    this.riseVelocities = new Float32Array(N);

    // Pre-allocate dummy Object3D for matrix updates (reused every frame)
    this._dummyObj = new THREE.Object3D();

    this.instancedMesh = mesh;
    this.scene.add(mesh);
  }

  // ── Start / Stop ──
  start() {
    if (!this.instancedMesh || this.running) return;
    this.running = true;

    if (!this.reduceMotion) {
      this.canvas.addEventListener('pointermove', this._onPointerMove);
      this.canvas.addEventListener('pointerleave', this._onPointerLeave);
      this.canvas.addEventListener('touchstart', this._onTouchStart, { passive: true });
      this.canvas.addEventListener('touchmove', this._onTouchMove, { passive: true });
      this.canvas.addEventListener('touchend', this._onTouchEnd);
      document.addEventListener('visibilitychange', this._onVisibility);
    }

    this.lastTime = performance.now();
    this._animate(this.lastTime);
  }

  stop() {
    this.running = false;
    cancelAnimationFrame(this.rafId);

    this.canvas.removeEventListener('pointermove', this._onPointerMove);
    this.canvas.removeEventListener('pointerleave', this._onPointerLeave);
    this.canvas.removeEventListener('touchstart', this._onTouchStart);
    this.canvas.removeEventListener('touchmove', this._onTouchMove);
    this.canvas.removeEventListener('touchend', this._onTouchEnd);
    document.removeEventListener('visibilitychange', this._onVisibility);
  }

  dispose() {
    this.stop();
    window.removeEventListener('resize', this._onResize);
    if (this.instancedMesh) {
      this.instancedMesh.geometry.dispose();
      this.instancedMesh.material.dispose();
      this.scene.remove(this.instancedMesh);
      this.instancedMesh = null;
    }
    if (this.renderer) {
      this.renderer.dispose();
      this.renderer = null;
    }
  }

  // ── Resize ──
  _onResize() {
    const canvas = this.canvas;
    const parent = canvas.parentElement;
    const rect = parent ? parent.getBoundingClientRect() : { width: window.innerWidth, height: window.innerHeight };
    const w = rect.width;
    const h = rect.height;

    this.dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(w * this.dpr);
    canvas.height = Math.round(h * this.dpr);
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';

    if (this.renderer) {
      this.renderer.setSize(canvas.width, canvas.height, false);

      // Update orthographic camera
      const aspect = w / Math.max(h, 1);

      // Fit the grid: scale so the grid fills the viewport, centering
      const gridAspect = this.cols / this.rows;
      let viewW, viewH;

      if (aspect > gridAspect) {
        // Viewport wider than grid — fit height
        viewH = this.rows;
        viewW = this.rows * aspect;
      } else {
        // Viewport taller than grid — fit width
        viewW = this.cols;
        viewH = this.cols / aspect;
      }

      if (this.camera) {
        this.camera.left = -viewW / 2 + this.cols / 2;
        this.camera.right = viewW / 2 + this.cols / 2;
        this.camera.top = viewH / 2 + this.rows / 2;
        this.camera.bottom = -viewH / 2 + this.rows / 2;
        this.camera.updateProjectionMatrix();
      }
    }
  }

  // ── Pointer input ──
  _screenToWorld(clientX, clientY) {
    const rect = this.canvas.getBoundingClientRect();
    const x = ((clientX - rect.left) / rect.width) * 2 - 1;
    const y = -((clientY - rect.top) / rect.height) * 2 + 1;
    this.mouseNDC.set(x, y);
  }

  _onPointerMove(e) {
    this._screenToWorld(e.clientX, e.clientY);
    this.mouse.x = e.clientX;
    this.mouse.y = e.clientY;
  }

  _onPointerLeave() {
    this.mouseNDC.set(-999, -999);
  }

  _onTouchStart(e) {
    const t = e.touches[0];
    if (t) this._onPointerMove({ clientX: t.clientX, clientY: t.clientY });
  }

  _onTouchMove(e) {
    const t = e.touches[0];
    if (t) this._onPointerMove({ clientX: t.clientX, clientY: t.clientY });
  }

  _onTouchEnd() {
    this._onPointerLeave();
  }

  _onVisibility() {
    if (document.hidden) {
      this.mouseNDC.set(-999, -999);
    }
  }

  // ── Hover detection ──
  _updateHover() {
    if (!this.instancedMesh) return;

    this.raycaster.setFromCamera(this.mouseNDC, this.camera);
    const intersects = this.raycaster.intersectObject(this.instancedMesh);

    if (intersects.length > 0) {
      const hit = intersects[0];
      this.mouseTile = hit.instanceId;
    } else {
      this.mouseTile = null;
    }
  }

  // ── Animation loop ──
  _animate(now) {
    if (!this.running) return;

    const dt = Math.min((now - this.lastTime) * 0.001, 0.05);
    this.lastTime = now;

    // Update hover
    this._updateHover();

    // Physics: spring-based rise animation
    const STIFF = 0.14;
    const DAMP = 0.78;
    const RELEASE = 0.06;
    const RISE_HEIGHT = this.riseHeight;
    const RADIUS = this.hoverRadius;

    const N = this.N;
    const cols = this.cols;
    const targets = this.riseTargets;
    const values = this.riseValues;
    const velocities = this.riseVelocities;

    // Reset all targets
    targets.fill(0);

    // Set targets for tiles near the hover point
    if (this.mouseTile !== null) {
      const centerCol = this.mouseTile % cols;
      const centerRow = Math.floor(this.mouseTile / cols);

      const radiusSq = RADIUS * RADIUS;
      const colStart = Math.max(0, centerCol - RADIUS);
      const colEnd = Math.min(cols - 1, centerCol + RADIUS);
      const rowStart = Math.max(0, centerRow - RADIUS);
      const rowEnd = Math.min(this.rows - 1, centerRow + RADIUS);

      for (let r = rowStart; r <= rowEnd; r++) {
        for (let c = colStart; c <= colEnd; c++) {
          const dx = c - centerCol;
          const dy = r - centerRow;
          const d2 = dx * dx + dy * dy;
          if (d2 < radiusSq) {
            const t = 1.0 - Math.sqrt(d2 / radiusSq);
            // Smoothstep falloff
            targets[r * cols + c] = t * t * (3.0 - 2.0 * t);
          }
        }
      }
    }

    // Spring update
    const dummy = this._dummyObj;
    let matrixDirty = false;

    for (let i = 0; i < N; i++) {
      const target = targets[i];
      let value = values[i];

      if (target > value) {
        let v = velocities[i];
        v += (target - value) * STIFF;
        v *= DAMP;
        value += v;
        if (value > 1.15) value = 1.15;
        velocities[i] = v;
      } else {
        value += (target - value) * RELEASE;
        if (value < 0.001) value = 0;
        if (value < 0) value = 0;
        velocities[i] = 0;
      }

      // Only update matrix if value changed enough
      if (Math.abs(value - values[i]) > 0.0001 || value > 0) {
        values[i] = value;

        const col = i % cols;
        const row = Math.floor(i / cols);
        dummy.position.set(col + 0.5, row + 0.5, value * RISE_HEIGHT);
        dummy.rotation.set(0, 0, 0);
        dummy.scale.set(1 + value * 0.08, 1 + value * 0.08, 1);
        dummy.updateMatrix();
        this.instancedMesh.setMatrixAt(i, dummy.matrix);
        matrixDirty = true;
      } else {
        values[i] = value;
      }
    }

    if (matrixDirty) {
      this.instancedMesh.instanceMatrix.needsUpdate = true;
    }

    // Update shader uniforms
    const mat = this.instancedMesh.material;
    if (mat.uniforms) {
      mat.uniforms.uTime.value = now * 0.001;
      mat.uniforms.uCameraPos.value.set(
        this.camera.position.x,
        this.camera.position.y,
        this.camera.position.z
      );
    }

    // Render
    this.renderer.render(this.scene, this.camera);

    this.rafId = requestAnimationFrame((t) => this._animate(t));
  }
}

// ── Convenience: auto-init for mosaic-galaxy canvases ──
export async function initMosaicGalaxy(canvasId, dataUrl, config = {}) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;

  const mosaic = new MosaicRenderer(canvas, config);
  try {
    await mosaic.loadTileData(dataUrl);
    mosaic.start();
    return mosaic;
  } catch (err) {
    console.error('Mosaic init failed:', err);
    canvas.style.display = 'none';
    return null;
  }
}
