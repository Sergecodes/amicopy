import type { NextPage } from 'next'
import { useState } from 'react';
import Layout from '../components/Layout'
import type { BillingType, UserPlanState } from '../types'
import BillingSelect from '../components/pricing/BillingSelect'
import Plans from '../components/pricing/Plans'
import Table from '../components/pricing/Table'
import FAQ from '../components/pricing/FAQ'
// import SectionIntro from '../components/Layout/SectionIntro';


const Pricing: NextPage = () => {
   const [billingType, setBillingType] = useState<BillingType>('month');
   const loggedIn = false, isPremium = false, isGold = false;
   const Space = <div style={{ minHeight: '4rem' }}></div>;

   const userPlanState: UserPlanState = (function () {
      if (isGold) return "isGold";
      else if (isPremium) return "isPremium";
      else if (loggedIn) return "loggedIn";
      return "";
   })();

   const handleBillingClick = (event: React.MouseEvent<HTMLElement>, type: BillingType) => {
      if (type != billingType)
        setBillingType(type);
    }

   return (
      <Layout title="Pricing" loggedIn={loggedIn}>
         <h1 className="text-3xl text-center font-extrabold mb-8">
            {/* Choose the plan that's right for you */}
            Choose the plan that suits your needs
         </h1>

         <BillingSelect type={billingType} onClick={handleBillingClick} />
         {Space}

         <Plans type={billingType} planState={userPlanState} />
         {Space}

         <Table planState={userPlanState} />
         {Space}

         <FAQ />
         {Space}
      </Layout>
   )
}

export default Pricing
