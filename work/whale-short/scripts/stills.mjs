// usage: node scripts/stills.mjs <Comp> <outPrefix> <f,f,...> [scale]   (bundles once; Chromium with SwiftShader/ANGLE GL)
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";
const [comp, prefix, frames, scale = "0.5"] = process.argv.slice(2);
const chromiumOptions = { gl: process.env.GL || "swangle" };
const browserExecutable = process.env.CHROME || null;
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts"), publicDir: path.resolve("public") });
const inputProps = process.env.PROPS ? JSON.parse(process.env.PROPS) : {};
const composition = await selectComposition({ serveUrl, id: comp, chromiumOptions, browserExecutable, inputProps });
const onBrowserLog = (l) => { if (l.type === "error" || l.type === "warning") console.log(`[${l.type}]`, l.text.slice(0, 300)); };
for (const f of frames.split(",").map(Number)) {
  const t0 = Date.now();
  await renderStill({ composition, serveUrl, frame: f, output: `${prefix}${f}.${process.env.PNG ? "png" : "jpg"}`, imageFormat: process.env.PNG ? "png" : "jpeg", ...(process.env.PNG ? {} : { jpegQuality: 88 }), scale: Number(scale),
    chromiumOptions, browserExecutable, inputProps, timeoutInMilliseconds: 300000, onBrowserLog });
  console.log("still", f, ((Date.now() - t0) / 1000).toFixed(1) + "s");
}
process.exit(0);
