// Analytic camera check over the whole (old-clock) timeline: per-frame screen speed estimate in 720p px/frame
// (rotation of the view axis x focal length + translation of the look point / distance), flags moves above the gate.
import { SHOTS, camAt, TOTAL } from "../out/campath_story.mjs";
const fpx = (fov) => 640 / Math.tan((fov * Math.PI) / 360); // 720x1280: half-height 640 px
let prev = null, worst = [];
const shotOf = (f) => SHOTS.find((s) => f >= s.a && f < s.b) ?? SHOTS[SHOTS.length - 1];
for (let f = 0; f < TOTAL; f++) {
  const s = shotOf(f), c = camAt(s.id, f);
  const d = c.look.map((v, i) => v - c.pos[i]), L = Math.hypot(...d), u = d.map((v) => v / L);
  if (prev && prev.id === s.id || (prev && prev.id !== s.id)) {
    const dot = Math.min(1, u[0] * prev.u[0] + u[1] * prev.u[1] + u[2] * prev.u[2]);
    const rot = Math.acos(dot) * fpx(c.fov);
    const tr = Math.hypot(...c.pos.map((v, i) => v - prev.pos[i])) / L * fpx(c.fov) * 0.5;
    const zoom = Math.abs(Math.log(Math.tan((c.fov * Math.PI) / 360) / Math.tan((prev.fov * Math.PI) / 360))) * 734;
    const sp = rot + tr + zoom;
    worst.push([f, s.id, Math.round(sp)]);
  }
  prev = { id: s.id, u, pos: c.pos, fov: c.fov };
}
const big = worst.filter((w) => w[2] > 40);
console.log("frames > 40 px/f:", big.length, " max:", Math.max(...worst.map((w) => w[2])));
const runs = []; for (const w of big) { const r = runs[runs.length - 1]; if (r && w[0] - r[1] <= 2) { r[1] = w[0]; r[2] = Math.max(r[2], w[2]); } else runs.push([w[0], w[0], w[2], w[1]]); }
console.log(runs.map((r) => `f${r[0]}-${r[1]} shot${r[3]} peak ${r[2]}`).join("\n"));
