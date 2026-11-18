import React from 'react';
import {Composition} from 'remotion';
import {Main} from './Main';
import data from './data.json';
export const Root: React.FC = () => (
  <Composition id="Main" component={Main} fps={data.fps} width={1080} height={1920}
    durationInFrames={Math.ceil(data.duration * data.fps)} />
);
