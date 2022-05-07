import { useLayoutEffect, useEffect, useState } from 'react'


const useIsomorphicLayoutEffect = typeof window !== 'undefined' ? useLayoutEffect : useEffect;


/**
 * React hook that listens to the window resize event and returns the size.
 */
export function useWindowSize() {
   const [size, setSize] = useState([1000, 670]);
   // useLayoutEffect(() => {
   //    function updateSize() {
   //       setSize([window.innerWidth, window.innerHeight]);
   //    }

   //    window.addEventListener('resize', updateSize);
   //    updateSize();
      
   //    return () => window.removeEventListener('resize', updateSize);
   // }, []);
   
   useIsomorphicLayoutEffect(() => {
      let doIt: NodeJS.Timeout;

      function updateSize() {
         console.log(typeof window);
         setSize([window.innerWidth, window.innerHeight]);
         // if (typeof window === "undefined") {
         //    setSize([1000, 670]);
         // } else {
         //    setSize([window.innerWidth, window.innerHeight]);
         // }
      }

      window.onresize = function() {
         clearTimeout(doIt);
         doIt = setTimeout(updateSize, 700);
      }

      // window.addEventListener('resize', updateSize);
      updateSize();
      
      return () => window.removeEventListener('resize', updateSize);
   }, []);


   console.log("rendered use window size")
   return size;
}

