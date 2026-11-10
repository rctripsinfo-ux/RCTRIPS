import React from "react";
import { Composition } from "remotion";
import { WhaleShort, WHALE_FRAMES } from "./videos/whale/Whale";
import { Avatar, Banner } from "./channel/ChannelArt";
export const Root: React.FC = () => (
  <>
    <Composition id="EmuShort" component={WhaleShort} durationInFrames={WHALE_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="Avatar" component={Avatar} durationInFrames={1} fps={30} width={800} height={800} />
    <Composition id="Banner" component={Banner} durationInFrames={1} fps={30} width={2560} height={1440} />
  </>
);
