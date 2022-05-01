import type { NextPage } from 'next'
import Head from 'next/head'
import styles from '../styles/Home.module.css'
import Header from '../components/Header'
import CoverSection from '../components/CoverSection'
import HowItWorks from '../components/HowItWorks'
import FeaturesSection from '../components/FeaturesSection'
import Testimonials from '../components/Testimonials'
import StatisticsSection from '../components/StatisticsSection'
import Footer from '../components/Footer'
import { useState } from 'react'


const Home: NextPage = () => {
  const [loggedIn, setLoggedIn] = useState(false);

  const Space = <div style={{ minHeight: '5rem' }}></div>;

  return (
    <section className={styles.container}>
      <Head>
        <title>Amicopy</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.png" />
      </Head>

      <main className={styles.main}>
        <Header loggedIn={loggedIn} />

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

        <Footer />
      </main>
    </section>
  )
}

export default Home
