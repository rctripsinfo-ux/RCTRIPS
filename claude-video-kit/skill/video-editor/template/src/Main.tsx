import React from 'react';
import {AbsoluteFill, Audio, Sequence, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate, Easing} from 'remotion';
import data from './data.json';

const fontFamily = 'MontserratLocal';
if (typeof document !== 'undefined' && !document.getElementById('mfont')) {
  const st = document.createElement('style'); st.id = 'mfont';
  st.innerHTML = [800, 900].map((w) => `@font-face{font-family:MontserratLocal;font-weight:${w};src:url(${staticFile(`Montserrat-${w}.woff2`)}) format('woff2');}`).join('');
  document.head.appendChild(st);
}
const YELLOW = '#FFD60A';

type Cap = {s: number; e: number; words: string[]; hi: number[]};
type Zoom = {s: number; e: number; scale: number};

const zoomAt = (t: number, fps: number, frame: number) => {
  let scale = 1 + 0.03 * Math.sin(t / 6); // slow breathing drift
  for (const z of data.zooms as Zoom[]) {
    if (t >= z.s && t < z.e) {
      const inn = spring({frame: frame - z.s * fps, fps, config: {damping: 18, stiffness: 200}});
      const out = interpolate(t, [z.e - 0.15, z.e], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
      scale *= 1 + (z.scale - 1) * inn * out;
    }
  }
  return scale;
};

const Captions: React.FC<{t: number; frame: number; fps: number}> = ({t, frame, fps}) => {
  const hidden = ((data as any).hideCaptions || []).some(([a, b]: number[]) => t >= a && t < b);
  const cap = (data.captions as Cap[]).find((c) => t >= c.s && t < c.e);
  if (!cap || hidden) return null;
  const pop = spring({frame: frame - cap.s * fps, fps, config: {damping: 12, stiffness: 260}});
  return (
    <AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'center', top: 1330}}>
      <div style={{fontFamily, fontWeight: 900, fontSize: 92, lineHeight: 1.05, textAlign: 'center',
        maxWidth: 880, textTransform: 'uppercase', transform: `scale(${0.75 + 0.25 * pop})`, opacity: pop,
        filter: `blur(${(1 - pop) * 6}px)`}}>
        {cap.words.map((w, i) => (
          <span key={i} style={{color: cap.hi.includes(i) ? YELLOW : 'white', margin: '0 12px', display: 'inline-block',
            WebkitTextStroke: '3px black', paintOrder: 'stroke fill',
            textShadow: '0 6px 18px rgba(0,0,0,0.65)'}}>{w}</span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const Hook: React.FC<{frame: number; fps: number}> = ({frame, fps}) => {
  const h = data.hook;
  const t = frame / fps;
  if (t > h.e) return null;
  const inn = spring({frame, fps, config: {damping: 14}});
  const out = interpolate(t, [h.e - 0.3, h.e], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{alignItems: 'center', top: 250}}>
      <div style={{fontFamily, fontWeight: 900, fontSize: 64, color: 'black', background: YELLOW, padding: '18px 34px',
        borderRadius: 22, textAlign: 'center', maxWidth: 900, lineHeight: 1.1, opacity: out,
        transform: `translateY(${(1 - inn) * -60}px) rotate(-2deg)`, boxShadow: '0 12px 40px rgba(0,0,0,0.45)'}}>
        {h.text}
      </div>
    </AbsoluteFill>
  );
};

export const Main: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const scale = zoomAt(t, fps, frame);
  const vignette = 'radial-gradient(ellipse at 50% 40%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%)';
  return (
    <AbsoluteFill style={{backgroundColor: 'black'}}>
      <AbsoluteFill style={{transform: `scale(${scale})`, transformOrigin: '50% 35%'}}>
        <OffthreadVideo src={staticFile('main.mp4')} style={{width: '100%', height: '100%', objectFit: 'cover',
          filter: 'contrast(1.08) saturate(1.12) brightness(1.03)'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: vignette}} />
      <Captions t={t} frame={frame} fps={fps} />
      <Hook frame={frame} fps={fps} />
      {data.sfx.map((x, i) => (
        <Sequence key={i} from={Math.round(x.at * fps)} durationInFrames={Math.round(fps * 0.6)}>
          <Audio src={staticFile(x.src)} volume={x.volume} />
        </Sequence>
      ))}
      <AbsoluteFill style={{top: 0, height: 10, width: `${(t / data.duration) * 100}%`, background: YELLOW}} />
    </AbsoluteFill>
  );
};
