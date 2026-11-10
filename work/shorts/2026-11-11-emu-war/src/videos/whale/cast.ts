// Our cast as lit flat sprites in the 3D world. Each frame every character asks for a drawing (a key + a draw call);
// the pool keeps one canvas per distinct drawing, so soldiers marching in step share canvases (7 head shapes x 4
// outfits). Characters are yaw-only billboards shaded by cardShade() (scene tint, bright floor, side gradient toward
// the sun, painted crescent in the drawing); standing ones get a soft multiply contact blob. Effects are unlit cards.
// Cards, effects and blobs live on the NOINK layer so the world ink pass never outlines their quads.
import * as THREE from "three";
import { Pen, bodyFront, bodySide, KID, SKINS, INK, fxBurst, fxSplash, fxStars, fxPuff, fxShadow, fxContact, Outfit, Expr, FrontOpts, SideOpts } from "./toon";
import { fxShockLines, fxEmu, fxStreak, fxPop, fxBowl, fxQuestion } from "./fx70";
import { FPS, SHOTS, V3, smooth, clamp01, MAJOR, GUN, DAM, KID_AT, ROAD_Z, JAM, truckAt } from "./story";
import { LIGHTS } from "./lights";
import { NOINK } from "./ink";
import { cardShade, blobMaterial, CARD_K } from "./cardshade";

// ---------------- canvas pool ----------------
type Entry = { cv: HTMLCanvasElement; tex: THREE.CanvasTexture; w: number; h: number };
export type Req = { key: string; w: number; h: number; k: number; draw: (p: Pen) => void; tex?: THREE.CanvasTexture };
const makeEntry = (w: number, h: number): Entry => {
  const cv = document.createElement("canvas");
  cv.width = w; cv.height = h;
  const tex = new THREE.CanvasTexture(cv);
  tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  return { cv, tex, w, h };
};
export class Pool {
  private live = new Map<string, Entry>();
  private free: Entry[] = [];
  private reqs: Req[] = [];
  req(key: string, w: number, h: number, k: number, draw: (p: Pen) => void) {
    const r: Req = { key: `${w}x${h}|${key}`, w, h, k, draw };
    this.reqs.push(r);
    return r;
  }
  flush() {
    const want = new Map<string, Req[]>();
    for (const r of this.reqs) { const l = want.get(r.key); if (l) l.push(r); else want.set(r.key, [r]); }
    for (const [key, e] of this.live) if (!want.has(key)) { this.live.delete(key); this.free.push(e); }
    for (const [key, rs] of want) {
      let e = this.live.get(key);
      if (!e) {
        const r = rs[0], i = this.free.findIndex((x) => x.w === r.w && x.h === r.h);
        e = i >= 0 ? this.free.splice(i, 1)[0] : makeEntry(r.w, r.h);
        const g = e.cv.getContext("2d")!;
        g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, e.w, e.h); g.setTransform(r.k, 0, 0, r.k, 0, 0);
        r.draw(new Pen(g));
        e.tex.needsUpdate = true;
        this.live.set(key, e);
      }
      for (const r of rs) r.tex = e.tex;
    }
    this.reqs = [];
  }
}

// ---------------- sprite meshes ----------------
const blank = (() => { const c = document.createElement("canvas"); c.width = c.height = 2; return new THREE.CanvasTexture(c); })();
export const SU = 0.00216; // metres per design unit: 1000 units = 2.16 m
export const SU_SWING = 2.3 / 1830; // swing canvas: rope of 1830 units = 2.3 m
const BODY = (() => { const g = new THREE.PlaneGeometry(600 * SU, 1000 * SU); g.translate(0, (975 - 500) * SU, 0); return g; })();
const CARD = new THREE.PlaneGeometry(1, 1);
/** world roots that hold actors (to find the scene's sun when world.ts does not pass it) */
const ROOTS = new Set<THREE.Object3D>();

/** lit flat character: cardShade() material, receives shadows (dims to the bright floor only), casts its silhouette
 *  when world.ts says so (golden). Drawn after the contact blobs (renderOrder 1). */
export class Actor {
  mesh: THREE.Mesh; mat: THREE.MeshLambertMaterial; dmat: THREE.MeshDepthMaterial; r: Req | null = null;
  constructor(parent: THREE.Object3D, geo: THREE.BufferGeometry = BODY) {
    this.mat = cardShade(new THREE.MeshLambertMaterial({ map: blank, alphaTest: 0.5, side: THREE.DoubleSide }));
    this.mat.alphaToCoverage = false; // A2C + MSAA left 1 px sky-depth seams on blurred far cards (POST)
    this.dmat = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: blank, alphaTest: 0.5, side: THREE.DoubleSide });
    this.mesh = new THREE.Mesh(geo, this.mat);
    this.mesh.customDepthMaterial = this.dmat;
    // rim width is in output pixels: tell the card shader the render height (1920 = 1080 x 1920 frame)
    this.mesh.onBeforeRender = (r) => { const rt = r.getRenderTarget(); CARD_K.uPx.value = (rt ? rt.height : r.domElement.height) / 1920; };
    this.mesh.castShadow = false; this.mesh.receiveShadow = true; this.mesh.visible = false;
    this.mesh.rotation.order = "YXZ"; this.mesh.renderOrder = 1; this.mesh.layers.set(NOINK);
    parent.add(this.mesh);
    ROOTS.add(parent);
  }
  bind() { const t = this.r?.tex; if (t) { this.mat.map = t; this.dmat.map = t; } }
}
/** unlit effect card: hard cut-out (ink drawings), soft see-through (dust, mist) or a multiply ground blob */
export class Fx {
  mesh: THREE.Mesh; mat: THREE.MeshBasicMaterial; soft: THREE.MeshBasicMaterial; blob: THREE.MeshBasicMaterial; r: Req | null = null;
  constructor(parent: THREE.Object3D) {
    this.mat = new THREE.MeshBasicMaterial({ map: blank, alphaTest: 0.5, side: THREE.DoubleSide });
    this.mat.alphaToCoverage = false; // A2C + MSAA left 1 px sky-depth seams on blurred far cards (POST)
    this.soft = new THREE.MeshBasicMaterial({ map: blank, transparent: true, depthWrite: false, side: THREE.DoubleSide });
    this.blob = blobMaterial(blank);
    this.mesh = new THREE.Mesh(CARD, this.mat);
    this.mesh.visible = false; this.mesh.layers.set(NOINK);
    parent.add(this.mesh);
  }
  use(soft: boolean) { this.mesh.material = soft ? this.soft : this.mat; }
  bind() {
    const t = this.r?.tex;
    if (!t) return;
    if (this.r!.key.includes("|blob|")) {
      // no mipmaps: at grazing views the mip chain averages the blob with its white surround and it fades out
      if (t.generateMipmaps) { t.generateMipmaps = false; t.minFilter = THREE.LinearFilter; t.needsUpdate = true; }
      this.blob.map = t; this.mesh.material = this.blob; this.mesh.renderOrder = 0.5;
    }
    else { this.mat.map = t; this.soft.map = t; this.mesh.renderOrder = 0; }
  }
}

// ---------------- placements ----------------
export type Place = {
  key: string; draw: (p: Pen) => void; x: number; y: number; z: number;
  scale?: number; mirror?: boolean; yaw?: number; geo?: "body" | "swing"; roll?: number; size?: [number, number, number];
};
export type FxPlace = { key: string; cw: number; ch: number; draw: (p: Pen) => void; x: number; y: number; z: number; w: number; h: number; flat?: boolean; rot?: number; soft?: boolean };
/** sun = world direction TOWARD the sun (optional: when absent the scene's shadow-casting light is used) */
export type CamInfo = { pos: THREE.Vector3; right: THREE.Vector3; sun?: THREE.Vector3 };

const hh = (i: number, s = 0) => { const v = Math.sin(i * 127.1 + s * 311.7) * 43758.5453; return v - Math.floor(v); };
const q = (v: number, n = 120) => Math.round(v * n) / n;
const vOf = (i: number) => (i * 7 + (i >> 2)) % 4;
/** head-shape seed: 7 shapes, so marching soldiers in step still share canvases */
const seedOf = (i: number) => ((i * 5 + 3) % 7) + 1;
/** drawing resolution by distance: [canvas w, h, scale from the 600 x 1000 design]; sized for the 1440 x 2560 final */
const tier = (d: number): [number, number, number] =>
  d < 3.2 ? [1800, 3000, 3.0] : d < 6.5 ? [1080, 1800, 1.8] : d < 16 ? [480, 800, 0.8] : [240, 400, 0.4];

// ---------------- light ----------------
const SUN = new THREE.Vector3(0.5, 0.75, -0.4).normalize();
const tmp = new THREE.Vector3();
let LNAME: "day" | "golden" | "night" = "day";
const sunOf = (root: THREE.Object3D) => {
  let s: THREE.DirectionalLight | null = null;
  root.traverse((o) => { if (!s && o instanceof THREE.DirectionalLight && o.castShadow) s = o; });
  return s as THREE.DirectionalLight | null;
};
/** the sun of the world that is calling: the attached root whose sun target sits on this camera's view axis */
const findSun = (cam: CamInfo, out: THREE.Vector3) => {
  if (cam.sun) return out.copy(cam.sun).normalize();
  let best: THREE.DirectionalLight | null = null, err = Infinity;
  for (const r of ROOTS) {
    if (!r.parent) continue;
    const s = sunOf(r);
    if (!s) continue;
    const d = tmp.copy(s.target.position).sub(cam.pos), e = Math.abs(d.dot(cam.right)) / (d.length() || 1);
    if (e < err) { err = e; best = s; }
  }
  return best ? out.copy(best.position).sub(best.target.position).normalize() : out;
};
/** canvas angle the sun comes FROM on an upright card facing the camera, in 45-degree steps (small texture cache) */
const light2D = (cam: CamInfo, mirror: boolean) => {
  const sx = SUN.dot(cam.right) * (mirror ? -1 : 1), sy = -SUN.y;
  return Math.round(Math.atan2(sy, sx) / (Math.PI / 4)) * (Math.PI / 4);
};

/** front / side view and mirroring for someone at (x, z) walking along (dx, dz); fs = foreshortening of the walk */
const viewOf = (cam: CamInfo, x: number, z: number, dx: number, dz: number) => {
  const tx = cam.pos.x - x, tz = cam.pos.z - z, tl = Math.hypot(tx, tz) || 1;
  const c = (tx * dx + tz * dz) / tl;
  return { side: c < 0.57, mirror: dx * cam.right.x + dz * cam.right.z < 0, fs: Math.round(Math.sqrt(Math.max(0, 1 - c * c)) * 20) / 20 };
};

// ---------------- life: blinks and reaction timing ----------------
/** reference expression and action changes land 0-3 f before the word onset */
const LEAD = 2 / FPS;
/** eyelid 0 open .. 1 shut. Reference: gaps 0.5-2.3 s, 4-frame blink half / shut / shut / half, plus a blink across
 *  every expression swap (the shut frames hide the swap) */
const LID = [0.5, 1, 1, 0.5];
const lidAt = (t: number, i: number, swaps: number[] = []) => {
  const f = Math.round(t * FPS);
  if (f < 45) return 0; // eyes open for the first 1.5 s: frame 0 is the thumbnail
  for (const ts of swaps) { const k = f - Math.round((ts - LEAD) * FPS) + 1; if (k >= 0 && k < 4) return LID[k]; }
  let s = Math.round(-60 * hh(i, 9));
  for (let n = 0; s <= f && n < 400; n++) {
    const k = f - s;
    if (k >= 0 && k < 4) return LID[k];
    s += Math.round(15 + 54 * hh(i * 31 + n, 13)); // next blink 0.5-2.3 s later
  }
  return 0;
};
const fkey = (o: object) => JSON.stringify(o, (_k, v) => (typeof v === "number" ? q(v) : v));

type Who = { i: number; o: Outfit; okey: string };
/** one character drawing in the 600 x 1000 design space, sized by distance, lit from the scene's sun */
const person = (cam: CamInfo, who: Who, x: number, y: number, z: number, view0: { side: boolean; mirror: boolean }, fo: FrontOpts, so: SideOpts, scale = 1): Place & { tierKey: string } => {
  const d = cam.pos.distanceTo(tmp.set(x, y + 1.2, z)) / scale;
  const walkingSide = view0.side && (so.mode === "march") && so.phase !== undefined && so.phase !== 0;
  const view = d < 9 && !walkingSide ? { side: false, mirror: false } : view0;
  if (view !== view0 && fo.mode === "march") fo = { ...fo };
  const [w, h, k] = tier(d);
  const mirror = view.side && view.mirror, light = light2D(cam, mirror), seed = seedOf(who.i);
  const f2: FrontOpts = { ...fo, light, seed }, s2: SideOpts = { ...so, light, seed };
  const key = view.side ? `S|${who.okey}|${fkey(s2)}` : `F|${who.okey}|${fkey(f2)}`;
  return {
    key, x, y, z, scale, mirror, tierKey: `${w}`,
    draw: (p) => (view.side ? bodySide(p, who.o, s2) : bodyFront(p, who.o, f2)),
    size: [w, h, k],
  };
};

/** ground shadow under a standing / sitting card (review rounds 2-4), multiply, blue-violet: a TIGHT contact pool right under
 *  the feet (~.5 on screen at the core) so nobody floats, plus by day (cards cast no real shadow) a lighter soft tail
 *  stretched AWAY from the sun, length ~1.6 m / tan(sun elevation), capped. Golden: world.ts casts real card shadows. */
const CONTACT: Record<"day" | "golden" | "night", [number, number, number]> = { day: [0.2, 0.21, 0.33], golden: [0.24, 0.2, 0.33], night: [0.14, 0.16, 0.34] };
const TAIL: [number, number, number] = [0.42, 0.44, 0.62];
const toSrgb = (v: number) => { const c = clamp01(v); return c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055; };
const hexOf = (c: [number, number, number], k: number) => "#" + c.map((v) => Math.round(255 * toSrgb(1 - (1 - v) * k)).toString(16).padStart(2, "0")).join("");
const blob = (out: Stage, x: number, y: number, z: number, sc = 1, k = 1) => {
  const hl = Math.hypot(SUN.x, SUN.z) || 1, ox = -SUN.x / hl, oz = -SUN.z / hl, rot = Math.atan2(-ox, -oz);
  if (LNAME === "day") {
    const el = Math.asin(Math.min(0.99, Math.max(0.1, SUN.y)));
    const len = Math.min(2.4, Math.max(0.5, 1.6 / Math.tan(el))) * sc, h = len + 0.55 * sc, c = 0.3 * h; // feet at v = .2 of the card
    const tc = hexOf(TAIL, k);
    out.fx.push({ key: `blob|shadow|${tc}`, cw: 128, ch: 256, draw: (p) => fxShadow(p, tc), x: x + ox * c, y: y + 0.018, z: z + oz * c,
      w: 0.72 * sc, h, flat: true, rot });
  }
  const cc = hexOf(CONTACT[LNAME], k);
  out.fx.push({ key: `blob|contact|${cc}`, cw: 128, ch: 128, draw: (p) => fxContact(p, cc), x: x + ox * 0.03 * sc, y: y + 0.022, z: z + oz * 0.03 * sc,
    w: 0.52 * sc, h: 0.4 * sc, flat: true, rot });
};

export type Stage = { places: Place[]; fx: FxPlace[] };



// ---------------- our cast (Western Australia 1932: the major, two gunners, a farmer, a kid; the emus are cards) ----------------
const PALE = "#fbf8f4", CREAM = "#ffe7c9";
const MAJORO: Outfit = { jacket: "#7a6a3e", pants: "#5a5232", boots: INK, hat: "cap", cap: "#5f5028", sash: "#8a3a2a", skin: CREAM, moustache: "#4a3426", build: "stout" };
const SOLD = (v: number): Outfit => ({ jacket: "#8a7a48", pants: "#6a6038", boots: INK, hat: "cap", cap: "#6f6232", skin: v ? PALE : CREAM, moustache: v ? undefined : "#5a3b2a" });
const FARMER: Outfit = { jacket: "#3f6fb5", pants: "#2f4f7a", boots: "#4a3426", hat: "hair", hair: "#8a4a2a", skin: PALE, moustache: "#8a4a2a" };
const STAGED = new Set<number>();
const one = (cam: CamInfo, out: Stage, i: number, o: Outfit, okey: string, x: number, z: number, expr: Expr, t: number,
  opts: { dx?: number; dz?: number; wave?: number; y?: number; tilt?: number; scale?: number; blob?: boolean } = {}) => {
  if (STAGED.has(i)) return; STAGED.add(i);
  const y = opts.y ?? 0, view = { side: false, mirror: false };
  const fo: FrontOpts = { mode: "stand", expr, blink: lidAt(t, i), wave: opts.wave, tilt: opts.tilt };
  out.places.push(person(cam, { i, o, okey }, x, y, z, view, fo, {}, opts.scale ?? 1));
  if (opts.blob !== false) blob(out, x, y, z, opts.scale ?? 1);
};
const card = (out: Stage, key: string, cw: number, ch: number, draw: (p: Pen) => void, x: number, y: number, z: number, w: number, h: number, rot = 0, flat = false, soft = false) =>
  out.fx.push({ key, cw, ch, draw, x, y, z, w, h, rot, flat, soft });
const hsh = (i: number, k = 0) => { const v = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return v - Math.floor(v); };
/** one emu card: mode, legs phase, facing (+1 = toward screen right in world +x, -1 = left), size (m) */
const emu = (out: Stage, cam: CamInfo, x: number, z: number, mode: string, phase: number, dirX: number, size = 1.8, helmet = false) => {
  const ph = q(phase % 1, 8), right = cam.right.x * dirX >= 0 ? 1 : -1, w = size * 0.76;
  card(out, `emu|${mode}|${ph}|${helmet ? 1 : 0}`, 320, 420, (p) => fxEmu(p, mode, ph, helmet), x, size / 2 - size * 0.02, z, w * right, size);
  blob(out, x, 0, z, size / 2.1);
};
const shock = (out: Stage, x: number, y: number, z: number) => card(out, "shock", 300, 300, fxShockLines, x, y + 2.0, z + 0.05, 1.1, 1.1);
const flash = (out: Stage, t: number, x: number, y: number, z: number, k: number) => { const u = q((t * 9 + k * 0.37) % 1, 6); if (u < 0.5) card(out, `burst${u}`, 500, 500, (p) => fxBurst(p, u, "#fff3b0", 10, 30, 220), x, y, z, 0.8, 0.8); };

export const stage = (id: number, f: number, t: number, tau: number, cam: CamInfo): Stage => {
  const out: Stage = { places: [], fx: [] };
  const s = SHOTS[id - 1];
  LNAME = s.light; STAGED.clear();
  findSun(cam, SUN);
  const M = MAJOR, G = GUN, D = DAM, K = KID_AT;
  const crew = (e0: Expr, e1: Expr, e2: Expr) => { one(cam, out, 1, MAJORO, "major", M[0], M[2], e0, t); one(cam, out, 2, SOLD(0), "s0", G[0] - 0.2, G[2] - 1.1, e1, t); one(cam, out, 3, SOLD(1), "s1", G[0] - 3.4, G[2] - 1.3, e2, t); };
  const pecking = (n: number, cx: number, cz: number, r: number, seed: number) => { for (let i = 0; i < n; i++) emu(out, cam, cx + (hsh(i, seed) - 0.5) * 2 * r, cz + (hsh(i, seed + 1) - 0.5) * 2 * r, hsh(i, seed + 2) < 0.6 ? "peck" : "stand", t * 0.5 + hsh(i, seed + 3), hsh(i, seed + 4) < 0.5 ? 1 : -1, 1.6 + 0.3 * hsh(i, seed + 5)); };
  switch (s.scene) {
    case "hook":
      one(cam, out, 1, MAJORO, "major", M[0], M[2], "shock", t);
      emu(out, cam, M[0] - 1.5, M[2] + 5.5, "run", t * 2.4, 1, 2.3); emu(out, cam, M[0] + 1.7, M[2] + 6.2, "run", t * 2.4 + 0.5, -1, 2.3);
      for (let i = 0; i < 9; i++) { const z = M[2] + 5 + i * 2.2 - 3 * ((t * 0.3) % 1), x = M[0] - 5 + (i % 5) * 2.6 + (hsh(i) - 0.5); emu(out, cam, x, z, "run", t * 2.4 + hsh(i, 2), i % 2 ? 1 : -1, 1.8 + 0.2 * hsh(i, 3)); }
      break;
    case "farm":
      pecking(70, -6, 32, 22, 11);
      if (f >= 150) { pecking(7, 0, 19, 4, 3); one(cam, out, 4, FARMER, "farmer", 3.0, 13.8, "stern", t, { wave: q(Math.sin(t * 9), 20) }); }
      break;
    case "army":
      crew("stern", "grin", "smile");
      break;
    case "dayone": {
      crew("nervous", "shock", "nervous");
      for (let i = 0; i < 16; i++) { const z = 6 + i * 1.6 + 8 * Math.max(0, tau - 12.2), x = -8 + (i % 8) * 2.2 + hsh(i) * 1.5; emu(out, cam, x, z, "run", t * 2.4 + hsh(i, 2), hsh(i, 5) < 0.5 ? 1 : -1, 1.8); }
      break;
    }
    case "dam": case "ambush": {
      for (let i = 0; i < 110; i++) { const row = i % 11, col = Math.floor(i / 11), x = D[0] - 48 + col * 3.4 + 2.2 * Math.max(0, tau - 14.2) + hsh(i) * 2, z = D[2] - 8 + row * 1.6 + hsh(i, 1); emu(out, cam, x, z, "walk", t * 1.2 + hsh(i, 2), 1, 1.75); }
      one(cam, out, 1, MAJORO, "major", M[0] + 0.2, D[2] - 19, s.scene === "ambush" ? "grin" : "stern", t);
      break;
    }
    case "jam": {
      const jammed = tau >= JAM;
      one(cam, out, 2, SOLD(0), "s0", G[0] - 0.5, G[2] - 0.9, jammed ? "shock" : "grin", t);
      if (!jammed) flash(out, t, G[0], 0.95, G[2] + 1.1, 0);
      else { card(out, "q", 200, 300, fxQuestion, G[0] + 0.1, 2.15, G[2] - 0.8, 0.45, 0.68); card(out, `puff${q((tau - JAM) % 1, 10)}`, 300, 300, (p) => fxPuff(p, q((tau - JAM) % 1, 10)), G[0], 1.1 + 0.6 * ((tau - JAM) % 1), G[2] + 0.9, 0.9, 0.9, 0, false, true); }
      for (let i = 0; i < 24; i++) { const k = jammed ? tau - JAM : 0, a = hsh(i) * 6.28; emu(out, cam, D[0] - 10 + (i % 6) * 2.4 + Math.cos(a) * 6 * k, D[2] - 6 + Math.floor(i / 6) * 1.8 + Math.sin(a) * 6 * k, jammed ? "run" : "walk", t * (jammed ? 2.4 : 1.2) + hsh(i, 2), Math.cos(a) > 0 ? 1 : -1, 1.75); }
      break;
    }
    case "truck": case "aim": {
      const tk = truckAt(s.scene === "aim" ? "truck" : "truck", tau), gx = tk.x - 1.2, gy = tk.bounce + 0.75;
      one(cam, out, 2, SOLD(0), "s0", gx, tk.z, f < 633 ? "grin" : "nervous", t, { y: gy, tilt: 6 * Math.sin(t * 11) * Math.min(1, tk.bounce * 6) });
      for (let i = 0; i < 14; i++) { const x = tk.x + 8 + i * 1.8 + 3.5 * (tau - 20.0) * 0.3, z = tk.z + (hsh(i) - 0.5) * 10; emu(out, cam, x, z, "run", t * 2.8 + hsh(i, 2), 1, 1.8); }
      if (s.scene === "aim") for (let k = 0; k < 3; k++) { const u = (t * 2 + k * 0.33) % 1; card(out, "streak", 400, 60, fxStreak, gx + 1 + 6 * u, gy + 1.4 + 3 * u, tk.z, 1.2, 0.18, 0.5); }
      break;
    }
    case "herd": {
      const split = smooth((tau - 28.4) / 2.2);
      for (let g = 0; g < 6; g++) { const a = (g / 6) * Math.PI * 2 + 0.3, gx = Math.cos(a) * 18 * split, gz = 16 + Math.sin(a) * 12 * split;
        for (let i = 0; i < 9; i++) { const j = g * 9 + i, r = 2.6 + (split < 0.2 ? 6 : 0) * hsh(j, 3), b = hsh(j) * 6.28; const x = gx + Math.cos(b) * r * (0.4 + hsh(j, 1)), z = gz + Math.sin(b) * r * (0.4 + hsh(j, 1));
          const lookout = i === 0 && split > 0.5; emu(out, cam, x, z, lookout ? "look" : split > 0.05 && split < 0.95 ? "run" : "peck", t * 2 + hsh(j, 2), Math.cos(a) > 0 ? 1 : -1, lookout ? 2.2 : 1.7); } }
      break;
    }
    case "popcorn": {
      one(cam, out, 5, KID, "kid", K[0], K[2], tau > 33.2 ? "shock" : "grin", t, { wave: q(Math.sin(t * 10), 20), scale: 0.9 });
      card(out, "bowl", 300, 160, fxBowl, K[0], 0.95, K[2] + 0.25, 0.75, 0.4);
      for (let k = 0; k < 10; k++) { const u = (t * 0.9 + k * 0.1) % 1, a = hsh(k) * 6.28; card(out, `pop${k % 3}`, 120, 120, (p) => fxPop(p, k % 3), K[0] + Math.cos(a) * 1.4 * u, 1.0 + 2.4 * u - 2.6 * u * u, K[2] + 0.4 + Math.sin(a) * 0.4 * u, 0.18, 0.18, u * 6); }
      break;
    }
    case "home": {
      for (let i = 0; i < 10; i++) emu(out, cam, -22 + i * 1.6, ROAD_Z + 5 + hsh(i) * 1.5, "stand", 0, 1, 1.8);
      break;
    }
    case "bullets": {
      crew("stern", "nervous", "nervous");
      flash(out, t, G[0] + 0.5, 1.0, G[2] + 1.0, 0); flash(out, t, G[0] - 2.7, 1.0, G[2] + 0.7, 1);
      if (f >= 1169) { emu(out, cam, 0, 13, "stand", 0, -1, 2.0); for (let k = 0; k < 4; k++) { const u = (t * 1.5 + k * 0.25) % 1; card(out, "streak", 400, 60, fxStreak, -3 + 6 * u, 0.7 + k * 0.45, 13.2, 1.0, 0.15, 0); } }
      break;
    }
    case "wheat":
      pecking(8, 0, 20, 4, 5);
      one(cam, out, 4, FARMER, "farmer", 3.0, 13.8, "pained", t, { tilt: 8 });
      break;
    case "twist": {
      one(cam, out, 1, MAJORO, "major", M[0], M[2], tau > 45.0 ? "nervous" : "stern", t, { wave: tau < 45 ? 0.9 : undefined });
      emu(out, cam, M[0] + 1.6, M[2] + 0.3, "stand", 0, -1, 2.0, true);
      for (let i = 0; i < 8; i++) emu(out, cam, M[0] - 8 + i * 2.2 + 1.2 * ((t * 0.5) % 1), M[2] + 9, "walk", t * 1.2 + i * 0.12, 1, 1.8, true);
      break;
    }
  }
  return out;
};
void bodyFront; void bodySide; void fxContact; void fxShadow; void fxSplash; void fxStars; void SKINS; void clamp01;
