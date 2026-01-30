import {Composition} from 'remotion';
import {CodeBuddyIntro} from './CodeBuddyIntro';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="codebuddy-intro"
        component={CodeBuddyIntro}
        durationInFrames={540}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{}}
      />
    </>
  );
};
