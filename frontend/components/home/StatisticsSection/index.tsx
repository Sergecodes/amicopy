import styles from './styles.module.css'
// import SectionIntro from '../../components/SectionIntro'
// import { DiPhonegap } from 'react-icons/di'
// import { SiAtom } from 'react-icons/si'
// import { MdOutlineAddLink } from 'react-icons/md'
import React from 'react'
import { InView } from 'react-intersection-observer'


type State = {
   numSessions: number;
   numTransactions: number;
   numDevices: number;
   done: boolean;
};


export default class StatisticsSection extends React.Component<{}, State> {
   state: State = {
      numSessions: 0,
      numTransactions: 0,
      numDevices: 0,
      done: false
   };

   totalSessions = 2500; totalTransactions = 12000; totalDevices = 650;
   speed = 5;

   constructor(props: {}) {
      super(props);
      this.handleViewChange = this.handleViewChange.bind(this);
   }

   countUp() {
      let { numSessions, numTransactions, numDevices } = this.state;

      if (numSessions < this.totalSessions) {
         this.setState(prevState => ({
            numSessions: prevState.numSessions + 100
         }));
      }

      if (numTransactions < this.totalTransactions) {
         this.setState(prevState => ({
            numTransactions: prevState.numTransactions + 500
         }));
      }

      if (numDevices < this.totalDevices) {
         this.setState(prevState => ({
            numDevices: prevState.numDevices + 20
         }));
      }
   }

   notDone() {
      return this.state.numSessions < this.totalSessions ||
         this.state.numDevices < this.totalDevices ||
         this.state.numTransactions < this.totalTransactions;
   }

   handleViewChange(inView: boolean, entry: IntersectionObserverEntry) {
      // console.log('Inview:', inView);
      // console.log(this.state.done);

      if (!this.state.done) {
         if (inView) {
            const interval = setInterval(() => {
               this.notDone() ? this.countUp() : clearInterval(interval);
            }, this.speed);
            
            this.setState({ done: true });
         }
      }
      
   }

   render() {
      return (
         <InView 
            as="section" 
            onChange={this.handleViewChange} 
            className={`py-40 ${styles.container}`}
         >
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

               <div className={`sm:col-span-2 md:col-span-1 ${styles.gridItem}`}>
                  <span className={styles.countSpan}>
                     {this.state.numTransactions}
                     <span className={styles.plus}>+</span>
                  </span>
                  <span className={styles.titleSpan}>Transactions</span>
               </div>
            </div>
         </InView>
      );
   }
}

