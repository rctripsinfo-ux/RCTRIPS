// 2D effect cards for the whale short (our own drawings, same plum ink as the cast): blubber chunks, splats,
// seagulls, stink lines, the explosion cloud, arrows, ketchup packet + squirt, a speech bubble with dynamite sticks.
import { Pen, INK } from "./toon";

type P2 = [number, number];
const rnd = (seed: number, k: number) => { const x = Math.sin(seed * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
const blobRing = (cx: number, cy: number, rx: number, ry: number, seed: number, n = 14, wob = 0.22): P2[] => {
  const pts: P2[] = [];
  for (let i = 0; i <= 48; i++) {
    const a = (i / 48) * Math.PI * 2;
    let r = 1;
    for (let k = 1; k <= 3; k++) r += (wob / k) * Math.sin(a * (k + 1) + rnd(seed, k) * 6.28);
    r += 0.06 * Math.sin(a * n + seed);
    pts.push([cx + Math.cos(a) * rx * r, cy + Math.sin(a) * ry * r]);
  }
  return pts;
};

/** blubber chunk (canvas 256 x 256): grey whale skin on one side, pale pink blubber on the torn side */
export const fxChunk = (p: Pen, seed: number) => {
  const out = blobRing(128, 128, 96, 78, seed);
  p.poly(out, "#f0cfc0", 0);
  p.clip(out, () => {
    p.poly(blobRing(70 + 30 * rnd(seed, 4), 92, 110, 90, seed + 3), "#5d6476", 0);
    p.poly(blobRing(60 + 30 * rnd(seed, 4), 80, 70, 40, seed + 5), "#737b8f", 0);
    p.stroke([[150, 120], [176, 150], [196, 140]], 9, "#d27f86");
    p.stroke([[120, 176], [150, 186]], 7, "#d27f86");
  });
  p.poly(out, null, 11);
};

/** chunk that has landed: flattened, with a few drops around (canvas 300 x 200, seen from above / grazing) */
export const fxSplat = (p: Pen, seed: number) => {
  for (let i = 0; i < 6; i++) {
    const a = rnd(seed, i) * 6.28, d = 105 + 25 * rnd(seed, i + 9);
    p.ell(150 + Math.cos(a) * d, 100 + Math.sin(a) * d * 0.55, 10 + 8 * rnd(seed, i + 3), 7 + 5 * rnd(seed, i + 5), "#e7c2b6", 5);
  }
  const out = blobRing(150, 100, 95, 62, seed, 9, 0.28);
  p.poly(out, "#efc9bb", 0);
  p.clip(out, () => { p.poly(blobRing(110, 80, 80, 50, seed + 2), "#5d6476", 0); p.stroke([[160, 110], [205, 120]], 8, "#d27f86"); });
  p.poly(out, null, 10);
};

/** seagull in flight (canvas 400 x 260), wings by flap phase 0..1: white head and belly, grey wings with black
 *  white-spotted tips, yellow beak with the red spot, dark eye, tucked orange feet */
export const fxGull = (p: Pen, flap: number) => {
  const w = Math.sin(flap * Math.PI * 2);
  const tipY = 60 - 80 * w, midY = 118 - 32 * w;
  for (const s of [-1, 1]) {
    const wing: P2[] = [[200 - s * 4, 136], [200 + s * 60, midY - 6], [200 + s * 130, (midY + tipY) / 2 - 4], [200 + s * 185, tipY], [200 + s * 150, tipY + 26], [200 + s * 96, midY + 30], [200 + s * 36, 160]];
    p.poly(wing, "#aab4c4", 8);
    p.poly([[200 + s * 150, tipY + 8], [200 + s * 185, tipY], [200 + s * 158, tipY + 28], [200 + s * 132, (midY + tipY) / 2 + 12]], "#23242c", 0);
    p.dot(200 + s * 166, tipY + 12, 4, "#ffffff");
    p.poly([[200 + s * 10, 140], [200 + s * 60, midY + 4], [200 + s * 70, midY + 16], [200 + s * 20, 152]], "#d5dbe5", 0);
  }
  p.poly([[132, 150], [100, 136], [104, 166]], "#f4f5f8", 7); // tail
  p.ell(196, 152, 62, 28, "#ffffff", 8);
  p.ell(252, 134, 28, 24, "#ffffff", 8);
  p.poly([[274, 132], [312, 140], [274, 148]], "#f3c232", 6);
  p.dot(298, 143, 4, "#d8352f");
  p.dot(258, 128, 5, "#1d1a24");
  p.stroke([[176, 176], [166, 188]], 5, "#f08a3c"); p.stroke([[196, 178], [188, 190]], 5, "#f08a3c");
};
/** seagull standing (canvas 300 x 300), facing right; peck = 0..1 head dip */
export const fxGullStand = (p: Pen, peck: number) => {
  const hy = 92 + 40 * peck, hx = 196 + 14 * peck;
  p.stroke([[136, 230], [132, 284]], 7, "#f08a3c"); p.stroke([[160, 232], [164, 284]], 7, "#f08a3c");
  p.stroke([[122, 286], [142, 286]], 6, "#f08a3c"); p.stroke([[154, 286], [176, 286]], 6, "#f08a3c");
  p.poly([[70, 196], [34, 182], [44, 212]], "#23242c", 6); // black tail tip
  p.ell(146, 196, 82, 46, "#ffffff", 9);
  p.poly([[78, 176], [130, 160], [196, 182], [178, 214], [96, 214]], "#aab4c4", 7); // folded wing
  p.poly([[78, 176], [96, 214], [64, 202]], "#23242c", 0);
  p.stroke([[190, 170], [hx - 6, hy + 18]], 34, "#ffffff");
  p.ell(hx, hy, 34, 30, "#ffffff", 8);
  p.poly([[hx + 28, hy - 2], [hx + 66, hy + 6], [hx + 28, hy + 14]], "#f3c232", 6);
  p.dot(hx + 52, hy + 9, 4, "#d8352f");
  p.dot(hx + 10, hy - 6, 5.5, "#1d1a24");
};

/** stink lines (canvas 300 x 400), t = 0..1 loop */
export const fxStink = (p: Pen, t: number) => {
  for (let k = 0; k < 3; k++) {
    const x0 = 70 + k * 80, pts: P2[] = [];
    for (let i = 0; i <= 20; i++) { const y = 380 - i * 17; pts.push([x0 + 22 * Math.sin(i * 0.7 + t * 6.28 + k * 2), y - t * 30]); }
    p.line(pts, "#b7d36a", 12);
  }
};

/** explosion cloud (canvas 800 x 800), u = 0..1 age: a hot flash early, then a mushroom of sand and smoke */
export const fxBoom = (p: Pen, u: number) => {
  const g = Math.min(1, u * 3), hot = Math.max(0, 1 - u * 3);
  const capY = 640 - 400 * g, capR = 90 + 200 * g, colW = 70 + 70 * g;
  // dust skirt along the sand
  p.ell(400, 720, 140 + 220 * g, 46 + 30 * g, "#d7c4a2", 12);
  // column
  p.poly([[400 - colW, 730], [400 + colW, 730], [400 + colW * 0.7, capY + 40], [400 - colW * 0.7, capY + 40]], "#cbb89a", 12);
  // cap: filled body + lobes round it
  const lobes: [number, number, number][] = [];
  for (let i = 0; i < 9; i++) { const a = Math.PI + (i / 8) * Math.PI; lobes.push([400 + Math.cos(a) * capR * 0.8, capY + Math.sin(a) * capR * 0.55 + 20, capR * (0.34 + 0.06 * rnd(7, i))]); }
  for (const [x, y, r] of lobes) p.ell(x, y, r, r * 0.85, "#cbb89a", 12);
  p.ell(400, capY + 30, capR * 0.95, capR * 0.5, "#cbb89a", 12);
  p.ell(400, capY + 30, capR * 0.95 - 6, capR * 0.5 - 6, "#cbb89a", 0);
  for (const [x, y, r] of lobes) p.ell(x - r * 0.15, y - r * 0.2, r * 0.7, r * 0.6, "#efe2c8", 0);
  p.ell(400 - capR * 0.2, capY, capR * 0.5, capR * 0.25, "#f6eddb", 0);
  if (hot > 0) {
    const r = 120 + 160 * (1 - hot);
    p.ell(400, 660, r, r * 0.8, "#ff9a3a", 12);
    p.ell(400, 660, r * 0.66, r * 0.52, "#ffe27a", 0);
    p.ell(400, 660, r * 0.3, r * 0.24, "#fffbe8", 0);
  }
};

/** fat cartoon arrow pointing up (canvas 200 x 400) */
export const fxArrow = (p: Pen, col = "#ffd23f") => {
  p.poly([[70, 380], [130, 380], [130, 170], [180, 170], [100, 30], [20, 170], [70, 170]], col, 12);
};
/** blocked arrow: points down into a bar (canvas 200 x 400) */
export const fxArrowBlocked = (p: Pen, col = "#ffd23f") => {
  p.poly([[70, 20], [130, 20], [130, 200], [180, 200], [100, 320], [20, 200], [70, 200]], col, 12);
  p.poly([[10, 340], [190, 340], [190, 384], [10, 384]], "#b98a54", 12);
};

/** ketchup packet lying flat (canvas 300 x 200); squashed 0..1 */
export const fxPacket = (p: Pen, squashed: number) => {
  const h = 70 * (1 - 0.5 * squashed), y0 = 100 - h / 2;
  p.poly([[30, y0], [270, y0], [270, y0 + h], [30, y0 + h]], "#e23a2f", 10);
  p.poly([[110, y0 + 12], [190, y0 + 12], [190, y0 + h - 12], [110, y0 + h - 12]], "#ffffff", 0);
  p.ell(150, 100, 20, Math.max(6, h / 2 - 20), "#e23a2f", 0);
};
/** ketchup squirt: a thick red stream along a curve, growing with u (canvas 600 x 300, travels to the right) */
export const fxSquirt = (p: Pen, u: number) => {
  const n = Math.max(2, Math.round(24 * Math.min(1, u * 1.6))), pts: P2[] = [];
  for (let i = 0; i <= n; i++) { const x = 30 + (i / 24) * 540; pts.push([x, 250 - 140 * Math.sin((i / 24) * Math.PI * 0.8)]); }
  p.line(pts, "#d8231c", 26);
  const e = pts[pts.length - 1];
  p.ell(e[0], e[1], 26, 22, "#d8231c", 10);
};
/** ketchup splat on a shirt (canvas 200 x 200) */
export const fxKetchupHit = (p: Pen) => {
  const out = blobRing(100, 100, 70, 60, 3, 7, 0.3);
  p.poly(out, "#d8231c", 9);
  p.ell(80, 82, 16, 10, "#f26a5a", 0);
};

/** speech bubble with a small bundle of dynamite sticks inside (canvas 400 x 340) */
export const fxBubbleSticks = (p: Pen) => {
  p.poly([[90, 250], [70, 330], [150, 260]], "#ffffff", 10);
  p.ell(200, 150, 180, 120, "#ffffff", 10);
  for (let i = 0; i < 4; i++) {
    const x = 120 + i * 42;
    p.poly([[x, 90], [x + 34, 90], [x + 34, 210], [x, 210]], "#e2453c", 7);
    p.stroke([[x + 17, 90], [x + 22, 66], [x + 30, 56]], 5, INK);
  }
  p.poly([[110, 140], [290, 140], [290, 160], [110, 160]], "#f1e3c2", 6);
};

/** big "!" style shock lines around a head (canvas 300 x 300) */
export const fxShockLines = (p: Pen) => {
  for (let i = 0; i < 7; i++) {
    const a = -Math.PI * 0.95 + i * (Math.PI * 0.9 / 6);
    p.stroke([[150 + Math.cos(a) * 95, 170 + Math.sin(a) * 95], [150 + Math.cos(a) * 140, 170 + Math.sin(a) * 140]], 11, INK);
  }
};

/** surf foam strip (canvas 1024 x 64): scalloped white edge */
export const fxFoam = (p: Pen, seed: number) => {
  const pts: P2[] = [[0, 64]];
  for (let i = 0; i <= 64; i++) pts.push([i * 16, 24 + 12 * Math.sin(i * 0.9 + seed) + 6 * Math.sin(i * 2.3 + seed * 2)]);
  pts.push([1024, 64]);
  p.poly(pts, "#ffffff", 0);
};
