import { CSSProperties } from "react";
import { useColorModeValue } from '@chakra-ui/react';


const SectionIntro: React.FC<{ 
   heading: string, 
   span1?: string, 
   span2?: string,
   styles?: CSSProperties
}> = (props) => {
   // --text: #535c68
   let headingColor = useColorModeValue('#535c68', 'slategray');

   return (
      <section className="text-center mb-7" style={props.styles || {}}>
         <h2 className={`font-bold capitalize mb-3 heading`} style={{color: headingColor}}>
            {props.heading}
         </h2>
         <p className="text-center text-lg subHeading">
            {props.span1 ?
               <span>{props.span1}</span> : <></>
            }
            {props.span2 ?
               <>
                  <br/>
                  <span>{props.span2}</span>
               </> : <></>
            }
         </p>

         <style jsx>{`
            section {
               padding-left: 2.8rem;
               padding-right: 2.8rem;
            }
            
            .heading {
               font-size: 2.5rem;
            }

            .subHeading {
               color: var(--text);
            }
         `}</style>
      </section>
   );
}

export default SectionIntro;
