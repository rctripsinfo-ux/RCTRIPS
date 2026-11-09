// usage: node scripts/render.mjs <Comp> <out.mp4> [from-to] [scale] [concurrency]
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import path from "node:path";
const [comp, out, range, scale = "1", conc = "1"] = process.argv.slice(2);
const chromiumOptions = { gl: process.env.GL || "swangle" };
const browserExecutable = process.env.CHROME || null;
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts"), publicDir: path.resolve("public") });
const inputProps = process.env.PROPS ? JSON.parse(process.env.PROPS) : {};
const composition = await selectComposition({ serveUrl, id: comp, chromiumOptions, browserExecutable, inputProps });
const frameRange = range && range !== "all" ? range.split("-").map(Number) : null;
const t0 = Date.now(); let last = 0;
await renderMedia({ composition, serveUrl, codec: "h264", crf: 16, outputLocation: out, scale: Number(scale), concurrency: Number(conc),
  frameRange, inputProps, chromiumOptions, browserExecutable, timeoutInMilliseconds: 600000, muted: true,
  onProgress: ({ renderedFrames }) => { if (renderedFrames - last >= 10) { last = renderedFrames; console.log("frames", renderedFrames, ((Date.now() - t0) / 1000).toFixed(0) + "s"); } } });
console.log("done", ((Date.now() - t0) / 1000).toFixed(1) + "s");
process.exit(0);
