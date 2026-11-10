// "Australia Lost a War to Emus" (1932): timeline of Blunderloop short #3. Engine and rules from short #2:
// clean cuts, slow push-ins (capped), subject + context from frame 0 (frame 0 = thumbnail), no blink at the start.
export const FPS = 30;
export const TOTAL = 1445;
export const D0 = 0;
export type V3 = [number, number, number];
export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
export const smooth = (x: number) => { const u = clamp01(x); return u * u * (3 - 2 * u); };
export const easeOut = (u: number) => 1 - (1 - clamp01(u)) ** 4;

// ---------------- places ----------------
export const H = (_x: number, _z: number) => 0;
export const MAJOR: V3 = [0, 0, -20];
export const GUN: V3 = [1.6, 0, -18.4];
export const DAM: V3 = [14, 0, 26];
export const FARM: V3 = [-30, 0, 70];
export const KID_AT: V3 = [-60, 0, -70];
export const ROAD_Z = -34;

// ---------------- story clock (seconds of the voice) ----------------
export const JAM = 18.6;
export const BUMPS = [21.5, 22.3, 23.1, 24.0, 24.9];
/** the army truck along the road / across the field: x position and bounce at time tau */
export const truckAt = (scene: Scene, tau: number): { x: number; z: number; yaw: number; bounce: number } => {
  if (scene === "truck") { const k = tau - 20.0; return { x: -30 + 9 * k, z: 6, yaw: Math.PI / 2, bounce: 0.18 * Math.abs(Math.sin(k * 9)) }; }
  if (scene === "home") { const k = Math.max(0, tau - 34.4); return { x: -6 - 7 * k, z: ROAD_Z, yaw: -Math.PI / 2, bounce: 0.04 * Math.abs(Math.sin(k * 7)) }; }
  return { x: 6, z: -24, yaw: -Math.PI / 2, bounce: 0 };
};

// ---------------- shots ----------------
export type Light = "day" | "golden" | "night";
export type Scene = "hook" | "farm" | "army" | "dayone" | "dam" | "ambush" | "jam" | "truck" | "aim" | "herd" | "popcorn" | "home"
  | "back" | "bullets" | "wheat" | "twist";
export type ShotDef = { id: number; a: number; b: number; light: Light; scene: Scene; tau: (t: number) => number; sunAz?: number; sunEl?: number };
const T0 = (t: number) => t;
export const SHOTS: ShotDef[] = [
  { id: 1, a: 0, b: 119, light: "golden", scene: "hook", tau: T0 },
  { id: 2, a: 119, b: 221, light: "golden", scene: "farm", tau: T0 },
  { id: 3, a: 221, b: 364, light: "golden", scene: "army", tau: T0 },
  { id: 4, a: 364, b: 428, light: "golden", scene: "dayone", tau: T0 },
  { id: 5, a: 428, b: 505, light: "golden", scene: "dam", tau: T0 },
  { id: 6, a: 505, b: 532, light: "golden", scene: "ambush", tau: T0 },
  { id: 7, a: 532, b: 600, light: "golden", scene: "jam", tau: T0 },
  { id: 8, a: 600, b: 742, light: "golden", scene: "truck", tau: T0 },
  { id: 9, a: 742, b: 777, light: "golden", scene: "aim", tau: T0 },
  { id: 10, a: 777, b: 969, light: "night", scene: "herd", tau: T0 },
  { id: 11, a: 969, b: 1032, light: "night", scene: "popcorn", tau: T0 },
  { id: 12, a: 1032, b: 1100, light: "golden", scene: "home", tau: T0 },
  { id: 13, a: 1100, b: 1226, light: "golden", scene: "bullets", tau: T0 },
  { id: 14, a: 1226, b: 1269, light: "golden", scene: "wheat", tau: T0 },
  { id: 15, a: 1269, b: TOTAL, light: "golden", scene: "twist", tau: T0 },
];
export const XFADE: Record<number, number> = { 10: 8, 12: 8 };
export const FLASH_AT = -100;
export const FLASHES: number[] = [];
export const TRAVEL: Record<number, number> = {};
export const shotAt = (f: number) => SHOTS.find((s) => f >= s.a && f < s.b) ?? SHOTS[SHOTS.length - 1];
export const layersAt = (f: number): { id: number; alpha: number }[] => {
  for (const s of SHOTS) {
    const x = XFADE[s.id];
    if (x && f >= s.a - x / 2 && f < s.a + x / 2) return [{ id: s.id - 1, alpha: 1 }, { id: s.id, alpha: (f - (s.a - x / 2) + 1) / (x + 1) }];
  }
  return [{ id: shotAt(f).id, alpha: 1 }];
};
export type Fg = { a: number; b: number; kind: "grass" | "crate" | "log" | "stake"; dist: number; lat: number; s?: number };
export const FOREGROUND: Fg[] = [];

// ---------------- camera ----------------
export type Cam = { pos: V3; look: V3; fov: number; roll: number };
type Shot = Partial<Cam> & { pos: V3; look: V3 };
type Key = { f: number; dur?: number; cut?: boolean; s: (f: number) => Shot };
export const glide = (u: number) => { const x = clamp01(u); return x * x * x * (x * (6 * x - 15) + 10); };
const mixCam = (a: Cam, b: Cam, k: number): Cam => ({
  pos: a.pos.map((v, i) => v + (b.pos[i] - v) * k) as V3, look: a.look.map((v, i) => v + (b.look[i] - v) * k) as V3,
  fov: a.fov + (b.fov - a.fov) * k, roll: a.roll + (b.roll - a.roll) * k,
});
const full = (c: Shot): Cam => ({ fov: 40, roll: 0, ...c });
/** frames that stay true cuts (they sit under a white flash) */
const HARD = new Set<number>([]);
/** lift of the camera path at the middle of a move (m): arcs over whatever lies between two framings */
const dirOf = (c: Cam) => { const d = c.look.map((v, i) => v - c.pos[i]) as V3, L = Math.hypot(...d) || 1; return { u: d.map((v) => v / L) as V3, L }; };
/** angle (deg) between two framings' view axes */
export const turnDeg = (a: Cam, b: Cam) => { const A = dirOf(a).u, B = dirOf(b).u; return (Math.acos(Math.max(-1, Math.min(1, A[0] * B[0] + A[1] * B[1] + A[2] * B[2]))) * 180) / Math.PI; };
/** one continuous move: position on a lifted arc, view direction turned at an even rate (slerp), look distance and
 *  lens eased; so a framing on the other side of a subject is reached by a smooth swing, never a flip */
const arc = (a: Cam, b: Cam, u: number): Cam => {
  const d = Math.hypot(b.pos[0] - a.pos[0], b.pos[1] - a.pos[1], b.pos[2] - a.pos[2]), lift = Math.min(9, Math.max(0, (d - 4) * 0.22));
  const k = glide(u), m = mixCam(a, b, k), A = dirOf(a), B = dirOf(b);
  const om = Math.acos(Math.max(-1, Math.min(1, A.u[0] * B.u[0] + A.u[1] * B.u[1] + A.u[2] * B.u[2])));
  let dir: V3 = m.look.map((v, i) => v - m.pos[i]) as V3;
  if (om > 1e-3) { const s0 = Math.sin((1 - k) * om) / Math.sin(om), s1 = Math.sin(k * om) / Math.sin(om); dir = [0, 1, 2].map((i) => A.u[i] * s0 + B.u[i] * s1) as V3; }
  const len = A.L + (B.L - A.L) * k, n = Math.hypot(...dir) || 1;
  const pos: V3 = [m.pos[0], m.pos[1] + lift * Math.sin(Math.PI * k), m.pos[2]];
  return { ...m, pos, look: [pos[0] + (dir[0] / n) * len, pos[1] + (dir[1] / n) * len, pos[2] + (dir[2] / n) * len] };
};
const run = (keys: Key[], f: number) => {
  let cur = full(keys[0].s(f));
  for (let i = 1; i < keys.length; i++) {
    const k = keys[i];
    if (k.cut) { if (f < k.f) break; cur = full(k.s(f)); continue; } // user: clean cuts between angles
    // a former cut glides in, centred a little before its word: 10 f early, 14-32 f long (until the next key)
    const nextF = keys[i + 1]?.f ?? Infinity;
    const start = k.cut ? k.f - 10 : k.f, dur = k.cut ? Math.max(14, Math.min(32, nextF - k.f + 6)) : k.dur ?? 24;
    if (f < start) break;
    cur = arc(cur, full(k.s(f)), (f - start) / dur);
  }
  return cur;
};
const T = (f: number) => f / FPS;
/** push-in: the subject grows ~rate per frame. Capped at 15 % closer per key (lesson from short #2: an uncapped punch
 *  pushed the opening close-up until only a cap filled the frame and the subject left it). */
const pushK = (f: number, f0: number, rate: number, punch = 0, n = 35) => Math.max(0.85, pushRaw(f, f0, rate, punch, n));
const pushRaw = (f: number, f0: number, rate: number, punch = 0, n = 35) => {
  const x = Math.max(0, f - f0);
  let s = rate * x;
  if (punch > rate) for (let i = 0; i < Math.min(x, n); i++) s += (punch - rate) * Math.max(0, Math.min(1, (i + 0.5) / 8, (n - i - 0.5) / 8));
  return Math.exp(-s);
};
const dolly = (pos: V3, look: V3, k: number, rest: Partial<Cam> = {}): Shot =>
  ({ pos: [look[0] + (pos[0] - look[0]) * k, look[1] + (pos[1] - look[1]) * k, look[2] + (pos[2] - look[2]) * k], look, ...rest });
const zoom = (pos: V3, look: V3, fov: number, k: number, rest: Partial<Cam> = {}): Shot =>
  ({ pos, look, fov: (360 / Math.PI) * Math.atan(Math.tan((fov * Math.PI) / 360) * k), ...rest });
const rolled = (s: (f: number) => Shot, roll: number) => (f: number): Shot => ({ ...s(f), roll });
const at = (x: number, z: number, dy: number): V3 => [x, H(x, z) + dy, z];

const M = MAJOR, G = GUN, D = DAM, K = KID_AT;
const CAMS: Record<number, Key[]> = {
  // 1 hook (frame 0 = thumbnail): the major's shocked face, emus charging through the wheat right behind him
  1: [{ f: 0, s: (f) => dolly([M[0] + 0.15, 1.45, M[2] - 2.4], [M[0] + 0.2, 2.2, M[2] + 8], pushK(f, 0, 0.0012), { fov: 52, roll: -0.02 }) }],
  // 2 the farm: wide over the wheat (farmhouse, windpump), then the emus eating it, an angry farmer
  2: [{ f: 119, s: (f) => dolly([24, 13, -18], [-12, 3, 45], pushK(f, 119, 0.0016), { fov: 46 }) },
      { f: 150, cut: true, s: (f) => dolly([4, 1.6, 9], [0, 1.0, 22], pushK(f, 150, 0.0022), { fov: 46 }) }],
  // 3 the army: major, two soldiers, two guns, ammunition boxes
  3: [{ f: 221, s: (f) => dolly([M[0] + 1.2, 1.7, M[2] - 7.5], [M[0] + 0.6, 1.3, M[2]], pushK(f, 221, 0.0018), { fov: 46 }) }],
  // 4 day one: the emus run out of range
  4: [{ f: 364, s: (f) => dolly([M[0] - 3, 2.6, M[2] - 6], [M[0] + 2, 1.5, M[2] + 30], pushK(f, 364, 0.0016), { fov: 48 }) }],
  // 5 the dam: a thousand emus walking toward the water
  5: [{ f: 428, s: (f) => dolly([D[0] - 4, 15, D[2] - 32], [D[0] - 14, 0, D[2] - 1], pushK(f, 428, 0.0016), { fov: 48 }) }],
  // 6 "Perfect ambush": the major grinning behind a bush
  6: [{ f: 505, s: (f) => dolly([M[0] - 0.6, 1.5, M[2] - 4.6], [M[0] + 0.4, 1.4, M[2] + 2], pushK(f, 505, 0.002), { fov: 44 }) }],
  // 7 the gun fires and jams
  7: [{ f: 532, s: (f) => dolly([G[0] - 2.4, 1.4, G[2] - 3.6], [G[0] + 0.4, 1.0, G[2] + 1.5], pushK(f, 532, 0.002), { fov: 46, roll: 0.03 }) }],
  // 8 the truck: soldier grinning on it, then the chase across the field
  8: [{ f: 600, s: (f) => { const x = -30 + 9 * (f / 30 - 20.0); return dolly([x + 3.5, 2.2, 6 - 6.5], [x, 1.6, 6], 1, { fov: 44 }); } },
      { f: 633, cut: true, s: (f) => { const x = -30 + 9 * (f / 30 - 20.0); return dolly([x - 12, 5, 6 - 16], [x + 12, 1, 6], 1, { fov: 50 }); } }],
  // 9 the gunner bouncing, can't aim
  9: [{ f: 742, s: (f) => { const x = -30 + 9 * (f / 30 - 20.0); return dolly([x + 1.4, 2.4, 6 - 4.2], [x - 1.2, 2.1, 6], 1, { fov: 42, roll: 0.04 }); } }],
  // 10 night: one big herd splits into small groups, each with a lookout (high wide)
  10: [{ f: 777, s: (f) => dolly([0, 13, -16], [0, 0, 20], pushK(f, 777, 0.0012), { fov: 56 }) }],
  // 11 popcorn
  11: [{ f: 969, s: (f) => dolly([K[0] + 0.3, 1.2, K[2] - 3.4], [K[0], 1.3, K[2]], pushK(f, 969, 0.002), { fov: 46 }) }],
  // 12 the army goes home (truck down the road, emus watching), then comes back
  12: [{ f: 1032, s: (f) => dolly([-8, 3.2, ROAD_Z - 16], [-14, 1.2, ROAD_Z + 4], pushK(f, 1032, 0.0016), { fov: 48 }) }],
  // 13 bullets: soldiers firing, the pile of empty shells growing; one emu untouched
  13: [{ f: 1100, s: (f) => dolly([G[0] - 1.6, 1.7, G[2] - 5.4], [G[0] - 1.2, 1.0, G[2] + 1], pushK(f, 1100, 0.002), { fov: 48 }) },
       { f: 1169, cut: true, s: (f) => dolly([2, 1.5, 4], [0, 1.3, 13], pushK(f, 1169, 0.002), { fov: 44 }) }],
  // 14 the wheat: emus eating, farmer slumped
  14: [{ f: 1226, s: (f) => dolly([4, 1.6, 9], [0, 1.0, 22], pushK(f, 1226, 0.002), { fov: 46 }) }],
  // 15 twist: the major saluting an emu in a helmet; a column of emus marching like tanks behind them
  15: [{ f: 1269, s: (f) => dolly([M[0] + 1.0, 1.6, M[2] - 5.6], [M[0] + 0.8, 1.5, M[2]], pushK(f, 1269, 0.0018), { fov: 46 }) }],
};

// impact kicks: image offset flips sign every frame, decays to 0 in 7 f
const KICKS: [number, number][] = [[JAM, 0.9], [17.95, 0.4], [18.15, 0.4], ...BUMPS.map((t): [number, number] => [t, 0.7])];
export const kickAt = (t: number) => {
  let a = 0;
  for (const [t0, g] of KICKS) {
    const n = Math.floor((t - t0) * FPS + 1e-6);
    if (n >= 0 && n < 7) a += g * (n % 2 ? -1 : 1) * (1 - n / 7) ** 1.5;
  }
  return a;
};
const base = (id: number, f: number) => run(CAMS[id], f);
const join = (a: Cam, b: Cam, f: number, b0: number, H: number) => arc(a, b, (f - (b0 - H)) / (2 * H));
/** half-length of the flown change into shot `id`: at least TRAVEL[id], longer for big turns (~0.28 f per degree), <= 45 */
const HL = new Map<number, number>();
const halfLen = (id: number) => {
  let h = HL.get(id);
  if (h === undefined) { const b0 = SHOTS[id - 1].a; h = Math.min(45, Math.max(TRAVEL[id], Math.round(turnDeg(base(id - 1, b0), base(id, b0)) * 0.28))); HL.set(id, h); }
  return h;
};
export const camAt = (id: number, f: number): Cam => {
  let c = base(id, f);
  const s = SHOTS[id - 1], nx = SHOTS[id];
  if (TRAVEL[id] && f < s.a + halfLen(id)) c = join(base(id - 1, f), c, f, s.a, halfLen(id));
  if (nx && TRAVEL[nx.id] && f >= nx.a - halfLen(nx.id)) c = join(c, base(nx.id, f), f, nx.a, halfLen(nx.id));
  const a = kickAt(T(f));
  if (!a) return c;
  const d: V3 = [c.look[0] - c.pos[0], c.look[1] - c.pos[1], c.look[2] - c.pos[2]];
  const Ln = Math.hypot(...d), h = Math.hypot(d[0], d[2]) || 1;
  const m = (3 / 640) * Math.tan((c.fov * Math.PI) / 360) * Ln * a;
  return { ...c, look: [c.look[0] - (d[2] / h) * m, c.look[1] + 0.6 * m, c.look[2] + (d[0] / h) * m], roll: c.roll + a * 0.004 };
};



// ---------------- lens ----------------
export type Dof = { f: number; dur?: number; cInf: number; focus?: (f: number) => V3 };
export const DOF: Dof[] = [
  { f: 0, cInf: 3, focus: () => [M[0], 1.8, M[2]] }, { f: 119, cInf: 0 }, { f: 150, cInf: 5 }, { f: 221, cInf: 4, focus: () => [M[0], 1.6, M[2]] }, { f: 364, cInf: 0 },
  { f: 505, cInf: 6 }, { f: 532, cInf: 6 }, { f: 600, cInf: 4 }, { f: 633, cInf: 0 }, { f: 742, cInf: 5 }, { f: 777, cInf: 0 }, { f: 969, cInf: 6 },
  { f: 1032, cInf: 0 }, { f: 1100, cInf: 5 }, { f: 1169, cInf: 4 }, { f: 1226, cInf: 4, focus: () => [3.0, 1.7, 13.8] }, { f: 1269, cInf: 4, focus: () => [M[0], 1.6, M[2]] },
];
export const dofAt = (f: number) => {
  let i = 0; while (i + 1 < DOF.length && f >= DOF[i + 1].f) i++;
  const d = DOF[i], p = DOF[Math.max(0, i - 1)];
  const k = Math.min(1, (f - d.f) / (d.dur ?? 20));
  return { cInf: p.cInf + (d.cInf - p.cInf) * k, focus: d.focus };
};
