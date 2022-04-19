import styles from './styles.module.css'
import SectionIntro from '../SectionIntro'
import { Carousel } from 'antd';


const Testimonials: React.FunctionComponent = () => {

   return (
      <section className={``}>
         <SectionIntro heading='What our users say' />

         <section>
            <Carousel autoplay effect="fade" dotPosition="left">
               <div>
                  <h3 className={styles.contentStyle}>1</h3>
               </div>
               <div>
                  <h3 className={styles.contentStyle}>2</h3>
               </div>
               <div>
                  <h3 className={styles.contentStyle}>3</h3>
               </div>
               <div>
                  <h3 className={styles.contentStyle}>4</h3>
               </div>
            </Carousel>
         </section>
         
      </section>
   );
}

export default Testimonials;
