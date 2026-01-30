import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
Config.setRenderingFps(30);
Config.setConcurrency(5);

export const config = Config.getPurgedConfig();
