/* Sistema de partículas 3D — red de nodos etéreos con Three.js */

const background = (() => {
  const canvas = document.getElementById('bg-canvas');
  if (!canvas || typeof THREE === 'undefined') return {};

  // ── Colores del tema ──────────────────────────────────────────────────
  function isDark() {
    return document.documentElement.getAttribute('data-theme') === 'dark';
  }

  /** Color de fondo como entero hex para Three.js */
  function bgHex() {
    return isDark() ? 0x0f172a : 0xf8fafc;
  }

  function themeColors() {
    const dark = isDark();
    return {
      nodeColor:   dark ? 0x60a5fa : 0x4f46e5,
      edgeColor:   dark ? 0x93c5fd : 0x818cf8,
      nodeOpacity: dark ? 0.95 : 0.85,
      edgeOpacity: dark ? 0.40 : 0.30,
    };
  }

  // ── Renderer (opaco — pinta el fondo del tema) ────────────────────────
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(bgHex(), 1);

  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 100);
  camera.position.set(0, 0, 14);

  // ── Nodos ─────────────────────────────────────────────────────────────
  const N         = 65;
  const MAX_LINES = 1500;
  const CONN_DIST = 4.2;
  const BX = 12, BY = 8, BZ = 6;

  const pos   = new Float32Array(N * 3);
  const vel   = new Float32Array(N * 3);
  const phase = new Float32Array(N);

  for (let i = 0; i < N; i++) {
    pos[i*3]   = (Math.random() - 0.5) * BX * 2;
    pos[i*3+1] = (Math.random() - 0.5) * BY * 2;
    pos[i*3+2] = (Math.random() - 0.5) * BZ * 2;
    vel[i*3]   = (Math.random() - 0.5) * 0.007;
    vel[i*3+1] = (Math.random() - 0.5) * 0.007;
    vel[i*3+2] = (Math.random() - 0.5) * 0.004;
    phase[i]   = Math.random() * Math.PI * 2;
  }

  // Puntos
  const ptGeo  = new THREE.BufferGeometry();
  const ptAttr = new THREE.BufferAttribute(pos, 3);
  ptAttr.setUsage(THREE.DynamicDrawUsage);
  ptGeo.setAttribute('position', ptAttr);

  let c = themeColors();
  const ptMat = new THREE.PointsMaterial({
    color: c.nodeColor, size: 0.18,
    transparent: true, opacity: c.nodeOpacity,
    sizeAttenuation: true,
  });
  scene.add(new THREE.Points(ptGeo, ptMat));

  // Aristas
  const lnBuf  = new Float32Array(MAX_LINES * 6);
  const lnGeo  = new THREE.BufferGeometry();
  const lnAttr = new THREE.BufferAttribute(lnBuf, 3);
  lnAttr.setUsage(THREE.DynamicDrawUsage);
  lnGeo.setAttribute('position', lnAttr);
  lnGeo.setDrawRange(0, 0);

  const lnMat = new THREE.LineBasicMaterial({
    color: c.edgeColor,
    transparent: true, opacity: c.edgeOpacity,
  });
  scene.add(new THREE.LineSegments(lnGeo, lnMat));

  // ── Cámara: reacciona a scroll y mouse ───────────────────────────────
  let rotYTarget = 0, rotYCur = 0;
  let rotXTarget = 0, rotXCur = 0;

  window.addEventListener('scroll', () => {
    rotYTarget = window.scrollY * 0.00028;
  }, { passive: true });

  window.addEventListener('mousemove', (e) => {
    rotYTarget = window.scrollY * 0.00028 + (e.clientX / window.innerWidth  - 0.5) * 0.55;
    rotXTarget = -(e.clientY / window.innerHeight - 0.5) * 0.30;
  });


  // ── Loop de animación ─────────────────────────────────────────────────
  let tick = 0;

  function animate() {
    requestAnimationFrame(animate);
    tick += 0.004;

    // Mover nodos con deriva suave
    for (let i = 0; i < N; i++) {
      const ix = i*3, iy = ix+1, iz = ix+2;
      let x = ptAttr.getX(i) + vel[ix]   + Math.sin(tick + phase[i])        * 0.0018;
      let y = ptAttr.getY(i) + vel[iy]   + Math.cos(tick * 0.75 + phase[i]) * 0.0018;
      let z = ptAttr.getZ(i) + vel[iz];

      if (x >  BX || x < -BX) vel[ix] *= -1;
      if (y >  BY || y < -BY) vel[iy] *= -1;
      if (z >  BZ || z < -BZ) vel[iz] *= -1;

      ptAttr.setXYZ(i, x, y, z);
    }
    ptAttr.needsUpdate = true;

    // Actualizar aristas (conectar nodos cercanos)
    let edgeIdx  = 0;
    const distSq = CONN_DIST * CONN_DIST;
    for (let i = 0; i < N && edgeIdx < MAX_LINES; i++) {
      const ax = ptAttr.getX(i), ay = ptAttr.getY(i), az = ptAttr.getZ(i);
      for (let j = i + 1; j < N && edgeIdx < MAX_LINES; j++) {
        const dx = ptAttr.getX(j) - ax;
        const dy = ptAttr.getY(j) - ay;
        const dz = ptAttr.getZ(j) - az;
        if (dx*dx + dy*dy + dz*dz < distSq) {
          lnAttr.setXYZ(edgeIdx*2,   ax, ay, az);
          lnAttr.setXYZ(edgeIdx*2+1, ptAttr.getX(j), ptAttr.getY(j), ptAttr.getZ(j));
          edgeIdx++;
        }
      }
    }
    lnAttr.needsUpdate = true;
    lnGeo.setDrawRange(0, edgeIdx * 2);

    // Suavizar rotación de cámara
    rotYCur += (rotYTarget - rotYCur) * 0.04;
    rotXCur += (rotXTarget - rotXCur) * 0.04;
    camera.rotation.y = rotYCur;
    camera.rotation.x = rotXCur;

    renderer.render(scene, camera);
  }

  // ── Observar cambio de tema ───────────────────────────────────────────
  new MutationObserver(() => {
    renderer.setClearColor(bgHex(), 1);
    c = themeColors();
    ptMat.color.setHex(c.nodeColor);
    ptMat.opacity    = c.nodeOpacity;
    lnMat.color.setHex(c.edgeColor);
    lnMat.opacity    = c.edgeOpacity;
  }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  // ── Resize ────────────────────────────────────────────────────────────
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  animate();
  return {};
})();
