import { CSSProperties } from "react";


const SectionIntro: React.FunctionComponent<{ 
   heading: string, 
   span1: string, 
   span2?: string,
   styles?: CSSProperties
}> = (props) => {
   return (
      <section className="text-center mb-7" style={props.styles || {}}>
         <h2 className={`font-bold capitalize mb-3 heading`}>
            {props.heading}
         </h2>
         <p className="text-center text-lg">
            <span>{props.span1}</span> 
            {props.span2 ?
               <>
                  <br/>
                  <span>{props.span2}</span>
               </> : 
               <></>
            }
         </p>

         <style jsx>{`
            .heading {
               font-size: 2.5rem;
            }
         `}</style>
      </section>
   );
}

export default SectionIntro;
