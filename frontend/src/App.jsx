import { Canvas } from "@react-three/fiber";
import { Experience } from "./components/Experience_2";
import { ScrollControls } from "@react-three/drei";
import { EffectComposer } from "@react-three/postprocessing";
import { Noise } from "lamina";
import { Overlay } from "./components/Overlay";
import { usePlay } from "./context/Play";


function App() {

  const {play,end} = usePlay();

  return (
    <>
    
      <Canvas camera={{
        position: [0, 0, 5],
        fov: 30,
      }}>
        <color attach="background" args={["#ececec"]} />
        <ScrollControls 
        pages={play && !end ? 20:0} damping={0.5} style={{
          top:"12px",
          left:"0px",
          bottom:"10px",
          right:"10px",
          width:"auto",
          height:"auto",
          animation:"fadeIn 2.4s ease-in-out 1.2s forwards",
          opacity:0,
        }}>
          <Experience />
        </ScrollControls>
        
      </Canvas>
      
      <Overlay/>
      
      
    </>
  );
}

export default App;