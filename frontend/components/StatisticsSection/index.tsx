import styles from './styles.module.css'
import SectionIntro from '../../components/SectionIntro'
import { DiPhonegap } from 'react-icons/di'
import { SiAtom } from 'react-icons/si'
import { MdOutlineAddLink } from 'react-icons/md'
import React from 'react'
import { InView } from 'react-intersection-observer'


type MyProps = {};

type MyState = {
   numSessions: number;
   numTransactions: number;
   numDevices: number;
};


export default class StatisticsSection extends React.Component<MyProps, MyState> {
   state: MyState = {
      numSessions: 0,
      numTransactions: 0,
      numDevices: 0
   };

   totalSessions = 15; totalTransactions = 10; totalDevices = 89;
   speed = 5;

   constructor(props: MyProps) {
      super(props);
      this.handleViewChange = this.handleViewChange.bind(this);
   }

   countUp = () => {
      let { numSessions, numTransactions, numDevices } = this.state;

      if (numSessions < this.totalSessions) {
         this.setState(prevState => ({
            numSessions: prevState.numSessions + 1
         }));
      }

      if (numTransactions < this.totalTransactions) {
         this.setState(prevState => ({
            numTransactions: prevState.numTransactions + 1
         }));
      }

      if (numDevices < this.totalDevices) {
         this.setState(prevState => ({
            numDevices: prevState.numDevices + 1
         }));
      }
   }

   notDone() {
      return this.state.numSessions < this.totalSessions ||
         this.state.numDevices < this.totalDevices ||
         this.state.numTransactions < this.totalTransactions;
   }

   handleViewChange(inView: boolean, entry: IntersectionObserverEntry) {
      console.log('Inview:', inView);

      if (inView) {
         const interval = setInterval(() => {
            this.notDone() ? this.countUp() : clearInterval(interval);
         }, this.speed);
      }
   }

   render() {
      return (
         <InView 
            as="section" 
            onChange={this.handleViewChange} 
            className={`py-40 ${styles.container}`}
         >
            {/* <SectionIntro heading='Stats' /> */}
            <section>
               <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-y-20">
                  <div className={styles.gridItem}>
                     <span className={styles.countSpan}>
                        {this.state.numDevices}
                        <span className={styles.plus}>+</span>
                     </span>
                     <span className={styles.titleSpan}>Devices</span>
                  </div>

                  <div className={`md:-m-6 ${styles.gridItem}`}>
                     <span className={styles.countSpan}>
                        {this.state.numSessions}
                        <span className={styles.plus}>+</span>
                     </span>
                     <span className={styles.titleSpan}>Sessions</span>
                  </div>

                  <div className={`sm:col-span-2 ${styles.gridItem}`}>
                     <span className={styles.countSpan}>
                        {this.state.numTransactions}
                        <span className={styles.plus}>+</span>
                     </span>
                     <span className={styles.titleSpan}>Transactions</span>
                  </div>
               </div>
            </section>
         </InView>
      );
   }
}




/*
const StatisticsSectiont: React.FunctionComponent = () => {
   const [ numSessions, setNumSessions ] = useState(0);
   const [ numTransactions, setNumTransactions ] = useState(0);
   const [ numDevices, setNumDevices ] = useState(0);

   let [totalSessions, totalTransactions, totalDevices] = [15, 10, 89];
   let speed = 20;

   const countSessionsUp = () => {
      if (numSessions < totalSessions)
         setNumSessions(numSessions + 1);
   }

   const countTransactionsUp = () => {
      if (numTransactions < totalTransactions)
         setNumTransactions(numTransactions + 1);  
   }

   const countDevicesUp = () => {
      if (numDevices < totalDevices) {
         console.log("counting devices up")
         setNumDevices(numDevices + 1); 
         console.log(numDevices)
      }
          
   }

   const handleViewChange = (inView: boolean, entry: IntersectionObserverEntry) => {
      console.log('Inview:', inView);
      console.log(numDevices);

      if (inView) {
         // const interval1 = setInterval(() => {
         //    numSessions < totalSessions ? countSessionsUp() : clearInterval(interval1);
         // }, speed);

         // const interval2 = setInterval(() => {
         //    numTransactions < totalTransactions ? countTransactionsUp() : clearInterval(interval2);
         // }, speed);

         const interval3 = setInterval(() => {
            numDevices < totalDevices ? countDevicesUp() : clearInterval(interval3);
         }, speed);
      }
   }
   
   return (
      <InView as="section" onChange={handleViewChange} className={`py-10 ${styles.container}`}>
         <SectionIntro heading='Stats' />
         <section>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-y-5">
               <div className="text-center">
                  <span className="inline-block"><MdOutlineAddLink /></span>
                  <span className={`font-bold`}>
                     {numDevices}
                  </span>
                  <span className={`font-bold`}></span>
               </div>
            </div>
         </section>
      </InView>
   );
}
*/

