import { Card, Badge } from "antd";
import { GiCheckMark } from "react-icons/gi";
import { getCtaBtn } from "../../../utils";
import type { BillingType, UserPlanState } from '../../../types'
// import SectionIntro from '../../../components/Layout/SectionIntro'


type Props = {
   type: BillingType;
   planState: UserPlanState;
};


const FeatureItem: React.FC<{ text: string }> = (props) => {
   return (
      <p className="mb-2">
         <span className="inline-block text-base mr-2">
            <GiCheckMark />
         </span>
         <span>{props.text}</span>
      </p>
   );
};


const Plans: React.FC<Props> = (props) => {
   const { type, planState } = props;

   const premiumPrice = { month: 1.99, year: 3 };
   const goldPrice = { month: 3.99, year: 3 };

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
               <div className="mb-8">{getCtaBtn("free", planState)}</div>
               <div className="text-lg">
                  <h5 className="mb-5 text-xl">Free features include:</h5>
                  <div className="pl-4">
                     <FeatureItem text="Access to our services without signing up" />
                     <FeatureItem text="Sign up to backup and keep track of your data" />
                     <FeatureItem text="Limited devices and users per session" />
                     <FeatureItem text="Limited access to our services" />
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
                        ${premiumPrice[type]}
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
               <div className="mb-8">{getCtaBtn("premium", planState)}</div>
               <div className="text-lg">
                  <h5 className="mb-5 text-xl">Premium features include:</h5>
                  <div className="pl-4">
                     <FeatureItem text="More access to our services" />
                     <FeatureItem text="More devices and users per session" />
                     <FeatureItem text="No Ads" />
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
                              ${goldPrice[type]}
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
                     <div className="mb-8">{getCtaBtn("gold", planState)}</div>
                     <div className="text-lg">
                        <h5 className="mb-5 text-xl">Gold features include:</h5>
                        <div className="pl-4">
                           <FeatureItem text="All Premium features" />
                           <FeatureItem text="Full access to all our services without restriction" />
                           <FeatureItem text="Highest security with two-factor authentication" />
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

