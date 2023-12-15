import { Environment, Sphere } from "@react-three/drei";
import { Gradient, LayerMaterial } from "lamina";

import * as THREE from "three";

export const Background = () => {

  const colorA = "#0923be"
  const colorB = "#ffad30";
  
  // const colorA = "#3535cc"
  // const colorB = "#abaadd";
  const start = 0.2
  const end = -0.5;

  return (
    <>
      <Environment resolution={256} background>
      <Sphere scale={[500, 500, 500]} rotation-y={Math.PI / 2} 
      rotation-X={Math.PI}>
        <LayerMaterial
          color={"#ffffff"}
      
        
          side={THREE.BackSide}
        >
          <Gradient
            colorA={colorA}
            colorB={colorB}
            axes={"y"}
            start={start}
            end={end}
          />
        </LayerMaterial>
      </Sphere>
      </Environment>
    </>
  );
};