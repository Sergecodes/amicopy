import type { NextPage } from 'next'
import CoverSection from '../components/Home/CoverSection'
import HowItWorks from '../components/Home/HowItWorks'
import FeaturesSection from '../components/Home/FeaturesSection'
import Testimonials from '../components/Home/Testimonials'
import StatisticsSection from '../components/Home/StatisticsSection'
import Layout from '../components/Layout'


const Home: NextPage = () => {
  const Space = <div style={{ minHeight: '5rem' }}></div>;
  const loggedIn = false;

  return (
    <Layout>
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
