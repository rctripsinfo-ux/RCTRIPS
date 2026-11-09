// The Piazza dei Miracoli as one three.js scene (our own simplified version): lawns and white paths, the cathedral,
// the baptistery, the city wall, houses, and the bell tower that grows floor by floor, leans, bends ("banana"), sinks,
// is tied with cables, weighted with lead, straightened a little and shaken by an earthquake. Plus the mattress demo.
import * as THREE from "three";
import { Batch, V, lam, boxGeo, prop, house, Kit } from "./build";
import { rep, ctex, rng, cloudHD, stoneHD, grassHD } from "./paint";
import { LIGHTS, LOOK, LightPreset } from "./lights";
import { TONE, CHAR, twoTone, untone } from "./shade";
import { NOINK } from "./ink";
import { Pool, Actor, Fx, stage } from "./cast";
import { FPS, SHOTS, H, camAt, V3, smooth, ShotDef, TOWER_R, floorsAt, leanAt, sinkAt, MATTRESS, RIG, QUAKE, QUAKE_END, FOREGROUND, kickAt } from "./story";

export const loadKit = () => Promise.resolve({} as Kit);
void FOREGROUND; void H;

// ---------------- painted textures ----------------
/** white marble arcade band: arches with dark recesses and slim columns, thin grey-green inlay lines */
const arcadeTex = (blind: boolean) => ctex("arcade" + blind, 1024, 256, (g) => {
  g.fillStyle = "#f3eee3"; g.fillRect(0, 0, 1024, 256);
  g.fillStyle = "#d9d2c3"; for (let y = 0; y < 256; y += 32) g.fillRect(0, y, 1024, 2);
  const n = 8, w = 1024 / n;
  for (let i = 0; i < n; i++) {
    const x = i * w, cx = x + w / 2;
    g.fillStyle = blind ? "#cfc6b4" : "#3b3d52";
    g.beginPath(); g.moveTo(x + 14, 250); g.lineTo(x + 14, 92); g.arc(cx, 92, w / 2 - 14, Math.PI, 0); g.lineTo(x + w - 14, 250); g.closePath(); g.fill();
    g.strokeStyle = "#8f8a7c"; g.lineWidth = 5; g.beginPath(); g.arc(cx, 92, w / 2 - 14, Math.PI, 0); g.stroke();
    g.fillStyle = "#faf6ee"; g.fillRect(x - 7, 60, 14, 196);
    g.fillStyle = "#b9b2a2"; g.fillRect(x - 10, 56, 20, 8);
  }
  g.fillStyle = "#6f8a7a"; g.fillRect(0, 0, 1024, 6); g.fillRect(0, 250, 1024, 6);
});
const domeStripes = () => ctex("stripes", 512, 512, (g) => {
  g.fillStyle = "#f2ede2"; g.fillRect(0, 0, 512, 512);
  g.fillStyle = "#7d8a86"; for (let y = 0; y < 512; y += 48) g.fillRect(0, y, 512, 8);
  g.fillStyle = "#3b3d52"; for (let x = 24; x < 512; x += 128) { g.beginPath(); g.moveTo(x, 470); g.lineTo(x, 330); g.arc(x + 40, 330, 40, Math.PI, 0); g.lineTo(x + 80, 470); g.fill(); }
});
const pathTex = () => ctex("path", 512, 512, (g, r) => {
  g.fillStyle = "#e9e4d8"; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 900; i++) { g.fillStyle = r() < 0.5 ? "rgba(150,140,120,0.25)" : "rgba(255,255,255,0.4)"; g.fillRect(r() * 512, r() * 512, 3, 3); }
  g.strokeStyle = "rgba(140,128,110,0.35)"; g.lineWidth = 3; for (let y = 0; y < 512; y += 64) { g.beginPath(); g.moveTo(0, y); g.lineTo(512, y); g.stroke(); }
});

// ---------------- geometry helpers ----------------
const quadUp = (x0: number, x1: number, z0: number, z1: number, y: number, u: number, v: number) => {
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute([x0, y, z1, x1, y, z1, x1, y, z0, x0, y, z1, x1, y, z0, x0, y, z0], 3));
  g.setAttribute("normal", new THREE.Float32BufferAttribute(Array(6).fill([0, 1, 0]).flat(), 3));
  g.setAttribute("uv", new THREE.Float32BufferAttribute([0, 0, u, 0, u, v, 0, 0, u, v, 0, v], 2));
  return g;
};

type Mats = Record<string, THREE.Material>;
/** one tower floor (unit-less: built at its height h and radius r, base at y = 0) */
const floorGeo = (r: number, h: number) => { const g = new THREE.CylinderGeometry(r, r, h, 48, 1, true); g.translate(0, h / 2, 0); return g; };
const corniceGeo = (r: number) => { const g = new THREE.CylinderGeometry(r + 0.45, r + 0.45, 0.55, 48); return g; };
const FLOORS = [{ h: 11, r: TOWER_R, blind: true }, ...Array.from({ length: 6 }, () => ({ h: 6.4, r: TOWER_R, blind: false })), { h: 6.2, r: 5.6, blind: false }];

export class World {
  root = new THREE.Group();
  private pool = new Pool();
  private actors: Actor[] = [];
  private fxs: Fx[] = [];
  private hemi: THREE.HemisphereLight; private sun: THREE.DirectionalLight;
  private sky: THREE.Mesh; private skyMat: THREE.ShaderMaterial;
  private fog = new THREE.Fog("#bccbec", 25, 420);
  private sunDisc: THREE.Sprite; private sunHalo: THREE.Sprite;
  private sunCache = new Map<number, THREE.Vector3>();
  private cloudMaps: Record<"day" | "golden" | "night", THREE.Texture[]>;
  private clouds: THREE.Mesh[] = [];
  private stars!: THREE.Points;
  private tower = new THREE.Group(); private floors: THREE.Group[] = [];
  private cables: THREE.Mesh[] = []; private lead = new THREE.Group(); private rig = new THREE.Group(); private soil!: THREE.Mesh;
  private scaffold = new THREE.Group(); private fence = new THREE.Group(); private vines!: THREE.Mesh;
  private mattress!: THREE.Mesh; private mattressG!: THREE.BufferGeometry; private mattressBase!: Float32Array;
  private frustum = new THREE.Frustum();
  private m4 = new THREE.Matrix4(); private v = new THREE.Vector3(); private sph = new THREE.Sphere(); private fwd = new THREE.Vector3();

  constructor(_kit: Kit) {
    const R = this.root, M: Mats = {};
    // ---- sky + light (as the bridge short) ----
    this.skyMat = new THREE.ShaderMaterial({
      uniforms: { c0: { value: new THREE.Color() }, c1: { value: new THREE.Color() }, c2: { value: new THREE.Color() },
        c3: { value: new THREE.Color() }, c4: { value: new THREE.Color() }, e: { value: new THREE.Vector4() } },
      vertexShader: "varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
      fragmentShader: `uniform vec3 c0, c1, c2, c3, c4; uniform vec4 e; varying vec3 vP;
        void main(){ float el = asin(clamp(normalize(vP).y, -1.0, 1.0));
          vec3 c = mix(c0, c1, smoothstep(0.0, e.x, el));
          c = mix(c, c2, smoothstep(e.x, e.y, el));
          c = mix(c, c3, smoothstep(e.y, e.z, el));
          c = mix(c, c4, smoothstep(e.z, e.w, el));
          gl_FragColor = vec4(c, 1.0); }`,
      side: THREE.BackSide, depthWrite: false, fog: false,
    });
    this.sky = new THREE.Mesh(new THREE.SphereGeometry(1100, 48, 24), this.skyMat);
    this.sky.renderOrder = -1; this.sky.frustumCulled = false; this.sky.layers.set(NOINK);
    R.add(this.sky);
    const disc = ctex("sunDisc", 128, 128, (g) => { const gr = g.createRadialGradient(64, 64, 58, 64, 64, 64); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); });
    const halo = ctex("sunHalo", 256, 256, (g) => {
      const im = g.createImageData(256, 256);
      for (let y = 0; y < 256; y++) for (let x = 0; x < 256; x++) {
        const u = Math.hypot(x - 127.5, y - 127.5) / 128;
        const a = (0.55 * Math.exp(-((u / 0.25) ** 2)) + 0.35 * Math.exp(-((u / 0.6) ** 2))) * (1 - Math.min(1, Math.max(0, (u - 0.8) / 0.2)));
        const i = (y * 256 + x) * 4; im.data[i] = im.data[i + 1] = im.data[i + 2] = 255; im.data[i + 3] = Math.round(255 * Math.min(1, a));
      }
      g.putImageData(im, 0, 0);
    });
    this.sunDisc = new THREE.Sprite(new THREE.SpriteMaterial({ map: disc, color: new THREE.Color(6.0, 4.4, 2.4), fog: false, depthWrite: false }));
    this.sunHalo = new THREE.Sprite(new THREE.SpriteMaterial({ map: halo, color: new THREE.Color(1, 1, 1), fog: false, depthWrite: false, transparent: true, blending: THREE.AdditiveBlending }));
    this.sunDisc.renderOrder = -0.5; this.sunHalo.renderOrder = 5;
    for (const m of [this.sunDisc, this.sunHalo]) { m.frustumCulled = false; m.layers.set(NOINK); R.add(m); }
    this.hemi = new THREE.HemisphereLight("#cfe6ff", "#6c5c8c", 1.1);
    this.sun = new THREE.DirectionalLight("#fff0d6", 2.6);
    this.sun.castShadow = true; this.sun.shadow.mapSize.set(2048, 2048);
    R.add(this.hemi, this.sun, this.sun.target);
    this.cloudMaps = { day: [0, 1, 2, 3].map((k) => cloudHD(k, LOOK.day.cloud)), golden: [0, 1, 2, 3].map((k) => cloudHD(k, LOOK.golden.cloud)), night: [0, 1, 2, 3].map((k) => cloudHD(k, LOOK.night.cloud)) };
    for (let i = 0; i < 10; i++) {
      const a = (i / 10) * Math.PI * 2 + 0.3, d = 600 + (i % 3) * 70;
      const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: this.cloudMaps.day[i % 4], color: new THREE.Color(1.1, 1.1, 1.1), transparent: true, depthWrite: false, fog: false }));
      const w = 140 + (i % 4) * 30;
      m.position.set(Math.cos(a) * d, 110 + (i % 4) * 36, Math.sin(a) * d); m.scale.set(w, w / 2, 1);
      m.layers.set(NOINK); this.clouds.push(m); R.add(m);
    }

    const rr = rng(77);
    // ---- static square ----
    const b = new Batch();
    M.lawn = lam("lawn", () => ({ map: rep(grassHD(), 60, 60) }));
    const lawn = new THREE.PlaneGeometry(700, 700); lawn.rotateX(-Math.PI / 2); b.add(lawn, M.lawn);
    M.path = lam("pathM", () => ({ map: rep(pathTex(), 1, 1) }));
    const strip = (x0: number, x1: number, z0: number, z1: number) => { const g = new THREE.PlaneGeometry(x1 - x0, z1 - z0); g.rotateX(-Math.PI / 2); g.translate((x0 + x1) / 2, 0.02, (z0 + z1) / 2); const uv = g.attributes.uv as THREE.BufferAttribute; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * (x1 - x0) / 8, uv.getY(i) * (z1 - z0) / 8); b.add(g, M.path); };
    strip(-200, 60, -34, -22); strip(-14, 14, -34, 14); strip(-150, -20, -6, 6);
    { const ring = new THREE.RingGeometry(TOWER_R + 0.3, TOWER_R + 5, 48); ring.rotateX(-Math.PI / 2); ring.translate(0, 0.025, 0); b.add(ring, M.path); }
    // cathedral (west): nave, aisles, transept, facade bands, dome
    M.marble = lam("marbleStripe", () => ({ map: rep(domeStripes(), 1, 1) }));
    M.roof = lam("leadRoof", () => ({ color: "#8a8f99" }));
    b.add(boxGeo(V(-130, 0, -12), V(-48, 26, 12), 12), M.marble);
    b.add(boxGeo(V(-130, 0, -20), V(-48, 15, 20), 12), M.marble);
    b.add(boxGeo(V(-100, 0, -40), V(-82, 22, 40), 12), M.marble);
    { const r1 = new THREE.CylinderGeometry(0.01, 15, 7, 4); r1.rotateY(Math.PI / 4); r1.scale(5.6, 1, 1.15); r1.translate(-89, 29.5, 0); b.add(r1, M.roof); }
    { const d = new THREE.SphereGeometry(9, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2); d.scale(1, 1.25, 1); d.translate(-91, 32, 0); b.add(d, M.roof);
      const dr = new THREE.CylinderGeometry(9, 9, 6, 32); dr.translate(-91, 29, 0); b.add(dr, M.marble); }
    // baptistery (far west) and the city wall (north) with its towers
    { const bt = new THREE.CylinderGeometry(17, 17, 24, 48); bt.translate(-185, 12, 0); b.add(bt, M.marble);
      const bd = new THREE.SphereGeometry(13, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2); bd.scale(1, 1.4, 1); bd.translate(-185, 24, 0); b.add(bd, M.roof); }
    M.wall = lam("cityWall", () => ({ map: rep(stoneHD("wallStone", ["#c9a77e", "#bf9d74", "#d1b089", "#b5946b"], "#8a6e50"), 30, 2) }));
    b.add(boxGeo(V(-320, 0, 70), V(220, 11, 74), 6), M.wall);
    for (let x = -300; x <= 200; x += 60) b.add(boxGeo(V(x - 4, 0, 68), V(x + 4, 15, 76), 6), M.wall);
    for (let i = 0; i < 9; i++) { const x = -120 + i * 34 + rr() * 6; house(b, x, 92 + rr() * 10, Math.PI + (rr() - 0.5) * 0.2, 12, 9, 9 + rr() * 6, i % 3, 0); }
    for (let i = 0; i < 7; i++) { const x = 60 + i * 30; house(b, x, -110 - rr() * 10, (rr() - 0.5) * 0.2, 12, 9, 9 + rr() * 5, i % 3, 0); }
    for (let i = 0; i < 40; i++) { const x = -260 + rr() * 480, z = 80 + rr() * 60; prop(b, {}, i % 3 ? "tree_cone" : "tree_oak", x, 0, z, 9 + rr() * 8, rr() * 6); }
    for (let i = 0; i < 14; i++) { const x = 40 + rr() * 120, z = -70 - rr() * 30; prop(b, {}, "tree_oak", x, 0, z, 7 + rr() * 5, rr() * 6); }
    b.build(R);
    // stars (night)
    const sp: number[] = [];
    for (let i = 0; i < 900; i++) { const a = rr() * Math.PI * 2, e = 0.08 + rr() * 1.3; sp.push(Math.cos(a) * Math.cos(e) * 900, Math.sin(e) * 900, Math.sin(a) * Math.cos(e) * 900); }
    const sg = new THREE.BufferGeometry(); sg.setAttribute("position", new THREE.Float32BufferAttribute(sp, 3));
    this.stars = new THREE.Points(sg, new THREE.PointsMaterial({ color: "#eef3ff", size: 2.2, sizeAttenuation: false, fog: false, depthWrite: false }));
    this.stars.layers.set(NOINK); this.stars.frustumCulled = false; R.add(this.stars);

    // ---- the tower: a chain of floors, each a child of the one below (bend = per-floor tilt) ----
    const arcO = lam("arcadeOpen", () => ({ map: arcadeTex(false), side: THREE.DoubleSide })), arcB = lam("arcadeBlind", () => ({ map: arcadeTex(true) }));
    const core = lam("towerCore", () => ({ color: "#2f3146" })), cornice = lam("cornice", () => ({ color: "#ebe5d6" })), bell = lam("bronze", () => ({ color: "#9b6a35" }));
    let parent: THREE.Object3D = this.tower;
    FLOORS.forEach((fl, i) => {
      const g = new THREE.Group();
      const shell = new THREE.Mesh(floorGeo(fl.r, fl.h), fl.blind ? arcB : arcO); shell.castShadow = true; shell.receiveShadow = true; g.add(shell);
      (shell.material as THREE.MeshLambertMaterial).map!.repeat.set(fl.blind ? 2 : 3, 1);
      if (!fl.blind) { const c = new THREE.Mesh(floorGeo(fl.r - 1.6, fl.h), core); g.add(c); }
      const cn = new THREE.Mesh(corniceGeo(fl.r), cornice); cn.position.y = fl.h; cn.castShadow = true; g.add(cn);
      if (i === FLOORS.length - 1) { const bl = new THREE.Mesh(new THREE.SphereGeometry(1.4, 16, 10, 0, Math.PI * 2, 0, Math.PI * 0.55), bell); bl.rotation.x = Math.PI; bl.position.y = fl.h * 0.75; g.add(bl);
        const cap = new THREE.Mesh(new THREE.CylinderGeometry(fl.r + 0.3, fl.r + 0.3, 0.6, 48), cornice); cap.position.y = fl.h + 0.3; g.add(cap); }
      g.position.y = i === 0 ? 0 : FLOORS[i - 1].h + 0.27;
      g.userData.h = fl.h; parent.add(g); this.floors.push(g); parent = g;
    });
    R.add(this.tower);
    // vines (the century of war)
    this.vines = new THREE.Mesh(new THREE.CylinderGeometry(TOWER_R + 0.05, TOWER_R + 0.05, 9, 48, 1, true), new THREE.MeshLambertMaterial({ map: ctex("vines", 512, 256, (g, r) => { g.clearRect(0, 0, 512, 256); g.strokeStyle = "#3f7a33"; g.lineWidth = 5; for (let i = 0; i < 26; i++) { let x = r() * 512, y = 256; g.beginPath(); g.moveTo(x, y); for (let k = 0; k < 8; k++) { x += (r() - 0.5) * 30; y -= 14 + r() * 18; g.lineTo(x, y); } g.stroke(); g.fillStyle = "#5aa83c"; g.beginPath(); g.arc(x, y, 7, 0, 7); g.fill(); } }), transparent: true, alphaTest: 0.4 }));
    this.vines.position.y = 4.5; this.floors[0].add(this.vines);
    // scaffolding (the building years): poles + planks around the top floor
    const wood = lam("scaffWood", () => ({ color: "#a8784a" }));
    for (let k = 0; k < 12; k++) { const a = (k / 12) * Math.PI * 2, p = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 8, 6), wood); p.position.set(Math.cos(a) * (TOWER_R + 1.4), 4, Math.sin(a) * (TOWER_R + 1.4)); this.scaffold.add(p); }
    for (const y of [2.5, 5.5]) { const ring = new THREE.Mesh(new THREE.TorusGeometry(TOWER_R + 1.4, 0.08, 6, 48), wood); ring.rotation.x = Math.PI / 2; ring.position.y = y; this.scaffold.add(ring); }
    this.scaffold.traverse((o) => { (o as THREE.Mesh).castShadow = true; });
    // 1990s fix: steel cables round floor 2, lead block stack on the high side, drill rig + soil pile
    const steel = lam("steelCable", () => ({ color: "#5b6170" }));
    for (const y of [3, 5]) { const c = new THREE.Mesh(new THREE.TorusGeometry(TOWER_R + 0.15, 0.12, 8, 64), steel); c.rotation.x = Math.PI / 2; c.position.y = y; this.floors[1].add(c); this.cables.push(c); }
    const leadM = lam("leadBlocks", () => ({ color: "#6c707c" }));
    for (let i = 0; i < 9; i++) { const m = new THREE.Mesh(boxGeo(V(-1, 0, -0.5), V(1, 0.7, 0.5)), leadM); m.position.set(-TOWER_R - 2.2 - (i % 3) * 0.1, Math.floor(i / 3) * 0.72, -2.2 + (i % 3) * 2.2); m.castShadow = true; this.lead.add(m); }
    R.add(this.lead);
    const yel = lam("rigYellow", () => ({ color: "#f2b632" })), dark = lam("rigDark", () => ({ color: "#2f2d38" }));
    const base = new THREE.Mesh(boxGeo(V(-2, 0, -1.4), V(2, 1.4, 1.4)), yel); base.castShadow = true; this.rig.add(base);
    const mast = new THREE.Mesh(boxGeo(V(-0.25, 1.4, -0.25), V(0.25, 7.5, 0.25)), yel); mast.rotation.z = -0.5; mast.position.set(0.6, 0, 0); mast.castShadow = true; this.rig.add(mast);
    const drill = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 6, 8), dark); drill.rotation.z = -0.5 - Math.PI / 2 + Math.PI / 2; drill.position.set(2.2, 1.6, 0); drill.rotation.z = 1.07; this.rig.add(drill);
    this.rig.position.set(...RIG); this.rig.rotation.y = 0; R.add(this.rig);
    this.soil = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 10, 0, Math.PI * 2, 0, Math.PI / 2), lam("soilPile", () => ({ color: "#7a5a3a" })));
    this.soil.position.set(RIG[0] - 3.5, 0, RIG[2] - 2.5); this.soil.castShadow = true; R.add(this.soil);
    // barrier fence (closed)
    const red = lam("fenceRed", () => ({ color: "#d8433a" })), white = lam("fenceWhite", () => ({ color: "#f3efe6" }));
    for (let k = 0; k < 8; k++) { const x = -9 + k * 2.6; const p = new THREE.Mesh(boxGeo(V(-0.06, 0, -0.06), V(0.06, 1.1, 0.06)), white); p.position.set(x, 0, -17); this.fence.add(p); }
    for (let k = 0; k < 7; k++) { const bar = new THREE.Mesh(boxGeo(V(0, 0.75, -0.04), V(2.6, 0.95, 0.04)), k % 2 ? white : red); bar.position.set(-9 + k * 2.6, 0, -17); bar.castShadow = true; this.fence.add(bar); }
    R.add(this.fence);
    // the mattress (explanation demo): a soft slab that dents under the kid's weight
    this.mattressG = new THREE.BoxGeometry(2.2, 0.5, 3.2, 24, 2, 24); this.mattressG.translate(0, 0.25, 0);
    this.mattressBase = (this.mattressG.attributes.position.array as Float32Array).slice();
    this.mattress = new THREE.Mesh(this.mattressG, lam("mattressM", () => ({ map: ctex("ticking", 256, 256, (g) => { g.fillStyle = "#f2efe8"; g.fillRect(0, 0, 256, 256); g.fillStyle = "#7d9cc9"; for (let x = 0; x < 256; x += 32) g.fillRect(x, 0, 10, 256); }) })));
    this.mattress.position.set(...MATTRESS); this.mattress.castShadow = true; this.mattress.receiveShadow = true; R.add(this.mattress);
  }

  /** camera-relative sun, frozen per shot */
  private shotSun(id: number, s: ShotDef, L: LightPreset): THREE.Vector3 {
    // one world sun per light, so flown transitions never jump: afternoon sun from the land side, camera-left of the
    // usual view (+z), so the whale's flank and the faces facing the sea side are lit; night: the lot's moon for both
    if (s.light === "golden") return (this.sunCache.get(-1) ?? this.sunCache.set(-1, new THREE.Vector3(0.55, 0.5, -0.65).normalize()).get(-1))!;
    let v = this.sunCache.get(id);
    if (v) return v;
    let fx = 0, fz = 0;
    for (let f = s.a; f < (id === 1 ? 66 : s.b); f += 3) {
      const c = camAt(id, f), x = c.look[0] - c.pos[0], z = c.look[2] - c.pos[2], n = Math.hypot(x, z) || 1;
      fx += x / n; fz += z / n;
    }
    const n = Math.hypot(fx, fz) || 1; fx /= n; fz /= n;
    const az = THREE.MathUtils.degToRad(s.sunAz ?? L.az), el = THREE.MathUtils.degToRad(s.sunEl ?? L.el);
    const hx = fx * Math.cos(az) - fz * Math.sin(az), hz = fz * Math.cos(az) + fx * Math.sin(az);
    v = new THREE.Vector3(hx * Math.cos(el), Math.sin(el), hz * Math.cos(el)).normalize();
    this.sunCache.set(id, v);
    return v;
  }
  private actor(i: number) { while (this.actors.length <= i) this.actors.push(new Actor(this.root)); return this.actors[i]; }
  private fx(i: number) { while (this.fxs.length <= i) this.fxs.push(new Fx(this.root)); return this.fxs[i]; }

  update(id: number, f: number, cam: THREE.PerspectiveCamera, scene: THREE.Scene) {
    const t = f / FPS, s = SHOTS[id - 1], tau = s.tau(t), L = LIGHTS[s.light];
    const c = camAt(id, f), qk = kickAt(t);
    cam.position.set(...c.pos); cam.up.set(0, 1, 0); cam.lookAt(...c.look); cam.rotateZ(c.roll);
    cam.fov = c.fov; cam.near = 0.2; cam.far = 1500; cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    const focus = V(...c.look), dist = cam.position.distanceTo(focus);
    cam.layers.enable(NOINK);
    void qk;
    // ---- light rig ----
    const K = LOOK[s.light], sunDir = this.shotSun(id, s, L);
    this.hemi.color.set(L.sky); this.hemi.groundColor.set(L.ground); this.hemi.intensity = L.hemiI;
    this.sun.color.set(L.sunCol); this.sun.intensity = L.sunI;
    let Rr = THREE.MathUtils.clamp(dist * 1.15 + 7, 12, 95);
    if (s.light === "golden") Rr = Math.max(Rr, 30);
    this.sun.position.copy(focus).addScaledVector(sunDir, 220); this.sun.target.position.copy(focus);
    const sc = this.sun.shadow.camera;
    sc.left = -Rr; sc.right = Rr; sc.top = Rr; sc.bottom = -Rr; sc.near = 20; sc.far = 480; sc.updateProjectionMatrix();
    this.sun.shadow.bias = L.bias; this.sun.shadow.normalBias = L.normalBias * (Rr / 12);
    TONE.uLitCol.value.set(...L.lit); TONE.uShadeCol.value.set(...L.shade); TONE.uShadeLift.value.set(...L.lift);
    TONE.uLambert.value = L.lambert; TONE.uSideK.value = L.sideK; TONE.uTerm.value = L.term; TONE.uBounce.value.set(...K.bounce); TONE.uSat.value = K.sat;
    CHAR.uCharTint.value.set(...L.charTint); CHAR.uCharShade.value = L.charShade; CHAR.uGrad.value = L.charGrad;
    CHAR.uBodyGrad.value = L.bodyGrad; CHAR.uSideTint.value.set(...L.sideTint);
    // ---- sky, fog, sun disc, clouds ----
    const su = this.skyMat.uniforms;
    K.sky.c.forEach((h, i) => untone(h, su["c" + i].value));
    const e = K.sky.e.map((deg) => THREE.MathUtils.degToRad(deg));
    su.e.value.set(e[1], e[2], e[3], e[4]);
    this.sky.position.copy(cam.position);
    untone(L.fog, this.fog.color); this.fog.near = L.fogNear; this.fog.far = L.fogFar;
    scene.fog = this.fog; scene.background = null;
    const showSun = s.light === "golden";
    this.sunDisc.visible = this.sunHalo.visible = showSun;
    if (showSun) {
      this.sunDisc.position.copy(cam.position).addScaledVector(sunDir, 900);
      this.sunDisc.scale.setScalar(2 * 900 * Math.tan(THREE.MathUtils.degToRad(1.7)));
      this.sunHalo.position.copy(this.sunDisc.position); this.sunHalo.scale.setScalar(2 * 900 * Math.tan(THREE.MathUtils.degToRad(24)));
      (this.sunHalo.material as THREE.SpriteMaterial).color.set(L.sunDisc).multiplyScalar(1.3);
    }
    for (let i = 0; i < this.clouds.length; i++) {
      const m = this.clouds[i];
      m.lookAt(cam.position.x, m.position.y, cam.position.z);
      (m.material as THREE.MeshBasicMaterial).map = this.cloudMaps[s.light][i % 4];
    }
    const night = s.light === "night";
    this.stars.visible = night; this.stars.position.copy(cam.position);
    // ---- the tower: floors standing, lean of the base, bend of the later floors, sinking, quake wobble ----
    const nf = floorsAt(s.scene, tau), lean = THREE.MathUtils.degToRad(leanAt(s.scene, tau));
    const quake = tau > QUAKE && tau < QUAKE_END && s.scene === "quake" ? Math.sin((tau - QUAKE) * 19) * 0.006 * Math.sin(Math.PI * (tau - QUAKE) / (QUAKE_END - QUAKE)) : 0;
    this.tower.position.set(0, -sinkAt(tau), 0); this.tower.rotation.set(0, 0, -(lean + quake));
    this.floors.forEach((g, i) => {
      const k = Math.max(0, Math.min(1, nf - i)); g.visible = k > 0.001;
      g.scale.set(1, Math.max(0.001, k), 1);
      // floors 4-8 built taller on the short side: each tilts back a little against the lean (the banana)
      g.rotation.z = i >= 3 ? 0.22 * lean * Math.min(1, (i - 2) / 2) : 0;
    });
    const building = tau < 26 && s.scene !== "hook" && s.scene !== "war" && s.scene !== "back";
    this.scaffold.visible = building; if (building) { const top = Math.max(0, Math.floor(nf - 0.001)); this.scaffold.removeFromParent(); this.floors[top].add(this.scaffold); }
    this.vines.visible = s.scene === "back";
    const fixing = tau > 37.5 && tau < 50 && (s.scene === "fix" || s.scene === "works");
    this.cables.forEach((c) => (c.visible = fixing)); this.lead.visible = fixing; this.rig.visible = fixing;
    this.soil.visible = fixing; this.soil.scale.set(1.6, 0.4 + 1.1 * smooth((tau - 39.5) / 4), 1.6);
    this.fence.visible = tau > 36.6 && tau < 50 && s.scene !== "pose" && s.scene !== "quake";
    // mattress dent under the kid's weight shifting to one foot
    { const p = this.mattressG.attributes.position as THREE.BufferAttribute, b0 = this.mattressBase, lean1 = smooth((tau - 30.3) / 0.8) * (tau < 34 ? 1 : 0);
      for (let i = 0; i < p.count; i++) { const x = b0[i * 3], y = b0[i * 3 + 1], z = b0[i * 3 + 2];
        const cx = -0.35 * lean1, d = Math.hypot(x - cx, z) / 0.9, dent = (0.12 + 0.2 * lean1) * Math.exp(-d * d) * (y / 0.5);
        p.setY(i, y - dent); }
      p.needsUpdate = true; this.mattressG.computeVertexNormals(); this.mattress.visible = s.scene === "mattress"; }
    // ---- cast + effects ----
    const right = V(0, 0, 0).setFromMatrixColumn(cam.matrixWorld, 0);
    const st = stage(id, f, t, tau, { pos: cam.position, right, sun: sunDir });
    this.frustum.setFromProjectionMatrix(this.m4.multiplyMatrices(cam.projectionMatrix, cam.matrixWorldInverse));
    let ai = 0;
    const used: Actor[] = [];
    for (const p of st.places) {
      const sc2 = p.scale ?? 1;
      if (!this.frustum.intersectsSphere(this.sph.set(this.v.set(p.x, p.y + 1.1 * sc2, p.z), 3.5))) continue;
      // nobody half-cut at the frame edge: a card closer than 4.5 m that sits off the view axis (> 9 deg) is left out
      {
        // sideways angle only (the shot's subject sits near the vertical centre line, e.g. the hook close-up looks up past him)
        const hx = p.x - cam.position.x, hz = p.z - cam.position.z, hd = Math.hypot(hx, hz);
        cam.getWorldDirection(this.fwd); const fl = Math.hypot(this.fwd.x, this.fwd.z) || 1;
        if (hd < 4.5 && (hx * this.fwd.x + hz * this.fwd.z) / (hd * fl) < Math.cos((9 * Math.PI) / 180)) continue;
      }
      const ac = this.actor(ai++);
      const [w, h, k] = p.size ?? [300, 500, 0.5];
      ac.r = this.pool.req(p.key, w, h, k, p.draw);
      ac.mesh.visible = true;
      ac.mesh.position.set(p.x, p.y, p.z);
      ac.mesh.rotation.set(0, p.yaw ?? Math.atan2(cam.position.x - p.x, cam.position.z - p.z), p.roll ?? 0);
      ac.mesh.scale.set(p.mirror ? -sc2 : sc2, sc2, sc2);
      ac.mesh.castShadow = L.actorShadow;
      used.push(ac);
    }
    for (let i = ai; i < this.actors.length; i++) this.actors[i].mesh.visible = false;
    let fi = 0;
    const fused: Fx[] = [];
    for (const p of st.fx) {
      if (!this.frustum.intersectsSphere(this.sph.set(this.v.set(p.x, p.y, p.z), Math.max(p.w, p.h)))) continue;
      const fe = this.fx(fi++);
      fe.r = this.pool.req(p.key, p.cw, p.ch, 1, p.draw);
      fe.use(!!p.soft);
      fe.mesh.visible = true;
      fe.mesh.position.set(p.x, p.y, p.z);
      if (p.flat) fe.mesh.rotation.set(-Math.PI / 2, 0, p.rot ?? 0);
      else { fe.mesh.quaternion.copy(cam.quaternion); fe.mesh.rotateZ(p.rot ?? 0); }
      fe.mesh.scale.set(p.w, p.h, 1);
      fused.push(fe);
    }
    for (let i = fi; i < this.fxs.length; i++) this.fxs[i].mesh.visible = false;
    this.pool.flush();
    for (const ac of used) ac.bind();
    for (const fe of fused) fe.bind();
    return focus;
  }
}
