import {Config} from '@remotion/cli/config';

const config = {
  videoImageFormat: 'jpeg' as const,
  overwrite: true,
  codec: 'h264' as const,
  fps: 30,
  proResProfile: undefined,
  audioBitrate: undefined,
  videoBitrate: undefined,
  crf: undefined,
  pixelFormat: undefined,
  scale: 1,
};

export default config;
