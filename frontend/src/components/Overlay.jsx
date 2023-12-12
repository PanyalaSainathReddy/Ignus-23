import { useProgress } from "@react-three/drei"
import { usePlay } from "../context/Play";
import { useEffect, useState } from "react";
export const Overlay = () =>{

    const {progress} = useProgress();
    const {play,setPlay,hasScroll,end,setEnd,setRevisit,revisit} = usePlay()
    const [isVisible,setIsVisible] = useState(true)
    useEffect(() => {
        // Disable scrolling on mount
        document.body.style.overflow = 'hidden';

        // Re-enable scrolling on unmount
        return () => {
            document.body.style.overflow = 'visible';
        };
    }, []); 

    const fadeOutOnClick = () => {
        setIsVisible(false);
      };

    return (
        <div className={`overlay ${play?"overlay--disable":""} ${hasScroll ? "overlay--scrolled":""}`}
        >
            <div className={`loader ${progress ===100?"loader-disappear":""}`}/>
            {
                progress === 100 && (
                    <div className={`intro ${play ?"intro--disappear":""}`}>
                        <div className="loader-header">
                        <img className="logo" src="./text-1702194921094.png" />
                        <p className="quote">Where passion meets pride</p>
                        <p className="date">15th - 18th February</p>
                    </div>
                    
                         
                   
                    <p className="intro__scroll">Scroll to begin the journey</p>
                    <button 
                    className={`explore ${play ? 'playing' : ''}`}
                    // onClick={()=>{
                    //     setPlay(true);
                        
                    // }}
                    >Explore</button>
                     
                    <button
                    className="registration">
                        Pre-Registration
                    </button>
            </div>
                )}
           <div className={`outro ${end ? "outro--appear" : ""} ${isVisible ? '' : 'outro--disappear'}`}>
                    <p className="outro__text">
                        Wish You had a great time
                    </p>
                    <button 
                    className={`revisit`} 
                    
                    
                    onClick={()=>{
                        setRevisit(true);
                        
                        setEnd(false)
                        setIsVisible(false)
                    }}>Revisit</button>
                    
                    
           </div>
        </div>
    )
}