import type { NextPage } from 'next'
import CoverSection from '../components/home/CoverSection'
import HowItWorks from '../components/home/HowItWorks'
import FeaturesSection from '../components/home/FeaturesSection'
import Testimonials from '../components/home/Testimonials'
import StatisticsSection from '../components/home/StatisticsSection'
import Layout from '../components/Layout'
import { useContext } from 'react'
import { DataContext } from './_app'
import _ from 'lodash'


const Home: NextPage = () => {
  const { user } = useContext(DataContext);
  const Space = <div style={{ minHeight: '5rem' }}></div>;
  const loggedIn = !(_.isEmpty(user));

  return (
    <Layout title="Amicopy" loggedIn={loggedIn}>
      <CoverSection loggedIn={loggedIn} /> 
      <a id="howItWorks"></a>       
      {Space}

      <HowItWorks />
      {Space}

      <FeaturesSection />
      {Space}

      <StatisticsSection />
      {Space}
      <div style={{ minHeight: '2rem' }}></div>

      <Testimonials />
      {Space}
    </Layout>
  )
}

export default Home
