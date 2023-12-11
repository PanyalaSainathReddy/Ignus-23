import { Center, Float, PerspectiveCamera, useScroll } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useEffect } from "react";
import { useMemo, useRef } from "react";
import * as THREE from "three";
import { Background } from "./Background";
import { Cloud } from "./Cloud";
import { Html} from '@react-three/drei';
import { Text } from "@react-three/drei";
import { Vector3 } from "three";
import { TextSection } from "./TextSection";
import { Billboard } from "@react-three/drei";
import { Image } from "@react-three/drei";
import { Text3D } from "@react-three/drei";
import { fadeOnBeforeCompileFlat } from "../utils/fadeMaterial"
import { usePlay } from "../context/Play";


const LINE_NB_POINTS = 12000;

export const Experience = () => {

  const curvePoints = useMemo(()=>[
    new THREE.Vector3(0, 0, 0),
    new THREE.Vector3(0, 0, -10),
    new THREE.Vector3(-2.25, 0, -20),
    new THREE.Vector3(-3, 0, -30),
    new THREE.Vector3(0, 0, -40),
    new THREE.Vector3(5, 0, -50),
    new THREE.Vector3(7, 0, -60),
    new THREE.Vector3(5, 0, -70),
    new THREE.Vector3(1, 0, -80),
    new THREE.Vector3(0, 0, -90),
    new THREE.Vector3(0, 0, -100),
],[]);

const sceneOpacity = useRef(0);
const lineMaterialRef = useRef();



  const curve = useMemo(() => {
    return new THREE.CatmullRomCurve3(
        curvePoints,
      false,
      "catmullrom",
      0.5
    );
  }, []);

  const textSections = useMemo(()=>{
    return [
      {
      position:new Vector3(
        7.5,
        0,
        -55
      ),
      title:"Theme",
      subtitle: 'Cultural Heritage',
      
    },
    {
      position:new Vector3(
        0,
        1,
        -102
      ),
      title:"IGNUS 24"
    },
    {
      position:new Vector3(
        1,
        0,
        -8,
      ),
      title:"About Us"
    }
  ]
  });

  const linePoints = useMemo(() => {
    return curve.getPoints(LINE_NB_POINTS);
  }, [curve]);

  const shape = useMemo(() => {
    const shape = new THREE.Shape();
    shape.moveTo(0, -1);
    shape.lineTo(0, 1);

    return shape;
  }, [curve]);

  const cameraGroup = useRef();
  const scroll = useScroll();


  const {play,setPlay,end,setEnd,revisit,setRevisit} = usePlay();


    


  useFrame((_state, delta) => {
    

    // lineMaterialRef.current.opacity = sceneOpacity.current;
    if(play && !end && sceneOpacity<1){
      sceneOpacity.current = THREE.MathUtils.lerp(
        sceneOpacity.current,
        1,
        delta * 0.1
      );
    }

    if(end && sceneOpacity.current>0){
      sceneOpacity.current = THREE.MathUtils.lerp(
        sceneOpacity.current,
        0,
        delta
      )
    }

    

    if(end){
      return ;
    }
    
    

    const curPointIndex = Math.min(
      Math.round(scroll.offset * linePoints.length),
      linePoints.length - 1
    );
    const curPoint = linePoints[curPointIndex];

    

    const pointAhead =
      linePoints[Math.min(curPointIndex + 1, linePoints.length - 1)];

    const xDisplacement = (pointAhead.x - curPoint.x) * 80;

    // Math.PI / 2 -> LEFT
    // -Math.PI / 2 -> RIGHT

    const angleRotation =
      (xDisplacement < 0 ? 1 : -1) *
      Math.min(Math.abs(xDisplacement), Math.PI / 3);

    
    const targetCameraQuaternion = new THREE.Quaternion().setFromEuler(
      new THREE.Euler(
        cameraGroup.current.rotation.x,
        angleRotation,
        cameraGroup.current.rotation.z
      )
    );

    cameraGroup.current.quaternion.slerp(targetCameraQuaternion, delta * 2);

    cameraGroup.current.position.lerp(curPoint, delta * 24);

    

    

    if (
      cameraGroup.current.position.z <
      curvePoints[curvePoints.length - 1].z +0.5
    ) {
      setEnd(true);
      
    }
   
    if(revisit){
      setEnd(false)
      window.location.reload();
      setPlay(true)
      setRevisit(false)
     
    }
    
    
    
  });


  return (
    <>
    <directionalLight position={[0,3,1]} intensity={0.1} />
      {/* <OrbitControls enableZoom={false} /> */}
      <group ref={cameraGroup}>
        <Background />
        <PerspectiveCamera position={[0, 0, 5]} fov={20} makeDefault />
        
      </group>
      {/* text */}

      {
        play && textSections.map((textSection,index)=>(
          <TextSection {...textSection} key={index} />
        ))
      }
      {/* <group position={[1,1,-8]}>
      <Image url="1.jpg" 
      transparent 
      opacity={0.5} 
      scale={1.8}
      />
      </group> */}

      <group position={[ 0,1,-107]}>
      {/* <Text3D smooth={1} lineHeight={0.5} letterSpacing={-0.025}>{`hello\nworld`}</Text3D> */}
      {/* <Center top center>
        <Text3D 
        
        font="./fonts/gentilis_regular.typeface.json">
              IGNUS 24
              <meshMatcapMaterial/>
             
          </Text3D>
      </Center> */}
      
      </group>
 
        

      {/* LINE */}
      <group position-y={-1}>
        <mesh>
          <extrudeGeometry
            args={[
              shape,
              {
                steps: LINE_NB_POINTS,
                bevelEnabled: false,
                extrudePath: curve,
              },
            ]}
          />
          <meshStandardMaterial 
          color={"rgb(157, 79, 153)"} 
          ref={lineMaterialRef}
          
          transparent 
          envMapIntensity={2}
          onBeforeCompile={fadeOnBeforeCompileFlat}/>
        </mesh>
      </group>

      {/* CLOUDS */}
      {/* <Cloud opacity={1} scale={[1, 1, 1.5]} position={[-3.5, -1.2, -7]} />
      <Cloud opacity={1}  scale={[1, 1, 2]} position={[2.3, -0.4, -15]} rotation-y={Math.PI}/>
      <Cloud opacity={1}  scale={[1, 1, 2]} position={[10, -0.4, -60]} rotation-y={Math.PI}/>
      <Cloud
        opacity={0}
        scale={[1,1,1]}
        rotation-y={Math.PI / 3}
        position={[-3.5,0.2,-12]}
      /> 
      <Cloud
        opacity={1}
        scale={[0.4, 0.4, 0.4]}
        rotation-y={Math.PI / 9}
        position={[-3,-0.5,-20]}
      />
      <Cloud opacity={1} scale={[0.5, 0.5, 0.5]} position={[-1, 1, -53]} />
     <Cloud opacity={0.5} scale={[0.8, 0.8, 0.8]} position={[0, 1, -100]} /> */}
    </>
  );
};