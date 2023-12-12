import React, { useRef } from 'react'
import { useGLTF } from '@react-three/drei'

export function Cloud({opacity,...props}) {
  const { nodes, materials } = useGLTF('./models/cloud/model.glb')
  return (
    <group {...props} dispose={null}>
      <mesh geometry={nodes.Node.geometry}
      >
        <meshStandardMaterial {...materials['lambert2SG.001']} 
        transparent 
        opacity={opacity}
        envMapIntensity={2}
        />
        </mesh>
    </group>
  )
}

useGLTF.preload('/model.glb')
