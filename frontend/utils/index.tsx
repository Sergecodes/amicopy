import { useLayoutEffect, useEffect, useState } from "react";
import { Button } from "antd";
import Link from 'next/link';
import styles from './styles.module.css'


const useIsomorphicLayoutEffect =
   typeof window !== "undefined" ? useLayoutEffect : useEffect;


/**
 * React hook that listens to the window resize event and returns the size.
 */
export function useWindowSize() {
   // Set initial size to enable server site rendering
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

      function doUpdateSize() {
         clearTimeout(doIt);
         doIt = setTimeout(updateSize, 700);
      }

      window.addEventListener('resize', doUpdateSize);
      doUpdateSize();

      return () => window.removeEventListener("resize", doUpdateSize);
   }, []);

   console.log("rendered use window size");
   return size;
}


/**
 * Get Call to action button to use
 */
export function getCtaBtn(
   type: "free" | "premium" | "gold",
   state: "" | "loggedIn" | "isGold" | "isPremium",
   forTable?: boolean
) {
   const btnClass = forTable ? styles.tableBtn : styles.ctaBtn;

   const GetStartedBtn = (
      <Button
         block
         type="primary"
         className={`${btnClass} ${type === "premium" && forTable ? styles.tablePremiumBtn : ""
            }`}
         style={{ borderColor: "var(--blue)" }}
      >
         Get Started
      </Button>
   );

   const GoldGetStartedBtn = (
      <Button block type="primary" className={`${btnClass} ${styles.goldGetStartedBtn}`}>
         Get Started
      </Button>
   );

   const ViewProfileBtn = (
      <Button block type="dashed" className={`${btnClass} ${styles.viewProfileBtn}`}>
         View Profile
      </Button>
   );

   const CreateSessionBtn = (
      <Button block className={`${btnClass} ${styles.createSessionBtn}`}>
         Create Session
      </Button>
   );

   if (state === "isGold") {
      return <Link href="/profile"><a>{ViewProfileBtn}</a></Link>;
   } else if (state === "isPremium") {
      if (type === "free" || type === "premium")
         return <Link href="/profile"><a>{ViewProfileBtn}</a></Link>;
      else if (type === "gold")
         return <Link href="/sign-up?to-gold"><a>{GoldGetStartedBtn}</a></Link>;
   } else if (state === "loggedIn") {
      if (type === "free") return <Link href="/new-session"><a>{CreateSessionBtn}</a></Link>;
      else if (type === "premium")
         return <Link href="/sign-up?to-premium"><a>{GetStartedBtn}</a></Link>;
      else if (type === "gold")
         return <Link href="/sign-up?to-gold"><a>{GoldGetStartedBtn}</a></Link>;
   }

   // Not logged in 
   if (type === "gold") 
      return <Link href="/sign-up?to-gold"><a>{GoldGetStartedBtn}</a></Link>;

   else if (type === "premium")
      return <Link href="/sign-up?to-premium"><a>{GetStartedBtn}</a></Link>;

      return <Link href="/sign-up"><a>{GetStartedBtn}</a></Link>;
}
