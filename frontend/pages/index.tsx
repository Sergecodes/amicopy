import type { NextPage } from 'next'
import CoverSection from '../components/home/CoverSection'
import HowItWorks from '../components/home/HowItWorks'
import FeaturesSection from '../components/home/FeaturesSection'
import Testimonials from '../components/home/Testimonials'
import StatisticsSection from '../components/home/StatisticsSection'
import Layout from '../components/Layout'


const Home: NextPage = () => {
  const Space = <div style={{ minHeight: '5rem' }}></div>;
  const loggedIn = false;

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
