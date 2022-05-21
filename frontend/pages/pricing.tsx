import type { NextPage } from 'next'
import { useState } from 'react';
import Layout from '../components/Layout'
import type { BillingType } from '../types'
import BillingSelect from '../components/Pricing/BillingSelect'
import Plans from '../components/Pricing/Plans'
import Table from '../components/Pricing/Table'
import FAQ from '../components/Pricing/FAQ'
// import SectionIntro from '../components/Layout/SectionIntro';


const Pricing: NextPage = () => {
   const [billingType, setBillingType] = useState<BillingType>('month');
   const loggedIn = false, isPremium = false, isGold = false;
   const Space = <div style={{ minHeight: '4rem' }}></div>;

   const handleBillingClick = (event: React.MouseEvent<HTMLElement>, type: BillingType) => {
      if (type != billingType)
        setBillingType(type);
    }

   return (
      <Layout title="Pricing">
         <h1 className="text-3xl text-center font-extrabold mb-8">
            {/* Choose the plan that's right for you */}
            Choose the plan that suits your needs
         </h1>

         <BillingSelect type={billingType} onClick={handleBillingClick} />
         {Space}

         <Plans type={billingType} loggedIn={loggedIn} isPremium={isPremium} isGold={isGold} />
         {Space}

         <Table loggedIn={loggedIn} isPremium={isPremium} isGold={isGold} />
         {Space}

         <FAQ />
         {Space}
      </Layout>
   )
}

export default Pricing
