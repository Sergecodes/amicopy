import { Card, Badge } from "antd";
import { GiCheckMark } from "react-icons/gi";
import { getCtaBtn } from "../../../utils";
import type { BillingType } from '../../../types'
// import SectionIntro from '../../../components/Layout/SectionIntro'


type Props = {
   type: BillingType;
   loggedIn: boolean;
   isPremium: boolean;
   isGold: boolean;
};


const FeatureItem: React.FunctionComponent<{ text: string }> = (props) => {
   return (
      <p className="mb-2">
         <span className="inline-block text-base mr-2">
            <GiCheckMark />
         </span>
         <span>{props.text}</span>
      </p>
   );
};


const Plans: React.FunctionComponent<Props> = (props) => {
   const { type, loggedIn, isPremium, isGold } = props;

   const premiumPrice = { month: "1.99", year: "3" };
   const goldPrice = { month: "3.99", year: "3" };

   const userPlanState = (function () {
      if (isGold) return "isGold";
      else if (isPremium) return "isPremium";
      else if (loggedIn) return "loggedIn";
      return "";
   })();

   return (
      // <section className="p-5">
      //    <SectionIntro heading="Choose the plan that's right for you" />
         <section className="grid grid-cols-12 sm:mx-0 gap-6">
            <Card className="col-span-12 sm:col-span-6 md:col-span-4">
               <div
                  className={`mb-10 ${type === "year" ? "sm:mb-20 md:mb-20" : "md:mb-12"
                     }`}
               >
                  <h3 className="text-2xl font-medium mb-0 planTier">Free</h3>
                  <div className="text-3xl">
                     <span className="font-bold">$0</span>
                  </div>
               </div>
               <div className="mb-8">{getCtaBtn("free", userPlanState)}</div>
               <div className="text-lg">
                  <h5 className="mb-5 text-xl">Free features include:</h5>
                  <div className="pl-4">
                     <FeatureItem text="Hello" />
                     <FeatureItem text="Hello" />
                     <FeatureItem text="Hello" />
                  </div>
               </div>
            </Card>
            <Card className="col-span-12 sm:col-span-6 md:col-span-4">
               <div
                  className={`mb-10 ${type === "year" ? "sm:mb-12 md:mb-8" : "sm:mb-8 md:mb-10"
                     }`}
               >
                  <h3 className="text-2xl font-medium mb-0 planTier">Premium</h3>
                  <div className="text-3xl">
                     <span className="tracking-wider font-bold">
                        {premiumPrice[type]}
                     </span>
                     <span className="text-sm ml-1 inline-block mb-3">/ month</span>
                     {type === "year" ? (
                        <span className="tracking-wider block text-xs">
                           Billed annually as one payment of
                           <span className="tracking-wider font-bold text-base">
                              {" "}
                              $50
                           </span>
                        </span>
                     ) : (
                        <></>
                     )}
                  </div>
               </div>
               <div className="mb-8">{getCtaBtn("premium", userPlanState)}</div>
               <div className="text-lg">
                  <h5 className="mb-5 text-xl">Premium features include:</h5>
                  <div className="pl-4">
                     <FeatureItem text="Hello" />
                     <FeatureItem text="Hello" />
                     <FeatureItem text="Hello" />
                  </div>
               </div>
            </Card>
            <div className="col-span-12 sm:col-span-12 md:col-span-4">
               <Badge.Ribbon text="Most used" color="gold">
                  <Card>
                     <div className={`mb-10 ${type === "year" ? "md:mb-8" : ""}`}>
                        <h3 className="text-2xl font-medium mb-0 planTier">Gold</h3>
                        <div className="text-3xl">
                           <span className="tracking-wider font-bold">
                              {goldPrice[type]}
                           </span>
                           <span className="text-sm ml-1 inline-block mb-3">
                              / month
                           </span>
                           {type === "year" ? (
                              <span className="tracking-wider block text-xs">
                                 Billed annually as one payment of
                                 <span className="tracking-wider font-bold text-base">
                                    {" "}
                                    $50
                                 </span>
                              </span>
                           ) : (
                              <></>
                           )}
                        </div>
                     </div>
                     <div className="mb-8">{getCtaBtn("gold", userPlanState)}</div>
                     <div className="text-lg">
                        <h5 className="mb-5 text-xl">Gold features include:</h5>
                        <div className="pl-4">
                           <FeatureItem text="Hello" />
                           <FeatureItem text="Hello" />
                           <FeatureItem text="Hello" />
                        </div>
                     </div>
                  </Card>
               </Badge.Ribbon>
            </div>
         
            <style jsx>{`
               .planTier {
                  font-size: 1.6rem;
               }
            `}</style>
         </section>
      // </section>
   );

}


export default Plans;

