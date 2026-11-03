// "The Day Oregon Blew Up a Whale": timeline of our own short. Shots are timed to the voice (voice/lines.json),
// story physics (the blast, the chunk rain) and the camera grammar of the cartoon-3d-short skill: slow push-ins on
// every hold, smootherstep glides of 18-40 f, hard cuts on big reframes, 7-frame flip kicks on impacts.
export const FPS = 30;
export const TOTAL = 1975;
export const D0 = 0;
export type V3 = [number, number, number];

export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
export const smooth = (x: number) => { const u = clamp01(x); return u * u * (3 - 2 * u); };
export const easeOut = (u: number) => 1 - (1 - clamp01(u)) ** 4;

// ---------------- places ----------------
export const SEA_Y = -0.35;
export const LOT_Y = 7;
/** ground height: flat beach, shore sloping under the sea (z > 9), dunes rising behind (z < -20) to the plateau with
 *  the parking lot (flattened: x -26..22, z -61..-82) */
export const H = (x: number, z: number) => {
  if (z > 9) return -(z - 9) * 0.09;
  if (z > -20) return 0;
  const s = smooth((-20 - z) / 26);
  const lot = smooth((x + 30) / 4) * smooth((26 - x) / 4) * smooth((-57 - z) / 4) * smooth((z + 86) / 4);
  const bumps = 1.3 * Math.sin(x * 0.11 + 1) * Math.sin(z * 0.13) * s * (1 - s) * 4 + 0.35 * Math.sin(x * 0.07 + 2) * Math.sin(z * 0.09) * s;
  return LOT_Y * s + bumps * (1 - lot);
};
export const WHALE: V3 = [0, 0, 2];
export const WHALE_LEN = 14;
export const ENG: V3 = [10, 0, -14];
export const PLUNGER: V3 = [10.1, 0, -14.75]; // land side of the engineer: every camera now looks out to sea
export const TVCAM: V3 = [-7, 0, -18];
export const TRUCK_HITCH: V3 = [-11.5, 0, 2.6];
export const UMEN: V3 = [-3, H(-3, -24.5), -24.5];
export const UCAR: V3 = [-6, LOT_Y, -68];
export const PACKET: V3 = [17, LOT_Y, -62.4];
export const LUCKY: V3 = [2.4, H(2.4, -27), -27];

// ---------------- story clock ----------------
export const BOOM = 31.2;          // f 936, the plunger goes down on the beat after "One."
export const CRUSH = 64.05;        // the chunk lands on the car
export const LUCKY_HIT = 40.62;    // "Unluckily": a chunk lands next to the lucky man
export const STEP = 45.9;          // the foot lands on the ketchup packet
export const SQUIRT = 47.82;       // "It shoots out sideways"
export const SQUIRT_HIT = 48.35;
export const UP = 53.22;           // "Up."

// ---------------- shots ----------------
export type Light = "day" | "golden" | "night";
export type Scene = "hook" | "arrive" | "whale" | "bury" | "tow" | "engineer" | "gulls" | "umen" | "cases" | "gather" | "count" | "boom"
  | "fall" | "lucky" | "ketchup" | "physics" | "after" | "car";
export type ShotDef = { id: number; a: number; b: number; light: Light; scene: Scene; tau: (t: number) => number; sunAz?: number; sunEl?: number };
const T0 = (t: number) => t;
export const SHOTS: ShotDef[] = [
  { id: 1, a: 0, b: 124, light: "golden", scene: "hook", tau: (t) => 35.6 + t },
  { id: 2, a: 124, b: 230, light: "golden", scene: "arrive", tau: T0, sunAz: 150, sunEl: 12 },
  { id: 3, a: 230, b: 305, light: "golden", scene: "whale", tau: T0 },
  { id: 4, a: 305, b: 379, light: "golden", scene: "bury", tau: T0 },
  { id: 5, a: 379, b: 420, light: "golden", scene: "tow", tau: T0 },
  { id: 6, a: 420, b: 508, light: "golden", scene: "engineer", tau: T0 },
  { id: 7, a: 508, b: 592, light: "golden", scene: "gulls", tau: T0 },
  { id: 8, a: 592, b: 754, light: "golden", scene: "umen", tau: T0 },
  { id: 9, a: 754, b: 831, light: "golden", scene: "cases", tau: T0 },
  { id: 10, a: 831, b: 881, light: "golden", scene: "gather", tau: T0 },
  { id: 11, a: 881, b: 936, light: "golden", scene: "count", tau: T0 },
  { id: 12, a: 936, b: 1005, light: "golden", scene: "boom", tau: T0 },
  { id: 13, a: 1005, b: 1176, light: "golden", scene: "fall", tau: T0 },
  { id: 14, a: 1176, b: 1277, light: "golden", scene: "lucky", tau: T0 },
  { id: 15, a: 1277, b: 1500, light: "night", scene: "ketchup", tau: T0, sunAz: 55, sunEl: 35 },
  { id: 16, a: 1500, b: 1645, light: "night", scene: "physics", tau: T0, sunAz: 120, sunEl: 30 },
  { id: 17, a: 1645, b: 1822, light: "golden", scene: "after", tau: T0 },
  { id: 18, a: 1822, b: TOTAL, light: "golden", scene: "car", tau: T0 },
];
/** crossfades (frames) at place / time changes; a white 4-frame flash after the hook */
export const XFADE: Record<number, number> = { 15: 8, 17: 8 };
/** shot changes that are flown, not cut: the camera travels from the old framing to the new one over 2 x H frames
 *  centred on the change (reference: "the camera physically travels into the next moment"). Only time-of-day
 *  changes (14 -> 15 day to night, 16 -> 17 night to day) dissolve, and the hook ends on its flash. */
export const TRAVEL: Record<number, number> = {}; // user (3 Nov): flown changes felt too fast; cut between shots instead
export const FLASH_AT = 124;
/** frames that start a 4-frame white flash (reference: most hard changes are 4-frame flashes, not plain cuts) */
export const FLASHES = [66, 124];

export const shotAt = (f: number) => SHOTS.find((s) => f >= s.a && f < s.b) ?? SHOTS[SHOTS.length - 1];
export const layersAt = (f: number): { id: number; alpha: number }[] => {
  for (const s of SHOTS) {
    const x = XFADE[s.id];
    if (x && f >= s.a - x / 2 && f < s.a + x / 2) return [{ id: s.id - 1, alpha: 1 }, { id: s.id, alpha: (f - (s.a - x / 2) + 1) / (x + 1) }];
  }
  return [{ id: shotAt(f).id, alpha: 1 }];
};

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
const HARD = new Set([66]);
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
const pushK = (f: number, f0: number, rate: number, punch = 0, n = 35) => {
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

const C = UMEN, L = LUCKY;
const S2b = (f: number) => dolly([15, 5.5, -13], [0, 1.2, 1.5], pushK(f, 225, 0.0022), { fov: 42 }); // land side, so the travel into the head never crosses the snout
const S3b = (f: number) => dolly([-2.6, 1.55, -7.2], [-1.6, 1.45, -2.4], pushK(f, 300, 0.003), { fov: 40, roll: -0.04 });
const CAMS: Record<number, Key[]> = {
  // 1 hook: the crowd under the falling sky, low from the beach side; closer on "rain whale" (roll)
  1: [
    { f: 0, s: (f) => dolly([C[0] + 0.1, C[1] + 1.45, C[2] - 2.15], [C[0] - 0.05, C[1] + 2.35, C[2] + 6], pushK(f, 0, 0.0018, 0.004, 20), { fov: 54, roll: -0.03 }) },
    { f: 66, cut: true, s: (f) => dolly(at(1.6, -19.2, 0.9), at(0, -25.5, 1.75), pushK(f, 66, 0.0025, 0.006, 30), { fov: 44, roll: -0.03 }) },
  ],
  // 2 arrive: high over the sea, then glide down to the whale on the sand ("washes up on the beach at Florence")
  2: [
    { f: 120, s: (f) => zoom([22, 15, 34], [0, 0.5, -4], 44, pushK(f, 120, 0.0018)) },
    { f: 190, dur: 56, s: S2b },
  ],
  // 3 whale CU ("Eight tons", punch) -> the man beside it ("And it stinks", roll)
  // (reference grammar: no hard cut inside a place; the camera travels from the aerial into the whale's head, then
  //  slides along the body to the man and on to the worker)
  3: [
    { f: 230, s: (f) => dolly([12.5, 1.7, -5.5], [5.5, 1.5, 2], pushK(f, 262, 0.0025, 0.004, 20), { fov: 40 }) },
    { f: 282, dur: 34, s: S3b },
  ],
  // 4 bury: worker with a shovel, the tide behind him
  4: [{ f: 305, s: (f) => dolly([6.5, 1.4, -6.5], [4.2, 1.2, 1.5], pushK(f, 325, 0.0025), { fov: 44 }) }],
  // 5 tow: the truck straining at the tail
  5: [{ f: 379, s: (f) => dolly([-15.5, 2.2, -8.5], [-11, 1.0, 2.5], pushK(f, 379, 0.003), { fov: 44, roll: 0.03 }) }],
  // 6 engineer: MS, then closer on "blow it up" (punch + roll)
  6: [
    { f: 420, s: (f) => dolly([ENG[0] - 1.0, 1.65, ENG[2] - 5.4], [ENG[0], 1.5, ENG[2]], pushK(f, 420, 0.0025), { fov: 40 }) },
    { f: 476, dur: 20, s: (f) => dolly([ENG[0] - 0.5, 1.75, ENG[2] - 3.6], [ENG[0], 1.65, ENG[2]], pushK(f, 476, 0.002, 0.006, 30), { fov: 38, roll: 0.04 }) },
  ],
  // 7 gulls on the whale's back, low and close
  7: [{ f: 508, s: (f) => dolly([-6.5, 2.4, -9.5], [-0.5, 3.4, 2], pushK(f, 508, 0.0025), { fov: 44, roll: -0.03 }) }],
  // 8 Umenhofer in the crowd: MS -> closer when he raises his hand ("twenty sticks")
  8: [
    { f: 592, s: (f) => dolly([C[0] + 0.8, C[1] + 1.55, C[2] - 4.2], [C[0], C[1] + 1.35, C[2]], pushK(f, 592, 0.0025), { fov: 40 }) },
    { f: 700, dur: 24, s: (f) => dolly([C[0] + 0.3, C[1] + 1.7, C[2] - 3.8], [C[0] + 0.35, C[1] + 1.75, C[2]], pushK(f, 712, 0.002), { fov: 38, roll: -0.04 }) },
  ],
  // 9 cases: workers stacking -> punch into the stack on "Half a ton"
  9: [
    { f: 754, s: (f) => dolly([3.5, 1.5, -6.5], [0, 0.9, 0.2], pushK(f, 754, 0.0025), { fov: 44 }) },
    { f: 790, cut: true, s: (f) => dolly([1.4, 0.75, -3.2], [0, 0.45, 0.4], pushK(f, 790, 0.002, 0.007, 30), { fov: 40, roll: 0.045 }) },
  ],
  // 10 gather: wide over the crowd toward the whale -> the TV camera ("Cameras roll")
  10: [
    { f: 831, s: (f) => dolly([-6, 7.5, -40], [0, 0.8, -6], pushK(f, 831, 0.002), { fov: 44 }) },
    { f: 855, cut: true, s: (f) => dolly([TVCAM[0] - 3.0, 1.45, TVCAM[2] - 2.8], [TVCAM[0] - 0.2, 1.3, TVCAM[2]], pushK(f, 855, 0.003), { fov: 40, roll: 0.03 }) },
  ],
  // 11 count: engineer + plunger ("Three") -> whale and cases ("Two") -> tense faces ("One")
  11: [
    { f: 881, s: (f) => dolly([ENG[0] - 0.9, 1.35, ENG[2] - 3.4], [ENG[0] + 0.05, 1.15, ENG[2] - 0.4], pushK(f, 881, 0.004)) },
    { f: 897, cut: true, s: (f) => dolly([4, 1.3, -11], [0, 1.2, 1.5], pushK(f, 897, 0.004), { fov: 42 }) },
    { f: 913, cut: true, s: (f) => dolly(at(0.4, -29.6, 1.45), at(0, -25.5, 1.9), pushK(f, 913, 0.005), { fov: 40, roll: -0.03 }) },
    { f: 924, cut: true, s: (f) => dolly([PLUNGER[0] - 0.55, 1.05, PLUNGER[2] - 1.25], [PLUNGER[0], 0.78, PLUNGER[2]], pushK(f, 924, 0.006), { fov: 40, roll: 0.04 }) }, // insert: the plunger goes down
  ],
  // 12 boom: wide from behind the crowd, slow tilt up with the cloud
  12: [
    { f: 936, s: (f) => dolly(at(-1.6, -31.8, 1.05), [0, 3.2, 2], pushK(f, 936, 0.0012), { fov: 50 }) },
    { f: 960, dur: 40, s: (f) => dolly(at(-1.6, -31.8, 0.95), [0, 7, 2], pushK(f, 960, 0.001), { fov: 52 }) },
  ],
  // 13 fall: faces look up -> crowd runs under the rain -> dunes -> parking lot
  13: [
    { f: 1005, s: (f) => dolly(at(0.9, -30.5, 1.1), at(0, -25.5, 2.3), pushK(f, 1005, 0.0025), { fov: 44 }) },
    { f: 1045, cut: true, s: (f) => dolly(at(9, -32, 3.4), at(0, -27, 1.4), pushK(f, 1045, 0.002), { fov: 46, roll: -0.03 }) },
    { f: 1100, cut: true, s: (f) => dolly(at(4, -50, 3.0), at(5, -38, 0.6), pushK(f, 1100, 0.0025), { fov: 46 }) },
    { f: 1132, cut: true, s: (f) => dolly([2, LOT_Y + 3.0, -80], [1, LOT_Y + 0.8, -67], pushK(f, 1132, 0.0025), { fov: 46 }) },
  ],
  // 14 lucky man: relief MS -> "Unluckily" (kick)
  14: [
    { f: 1176, s: (f) => dolly([L[0] + 0.9, L[1] + 1.65, L[2] - 4.2], [L[0], L[1] + 1.55, L[2]], pushK(f, 1176, 0.0025), { fov: 40 }) },
    { f: 1212, dur: 18, s: (f) => dolly([L[0] + 0.3, L[1] + 1.6, L[2] - 3.3], [L[0] + 0.3, L[1] + 1.5, L[2]], pushK(f, 1220, 0.002), { fov: 40, roll: 0.04 }) },
  ],
  // 15 ketchup (golden, parking lot): two friends -> the foot on the packet -> the squirt
  15: [
    { f: 1270, s: (f) => dolly([PACKET[0] + 0.5, LOT_Y + 1.3, PACKET[2] - 6.4], [PACKET[0] + 0.5, LOT_Y + 1.0, PACKET[2]], pushK(f, 1270, 0.0022), { fov: 54 }) },
    { f: 1347, cut: true, s: (f) => dolly([PACKET[0] - 0.15, LOT_Y + 0.5, PACKET[2] - 1.7], [PACKET[0], LOT_Y + 0.2, PACKET[2]], pushK(f, 1347, 0.003), { fov: 46, roll: 0.03 }) },
    { f: 1434, cut: true, s: (f) => dolly([PACKET[0] + 0.5, LOT_Y + 1.2, PACKET[2] - 6.2], [PACKET[0] + 0.5, LOT_Y + 0.95, PACKET[2]], pushK(f, 1434, 0.002, 0.006, 25), { fov: 54, roll: -0.04 }) },
  ],
  // 16 physics (golden, the beach): low side view of whale + cases -> tilt up on "Up." -> pan to the people
  16: [
    { f: 1494, s: (f) => dolly([3, 2.6, -17], [0, 1.4, 1.5], pushK(f, 1494, 0.002), { fov: 44 }) },
    { f: 1590, dur: 22, s: (f) => dolly([3, 2.4, -19], [0, 8, 1.5], pushK(f, 1590, 0.0015), { fov: 50 }) },
    { f: 1612, dur: 34, s: (f) => dolly([5, 12, -40], [0, 3, -8], pushK(f, 1626, 0.002), { fov: 48, roll: 0.03 }) },
  ],
  // 17 after: gulls fleeing over the sea -> the whale still lying there -> the crew burying it
  17: [
    { f: 1641, s: (f) => dolly([-6, 2.5, -9], [-1, 7, 6], pushK(f, 1641, 0.002), { fov: 46 }) },
    { f: 1725, cut: true, s: (f) => dolly([7.5, 2.2, -7.5], [0, 1.0, 1.5], pushK(f, 1725, 0.0025), { fov: 44 }) },
    { f: 1774, cut: true, s: (f) => dolly([1.5, 4.0, -18], [0.8, 1.0, -1.5], pushK(f, 1774, 0.0022), { fov: 48, roll: 0.03 }) },
  ],
  // 18 car: Umenhofer walks to his car -> looks up ("biggest chunk") -> crush on "car" (kick) -> dazed
  18: [
    { f: 1819, s: (f) => dolly([UCAR[0] + 5.2, LOT_Y + 1.8, UCAR[2] - 7.0], [UCAR[0] - 0.5, LOT_Y + 1.2, UCAR[2]], pushK(f, 1819, 0.0022), { fov: 42 }) },
    { f: 1887, cut: true, s: (f) => dolly([UCAR[0] + 3.4, LOT_Y + 0.9, UCAR[2] - 5.0], [UCAR[0], LOT_Y + 3.4, UCAR[2]], pushK(f, 1887, 0.0025), { fov: 46, roll: 0.04 }) },
    { f: 1935, cut: true, s: (f) => dolly([UCAR[0] + 3.4, LOT_Y + 1.75, UCAR[2] - 5.6], [UCAR[0] + 1.2, LOT_Y + 1.45, UCAR[2] - 1.0], pushK(f, 1935, 0.0018), { fov: 42, roll: -0.03 }) },
  ],
};

/** near framing props (reference: ~38 % of MS/CU have one): placed on the ground `dist` m ahead of the lens at frame a,
 *  `lat` m to the side (+ = screen right), visible a <= f < b */
export type Fg = { a: number; b: number; kind: "grass" | "crate" | "log" | "stake"; dist: number; lat: number; s?: number };
export const FOREGROUND: Fg[] = [
  { a: 317, b: 379, kind: "log", dist: 3.6, lat: 0.45 },
  { a: 420, b: 508, kind: "crate", dist: 3.2, lat: -0.62 },
  { a: 592, b: 754, kind: "grass", dist: 3.0, lat: 0.78, s: 1.7 },
  { a: 855, b: 881, kind: "grass", dist: 3.0, lat: -0.62, s: 1.6 },
  { a: 1176, b: 1277, kind: "grass", dist: 2.8, lat: -1.05, s: 1.6 },
  { a: 1774, b: 1822, kind: "grass", dist: 5.5, lat: -1.1, s: 2.0 },
];

// impact kicks: image offset flips sign every frame, decays to 0 in 7 f
const KICKS: [number, number][] = [[BOOM, 1.8], [BOOM + 0.25, 0.8], [35.6, 0.35], [36.5, 0.35], [LUCKY_HIT, 1.0], [SQUIRT_HIT, 0.5], [UP, 0.8], [CRUSH, 1.6]];
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
  { f: 0, cInf: 5, focus: () => [UMEN[0], UMEN[1] + 1.8, UMEN[2]] }, { f: 66, cInf: 14 },
  { f: 124, cInf: 0 },
  { f: 230, dur: 66, cInf: 7 }, { f: 282, dur: 34, cInf: 8 },
  { f: 300, dur: 30, cInf: 6 }, { f: 379, cInf: 0 },
  { f: 420, cInf: 7 }, { f: 476, dur: 20, cInf: 8 },
  { f: 508, cInf: 10 },
  { f: 592, cInf: 12, focus: () => [UMEN[0], UMEN[1] + 1.75, UMEN[2]] }, { f: 700, dur: 24, cInf: 14, focus: () => [UMEN[0], UMEN[1] + 1.75, UMEN[2]] },
  { f: 754, cInf: 6 }, { f: 790, cInf: 14 },
  { f: 831, cInf: 0 }, { f: 855, cInf: 12 },
  { f: 881, cInf: 14 }, { f: 897, cInf: 6 }, { f: 913, cInf: 14 }, { f: 924, cInf: 14, focus: () => [PLUNGER[0], 0.85, PLUNGER[2]] },
  { f: 936, cInf: 0 },
  { f: 1005, cInf: 12 }, { f: 1045, cInf: 0 },
  { f: 1176, cInf: 12, focus: () => [LUCKY[0], LUCKY[1] + 1.75, LUCKY[2]] },
  { f: 1277, cInf: 8 }, { f: 1347, cInf: 14 }, { f: 1434, cInf: 7 },
  { f: 1500, cInf: 0 },
  { f: 1645, cInf: 0 }, { f: 1725, cInf: 6 }, { f: 1774, cInf: 0 },
  { f: 1822, cInf: 7, focus: () => [UCAR[0] + 2.4, LOT_Y + 1.75, UCAR[2] - 2.0] }, { f: 1887, cInf: 5 }, { f: 1935, cInf: 10, focus: () => [UCAR[0] + 1.9, LOT_Y + 1.75, UCAR[2] - 2.0] },
];
export const dofAt = (f: number) => {
  let i = 0; while (i + 1 < DOF.length && f >= DOF[i + 1].f) i++;
  const d = DOF[i], p = DOF[Math.max(0, i - 1)];
  const k = Math.min(1, (f - d.f) / (d.dur ?? 20));
  return { cInf: p.cInf + (d.cInf - p.cInf) * k, focus: d.focus };
};
