// The whole place as one three.js scene: sky, sea with surf, beach, dunes with beach grass, the parking lot on the
// plateau with 1970s cars, pines and a headland, the whale (intact / blown open / buried), the dynamite cases, the
// plunger box, the TV camera, the tow truck, the bulldozer, falling 3D chunks and the cast.
// update(id, f, camera) poses everything for shot `id` at frame f (pure function of id + f).
import * as THREE from "three";
import { Batch, V, lam, boxGeo, prop, house, Kit } from "./build";
import { rep, ctex, rng, waterNear, waterFar, cloudHD, stoneHD } from "./paint";
import { Pen } from "./toon";
import { LIGHTS, LOOK, LightPreset } from "./lights";
import { TONE, CHAR, LFB, twoTone, untone } from "./shade";
import { NOINK } from "./ink";
import { Pool, Actor, Fx, stage } from "./cast";
import { fxFoam } from "./fx70";
import {
  FPS, SHOTS, H, SEA_Y, LOT_Y, WHALE, WHALE_LEN, PLUNGER, TVCAM, TRUCK_HITCH, UCAR, BOOM, CRUSH, camAt, V3, smooth, clamp01, ShotDef,
} from "./story";

export const loadKit = () => Promise.resolve({} as Kit);

// ---------------- painted textures ----------------
const sandHD = () => ctex("sandHD", 1024, 1024, (g, r) => {
  const S = 1024;
  g.fillStyle = "#ead6a6"; g.fillRect(0, 0, S, S);
  for (let i = 0; i < 18; i++) {
    const x = r() * S, y = r() * S, rad = 120 + r() * 220, light = r() > 0.5;
    for (const ox of [-S, 0, S]) for (const oy of [-S, 0, S]) {
      const gr = g.createRadialGradient(x + ox, y + oy, 0, x + ox, y + oy, rad);
      gr.addColorStop(0, light ? "rgba(248,232,190,0.18)" : "rgba(214,188,140,0.16)"); gr.addColorStop(1, "rgba(0,0,0,0)");
      g.fillStyle = gr; g.fillRect(x + ox - rad, y + oy - rad, rad * 2, rad * 2);
    }
  }
  g.lineCap = "round";
  for (let i = 0; i < 140; i++) { // wind ripples
    const x = r() * S, y = r() * S, l = 30 + r() * 70;
    g.strokeStyle = "rgba(190,160,110,0.35)"; g.lineWidth = 2.2;
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + l / 2, y - 6, x + l, y); g.stroke();
  }
  for (let i = 0; i < 2200; i++) { const x = r() * S, y = r() * S; g.fillStyle = r() < 0.5 ? "rgba(150,120,80,0.35)" : "rgba(255,250,235,0.5)"; g.fillRect(x, y, 2, 2); }
});
const asphaltHD = () => ctex("asphaltHD", 1024, 1024, (g, r) => {
  g.fillStyle = "#6b6a72"; g.fillRect(0, 0, 1024, 1024);
  for (let i = 0; i < 4000; i++) { g.fillStyle = r() < 0.5 ? "rgba(40,40,50,0.35)" : "rgba(170,170,180,0.3)"; g.fillRect(r() * 1024, r() * 1024, 3, 3); }
  g.strokeStyle = "rgba(40,36,48,0.6)"; g.lineWidth = 3;
  for (let i = 0; i < 6; i++) { let x = r() * 1024, y = r() * 1024; g.beginPath(); g.moveTo(x, y); for (let k = 0; k < 6; k++) { x += (r() - 0.5) * 120; y += (r() - 0.5) * 120; g.lineTo(x, y); } g.stroke(); }
});
/** sperm whale skin: dark slate with long wrinkles, a paler belly (u around the body, v along it) */
const whaleTex = () => ctex("whaleSkin", 1024, 1024, (g, r) => {
  const gr = g.createLinearGradient(0, 0, 1024, 0);
  gr.addColorStop(0, "#9aa0ae"); gr.addColorStop(0.18, "#626a7e"); gr.addColorStop(0.5, "#545b6e"); gr.addColorStop(0.82, "#626a7e"); gr.addColorStop(1, "#9aa0ae");
  g.fillStyle = gr; g.fillRect(0, 0, 1024, 1024);
  g.lineCap = "round";
  for (let i = 0; i < 260; i++) {
    const x = r() * 1024, y = r() * 1024, l = 40 + r() * 160;
    g.strokeStyle = r() < 0.6 ? "rgba(40,44,60,0.45)" : "rgba(170,176,192,0.35)"; g.lineWidth = 2 + r() * 2;
    g.beginPath(); g.moveTo(x, y); g.bezierCurveTo(x + 10, y + l * 0.3, x - 10, y + l * 0.6, x + 4, y + l); g.stroke();
  }
  for (let i = 0; i < 40; i++) { g.fillStyle = "rgba(235,235,240,0.5)"; g.beginPath(); g.ellipse(r() * 1024, r() * 1024, 6 + r() * 10, 2 + r() * 3, r() * 3, 0, 6.3); g.fill(); }
});
const crateTex = () => ctex("crate", 256, 256, (g) => {
  g.fillStyle = "#b8392c"; g.fillRect(0, 0, 256, 256);
  g.fillStyle = "#8d2a22"; for (let i = 0; i < 4; i++) g.fillRect(0, i * 64 + 60, 256, 4);
  g.fillStyle = "#f2e6c4"; g.fillRect(40, 96, 176, 64);
  g.fillStyle = "#2a2230"; for (let i = 0; i < 5; i++) g.fillRect(58 + i * 30, 112, 18, 32);
  g.strokeStyle = "#5a1e1a"; g.lineWidth = 8; g.strokeRect(4, 4, 248, 248);
});
const foamTex = (seed: number) => ctex("foam" + seed, 1024, 64, (g) => fxFoam(new Pen(g), seed));

// ---------------- geometry helpers ----------------
const quadUp = (x0: number, x1: number, z0: number, z1: number, y: number, u: number, v: number) => {
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute([x0, y, z1, x1, y, z1, x1, y, z0, x0, y, z1, x1, y, z0, x0, y, z0], 3));
  g.setAttribute("normal", new THREE.Float32BufferAttribute(Array(6).fill([0, 1, 0]).flat(), 3));
  g.setAttribute("uv", new THREE.Float32BufferAttribute([0, 0, u, 0, u, v, 0, 0, u, v, 0, v], 2));
  return g;
};
/** displaced ground mesh with vertex tints: dry sand, wet sand at the shore, olive dune grass on the plateau */
const groundGeo = () => {
  const W = 520, D = 300, nx = 260, nz = 170;
  const g = new THREE.PlaneGeometry(W, D, nx, nz); g.rotateX(-Math.PI / 2); g.translate(0, 0, -D / 2 + 30);
  const p = g.attributes.position as THREE.BufferAttribute, col: number[] = [], uv = g.attributes.uv as THREE.BufferAttribute;
  const wet = new THREE.Color("#d9c49a"), dry = new THREE.Color("#ffffff"), olive = new THREE.Color("#a9ad6a"), c = new THREE.Color();
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), z = p.getZ(i), y = H(x, z);
    p.setY(i, y);
    uv.setXY(i, x / 9, z / 9);
    c.copy(dry);
    if (z > 5) c.lerp(wet, smooth((z - 5) / 6));
    const inLot = x > -28 && x < 24 && z < -59 && z > -84;
    if (z < -40 && !inLot) c.lerp(olive, smooth((-40 - z) / 14) * 0.85);
    col.push(c.r, c.g, c.b);
  }
  g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
  g.computeVertexNormals();
  return g;
};
/** sperm whale lying on its side along x (tail at -x), base on the sand */
const whaleGeo = () => {
  const pts: THREE.Vector2[] = [];
  for (let i = 0; i <= 40; i++) {
    const s = i / 40;
    let r = s < 0.14 ? 0.22 + (s / 0.14) * 0.55 : s < 0.55 ? 0.77 + ((s - 0.14) / 0.41) * 0.68 : 1.45 + ((s - 0.55) / 0.4) * 0.12;
    if (s > 0.95) r = 1.57 * Math.sqrt(Math.max(0, 1 - ((s - 0.95) / 0.05) ** 2));
    if (i === 0) r = 0.05;
    pts.push(new THREE.Vector2(Math.max(0.001, r), (s - 0.5) * WHALE_LEN));
  }
  const g = new THREE.LatheGeometry(pts, 36);
  g.rotateZ(-Math.PI / 2); // lathe axis y -> x, head at +x
  g.scale(1, 0.82, 1);
  return g;
};
const flukeGeo = () => {
  const s = new THREE.Shape();
  s.moveTo(0, 0); s.quadraticCurveTo(-0.9, 1.3, -2.0, 2.1); s.quadraticCurveTo(-1.2, 0.9, -1.0, 0); s.quadraticCurveTo(-1.2, -0.9, -2.0, -2.1); s.quadraticCurveTo(-0.9, -1.3, 0, 0);
  const g = new THREE.ExtrudeGeometry(s, { depth: 0.14, bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.05, bevelSegments: 2 });
  g.translate(0, 0, -0.07);
  return g;
};
/** a lumpy blubber chunk (3D): pink inside, grey skin on top (vertex colours) */
const chunkGeo = (seed: number, r = 1) => {
  const g = new THREE.IcosahedronGeometry(r, 2), p = g.attributes.position as THREE.BufferAttribute, rr = rng(seed), col: number[] = [];
  const k = [rr() * 6, rr() * 6, rr() * 6];
  for (let i = 0; i < p.count; i++) {
    const v = V(p.getX(i), p.getY(i), p.getZ(i)), n = v.clone().normalize();
    const d = 1 + 0.22 * Math.sin(n.x * 3 + k[0]) * Math.sin(n.y * 3 + k[1]) + 0.12 * Math.sin(n.z * 5 + k[2]);
    v.multiplyScalar(d); v.y *= 0.62; p.setXYZ(i, v.x, v.y, v.z);
    const skin = n.x * 0.8 + n.y * 0.6 > 0.55 ? 1 : 0;
    const c = new THREE.Color(skin ? "#5d6476" : "#f0c9bb");
    col.push(c.r, c.g, c.b);
  }
  g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
  g.computeVertexNormals();
  return g;
};
const rockGeo = (seed: number, sx: number, sy: number, sz: number) => {
  const g = new THREE.IcosahedronGeometry(1, 3), p = g.attributes.position as THREE.BufferAttribute, rr = rng(seed), k = [rr() * 6, rr() * 6, rr() * 6];
  for (let i = 0; i < p.count; i++) {
    const v = V(p.getX(i), p.getY(i), p.getZ(i)), n = v.clone().normalize();
    v.multiplyScalar(1 + 0.18 * Math.sin(n.x * 4 + k[0]) * Math.sin(n.z * 4 + k[1]) + 0.08 * Math.sin(n.y * 9 + k[2]));
    p.setXYZ(i, v.x * sx, v.y * sy, v.z * sz);
  }
  g.computeVertexNormals();
  return g;
};
const cyl = (r: number, h: number, n = 14) => new THREE.CylinderGeometry(r, r, h, n);
/** 1970s sedan facing +z (nose), base on y = 0; returns the group and the cabin + roof (for the crush) */
const sedan = (col: string) => {
  const grp = new THREE.Group(), body = lam("car" + col, () => ({ color: col }));
  const glass = lam("carGlass", () => ({ color: "#a8c4dc" })), chrome = lam("chrome", () => ({ color: "#d7dbe0" })), tyre = lam("tyre", () => ({ color: "#2b2a33" }));
  const add = (g: THREE.BufferGeometry, m: THREE.Material, parent: THREE.Object3D = grp) => { const me = new THREE.Mesh(g, m); me.castShadow = true; me.receiveShadow = true; parent.add(me); return me; };
  add(boxGeo(V(-0.95, 0.32, -2.5), V(0.95, 1.0, 2.5)), body);
  add(boxGeo(V(-1.0, 0.3, 2.45), V(1.0, 0.5, 2.62)), chrome);
  add(boxGeo(V(-1.0, 0.3, -2.62), V(1.0, 0.5, -2.45)), chrome);
  const cabin = new THREE.Group(); cabin.position.y = 1.0; grp.add(cabin);
  add(boxGeo(V(-0.86, 0, -1.25), V(0.86, 0.56, 1.0)), glass, cabin);
  add(boxGeo(V(-0.9, 0.56, -1.3), V(0.9, 0.66, 1.05)), body, cabin);
  for (const x of [-0.86, 0.86]) for (const z of [-1.2, 0.95]) add(boxGeo(V(x - 0.05, 0, z - 0.06), V(x + 0.05, 0.57, z + 0.06)), body, cabin);
  for (const x of [-0.92, 0.92]) for (const z of [-1.55, 1.6]) { const w = add(cyl(0.34, 0.26), tyre); w.rotation.z = Math.PI / 2; w.position.set(x, 0.34, z); }
  for (const x of [-0.6, 0.6]) { const l = add(cyl(0.12, 0.05), lam("lamp", () => ({ color: "#fff6d8" }))); l.rotation.x = Math.PI / 2; l.position.set(x, 0.75, 2.52); }
  return { grp, cabin };
};

type Mats = Record<string, THREE.Material>;
const smokeTex = () => ctex("smoke", 256, 256, (g) => { const p = new Pen(g); p.ell(128, 128, 110, 95, "#efe6d6", 0); });

export class World {
  root = new THREE.Group();
  private pool = new Pool();
  private actors: Actor[] = [];
  private fxs: Fx[] = [];
  private hemi: THREE.HemisphereLight; private sun: THREE.DirectionalLight;
  private sky: THREE.Mesh; private skyMat: THREE.ShaderMaterial;
  private fog = new THREE.Fog("#bccbec", 25, 420);
  private WU: Record<string, THREE.IUniform>;
  private sunDisc: THREE.Sprite; private sunHalo: THREE.Sprite;
  private sunCache = new Map<number, THREE.Vector3>();
  private cloudMaps: Record<"day" | "golden", THREE.Texture[]>;
  private clouds: THREE.Mesh[] = [];
  private foam: THREE.Mesh[] = [];
  private whale = new THREE.Group(); private remains = new THREE.Group(); private crater: THREE.Mesh;
  private cases: THREE.Mesh[] = [];
  private handle = new THREE.Group();
  private truck = new THREE.Group(); private rope: THREE.Mesh;
  private dozer = new THREE.Group(); private mound: THREE.Mesh;
  private ucabin: THREE.Group; private ucar: THREE.Group;
  private bigChunk: THREE.Mesh;
  private frustum = new THREE.Frustum();
  private m4 = new THREE.Matrix4(); private v = new THREE.Vector3(); private sph = new THREE.Sphere();

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
    this.cloudMaps = { day: [0, 1, 2, 3].map((k) => cloudHD(k, LOOK.day.cloud)), golden: [0, 1, 2, 3].map((k) => cloudHD(k, LOOK.golden.cloud)) };
    for (let i = 0; i < 10; i++) {
      const a = (i / 10) * Math.PI * 2 + 0.3, d = 600 + (i % 3) * 70;
      const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: this.cloudMaps.day[i % 4], color: new THREE.Color(1.1, 1.1, 1.1), transparent: true, depthWrite: false, fog: false }));
      const w = 140 + (i % 4) * 30;
      m.position.set(Math.cos(a) * d, 110 + (i % 4) * 36, Math.sin(a) * d); m.scale.set(w, w / 2, 1);
      m.layers.set(NOINK); this.clouds.push(m); R.add(m);
    }

    // ---- static world ----
    const b = new Batch();
    const sandMap = rep(sandHD(), 1, 1); sandMap.anisotropy = 16;
    M.ground = lam("ground", () => ({ map: sandMap, vertexColors: true }));
    const gm = new THREE.Mesh(groundGeo(), M.ground); gm.receiveShadow = true; gm.castShadow = true; R.add(gm);
    M.asphalt = lam("asphalt", () => ({ map: rep(asphaltHD(), 1, 1) }));
    const lot = quadUp(-26, 22, -82, -60, LOT_Y + 0.03, 6, 3); b.add(lot, M.asphalt);
    M.paint = lam("lotPaint", () => ({ color: "#f3efe2" }));
    for (let x = -24; x <= 20; x += 3.2) b.add(boxGeo(V(x - 0.06, LOT_Y + 0.03, -71.5), V(x + 0.06, LOT_Y + 0.045, -66)), M.paint);
    M.wood = lam("woodPost", () => ({ color: "#8a6a4a" }));
    for (let x = -26; x <= 22; x += 2.4) b.add(boxGeo(V(x - 0.08, LOT_Y, -59.6), V(x + 0.08, LOT_Y + 0.75, -59.4)), M.wood);
    b.add(boxGeo(V(-26, LOT_Y + 0.6, -59.6), V(22, LOT_Y + 0.7, -59.45)), M.wood);
    // beach grass clumps on the dunes: tufts of thin blades
    M.grass = lam("beachGrass", () => ({ color: "#8f9a4a" }));
    M.grass2 = lam("beachGrass2", () => ({ color: "#a7a85a" }));
    const blade = new THREE.ConeGeometry(0.05, 1, 4); blade.translate(0, 0.5, 0);
    const rr = rng(77);
    for (let i = 0; i < 700; i++) {
      const x = -90 + rr() * 180, z = -21 - rr() * 70;
      if (z < -57 && z > -86 && x > -30 && x < 26) continue;
      if (z > -33 && Math.abs(x) < 12) continue; // the crowd's patch stays clear
      const y = H(x, z), n = 5 + Math.floor(rr() * 4), hgt = 0.5 + rr() * 0.6;
      for (let k = 0; k < n; k++) {
        const a = rr() * Math.PI * 2, lean = 0.15 + rr() * 0.35;
        const m = new THREE.Matrix4().compose(V(x + Math.cos(a) * 0.12, y - 0.05, z + Math.sin(a) * 0.12),
          new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.sin(a) * lean, 0, -Math.cos(a) * lean)), V(1, hgt * (0.7 + rr() * 0.5), 1));
        b.add(blade, k % 3 ? M.grass : M.grass2, m);
      }
    }
    // driftwood logs on the beach
    M.drift = lam("drift", () => ({ color: "#b9a588" }));
    for (const [x, z, l, a] of [[-18, -8, 5, 0.3], [16, -11, 4, -0.5], [24, -4, 6, 0.1], [-26, -15, 3.5, 1.2], [-9, -17, 3, 0.7]] as const) {
      const g = cyl(0.22, l, 10); g.rotateZ(Math.PI / 2); g.rotateY(a); g.translate(x, 0.15, z); b.add(g, M.drift);
    }
    // pines on the plateau and the headland
    for (let i = 0; i < 70; i++) {
      const x = -140 + rr() * 280, z = -90 - rr() * 60;
      prop(b, {}, "tree_cone", x, H(x, z) - 0.2, z, 9 + rr() * 8, rr() * 6);
    }
    for (let i = 0; i < 26; i++) {
      const x = -30 + rr() * 60, z = -84 + rr() * 22;
      if (x > -30 && x < 26 && z > -84) { if (z > -86 && z < -58) continue; }
      prop(b, {}, "tree_cone", x, H(x, z) - 0.2, z, 7 + rr() * 6, rr() * 6);
    }
    // little shingle houses behind the lot
    for (const [x, z, yaw, si] of [[-22, -96, 0.2, 0], [-6, -100, -0.1, 1], [12, -97, 0.15, 2]] as const) house(b, x, z, yaw, 8, 7, 5.5, si, H(x, z));
    // headland (right of the beach seen from the dunes) and sea stacks
    M.rock = lam("rock", () => ({ map: rep(stoneHD("rockHD", ["#8b8783", "#7f7b78", "#96918c", "#77736f"], "#5f5b58"), 3, 3) }));
    b.add(rockGeo(5, 70, 34, 90), M.rock, new THREE.Matrix4().makeTranslation(-150, -6, 40));
    for (let i = 0; i < 18; i++) { const x = -150 + rr() * 50, z = 0 + rr() * 80; prop(b, {}, "tree_cone", x, 22 + rr() * 6, z, 9 + rr() * 6, rr() * 6); }
    for (const [x, z, s] of [[60, 120, 1], [95, 150, 0.7], [-60, 170, 1.3], [-95, 95, 0.8]] as const)
      b.add(rockGeo(x * 3 + z, 9 * s, 22 * s, 9 * s), M.rock, new THREE.Matrix4().makeTranslation(x, 4 * s, z));
    b.build(R);

    // ---- sea (the river shader of the bridge short, on open water) ----
    const wNear = waterNear(), wFar = waterFar();
    for (const t of [wNear, wFar]) { t.colorSpace = THREE.NoColorSpace; t.anisotropy = 16; t.needsUpdate = true; }
    this.WU = {
      wNearC: { value: new THREE.Color() }, wMidC: { value: new THREE.Color() }, wFarC: { value: new THREE.Color() },
      wCrest: { value: new THREE.Color() }, wTrough: { value: new THREE.Color() }, wGlint: { value: new THREE.Color() },
      wShade: { value: new THREE.Vector3(0.5, 0.56, 0.72) }, wNearTex: { value: wNear }, wFarTex: { value: wFar }, wTime: { value: 0 },
    };
    const waterM = new THREE.MeshLambertMaterial({ color: 0xffffff });
    waterM.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, this.WU);
      sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nvarying vec3 vWP;")
        .replace("#include <project_vertex>", "#include <project_vertex>\nvWP = (modelMatrix * vec4(transformed, 1.0)).xyz;");
      sh.fragmentShader = sh.fragmentShader.replace("#include <common>", WATER_DECL).replace("#include <map_fragment>", WATER_COL)
        .replace("#include <lights_fragment_begin>", "float sunVis = 1.0;\n" + LFB)
        .replace("#include <lights_fragment_end>", "#include <lights_fragment_end>\n  reflectedLight.directDiffuse = diffuseColor.rgb * mix(wShade, vec3(1.0), sunVis);\n  reflectedLight.indirectDiffuse = vec3(0.0);");
    };
    waterM.customProgramCacheKey = () => "sea1";
    const wm = new THREE.Mesh(quadUp(-900, 900, 9, 900, SEA_Y, 1, 1), waterM); wm.receiveShadow = true; R.add(wm);
    for (let i = 0; i < 4; i++) {
      const fm = new THREE.Mesh(new THREE.PlaneGeometry(260, 0.9), new THREE.MeshBasicMaterial({ map: rep(foamTex(i), 10, 1), transparent: true, depthWrite: false, opacity: 0.8 }));
      fm.rotation.x = -Math.PI / 2; fm.layers.set(NOINK); fm.renderOrder = 2; this.foam.push(fm); R.add(fm);
    }

    // ---- the whale ----
    const skin = lam("whaleSkin", () => ({ map: whaleTex() }));
    const body = new THREE.Mesh(whaleGeo(), skin); body.castShadow = true; body.receiveShadow = true; this.whale.add(body);
    const fl = new THREE.Mesh(flukeGeo(), lam("fluke", () => ({ color: "#5a6174" }))); fl.position.set(-WHALE_LEN / 2 + 0.2, 0, 0); fl.rotation.x = 0.25; fl.castShadow = true; this.whale.add(fl);
    const fin = new THREE.Mesh(rockGeo(9, 0.9, 0.15, 0.45), lam("fluke", () => ({}))); fin.position.set(3.0, 0.6, -0.95); fin.rotation.set(0.6, 0.4, 0.3); this.whale.add(fin);
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.11, 12, 8), lam("whaleEye", () => ({ color: "#1d1a24" }))); eye.position.set(5.6, -0.15, -1.18); this.whale.add(eye);
    const jaw = new THREE.Mesh(boxGeo(V(1.8, -0.06, -0.02), V(6.9, 0.06, 0.02)), lam("whaleEye", () => ({}))); jaw.position.set(0, -0.62, -1.12); jaw.rotation.y = -0.06; this.whale.add(jaw);
    this.whale.position.set(WHALE[0], 1.12, WHALE[2]);
    R.add(this.whale);
    // what is left after the blast: the whale lower and torn, a raw crater, big hunks around
    const rem = new THREE.Mesh(whaleGeo(), skin); rem.scale.set(0.95, 0.85, 0.97); rem.castShadow = true; rem.receiveShadow = true; this.remains.add(rem);
    const raw = lam("blubber", () => ({ vertexColors: true }));
    this.crater = new THREE.Mesh(chunkGeo(4, 1), raw); this.crater.scale.set(3.0, 0.75, 1.15); this.crater.position.set(-0.4, 0.95, -0.35); this.remains.add(this.crater);
    const rr2 = rng(31);
    for (let i = 0; i < 14; i++) {
      const c = new THREE.Mesh(chunkGeo(100 + i, 0.3 + rr2() * 0.5), raw);
      const a = rr2() * Math.PI * 2, d = 3 + rr2() * 9;
      c.position.set(Math.cos(a) * d * 1.3, -0.9, Math.sin(a) * d - 1.5); c.rotation.y = rr2() * 6; c.castShadow = true; this.remains.add(c);
    }
    this.remains.position.copy(this.whale.position); this.remains.visible = false;
    R.add(this.remains);
    // dynamite cases against the landward side, under the whale
    const crate = lam("crate", () => ({ map: crateTex() }));
    const cg = boxGeo(V(-0.3, 0, -0.18), V(0.3, 0.34, 0.18));
    for (let i = 0; i < 20; i++) {
      const layer = i < 12 ? 0 : 1, k = layer ? i - 12 : i;
      const x = -2.6 + (k % (layer ? 8 : 12)) * (layer ? 0.66 : 0.46) + (layer ? 0.3 : 0), z = WHALE[2] - 1.35 - (layer ? 0 : (k % 2) * 0.05);
      const m = new THREE.Mesh(cg, crate); m.position.set(x, layer * 0.34, z - (layer ? 0.08 : 0)); m.rotation.y = (rr2() - 0.5) * 0.2;
      m.castShadow = true; m.receiveShadow = true; this.cases.push(m); R.add(m);
    }
    // plunger box with its T-handle
    const box = new THREE.Mesh(boxGeo(V(-0.28, 0, -0.2), V(0.28, 0.42, 0.2)), lam("plungerBox", () => ({ color: "#9a6a3c" }))); box.castShadow = true;
    const pb = new THREE.Group(); pb.add(box); pb.position.set(...PLUNGER); R.add(pb);
    const rod = new THREE.Mesh(cyl(0.025, 0.6), lam("steelRod", () => ({ color: "#c9ccd2" }))); rod.position.y = 0.3;
    const bar = new THREE.Mesh(cyl(0.035, 0.5), lam("tHandle", () => ({ color: "#2d2a35" }))); bar.rotation.z = Math.PI / 2; bar.position.y = 0.6;
    this.handle.add(rod, bar); this.handle.position.set(PLUNGER[0], 0.42, PLUNGER[2]); R.add(this.handle);
    // TV camera on its tripod
    const tri = new THREE.Group(), dark = lam("camDark", () => ({ color: "#2f2d38" })), grey = lam("camGrey", () => ({ color: "#8b8f9a" }));
    for (let k = 0; k < 3; k++) { const a = (k / 3) * Math.PI * 2; const leg = new THREE.Mesh(cyl(0.03, 1.5), dark); leg.position.set(Math.cos(a) * 0.3, 0.7, Math.sin(a) * 0.3); leg.rotation.set(Math.sin(a) * 0.22, 0, -Math.cos(a) * 0.22); tri.add(leg); }
    const cbody = new THREE.Mesh(boxGeo(V(-0.18, 1.42, -0.32), V(0.18, 1.78, 0.32)), grey); tri.add(cbody);
    const lens = new THREE.Mesh(cyl(0.11, 0.3), dark); lens.rotation.x = Math.PI / 2; lens.position.set(0, 1.6, 0.46); tri.add(lens);
    const reel = new THREE.Mesh(cyl(0.2, 0.08), dark); reel.rotation.z = Math.PI / 2; reel.position.set(0, 1.98, -0.05); tri.add(reel);
    tri.position.set(TVCAM[0], H(TVCAM[0], TVCAM[2]), TVCAM[2]); tri.rotation.y = 0.15; tri.traverse((o) => { (o as THREE.Mesh).castShadow = true; }); R.add(tri);
    // tow truck (pickup) on the sand, facing away from the whale, with the rope to the tail
    const tcol = lam("truck", () => ({ color: "#d9a640" })), tyre = lam("tyre", () => ({ color: "#2b2a33" }));
    const tadd = (g: THREE.BufferGeometry, m: THREE.Material) => { const me = new THREE.Mesh(g, m); me.castShadow = true; me.receiveShadow = true; this.truck.add(me); return me; };
    tadd(boxGeo(V(-5.2, 0.45, -0.95), V(0, 1.15, 0.95)), tcol);
    tadd(boxGeo(V(-4.9, 1.15, -0.9), V(-3.3, 1.95, 0.9)), tcol);
    tadd(boxGeo(V(-4.85, 1.25, -0.92), V(-3.35, 1.8, 0.92)), lam("carGlass", () => ({ color: "#a8c4dc" })));
    for (const x of [-4.3, -0.9]) for (const z of [-0.98, 0.98]) { const w = tadd(cyl(0.42, 0.3), tyre); w.rotation.x = Math.PI / 2; w.position.set(x, 0.42, z); }
    this.truck.position.set(...TRUCK_HITCH); R.add(this.truck);
    this.rope = new THREE.Mesh(cyl(0.035, 1, 6), lam("rope", () => ({ color: "#e8d8a8" }))); this.rope.castShadow = true; R.add(this.rope);
    // bulldozer + the sand mound for the burial
    const ycol = lam("dozer", () => ({ color: "#f2b632" }));
    const dadd = (g: THREE.BufferGeometry, m: THREE.Material) => { const me = new THREE.Mesh(g, m); me.castShadow = true; me.receiveShadow = true; this.dozer.add(me); return me; };
    dadd(boxGeo(V(-1.6, 0.5, -1.0), V(1.4, 1.5, 1.0)), ycol);
    dadd(boxGeo(V(-1.4, 1.5, -0.8), V(0.2, 2.6, 0.8)), lam("carGlass", () => ({ color: "#a8c4dc" })));
    dadd(boxGeo(V(-1.5, 2.6, -0.9), V(0.3, 2.72, 0.9)), ycol);
    for (const z of [-1.05, 1.05]) dadd(boxGeo(V(-1.9, 0, z - 0.3), V(1.6, 0.7, z + 0.3)), dark);
    dadd(boxGeo(V(2.0, 0, -1.6), V(2.25, 1.3, 1.6)), ycol);
    this.dozer.visible = false; R.add(this.dozer);
    this.mound = new THREE.Mesh(new THREE.SphereGeometry(1, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), lam("moundSand", () => ({ map: rep(sandHD(), 2, 2) })));
    this.mound.castShadow = true; this.mound.receiveShadow = true; this.mound.visible = false; R.add(this.mound);
    // parking lot cars; Umenhofer's green sedan is the one that gets crushed
    for (const [x, col, yaw] of [[-18, "#c94a3a", 0], [-12, "#e6dcc0", 0.03], [0, "#3f6fb5", -0.02], [6, "#d9a640", 0], [12.5, "#8c3b4a", 0.04], [-15, "#5d7a3a", Math.PI]] as const) {
      const c = sedan(col); c.grp.position.set(x, LOT_Y, x === -15 ? -77 : -68); c.grp.rotation.y = yaw; R.add(c.grp);
    }
    const uc = sedan("#3f8a5a"); uc.grp.position.set(...UCAR); this.ucar = uc.grp; this.ucabin = uc.cabin; R.add(uc.grp);
    this.bigChunk = new THREE.Mesh(chunkGeo(9, 1.15), raw); this.bigChunk.castShadow = true; R.add(this.bigChunk);
  }

  /** camera-relative sun, frozen per shot */
  private shotSun(id: number, s: ShotDef, L: LightPreset) {
    let v = this.sunCache.get(id);
    if (v) return v;
    let fx = 0, fz = 0;
    for (let f = s.a; f < s.b; f += 3) {
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
    const c = camAt(id, f);
    cam.position.set(...c.pos); cam.up.set(0, 1, 0); cam.lookAt(...c.look); cam.rotateZ(c.roll);
    cam.fov = c.fov; cam.near = 0.2; cam.far = 1500; cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    const focus = V(...c.look), dist = cam.position.distanceTo(focus);
    cam.layers.enable(NOINK);
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
    // ---- sea + surf ----
    const W = this.WU, wc = K.water;
    untone(wc.near, W.wNearC.value); untone(wc.mid, W.wMidC.value); untone(wc.far, W.wFarC.value);
    untone(wc.crest, W.wCrest.value); untone(wc.trough, W.wTrough.value); untone(wc.glint, W.wGlint.value);
    W.wShade.value.set(...wc.shade); W.wTime.value = t;
    this.foam.forEach((fm, i) => {
      const u = ((t * 0.12 + i / 4) % 1), z = 18 - 5.5 * u;
      fm.position.set(0, SEA_Y + 0.03 + 0.01 * i, z); (fm.material as THREE.MeshBasicMaterial).opacity = 0.8 * Math.sin(Math.PI * u);
    });
    // ---- whale state ----
    const blown = s.scene !== "physics" && tau >= BOOM;
    this.whale.visible = !blown;
    this.remains.visible = blown;
    const nCases = s.scene === "physics" ? 20 : tau >= BOOM ? 0 : Math.round(20 * clamp01((tau - 24.4) / 2.2));
    this.cases.forEach((m, i) => { m.visible = i < nCases; });
    this.handle.position.y = 0.42 - (tau >= BOOM - 0.12 && s.scene !== "physics" ? 0.34 : 0);
    // tow: truck strains (shake), rope taut to the tail
    const towing = s.scene === "tow";
    this.truck.position.set(TRUCK_HITCH[0] + (towing ? 0.03 * Math.sin(t * 47) : 0), TRUCK_HITCH[1] + (towing ? 0.015 * Math.sin(t * 31) : 0), TRUCK_HITCH[2]);
    this.truck.visible = this.rope.visible = tau < 18 && !blown;
    const a = V(TRUCK_HITCH[0], 0.6, TRUCK_HITCH[2]), bb = V(-WHALE_LEN / 2 + 0.3, 0.9, WHALE[2]);
    this.rope.position.copy(a).add(bb).multiplyScalar(0.5); this.rope.scale.set(1, a.distanceTo(bb), 1);
    this.rope.quaternion.setFromUnitVectors(V(0, 1, 0), bb.clone().sub(a).normalize());
    // burial
    const bury = s.scene === "after" && f >= 1774;
    this.dozer.visible = bury; this.mound.visible = bury;
    if (bury) {
      const u = smooth((tau - 59.1) / 2.4);
      this.dozer.position.set(7.6 - 2.4 * u, 0, -3.0 + 0.6 * u); this.dozer.rotation.y = Math.PI + 0.3;
      this.mound.position.set(-1.5, -0.2, 1.5); this.mound.scale.set(5 + 3 * u, 1.2 + 1.6 * u, 3 + 1.2 * u);
    }
    // Umenhofer's car and the biggest chunk
    const crushed = s.scene === "car" && tau >= CRUSH;
    this.ucabin.scale.y = crushed ? 0.3 : 1;
    this.ucar.rotation.z = crushed ? 0.03 : 0;
    this.bigChunk.visible = s.scene === "car" && tau > CRUSH - 1.4;
    if (this.bigChunk.visible) {
      const roof = LOT_Y + (crushed ? 1.25 : 1.66) + 0.55, dt = Math.max(0, CRUSH - tau);
      this.bigChunk.position.set(UCAR[0] + 0.1, roof + 4.9 * dt * dt, UCAR[2] - 0.2);
      this.bigChunk.rotation.set(dt * 2.5, 0.4 + dt * 1.5, crushed ? 0.05 : dt * 1.2);
      this.bigChunk.scale.set(1.2, crushed ? 0.8 : 1, 1.1);
    }
    // ---- cast + effects ----
    const right = V(0, 0, 0).setFromMatrixColumn(cam.matrixWorld, 0);
    const st = stage(id, f, t, tau, { pos: cam.position, right, sun: sunDir });
    this.frustum.setFromProjectionMatrix(this.m4.multiplyMatrices(cam.projectionMatrix, cam.matrixWorldInverse));
    let ai = 0;
    const used: Actor[] = [];
    for (const p of st.places) {
      const sc2 = p.scale ?? 1;
      if (!this.frustum.intersectsSphere(this.sph.set(this.v.set(p.x, p.y + 1.1 * sc2, p.z), 3.5))) continue;
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

const WATER_DECL = `#include <common>
varying vec3 vWP;
uniform vec3 wNearC, wMidC, wFarC, wCrest, wTrough, wGlint, wShade;
uniform sampler2D wNearTex, wFarTex;
uniform float wTime;`;
const WATER_COL = `
  vec3 wV = vWP - cameraPosition;
  float wd = length(wV);
  float wDep = asin(clamp(-wV.y / wd, 0.0, 1.0));
  float wf = 1.0 - smoothstep(0.0, 0.42, wDep);
  vec3 wc = mix(mix(wNearC, wMidC, smoothstep(0.0, 0.55, wf)), wFarC, smoothstep(0.55, 1.0, wf));
  vec2 wp = vWP.xz + vec2(0.0, -0.6 * wTime);
  vec4 mk = mix(texture2D(wNearTex, wp / 8.0), texture2D(wFarTex, wp / 40.0 + 0.37), smoothstep(25.0, 90.0, wd));
  wc = mix(wc, wTrough, mk.g * 0.6);
  wc = mix(wc, wCrest, mk.r * 0.7);
  wc = mix(wc, wGlint, mk.b * (0.3 + 0.5 * wf));
  diffuseColor.rgb = wc;`;
void smokeTex;
