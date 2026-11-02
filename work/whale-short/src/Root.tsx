import React from "react";
import { Composition } from "remotion";
import { WhaleShort, WHALE_FRAMES } from "./videos/whale/Whale";
export const Root: React.FC = () => (
  <>
    <Composition id="WhaleShort" component={WhaleShort} durationInFrames={WHALE_FRAMES} fps={30} width={1080} height={1920} />
  </>
);
