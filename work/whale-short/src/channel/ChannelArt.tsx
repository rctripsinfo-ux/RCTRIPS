// Channel art for "Blunderloop": profile picture (800x800) and banner (2560x1440, everything that matters inside the
// 1546x423 centre area that every device shows). Drawn with the same toon/fx code as the shorts, on a 2D canvas.
import React, { useEffect, useRef, useState } from "react";
import { AbsoluteFill, continueRender, delayRender, staticFile } from "remotion";
import { Pen, bodyFront, Outfit, INK } from "../videos/whale/toon";
import { fxBoom, fxGull, fxChunk } from "../videos/whale/fx70";

const HERO: Outfit = { jacket: "#e8742c", pants: "#3b4a6b", boots: "#4a3426", hat: "cap", cap: "#2f6fb5", skin: "#fbf8f4", moustache: "#4a3426" };
const PAL = { gold: "#ffd23f", ink: INK, sky0: "#3d5aa8", sky1: "#9f86c7", sky2: "#ffb27a", sky3: "#ffd59a" };
const useFont = () => {
  const [ok, setOk] = useState(false);
  const [h] = useState(() => delayRender("font"));
  useEffect(() => {
    const f = new FontFace("Mont", `url(${staticFile("fonts/montserrat-latin-900-normal.woff2")})`, { weight: "900" });
    f.load().then((ff) => { document.fonts.add(ff); setOk(true); continueRender(h); });
  }, [h]);
  return ok;
};
/** draw fn into the canvas once the font is ready */
const Canvas: React.FC<{ w: number; h: number; draw: (g: CanvasRenderingContext2D) => void }> = ({ w, h, draw }) => {
  const ref = useRef<HTMLCanvasElement>(null), font = useFont();
  useEffect(() => { if (font && ref.current) draw(ref.current.getContext("2d")!); }, [font, draw]);
  return <canvas ref={ref} width={w} height={h} style={{ width: w, height: h }} />;
};
/** place a drawing made in (dw x dh) design units at (x, y) top-left, width w */
const at = (g: CanvasRenderingContext2D, x: number, y: number, s: number, fn: (p: Pen) => void, flip = false) => {
  g.save(); g.translate(x, y); g.scale(flip ? -s : s, s); if (flip) g.translate(0, 0); fn(new Pen(g)); g.restore();
};
/** thick looping arrow (the "loop"): a ~300 deg ring with an arrow head, ink outlined */
const loopArrow = (g: CanvasRenderingContext2D, cx: number, cy: number, r: number, w: number, a0 = -0.35 * Math.PI, sweep = 1.68 * Math.PI) => {
  g.lineCap = "round";
  const ring = (lw: number, col: string) => { g.beginPath(); g.arc(cx, cy, r, a0, a0 + sweep); g.strokeStyle = col; g.lineWidth = lw; g.stroke(); };
  ring(w + w * 0.42, PAL.ink); ring(w, PAL.gold);
  const a = a0 + sweep, tx = cx + r * Math.cos(a), ty = cy + r * Math.sin(a), dx = -Math.sin(a), dy = Math.cos(a), nx = Math.cos(a), ny = Math.sin(a);
  const L = w * 1.7, Wd = w * 1.25;
  const tri = [[tx + dx * L, ty + dy * L], [tx + nx * Wd, ty + ny * Wd], [tx - nx * Wd, ty - ny * Wd]];
  g.beginPath(); tri.forEach(([x, y], i) => (i ? g.lineTo(x, y) : g.moveTo(x, y))); g.closePath();
  g.lineJoin = "round"; g.lineWidth = w * 0.42; g.strokeStyle = PAL.ink; g.stroke(); g.fillStyle = PAL.gold; g.fill();
};
const title = (g: CanvasRenderingContext2D, text: [string, string], x: number, y: number, size: number) => {
  g.font = `900 ${size}px Mont`; g.textBaseline = "middle"; g.lineJoin = "round";
  const w1 = g.measureText(text[0]).width, w2 = g.measureText(text[1]).width, x0 = x - (w1 + w2) / 2;
  for (const [t, xx, col] of [[text[0], x0, "#ffffff"], [text[1], x0 + w1, PAL.gold]] as const) {
    g.lineWidth = size * 0.2; g.strokeStyle = PAL.ink; g.strokeText(t, xx, y + size * 0.06);
    g.strokeText(t, xx, y); g.fillStyle = col; g.fillText(t, xx, y);
  }
};
const sky = (g: CanvasRenderingContext2D, w: number, h: number, horizon: number) => {
  const gr = g.createLinearGradient(0, 0, 0, horizon);
  gr.addColorStop(0, PAL.sky0); gr.addColorStop(0.45, PAL.sky1); gr.addColorStop(0.8, PAL.sky2); gr.addColorStop(1, PAL.sky3);
  g.fillStyle = gr; g.fillRect(0, 0, w, horizon);
  const sea = g.createLinearGradient(0, horizon, 0, horizon + h * 0.08); sea.addColorStop(0, "#f1a982"); sea.addColorStop(1, "#4a6fb8");
  g.fillStyle = sea; g.fillRect(0, horizon, w, h * 0.08);
  const sand = g.createLinearGradient(0, horizon + h * 0.08, 0, h); sand.addColorStop(0, "#f2c77a"); sand.addColorStop(1, "#d99a52");
  g.fillStyle = sand; g.fillRect(0, horizon + h * 0.08, w, h);
};

export const Avatar: React.FC = () => (
  <AbsoluteFill>
    <Canvas w={800} h={800} draw={(g) => {
      const bg = g.createRadialGradient(400, 360, 60, 400, 400, 560); bg.addColorStop(0, "#ffd59a"); bg.addColorStop(0.55, "#ff9a6a"); bg.addColorStop(1, "#6b4fa8");
      g.fillStyle = bg; g.fillRect(0, 0, 800, 800);
      loopArrow(g, 400, 400, 292, 46);
      // shocked hero, head and shoulders inside the ring
      at(g, 400 - 300 * 1.25, 150, 1.25, (p) => bodyFront(p, HERO, { mode: "stand", expr: "shock", light: -2.1, seed: 3, wave: 0.6 }));
      // a blubber chunk flying past
      at(g, 560, 300, 0.55, (p) => fxChunk(p, 2));
    }} />
  </AbsoluteFill>
);

export const Banner: React.FC = () => (
  <AbsoluteFill>
    <Canvas w={2560} h={1440} draw={(g) => {
      const W = 2560, H = 1440, hz = 860;
      sky(g, W, H, hz);
      // decorative edges (seen only on TV / desktop): explosion far right, gulls, chunks
      at(g, 2050, 260, 0.9, (p) => fxBoom(p, 1));
      at(g, 120, 330, 1.1, (p) => fxGull(p, 0.2)); at(g, 350, 220, 0.8, (p) => fxGull(p, 0.6)); at(g, 1700, 110, 0.7, (p) => fxGull(p, 0.4));
      at(g, 300, 520, 0.6, (p) => fxChunk(p, 1)); at(g, 2300, 640, 0.55, (p) => fxChunk(p, 3));
      // ---- safe area (1546 x 423, centred): hero + title + tagline ----
      const sx = (W - 1546) / 2, sy = (H - 423) / 2;
      at(g, sx + 10, sy - 18, 0.47, (p) => bodyFront(p, HERO, { mode: "stand", expr: "shock", light: -2.1, seed: 3, wave: 0.6 }));
      loopArrow(g, sx + 300 + 640, sy + 165, 0, 0, 0, 0);
      title(g, ["BLUNDER", "LOOP"], sx + 300 + 640, sy + 170, 168);
      g.font = "900 50px Mont"; g.textAlign = "left";
      const tag = "TRUE STORIES THAT WENT HILARIOUSLY WRONG", tw = g.measureText(tag).width, tx = sx + 300 + 640 - tw / 2, ty = sy + 330;
      g.fillStyle = PAL.ink; g.beginPath(); g.roundRect(tx - 34, ty - 44, tw + 68, 88, 44); g.fill();
      g.fillStyle = PAL.gold; g.textBaseline = "middle"; g.fillText(tag, tx, ty + 3);
      // small loop arrow wrapped around the "O" of LOOP is implied by the title colour; a ring sits behind the hero
    }} />
  </AbsoluteFill>
);
