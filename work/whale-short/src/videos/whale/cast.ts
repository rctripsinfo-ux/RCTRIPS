// Our cast as lit flat sprites in the 3D world. Each frame every character asks for a drawing (a key + a draw call);
// the pool keeps one canvas per distinct drawing, so soldiers marching in step share canvases (7 head shapes x 4
// outfits). Characters are yaw-only billboards shaded by cardShade() (scene tint, bright floor, side gradient toward
// the sun, painted crescent in the drawing); standing ones get a soft multiply contact blob. Effects are unlit cards.
// Cards, effects and blobs live on the NOINK layer so the world ink pass never outlines their quads.
import * as THREE from "three";
import { Pen, bodyFront, bodySide, KID, SKINS, INK, fxBurst, fxSplash, fxStars, fxPuff, fxShadow, fxContact, Outfit, Expr, FrontOpts, SideOpts } from "./toon";
import { fxGullStand, fxChunk, fxSplat, fxGull, fxStink, fxBoom, fxArrow, fxArrowBlocked, fxPacket, fxSquirt, fxKetchupHit, fxBubbleSticks, fxShockLines } from "./fx70";
import {
  FPS, SHOTS, V3, smooth, clamp01, H, LOT_Y, WHALE, ENG, TVCAM, TRUCK_HITCH, UMEN, UCAR, PACKET, LUCKY, BOOM, CRUSH, LUCKY_HIT, STEP, SQUIRT, SQUIRT_HIT, UP,
} from "./story";
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

// ---------------- our cast (Florence, Oregon, November 1970) ----------------
const HAIRS = ["#5a3b2a", "#2a201a", "#d9a441", "#8a4a2a", "#3b2a20", "#7a5a3a"];
const PALE = "#fbf8f4", CREAM = "#ffe7c9";
const SKIN_OF = (v: number) => [PALE, PALE, CREAM, PALE, "#f5d2ae"][v % 5];
const COATS = ["#d9a441", "#b5653f", "#2f6f73", "#7a5a3a", "#3f6fb5", "#8c3b4a", "#5d7a3a", "#c25a7a"];
const folk = (v: number): Outfit => ({
  jacket: COATS[v % 8], pants: ["#3b4a6b", "#5a4632", "#3b3f52"][v % 3], boots: "#4a3426", skin: SKIN_OF(v),
  hat: v % 5 === 3 ? "cap" : "hair", hair: HAIRS[v % 6], cap: ["#c94a3a", "#2f5f6a", "#e6dcc0"][v % 3],
  dress: v % 4 === 1 ? ["#d9a441", "#c25a7a", "#5a8fc2"][v % 3] : undefined, moustache: v % 6 === 2 ? "#4a3426" : undefined,
});
const FOLK = Array.from({ length: 12 }, (_, v) => folk(v));
const ENGINEER: Outfit = { jacket: "#e8742c", pants: "#3b4a6b", boots: "#4a3426", hat: "cap", cap: "#f2c230", sash: "#f4f1d0", skin: PALE, moustache: "#5a3b2a", build: "stout" };
const WORKER: Outfit = { jacket: "#e8742c", pants: "#3b4a6b", boots: "#4a3426", hat: "cap", cap: "#f2c230", sash: "#f4f1d0", skin: PALE };
const UMENO: Outfit = { jacket: "#6b4a2f", pants: "#3d4440", boots: INK, hat: "cap", cap: "#38506a", moustache: "#4a3426", skin: CREAM };
const CAMMAN: Outfit = { jacket: "#3f6fb5", pants: "#3b3f52", boots: "#4a3426", hat: "hair", hair: "#2a201a", skin: PALE };
const LUCKYO: Outfit = { jacket: "#2f6f73", pants: "#5a4632", boots: "#4a3426", hat: "cap", cap: "#d8433a", skin: PALE };
const FRIEND_A: Outfit = { jacket: "#c25a7a", pants: "#3b4a6b", boots: "#4a3426", hat: "hair", hair: "#8a4a2a", skin: PALE };
const FRIEND_B: Outfit = { jacket: "#f1efe6", pants: "#5a4632", boots: "#4a3426", hat: "hair", hair: "#d9a441", skin: PALE };

/** crowd on the foot of the dunes, everyone facing the whale (+z) */
const CROWD: [number, number][] = [
  [-8, -23.5], [-5.6, -23.2], [-0.6, -23.6], [4.4, -23.4], [6.9, -23.8],
  [-9.6, -26.1], [-6.8, -26.3], [-4.8, -26.6], [-1.0, -26.2], [0.6, -25.9], [4.8, -26.4], [7.4, -26.1],
  [-7.6, -28.7], [-4.4, -28.9], [-1.8, -28.5], [1.0, -29.0], [3.8, -28.8], [6.1, -28.4],
  [-5.5, -33.5], [2.5, -34.4], [8.5, -32.6], [-10.5, -31.4],
];
type Mode = "watch" | "tense" | "boom" | "fall" | "run" | "scared";
const crowd = (cam: CamInfo, t: number, tau: number, out: Stage, mode: Mode, near?: [number, number, number]) => {
  CROWD.forEach(([x0, z0], i) => {
    if (near && Math.hypot(x0 - near[0], z0 - near[1]) > near[2]) return;
    const kid = i % 6 === 4, o = kid ? KID : FOLK[i % 12], sc = kid ? 0.72 : 1;
    const who: Who = { i: i + 10, o, okey: kid ? "kid" : `f${i % 12}` };
    let x = x0, z = z0, dx = 0, dz = 1;
    let expr: Expr = (["smile", "neutral", "grin", "smile_closed"] as Expr[])[i % 4];
    let fo: FrontOpts = { mode: "stand", expr, blink: lidAt(t, i + 10), look: 0 };
    let so: SideOpts = { mode: "stand", expr, blink: lidAt(t, i + 10) };
    if (mode === "tense") { expr = i % 3 ? "nervous" : "neutral"; }
    if (mode === "boom") expr = tau < BOOM - LEAD ? "nervous" : tau < 32.0 ? "shock" : (["grin", "laugh", "relief_open", "grin"] as Expr[])[i % 4];
    if (mode === "fall" || mode === "scared") expr = i % 3 === 1 ? "nervous" : "shock";
    let wave: number | undefined = undefined;
    if (mode === "fall" && i % 3 === 0) wave = q(Math.sin(t * 9 + i * 1.3), 30);
    if (mode === "boom" && tau > 32 && i % 4 === 1) wave = q(Math.sin(t * 7 + i), 30);
    let stride = 1, walking = false;
    if (mode === "run") {
      const dir = x0 < 0 ? -1 : 1, k = Math.max(0, tau - 35.0 - hh(i, 3) * 0.4);
      x = x0 + dir * 3.2 * k; dx = dir; dz = 0; walking = k > 0; expr = "shock";
    }
    const y = H(x, z);
    const view = viewOf(cam, x, z, dx, dz);
    const ph = walking ? q(((tau * 2.4 + hh(i, 5)) % 1), 60) : 0;
    fo = { mode: walking ? "march" : "stand", phase: ph, expr, blink: lidAt(t, i + 10), look: 0, wave, lift: 80, headTilt: walking ? 0 : Math.round(2.5 * Math.sin(t * 1.3 + i * 2.1)) };
    so = { mode: walking ? "march" : "stand", phase: ph, expr, blink: lidAt(t, i + 10), stomp: 1.3, stride: stride * view.fs };
    out.places.push(person(cam, who, x, y, z, view, fo, so, sc));
    blob(out, x, y, z, sc);
  });
};

/** one named character standing (or walking) at a spot */
const one = (cam: CamInfo, out: Stage, i: number, o: Outfit, okey: string, x: number, z: number, y: number, expr: Expr, t: number,
  opts: { dx?: number; dz?: number; wave?: number; prop?: FrontOpts["prop"]; walk?: number; headTilt?: number; scale?: number } = {}) => {
  const dx = opts.dx ?? 0, dz = opts.dz ?? 1, view = viewOf(cam, x, z, dx, dz), ph = opts.walk !== undefined ? q(opts.walk % 1, 60) : 0;
  const sway = opts.headTilt ?? Math.round(2.5 * Math.sin(t * 1.4 + i * 1.7));
  const fo: FrontOpts = { mode: opts.walk !== undefined ? "stroll" : "stand", phase: ph, expr, blink: lidAt(t, i), wave: opts.wave, prop: opts.prop ?? null, headTilt: sway };
  const so: SideOpts = { mode: opts.walk !== undefined ? "march" : "stand", phase: ph, expr, blink: lidAt(t, i), stomp: 0.55, stride: 0.875 * view.fs };
  out.places.push(person(cam, { i, o, okey }, x, y, z, view, fo, so, opts.scale ?? 1));
  blob(out, x, y, z, opts.scale ?? 1);
};

// ---------------- effects ----------------
const chunkCard = (out: Stage, x: number, y: number, z: number, size: number, rot: number, seed: number) =>
  out.fx.push({ key: `chunk${seed % 5}`, cw: 256, ch: 256, draw: (p) => fxChunk(p, seed % 5), x, y, z, w: size, h: size, rot });
const splatCard = (out: Stage, x: number, y: number, z: number, size: number, seed: number) =>
  out.fx.push({ key: `splat${seed % 4}`, cw: 300, ch: 200, draw: (p) => fxSplat(p, seed % 4), x, y: y + 0.03, z, w: size, h: size * 0.66, flat: true, rot: hh(seed, 2) * 6 });
/** chunks falling out of the sky onto an area, landing between t0 and t1, then lying there as splats */
const rain = (out: Stage, tau: number, cx: number, cz: number, R: number, t0: number, t1: number, n: number, seed: number, yAt = H) => {
  for (let i = 0; i < n; i++) {
    const tl = t0 + (t1 - t0) * hh(i, seed), x = cx + (hh(i, seed + 1) - 0.5) * 2 * R, z = cz + (hh(i, seed + 2) - 0.5) * 2 * R;
    const gy = yAt(x, z), size = 0.45 + 0.6 * hh(i, seed + 3), dt = tl - tau;
    if (dt > 0 && dt < 2.4) chunkCard(out, x + dt * 0.8 * (hh(i, seed + 4) - 0.5), gy + 0.3 + 14 * dt + 3 * dt * dt, z, size, dt * 5 * (hh(i, seed + 5) - 0.5) * 2, i + seed);
    else if (dt <= 0) splatCard(out, x, gy, z, size * 1.8, i + seed);
  }
};
/** the blast throws chunks from the whale: dt seconds after the blast */
const ballistic = (out: Stage, dt: number, n = 60, toward = 1) => {
  if (dt < 0) return;
  for (let i = 0; i < n; i++) {
    const vy = 15 + 13 * hh(i, 41), vz = -toward * (1 + 13 * hh(i, 42)), vx = (hh(i, 43) - 0.5) * 18, size = 0.6 + 0.9 * hh(i, 44);
    const x = WHALE[0] + vx * dt, z = WHALE[2] + vz * dt, y = 2.5 + vy * dt - 4.9 * dt * dt;
    const g = H(x, z);
    if (y > g + 0.2) chunkCard(out, x, y, z, size, dt * 4 * (hh(i, 45) - 0.5) * 2, i);
    else splatCard(out, x, g, z, size * 1.8, i);
  }
};
const boomCloud = (out: Stage, dt: number, scale = 1) => {
  if (dt < 0 || dt > 9) return;
  const u = q(Math.min(1, dt / 3.2), 30), w = 22 * scale;
  out.fx.push({ key: `boom${u}`, cw: 800, ch: 800, draw: (p) => fxBoom(p, u), x: WHALE[0], y: w * 0.41 + 0.6 * dt * scale, z: WHALE[2], w, h: w });
  if (dt < 0.25) out.fx.push({ key: `burst${q(dt / 0.25, 30)}`, cw: 500, ch: 500, draw: (p) => fxBurst(p, q(dt / 0.25, 30), "#fff3b0", 14, 60, 245), x: WHALE[0], y: 3, z: WHALE[2] - 2, w: 14 * scale, h: 14 * scale });
};
/** seagulls standing on the whale's back, pecking */
const gullsOnWhale = (out: Stage, t: number, n = 5) => {
  for (let i = 0; i < n; i++) {
    const x = WHALE[0] - 4.5 + i * 2.1, peck = q(Math.max(0, Math.sin(t * 3 + i * 1.7)) ** 3, 10), top = 1.02 + 1.3 * (1 - Math.abs(x) / 9);
    out.fx.push({ key: `gullS${peck}`, cw: 300, ch: 300, draw: (p) => fxGullStand(p, peck), x, y: top + 0.42, z: WHALE[2] - 0.2 + (i % 2) * 0.5, w: (i % 2 ? -1 : 1) * 0.95, h: 0.95 });
  }
};
/** seagulls: circling over the whale, or fleeing out to sea after `flee` */
const gulls = (out: Stage, t: number, n: number, flee?: number, near = 1, low = 0) => {
  for (let i = 0; i < n; i++) {
    const r = (6 + 8 * hh(i, 61)) * near, a = t * (0.35 + 0.25 * hh(i, 62)) * (i % 2 ? 1 : -1) + hh(i, 63) * 6.28, hgt = (6 + 6 * hh(i, 64)) * (1 - low) + low * (3 + 2.5 * hh(i, 64));
    let x = WHALE[0] + Math.cos(a) * r, y = hgt, z = WHALE[2] + Math.sin(a) * r * 0.7;
    let flap = (t * 2.2 + hh(i, 65)) % 1, dir = Math.sin(a) * (i % 2 ? 1 : -1) > 0 ? 1 : -1;
    if (flee !== undefined && t > flee) {
      const k = t - flee - 0.2 * hh(i, 66);
      if (k > 0) { x += (hh(i, 67) - 0.5) * 10 * k; y += 3.5 * k; z += 9 * k; flap = (t * 5 + hh(i, 65)) % 1; dir = hh(i, 67) > 0.5 ? 1 : -1; }
    }
    const f = q(flap, 12), w = 1.7 + 0.5 * hh(i, 68);
    out.fx.push({ key: `gull${f}`, cw: 400, ch: 260, draw: (p) => fxGull(p, f), x, y, z, w: w * dir, h: w * 0.65 });
  }
};
const puffs = (out: Stage, t: number, pts: V3[], size = 1.2) => pts.forEach(([x, y, z], i) => {
  const u = q(((t * 1.6 + i * 0.37) % 1), 20);
  out.fx.push({ key: `puff${u}`, cw: 300, ch: 300, draw: (p) => fxPuff(p, u), x, y: y + u * 0.6, z, w: size * (0.6 + u), h: size * (0.6 + u), soft: true });
});
const arrow = (out: Stage, x: number, y: number, z: number, w: number, rot = 0, blocked = false) =>
  out.fx.push({ key: blocked ? "arrowB" : "arrow", cw: 200, ch: 400, draw: (p) => (blocked ? fxArrowBlocked(p) : fxArrow(p)), x, y, z, w, h: w * 2, rot });

/** everything with a face or a flying piece in shot `id` at frame f */
export const stage = (id: number, f: number, t: number, tau: number, cam: CamInfo): Stage => {
  const out: Stage = { places: [], fx: [] };
  const s = SHOTS[id - 1];
  LNAME = s.light;
  findSun(cam, SUN);
  const EY = H(ENG[0], ENG[2]);
  switch (s.scene) {
    case "hook":
      crowd(cam, t, tau, out, "fall", [0, -25.5, 12]);
      one(cam, out, 55, UMENO, "umen", UMEN[0], UMEN[2], UMEN[1], "shock", t);
      boomCloud(out, tau - BOOM);
      rain(out, tau, 0, -25.5, 9, 35.4, 40.2, 30, 7);
      if (f < 66) {
        out.places = out.places.filter((p) => p.key.includes("umen") || p.z > UMEN[2] + 0.4);
        out.fx = out.fx.filter((p) => !p.flat || p.z > UMEN[2] - 0.5);
        for (let k = 0; k < 9; k++) {
          const ph = (tau * 0.45 + k * 0.17) % 1, x = UMEN[0] - 3.2 + k * 0.85, z = UMEN[2] + 2.5 + (k % 3) * 2.2;
          chunkCard(out, x, UMEN[1] + 7.5 - 6.5 * ph, z, 0.7 + 0.2 * (k % 3), ph * 3 + k, k);
        }
      }
      break;
    case "arrive":
      gulls(out, t, 9); gullsOnWhale(out, t);
      for (let i = 0; i < 4; i++) one(cam, out, 40 + i, FOLK[(i * 3 + 1) % 12], `f${(i * 3 + 1) % 12}`, -6 + i * 3.6, -7 - (i % 2) * 2.5, 0, (["smile", "neutral", "grin", "smile_closed"] as Expr[])[i], t);
      break;
    case "whale":
      gulls(out, t, 4, undefined, 0.7);
      if (f >= 292) {
        one(cam, out, 50, FOLK[5], "f5", -1.6, -2.4, 0, "pained", t, { wave: 0.2 });
        for (let k = 0; k < 4; k++) { const u = q(((t * 0.5 + k * 0.25) % 1), 30); out.fx.push({ key: `stink${u}`, cw: 300, ch: 400, draw: (p) => fxStink(p, u), x: -3.2 + k * 1.6, y: 3.2 + k % 2 * 0.3, z: 1.0, w: 1.1, h: 1.47 }); }
      }
      break;
    case "bury": {
      one(cam, out, 51, WORKER, "worker", 4.3, -1.2, 0, tau < 11.6 - LEAD ? "grin" : "nervous", t, { prop: "shovel" });
      out.fx.push({ key: "moundS", cw: 300, ch: 200, draw: (p) => fxSplat(p, 9), x: 5.4, y: 0.03, z: -1.4, w: 1.4, h: 0.9, flat: true });
      const u = (tau - 11.25) / 1.2;
      if (u > 0 && u < 1) out.fx.push({ key: `splash${q(u, 30)}`, cw: 800, ch: 800, draw: (p) => fxSplash(p, q(u, 30)), x: 4.5, y: 1.6, z: 10.5, w: 7, h: 7 });
      break;
    }
    case "tow":
      one(cam, out, 52, WORKER, "worker", TRUCK_HITCH[0] + 1.4, TRUCK_HITCH[2] - 3.2, 0, tau < 13.1 ? "stern" : "nervous", t);
      puffs(out, t, [[TRUCK_HITCH[0] - 0.4, 0.3, TRUCK_HITCH[2] - 1.0], [TRUCK_HITCH[0] - 3.8, 0.3, TRUCK_HITCH[2] - 1.0]], 1.0);
      break;
    case "engineer":
      one(cam, out, 53, ENGINEER, "eng", ENG[0], ENG[2], EY, f < 476 ? "grin" : "laugh", t, { wave: f >= 476 ? q(Math.sin(t * 8), 30) : undefined });
      one(cam, out, 54, WORKER, "worker", ENG[0] - 2.4, ENG[2] - 1.5, H(ENG[0] - 2.4, ENG[2] - 1.5), "smile", t, { prop: "shovel" });
      break;
    case "gulls":
      gulls(out, t, 6, undefined, 0.55, 1); gullsOnWhale(out, t, 5);
      break;
    case "umen": {
      crowd(cam, t, tau, out, "watch", [UMEN[0], UMEN[2], 6]);
      const warn = tau >= 23.5 - LEAD;
      one(cam, out, 55, UMENO, "umen", UMEN[0], UMEN[2], UMEN[1], warn ? "stern" : "neutral", t, { wave: warn ? q(0.3 * Math.sin(t * 5), 30) : undefined });
      if (tau >= 23.9 && tau < 25.4) { const k = Math.min(1, (tau - 23.9) / 0.15); out.fx.push({ key: "bubble", cw: 400, ch: 340, draw: fxBubbleSticks, x: UMEN[0] - 0.75, y: UMEN[1] + 2.55, z: UMEN[2] + 0.1, w: 1.1 * k, h: 0.94 * k }); }
      break;
    }
    case "cases":
      one(cam, out, 56, WORKER, "worker", 3.0, -1.3, 0, "grin", t);
      one(cam, out, 57, ENGINEER, "eng", -3.9, -1.6, 0, "smile", t);
      break;
    case "gather":
      crowd(cam, t, tau, out, "watch");
      one(cam, out, 58, CAMMAN, "camman", TVCAM[0] - 0.75, TVCAM[2] - 0.4, H(TVCAM[0], TVCAM[2]), "grin", t);
      one(cam, out, 53, ENGINEER, "eng", ENG[0], ENG[2], EY, "grin", t);
      break;
    case "count":
      if (f < 897) one(cam, out, 53, ENGINEER, "eng", ENG[0], ENG[2], EY, tau < 29.85 ? "nervous" : "grin", t);
      else if (f < 913) gulls(out, t, 5, undefined, 0.8);
      else crowd(cam, t, tau, out, "tense", [0, -25.5, 10]);
      break;
    case "boom":
      crowd(cam, t, tau, out, "boom");
      boomCloud(out, tau - BOOM);
      ballistic(out, tau - BOOM);
      gulls(out, t, 6, BOOM);
      break;
    case "fall":
      boomCloud(out, tau - BOOM);
      if (f < 1045) { crowd(cam, t, tau, out, "fall", [0, -25.5, 12]); rain(out, tau, 0, -25.5, 9, 34.6, 40.2, 28, 7); }
      else if (f < 1100) { crowd(cam, t, tau, out, "run"); rain(out, tau, 0, -27, 12, 34.6, 40.2, 34, 7); }
      else if (f < 1132) rain(out, tau, 6, -40, 8, 36.5, 37.9, 26, 21);
      else {
        rain(out, tau, 2, -66, 9, 37.6, 39.2, 24, 33, (x, z) => (z < -58 && z > -84 && x > -26 && x < 22 ? LOT_Y + 0.03 : H(x, z)));
        for (const [x, z, tl, k] of [[0, -68, 38.1, 1], [6, -68.2, 38.6, 2], [12.5, -67.8, 39.0, 3]] as const) {
          const dt = tl - tau;
          if (dt > 0 && dt < 2) chunkCard(out, x, LOT_Y + 1.9 + 14 * dt + 3 * dt * dt, z, 0.9, dt * 3, k);
          else if (dt <= 0) splatCard(out, x, LOT_Y + 1.66, z, 1.4, k);
        }
      }
      break;
    case "lucky": {
      crowd(cam, t, tau, out, "scared", [LUCKY[0], LUCKY[2], 5]);
      rain(out, tau, 0, -25.5, 9, 34.6, 40.2, 28, 7);
      const hit = tau >= LUCKY_HIT - LEAD;
      one(cam, out, 59, LUCKYO, "lucky", LUCKY[0], LUCKY[2], LUCKY[1], hit ? (tau > LUCKY_HIT + 0.8 ? "dazed" : "shock") : "relief", t);
      const dt = LUCKY_HIT - tau, top = LUCKY[1] + 2.08;
      if (dt > 0 && dt < 1.6) chunkCard(out, LUCKY[0], top + 14 * dt + 3 * dt * dt, LUCKY[2] + 0.05, 0.7, dt * 4, 3);
      else if (dt <= 0) {
        chunkCard(out, LUCKY[0] + 0.03, top - 0.05, LUCKY[2] + 0.05, 0.7, 0.15, 3);
        if (dt > -0.6) out.fx.push({ key: "shock", cw: 300, ch: 300, draw: fxShockLines, x: LUCKY[0], y: LUCKY[1] + 1.95, z: LUCKY[2] + 0.02, w: 1.3, h: 1.3 });
      }
      break;
    }
    case "ketchup": {
      const ax = PACKET[0] - 0.55, walk = tau < STEP;
      const xA = walk ? ax - 1.3 * (1 - smooth((tau - 42.4) / (STEP - 42.4))) : ax;
      one(cam, out, 60, FRIEND_A, "fa", xA, PACKET[2] + 0.05, LOT_Y, tau > SQUIRT_HIT ? "shock" : "grin", t, { dx: 1, dz: 0, walk: walk ? tau * 1.4 : undefined });
      const hitB = tau >= SQUIRT_HIT;
      one(cam, out, 61, FRIEND_B, "fb", PACKET[0] + 1.6, PACKET[2] - 0.05, LOT_Y, hitB ? "shock" : "smile", t, { dx: -1, dz: 0.3 });
      out.fx.push({ key: `packet${tau >= STEP ? 1 : 0}`, cw: 300, ch: 200, draw: (p) => fxPacket(p, tau >= STEP ? 1 : 0), x: PACKET[0], y: LOT_Y + 0.05, z: PACKET[2], w: 0.75, h: 0.5, flat: true, rot: 0.1 });
      if (tau >= 46.1 && tau < 47.75) arrow(out, PACKET[0] + 0.45, LOT_Y + 0.3, PACKET[2] + 0.1, 0.17 + 0.01 * Math.sin(t * 12), 0, true);
      if (tau >= SQUIRT && tau < SQUIRT + 1.1) { const u = q(clamp01((tau - SQUIRT) / 0.5), 30); out.fx.push({ key: `squirt${u}`, cw: 600, ch: 300, draw: (p) => fxSquirt(p, u), x: PACKET[0] + 0.8, y: LOT_Y + 0.62, z: PACKET[2] - 0.05, w: -1.7, h: 0.85 }); }
      if (hitB) out.fx.push({ key: "khit", cw: 200, ch: 200, draw: fxKetchupHit, x: PACKET[0] + 1.6, y: LOT_Y + 1.15, z: PACKET[2] - 0.12, w: 0.4, h: 0.4 });
      break;
    }
    case "physics": {
      if (tau >= 50.3 && tau < UP) arrow(out, 3.0, 1.05 + 0.08 * Math.sin(t * 10), 0.3, 0.8, 0, true);
      const dt = tau - UP;
      if (dt >= 0) { boomCloud(out, dt, 0.6); ballistic(out, dt, 40); if (dt < 1.4) arrow(out, 0, 8 + 4 * dt, 0, 2.2); }
      if (f >= 1612) {
        crowd(cam, t, tau, out, "scared");
        for (const [z, k] of [[-9, 0], [-15, 1], [-21, 2]] as const) arrow(out, -0.5, 3.5 - k * 0.4, z, 1.4, 0.15);
      }
      break;
    }
    case "after":
      if (f < 1725) gulls(out, t, 14, 55.7, 0.8);
      else if (f >= 1774) {
        one(cam, out, 62, WORKER, "worker", -2.2, -3.0, 0, "neutral", t, { prop: "shovel" });
        one(cam, out, 63, WORKER, "worker", 0.9, -3.6, 0, "smile_closed", t, { prop: "shovel" });
        one(cam, out, 64, ENGINEER, "eng", 3.3, -4.4, 0, "grin", t);
        puffs(out, t, [[4.6, 0.4, -3.6], [4.4, 0.4, -1.4]], 1.4);
      }
      break;
    case "car": {
      const x0 = UCAR[0] + 4.2, x1 = UCAR[0] + 1.9, k = smooth((tau - 60.6) / 1.9), x = x0 + (x1 - x0) * k, z = UCAR[2] + 2.0;
      const walking = tau > 60.6 && tau < 62.5;
      const expr: Expr = tau >= CRUSH - LEAD ? (f >= 1935 ? "dazed" : "shock") : tau > 62.9 ? "nervous" : "whistle";
      one(cam, out, 55, UMENO, "umen", x, z, LOT_Y, expr, t, { dx: -1, dz: 0, walk: walking ? tau * 1.4 : undefined });
      const dt = tau - CRUSH;
      if (dt >= 0 && dt < 0.2) out.fx.push({ key: `burst${q(dt / 0.2, 30)}`, cw: 500, ch: 500, draw: (p) => fxBurst(p, q(dt / 0.2, 30)), x: UCAR[0], y: LOT_Y + 1.8, z: UCAR[2] + 0.6, w: 3.2, h: 3.2 });
      if (dt >= 0 && dt < 0.7) out.fx.push({ key: "shock", cw: 300, ch: 300, draw: fxShockLines, x, y: LOT_Y + 2.0, z: z + 0.05, w: 1.0, h: 1.0 });
      if (f >= 1935) { const u = q((t * 0.9) % 1, 30); out.fx.push({ key: `stars${u}`, cw: 420, ch: 210, draw: (p) => fxStars(p, u), x, y: LOT_Y + 2.3, z: z + 0.1, w: 0.7, h: 0.35 }); }
      if (dt >= 0) for (let i = 0; i < 4; i++) splatCard(out, UCAR[0] + (hh(i, 71) - 0.5) * 3.2, LOT_Y + 0.03, UCAR[2] + (hh(i, 72) - 0.5) * 5.5, 0.8, 10 + i);
      break;
    }
  }
  return out;
};
void TVCAM; void fxContact; void fxShadow; void bodyFront; void bodySide; void Pen;
