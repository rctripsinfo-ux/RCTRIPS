// "The Tower That Fell Over For 200 Years": timeline of our second Blunderloop short (Pisa). Same engine and camera
// grammar as the whale short: clean cuts between angles, slow push-ins inside a shot, kicks on impacts.
export const FPS = 30;
export const TOTAL = 1755;
export const D0 = 0;
export type V3 = [number, number, number];
export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
export const smooth = (x: number) => { const u = clamp01(x); return u * u * (3 - 2 * u); };
export const easeOut = (u: number) => 1 - (1 - clamp01(u)) ** 4;

// ---------------- places ----------------
export const H = (_x: number, _z: number) => 0;
export const TOWER_R = 7.8;
export const BUILDER: V3 = [-4.5, 0, -19];
export const ARCH: V3 = [5.5, 0, -17];
export const MATTRESS: V3 = [-45, 0, -60];
export const RIG: V3 = [-14, 0, -6];
export const TOURIST: V3 = [3.5, 0, -24];

// ---------------- story clock (seconds of the voice) ----------------
export const LEAN_HIT = 13.0;   // "starts to lean"
export const CLOSE_HIT = 36.9;  // "They close it."
export const WORKS = 44.0;      // "It works."
export const QUAKE = 51.8, QUAKE_END = 57.5;
export const QUAKE_HITS = [51.85, 52.6, 53.4, 54.5, 55.9];
/** floors standing (0..8, fractional = the top floor rising) and the lean (deg) of the base axis */
export const floorsAt = (scene: Scene, tau: number) => {
  if (scene === "hook") return 7;
  if (tau < 10.5) return 1 + smooth((tau - 6.4) / 3.2);
  if (tau < 20) return 2 + smooth((tau - 10.7) / 1.8);
  if (tau < 26.5) return 3 + 4 * smooth((tau - 21.2) / 3.8);
  return 8;
};
export const leanAt = (scene: Scene, tau: number) => {
  if (scene === "hook") return 5.5;
  if (tau < 26.5) return 3.8 * smooth((tau - 12.4) / 1.6) + 1.0 * smooth((tau - 21.2) / 3.8);
  if (tau < 34) return 4.8 + 0.7 * smooth((tau - 32.1) / 1.8);
  if (tau < 44) return 5.5;
  return 5.5 - 1.5 * smooth((tau - 44.0) / 2.6);
};
/** the tower's settling into the clay (m), shown in the explanation */
export const sinkAt = (tau: number) => (tau > 26.5 && tau < 34 ? 0.9 * smooth((tau - 32.1) / 1.6) : 0);

// ---------------- shots ----------------
export type Light = "day" | "golden" | "night";
export type Scene = "hook" | "start" | "marble" | "plan" | "lean" | "war" | "back" | "idea" | "banana" | "clay" | "mattress" | "sank"
  | "1990" | "fix" | "works" | "pose" | "quake";
export type ShotDef = { id: number; a: number; b: number; light: Light; scene: Scene; tau: (t: number) => number; sunAz?: number; sunEl?: number };
const T0 = (t: number) => t;
export const SHOTS: ShotDef[] = [
  { id: 1, a: 0, b: 157, light: "golden", scene: "hook", tau: T0 },
  { id: 2, a: 157, b: 268, light: "golden", scene: "start", tau: T0 },
  { id: 3, a: 268, b: 291, light: "golden", scene: "marble", tau: T0 },
  { id: 4, a: 291, b: 316, light: "golden", scene: "plan", tau: T0 },
  { id: 5, a: 316, b: 429, light: "golden", scene: "lean", tau: T0 },
  { id: 6, a: 429, b: 522, light: "golden", scene: "war", tau: T0 },
  { id: 7, a: 522, b: 600, light: "golden", scene: "back", tau: T0 },
  { id: 8, a: 600, b: 754, light: "golden", scene: "idea", tau: T0 },
  { id: 9, a: 754, b: 797, light: "golden", scene: "banana", tau: T0 },
  { id: 10, a: 797, b: 867, light: "night", scene: "clay", tau: T0 },
  { id: 11, a: 867, b: 964, light: "night", scene: "mattress", tau: T0 },
  { id: 12, a: 964, b: 1024, light: "night", scene: "sank", tau: T0 },
  { id: 13, a: 1024, b: 1129, light: "golden", scene: "1990", tau: T0 },
  { id: 14, a: 1129, b: 1319, light: "golden", scene: "fix", tau: T0 },
  { id: 15, a: 1319, b: 1460, light: "golden", scene: "works", tau: T0 },
  { id: 16, a: 1460, b: 1529, light: "golden", scene: "pose", tau: T0 },
  { id: 17, a: 1529, b: TOTAL, light: "golden", scene: "quake", tau: T0 },
];
export const XFADE: Record<number, number> = { 10: 8, 13: 8 };
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

const B = BUILDER, A = ARCH, M = MATTRESS, G = RIG, U = TOURIST;
const CAMS: Record<number, Key[]> = {
  // 1 hook: low close-up on the builder's shocked face, the leaning tower behind him (thumbnail)
  1: [{ f: 0, s: (f) => dolly([B[0] - 0.1, 1.4, B[2] - 2.3], [B[0] + 0.45, 3.4, B[2] + 8], pushK(f, 0, 0.0022, 0.004, 20), { fov: 50, roll: -0.03 }) }],
  // 2 1173: wide over the square, the first floor going up, the cathedral beyond
  2: [{ f: 157, s: (f) => dolly([30, 14, -48], [-6, 4, 2], pushK(f, 157, 0.0018), { fov: 46 }) },
      { f: 220, dur: 40, s: (f) => dolly([16, 6, -32], [0, 4, 0], pushK(f, 240, 0.002), { fov: 46 }) }],
  // 3 "White marble": a worker hammering a block
  3: [{ f: 268, s: (f) => dolly([A[0] - 4.2, 1.2, A[2] - 2.6], [A[0] - 3.1, 0.7, A[2] - 0.2], pushK(f, 268, 0.004), { fov: 42, roll: 0.03 }) }],
  // 4 "Eight floors": the architect with his plan
  4: [{ f: 291, s: (f) => dolly([A[0] + 0.6, 1.65, A[2] - 3.8], [A[0] + 0.5, 1.5, A[2]], pushK(f, 291, 0.004), { fov: 42 }) }],
  // 5 floor three goes up, then the lean (kick)
  5: [{ f: 316, s: (f) => dolly([2, 3.5, -46], [0, 11, 0], pushK(f, 316, 0.0018), { fov: 44 }) },
      { f: 400, dur: 24, s: (f) => dolly([B[0] + 0.9, 1.65, B[2] - 3.8], [B[0], 1.55, B[2]], pushK(f, 400, 0.003), { fov: 42, roll: 0.04 }) }],
  // 6 war: the builders run off
  6: [{ f: 429, s: (f) => dolly([10, 2.6, -36], [0, 4, -12], pushK(f, 429, 0.002), { fov: 46, roll: -0.03 }) }],
  // 7 back a century later: old builders look up
  7: [{ f: 522, s: (f) => dolly([-0.5, 1.5, -27], [0, 6, 0], pushK(f, 522, 0.0022), { fov: 52 }) }],
  // 8 the idea: architect points; the new floors go up, taller on the short side
  8: [{ f: 600, s: (f) => dolly([A[0] + 0.6, 1.65, A[2] - 3.8], [A[0] + 0.5, 1.5, A[2]], pushK(f, 600, 0.003), { fov: 42 }) },
      { f: 632, cut: true, s: (f) => dolly([0, 18, -78], [0, 22, 0], pushK(f, 632, 0.0015), { fov: 44 }) },
      { f: 733, cut: true, s: (f) => dolly([10, 40, -40], [-3, 50, 0], pushK(f, 733, 0.003), { fov: 42, roll: 0.04 }) }],
  // 9 banana: side-on wide
  9: [{ f: 754, s: (f) => dolly([0, 20, -95], [0, 26, 0], pushK(f, 754, 0.002), { fov: 44 }) }],
  // 10 night: the base pressing into the soft ground
  10: [{ f: 797, s: (f) => dolly([20, 5, -28], [3, 2, -3], pushK(f, 797, 0.0025), { fov: 46 }) }],
  // 11 the mattress
  11: [{ f: 867, s: (f) => dolly([M[0] + 0.4, 1.3, M[2] - 4.6], [M[0], 1.0, M[2]], pushK(f, 867, 0.0025), { fov: 44 }) }],
  // 12 the heavier it got, the deeper it sank
  12: [{ f: 964, s: (f) => dolly([0, 6, -70], [0, 18, 0], pushK(f, 964, 0.0025), { fov: 44, roll: 0.03 }) }],
  // 13 1990: tourists under the leaning tower -> it is closed
  13: [{ f: 1024, s: (f) => dolly([U[0] + 1.0, 1.6, U[2] - 4.6], [U[0], 2.2, U[2] + 4], pushK(f, 1024, 0.0022), { fov: 48 }) },
       { f: 1106, cut: true, s: (f) => dolly([-2, 1.7, -28], [0, 1.6, -18], pushK(f, 1106, 0.003), { fov: 44, roll: -0.03 }) }],
  // 14 the fix: cables, lead weights, the drill rig
  14: [{ f: 1129, s: (f) => dolly([-34, 9, -30], [-4, 14, 0], pushK(f, 1129, 0.0018), { fov: 46 }) },
       { f: 1210, cut: true, s: (f) => dolly([G[0] + 4.5, 1.6, G[2] - 6.5], [G[0] + 2.6, 1.3, G[2] - 1.6], pushK(f, 1210, 0.0025), { fov: 46, roll: 0.03 }) }],
  // 15 it works, then they stop on purpose
  15: [{ f: 1319, s: (f) => dolly([0, 16, -80], [0, 25, 0], pushK(f, 1319, 0.0015), { fov: 44 }) },
       { f: 1408, cut: true, s: (f) => dolly([G[0] + 3.0, 1.65, G[2] - 5.6], [G[0] + 1.6, 1.5, G[2] - 1.6], pushK(f, 1408, 0.003), { fov: 42 }) }],
  // 16 tourists "holding up" the tower
  16: [{ f: 1460, s: (f) => dolly([U[0] + 0.5, 1.7, U[2] - 7], [U[0] - 0.5, 4.2, U[2] + 10], pushK(f, 1460, 0.0025), { fov: 50 }) }],
  // 17 the quake: wide, shaking; the tower stays up; close on a tourist
  17: [{ f: 1529, s: (f) => dolly([24, 8, -60], [0, 20, 0], pushK(f, 1529, 0.0015), { fov: 46 }) },
       { f: 1674, cut: true, s: (f) => dolly([U[0] + 0.5, 1.7, U[2] - 7], [U[0] - 0.5, 4.2, U[2] + 10], pushK(f, 1674, 0.0022), { fov: 50 }) }],
};

// impact kicks: image offset flips sign every frame, decays to 0 in 7 f
const KICKS: [number, number][] = [[LEAN_HIT, 1.2], [13.9, 0.5], [CLOSE_HIT, 0.8], [WORKS, 0.6], ...QUAKE_HITS.map((t): [number, number] => [t, 1.3])];
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
  { f: 0, cInf: 5, focus: () => [B[0], 1.8, B[2]] }, { f: 157, cInf: 0 }, { f: 268, cInf: 8 }, { f: 291, cInf: 8 }, { f: 316, cInf: 0 },
  { f: 400, cInf: 8 }, { f: 429, cInf: 0 }, { f: 600, cInf: 7 }, { f: 632, cInf: 0 }, { f: 797, cInf: 4 }, { f: 867, cInf: 7 },
  { f: 964, cInf: 0 }, { f: 1024, cInf: 5 }, { f: 1106, cInf: 6 }, { f: 1129, cInf: 0 }, { f: 1210, cInf: 6 }, { f: 1319, cInf: 0 },
  { f: 1408, cInf: 7 }, { f: 1460, cInf: 4 }, { f: 1529, cInf: 0 }, { f: 1674, cInf: 4 },
];
export const dofAt = (f: number) => {
  let i = 0; while (i + 1 < DOF.length && f >= DOF[i + 1].f) i++;
  const d = DOF[i], p = DOF[Math.max(0, i - 1)];
  const k = Math.min(1, (f - d.f) / (d.dur ?? 20));
  return { cInf: p.cInf + (d.cInf - p.cInf) * k, focus: d.focus };
};
