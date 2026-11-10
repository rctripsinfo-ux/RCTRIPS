// Western Australia, 1932, as one three.js scene (our own simplified version): golden wheat fields, fences, the farmhouse
// and a windpump, the dam, the road, the army's truck and two Lewis guns on tripods, ammunition boxes and the growing
// pile of empty shells. The emus and people are cards (cast.ts).
import * as THREE from "three";
import { Batch, V, lam, boxGeo, prop, house, Kit } from "./build";
import { rep, ctex, rng, cloudHD, stoneHD, grassHD } from "./paint";
import { LIGHTS, LOOK, LightPreset } from "./lights";
import { TONE, CHAR, twoTone, untone } from "./shade";
import { NOINK } from "./ink";
import { Pool, Actor, Fx, stage } from "./cast";
import { FPS, SHOTS, H, camAt, V3, smooth, ShotDef, FOREGROUND, kickAt, MAJOR, GUN, DAM, FARM, ROAD_Z, truckAt, JAM } from "./story";

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
  private truck = new THREE.Group(); private truckGun = new THREE.Group();
  private guns: THREE.Group[] = []; private shells!: THREE.InstancedMesh; private fan!: THREE.Group;
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
    const b = new Batch();
    // ---- wheat country: golden ground, field rows, dirt road, fences, scrub trees ----
    const wheatTex = ctex("wheatField", 512, 512, (g, r) => { g.fillStyle = "#d9b04f"; g.fillRect(0, 0, 512, 512);
      for (let i = 0; i < 2600; i++) { const x = r() * 512, y = r() * 512; g.strokeStyle = r() < 0.5 ? "rgba(150,105,30,0.45)" : "rgba(255,226,140,0.55)"; g.lineWidth = 2; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (r() - 0.5) * 3, y - 9); g.stroke(); }
      g.fillStyle = "rgba(170,120,40,0.25)"; for (let y = 0; y < 512; y += 32) g.fillRect(0, y, 512, 6); });
    const field = new THREE.PlaneGeometry(900, 900); field.rotateX(-Math.PI / 2); const uv0 = field.attributes.uv as THREE.BufferAttribute; for (let i = 0; i < uv0.count; i++) uv0.setXY(i, uv0.getX(i) * 110, uv0.getY(i) * 110);
    b.add(field, lam("wheatGround", () => ({ map: wheatTex })));
    const dirt = lam("dirtRoad", () => ({ map: ctex("dirt", 256, 256, (g, r) => { g.fillStyle = "#b9825a"; g.fillRect(0, 0, 256, 256); for (let i = 0; i < 700; i++) { g.fillStyle = r() < 0.5 ? "rgba(120,80,50,0.4)" : "rgba(230,190,150,0.4)"; g.fillRect(r() * 256, r() * 256, 3, 3); } }) }));
    { const rd = new THREE.PlaneGeometry(900, 6); rd.rotateX(-Math.PI / 2); rd.translate(0, 0.02, ROAD_Z); const u = rd.attributes.uv as THREE.BufferAttribute; for (let i = 0; i < u.count; i++) u.setXY(i, u.getX(i) * 150, u.getY(i)); b.add(rd, dirt);
      const camp = new THREE.CircleGeometry(9, 32); camp.rotateX(-Math.PI / 2); camp.translate(MAJOR[0], 0.02, MAJOR[2]); b.add(camp, dirt); }
    // 3D wheat tufts near the cameras' fields (golden stalks with a darker head)
    const stalk = new THREE.ConeGeometry(0.035, 1, 4); stalk.translate(0, 0.5, 0);
    const wA = lam("wheatA", () => ({ color: "#e2b85a" })), wB = lam("wheatB", () => ({ color: "#c99a3c" }));
    for (let i = 0; i < 900; i++) {
      const x = -40 + rr() * 80, z = -4 + rr() * 60; if (Math.hypot(x - DAM[0], z - DAM[2]) < 12) continue;
      for (let k = 0; k < 4; k++) { const a = rr() * 6.28, lean = rr() * 0.25; b.add(stalk, k % 2 ? wA : wB, new THREE.Matrix4().compose(V(x + Math.cos(a) * 0.12, 0, z + Math.sin(a) * 0.12), new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.sin(a) * lean, 0, -Math.cos(a) * lean)), V(1, 0.8 + rr() * 0.5, 1))); }
    }
    // fences along the paddock
    const post = lam("fencePost", () => ({ color: "#8a6a4a" }));
    for (let x = -60; x <= 60; x += 3) b.add(boxGeo(V(x - 0.07, 0, -6.07), V(x + 0.07, 1.2, -5.93)), post);
    for (const y of [0.55, 1.0]) b.add(boxGeo(V(-60, y, -6.02), V(60, y + 0.04, -5.98)), post);
    // farmhouse, sheds, gum trees
    house(b, FARM[0], FARM[2], Math.PI + 0.2, 12, 9, 6, 1, 0); house(b, FARM[0] + 18, FARM[2] + 4, Math.PI - 0.1, 8, 6, 4.5, 2, 0);
    for (let i = 0; i < 40; i++) { const x = -200 + rr() * 400, z = 80 + rr() * 120; prop(b, {}, i % 4 ? "tree_fat" : "tree_oak", x, 0, z, 8 + rr() * 6, rr() * 6); }
    for (let i = 0; i < 16; i++) { const x = -160 + rr() * 320, z = -60 - rr() * 90; prop(b, {}, "tree_fat", x, 0, z, 7 + rr() * 5, rr() * 6); }
    for (let i = 0; i < 10; i++) { const x = (rr() - 0.5) * 30, z = DAM[2] - 18 + rr() * 3; prop(b, {}, "plant_bush", x, 0, z, 1.2 + rr() * 0.4, rr() * 6); }
    // the dam: a muddy pond
    { const w = new THREE.CircleGeometry(10, 48); w.rotateX(-Math.PI / 2); w.translate(DAM[0], 0.03, DAM[2]); b.add(w, lam("damWater", () => ({ color: "#5f8fb8" })));
      const rim = new THREE.RingGeometry(10, 11.5, 48); rim.rotateX(-Math.PI / 2); rim.translate(DAM[0], 0.025, DAM[2]); b.add(rim, dirt); }
    b.build(R);
    const sp: number[] = [];
    for (let i = 0; i < 900; i++) { const a2 = rr() * Math.PI * 2, e = 0.08 + rr() * 1.3; sp.push(Math.cos(a2) * Math.cos(e) * 900, Math.sin(e) * 900, Math.sin(a2) * Math.cos(e) * 900); }
    const sg = new THREE.BufferGeometry(); sg.setAttribute("position", new THREE.Float32BufferAttribute(sp, 3));
    this.stars = new THREE.Points(sg, new THREE.PointsMaterial({ color: "#eef3ff", size: 2.2, sizeAttenuation: false, fog: false, depthWrite: false }));
    this.stars.layers.set(NOINK); this.stars.frustumCulled = false; R.add(this.stars);
    // windpump: lattice tower + bladed wheel (turns)
    { const wp = new THREE.Group(), steel = lam("pumpSteel", () => ({ color: "#8e939c" }));
      for (const [x, z] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) { const l = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 9.4, 6), steel); l.position.set(x * 0.6, 4.6, z * 0.6); l.rotation.set(z * 0.1, 0, -x * 0.1); wp.add(l); }
      this.fan = new THREE.Group(); for (let k = 0; k < 14; k++) { const bl = new THREE.Mesh(boxGeo(V(-0.12, 0.3, -0.02), V(0.12, 1.6, 0.02)), steel); bl.rotation.z = (k / 14) * Math.PI * 2; this.fan.add(bl); }
      this.fan.position.set(0, 9.4, 0.5); wp.add(this.fan); const tail = new THREE.Mesh(boxGeo(V(-0.05, 9.1, -2.6), V(0.05, 9.9, -0.6)), steel); wp.add(tail);
      wp.position.set(FARM[0] + 30, 0, FARM[2] - 10); wp.traverse((o) => { (o as THREE.Mesh).castShadow = true; }); R.add(wp); }
    // Lewis gun on a tripod: cooling jacket barrel + drum magazine
    const gunMetal = lam("gunMetal", () => ({ color: "#3a3d46" })), gunWood = lam("gunWood", () => ({ color: "#7a4f2e" }));
    const makeGun = () => { const g = new THREE.Group();
      for (const a of [0, 2.1, 4.2]) { const l = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.1, 6), gunMetal); l.position.set(Math.cos(a) * 0.3, 0.45, Math.sin(a) * 0.3); l.rotation.set(Math.sin(a) * 0.4, 0, -Math.cos(a) * 0.4); g.add(l); }
      const jacket = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 1.1, 12), gunMetal); jacket.rotation.x = Math.PI / 2; jacket.position.set(0, 0.95, 0.45); g.add(jacket);
      const drum = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.08, 18), gunMetal); drum.position.set(0, 1.1, 0.0); g.add(drum);
      const stock = new THREE.Mesh(boxGeo(V(-0.05, 0.86, -0.75), V(0.05, 0.98, -0.1)), gunWood); g.add(stock);
      g.traverse((o) => { (o as THREE.Mesh).castShadow = true; }); return g; };
    for (const [x, z] of [[GUN[0], GUN[2]], [GUN[0] - 3.2, GUN[2] - 0.3]]) { const g = makeGun(); g.position.set(x, 0, z); this.guns.push(g); R.add(g); }
    // ammunition boxes by the guns
    const box = lam("ammoBox", () => ({ color: "#5d6b3a" }));
    for (let i = 0; i < 6; i++) { const m = new THREE.Mesh(boxGeo(V(-0.35, 0, -0.2), V(0.35, 0.32, 0.2)), box); m.position.set(GUN[0] + 1.3 + (i % 2) * 0.8, Math.floor(i / 2) * 0.33, GUN[2] - 1.0); m.castShadow = true; R.add(m); }
    // the pile of empty shells (grows with the bullets fired)
    this.shells = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.03, 0.03, 0.14, 6), lam("brass", () => ({ color: "#d4a640" })), 700);
    { const mm = new THREE.Matrix4(), q = new THREE.Quaternion(); for (let i = 0; i < 700; i++) { const a = rr() * 6.28, r0 = Math.sqrt(rr()) * 1.2, h = Math.max(0, 0.5 - r0 * 0.4) * rr(); q.setFromEuler(new THREE.Euler(rr() * 3, rr() * 3, rr() * 3)); mm.compose(V(GUN[0] + 0.6 + Math.cos(a) * r0, h, GUN[2] + 0.4 + Math.sin(a) * r0 * 0.7), q, V(1, 1, 1)); this.shells.setMatrixAt(i, mm); } }
    this.shells.castShadow = true; R.add(this.shells);
    // the army truck (1930s): cab, bed, wheels, a Lewis gun on the back
    { const olive = lam("truckOlive", () => ({ color: "#6b7440" })), tyre = lam("tyre", () => ({ color: "#2b2a33" })), glass = lam("carGlass", () => ({ color: "#a8c4dc" }));
      const add = (g: THREE.BufferGeometry, m: THREE.Material) => { const me = new THREE.Mesh(g, m); me.castShadow = true; this.truck.add(me); return me; };
      add(boxGeo(V(-0.95, 0.5, 0.6), V(0.95, 1.2, 2.6)), olive); add(boxGeo(V(-0.9, 1.2, 0.8), V(0.9, 2.1, 1.9)), olive); add(boxGeo(V(-0.92, 1.4, 1.88), V(0.92, 1.95, 1.92)), glass);
      add(boxGeo(V(-1.0, 0.5, -2.4), V(1.0, 0.75, 0.6)), olive); for (const s of [-1, 1]) add(boxGeo(V(s * 1.0 - 0.05, 0.75, -2.4), V(s * 1.0 + 0.05, 1.2, 0.6)), olive);
      for (const x of [-0.95, 0.95]) for (const z of [-1.6, 1.9]) { const w = add(new THREE.CylinderGeometry(0.42, 0.42, 0.28, 16), tyre); w.rotation.z = Math.PI / 2; w.position.set(x, 0.42, z); }
      const tg = makeGun(); tg.position.set(0, 0.75, -1.2); tg.rotation.y = 0; this.truck.add(tg); this.truckGun = tg; R.add(this.truck); }
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
    this.fan.rotation.z = t * 1.6;
    // truck: drives along its path, bounces; hidden when it has no part in the shot
    const tk = truckAt(s.scene, tau); this.truck.visible = ["army", "truck", "aim", "home", "dayone"].includes(s.scene);
    this.truck.position.set(tk.x, tk.bounce, tk.z); this.truck.rotation.set(tk.bounce * 0.25 * Math.sin(t * 13), tk.yaw, tk.bounce * 0.2 * Math.sin(t * 11));
    this.truckGun.rotation.set(0.15 * Math.sin(t * 17) * (s.scene === "aim" || s.scene === "truck" ? 1 : 0), 0, 0);
    // guns recoil while firing (ambush/jam: until the jam; bullets scene: steady)
    const firing = (s.scene === "jam" && tau < JAM) || s.scene === "bullets";
    this.guns.forEach((g, i) => { g.position.z = (i ? GUN[2] - 0.3 : GUN[2]) - (firing ? 0.03 * Math.abs(Math.sin(t * 40 + i)) : 0); });
    // shells: none at first, a heap by the end
    const nShell = s.scene === "bullets" ? Math.round(120 + 580 * smooth((tau - 36.6) / 3.2)) : s.scene === "twist" ? 700 : s.scene === "jam" ? 40 : 0;
    this.shells.count = nShell;
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
