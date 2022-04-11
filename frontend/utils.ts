import { useLayoutEffect, useState } from 'react'


/**
 * React hook that listens to the window resize event and returns the size.
 */
export function useWindowSize() {
   const [size, setSize] = useState([0, 0]);
   // useLayoutEffect(() => {
   //    function updateSize() {
   //       setSize([window.innerWidth, window.innerHeight]);
   //    }

   //    window.addEventListener('resize', updateSize);
   //    updateSize();
      
   //    return () => window.removeEventListener('resize', updateSize);
   // }, []);

   useLayoutEffect(() => {
      let doIt: NodeJS.Timeout;

      function updateSize() {
         setSize([window.innerWidth, window.innerHeight]);
      }

      window.onresize = function() {
         clearTimeout(doIt);
         doIt = setTimeout(updateSize, 500);
      }

      // window.addEventListener('resize', updateSize);
      updateSize();
      
      return () => window.removeEventListener('resize', updateSize);
   }, []);

   console.log("rendered use window size")
   return size;
}

