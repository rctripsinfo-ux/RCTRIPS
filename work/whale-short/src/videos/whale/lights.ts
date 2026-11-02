// Light presets per time of day. The sun is CAMERA-RELATIVE and frozen per shot (world.ts update()):
// az = degrees from the shot camera's forward axis (0 = sun straight ahead = backlight, +90 = screen right,
// 180 = behind camera), el = elevation. lit/shade/lift are LINEAR RGB multipliers for shade.ts (may exceed 1).
// Field names follow lighting.md 9.1 exactly (the CHAR and POST agents read them); values are tuned on renders.
type C3 = [number, number, number];
export type LightPreset = {
  az: number; el: number;
  lit: C3; shade: C3; lift: C3; lambert: number; sideK: number; term: number;      // world two-tone (shade.ts)
  charTint: C3; charShade: number; charGrad: number; bodyGrad: number; sideTint: C3; // character cards (cast.ts)
  blob: C3; actorShadow: boolean;                                                    // contact blobs / card shadows
  top: string; hor: string; skyCurve: C3; fog: string; fogNear: number; fogFar: number; sunDisc: string; // depth.md 6.5
  sunCol: string; sunI: number; sky: string; ground: string; hemiI: number;         // three lights (unpatched mats only)
  bias: number; normalBias: number;
};
export type LightName = "day" | "golden" | "night";
export const LIGHTS: Record<LightName, LightPreset> = {
  day: {
    az: 62, el: 40,
    lit: [1.55, 1.46, 1.3], shade: [0.42, 0.38, 0.5], lift: [0.05, 0.06, 0.11], lambert: 0.35, sideK: 0.84, term: 0.2,
    charTint: [1.0, 0.94, 0.92], charShade: 0.86, charGrad: 0.07, bodyGrad: 0.2, sideTint: [0.92, 0.90, 0.96],
    blob: [0.62, 0.58, 0.58], actorShadow: false,
    top: "#3e7fd2", hor: "#b8d0ec", skyCurve: [0.0, 0.5, 0.6], fog: "#b8d0ec", fogNear: 25, fogFar: 300, sunDisc: "#000000",
    sunCol: "#fff3e0", sunI: 2.8, sky: "#dcecff", ground: "#b49a78", hemiI: 0.55,
    bias: -0.00025, normalBias: 0.015,
  },
  golden: { // late afternoon: warm key from the side-back, violet shade, colours kept (reference day/sunset blend)
    az: 40, el: 20,
    lit: [1.5, 1.24, 0.92], shade: [0.27, 0.26, 0.46], lift: [0.04, 0.05, 0.13], lambert: 0.35, sideK: 0.84, term: 0.12,
    charTint: [1.0, 0.9, 0.8], charShade: 0.88, charGrad: 0.09, bodyGrad: 0.22, sideTint: [0.88, 0.84, 0.96],
    blob: [0.7, 0.68, 0.86], actorShadow: true,
    top: "#4f7fc8", hor: "#ffcf9a", skyCurve: [0.05, 0.6, 1.0], fog: "#f2c9a0", fogNear: 45, fogFar: 380, sunDisc: "#ffd9a8",
    sunCol: "#ffcf9a", sunI: 4.0, sky: "#c9c8e0", ground: "#8a6a60", hemiI: 0.5,
    bias: -0.0006, normalBias: 0.03,
  },
  night: {
    az: 40, el: 32,
    lit: [0.62, 0.72, 1.12], shade: [0.11, 0.13, 0.32], lift: [0.03, 0.05, 0.16], lambert: 0.35, sideK: 0.84, term: 0.15,
    charTint: [0.80, 0.86, 1.06], charShade: 0.86, charGrad: 0.08, bodyGrad: 0.22, sideTint: [0.82, 0.86, 1.0],
    blob: [0.55, 0.6, 0.85], actorShadow: false,
    top: "#0e1838", hor: "#33478a", skyCurve: [0.0, 0.5, 0.6], fog: "#2b3d78", fogNear: 35, fogFar: 320, sunDisc: "#000000",
    sunCol: "#b8ccff", sunI: 1.4, sky: "#4a5ea8", ground: "#1d2244", hemiI: 0.4,
    bias: -0.0004, normalBias: 0.02,
  },
};

/** world-only look per light (sky stops by elevation in degrees, river colours, cloud palette). All colours are
 *  ON-SCREEN targets under the current PBR-Neutral tone map; world.ts pre-inverts the tone map (shade.ts untone). */
export type WorldLook = {
  sky: { c: string[]; e: number[] };                         // 5 stops: c[i] at elevation e[i] (deg), smoothstep between
  water: { near: string; mid: string; far: string; crest: string; trough: string; glint: string; shade: C3 };
  bounce: C3;                                                 // shade.ts uBounce: albedo x bounce on shaded faces turned to the lens
  sat: number;                                                // shade.ts uSat: world albedo saturation (1 = as painted)
  cloud: { lit: string; mid: string; shade: string };
};
export const LOOK: Record<LightName, WorldLook> = {
  day: {
    // depth.md 2.2: horizon #9fb6e6 just above the skyline, upper sky #5e93d9 at ~20 deg (grade: frame top #5997e2)
    sky: { c: ["#b8d0ec", "#9cbfea", "#6a9fe0", "#4f8cdb", "#3373cc"], e: [0, 3, 8, 16, 40] },
    water: { near: "#22a7b6", mid: "#167fb2", far: "#1a5596", crest: "#7ddfe8", trough: "#0e4a80", glint: "#ffffff", shade: [0.5, 0.56, 0.72] },
    cloud: { lit: "#fbf8f1", mid: "#e1e5f3", shade: "#c3cbe9" },
    bounce: [0, 0, 0],
    sat: 1.08,
  },
  golden: {
    sky: { c: ["#ffd3a0", "#f6c8a6", "#c9c3d6", "#88a6d8", "#4f7fc8"], e: [0, 4, 10, 20, 42] },
    water: { near: "#2a6fa0", mid: "#3d82b0", far: "#e0b090", crest: "#ffd9b8", trough: "#173f6a", glint: "#fff0d0", shade: [0.45, 0.5, 0.75] },
    cloud: { lit: "#ffe0bc", mid: "#f2b8a0", shade: "#a9a0cc" },
    bounce: [0.03, 0.02, 0.0],
    sat: 1.12,
  },
  night: {
    sky: { c: ["#3b5196", "#2e4386", "#22336f", "#18275a", "#0d1638"], e: [0, 3, 9, 18, 45] },
    water: { near: "#1d3f7a", mid: "#17336a", far: "#2c4688", crest: "#6f8fd0", trough: "#0e2048", glint: "#d8e4ff", shade: [0.45, 0.5, 0.75] },
    cloud: { lit: "#8e9fd2", mid: "#5d6fae", shade: "#3a4884" },
    bounce: [0, 0, 0],
    sat: 1.05,
  },
};
