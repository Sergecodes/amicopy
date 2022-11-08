import styles from './styles.module.css'
import SectionIntro from '../../Layout/SectionIntro'
import { Carousel, Card, Avatar } from 'antd'

const { Meta } = Card;


const Testimonials: React.FC = () => {

   return (
      <section className={``}>
         <SectionIntro heading='From our users' />

         <section>
            <Carousel autoplay dotPosition="left" >
               <div className={styles.cardWrp}>
                  <Card
                     className={styles.cardStyle}
                     extra={<a href="#">Via Twitter</a>}
                     cover={
                        <p style={{ marginTop: '1rem', padding: '8px' }}>
                           This is the content lorem ipsum ...
                        </p>
                     }
                  >
                     <Meta
                        style={{ textAlign: 'center' }}
                        title={
                           <Avatar 
                              size={70} 
                              style={{ display: 'inline-block', marginBottom: '10px' }} 
                              src="/gen3.jpeg" 
                           />
                        }
                        description="Daniel K."
                     />
                  </Card>
               </div>
               
               <div className={styles.cardWrp}>
                  <Card
                     className={styles.cardStyle}
                     extra={<a href="#">Via Twitter</a>}
                     cover={
                        <p style={{ marginTop: '1rem', padding: '8px' }}>
                           This is the content lorem ipsum ...
                        </p>
                     }
                  >
                     <Meta
                        style={{ textAlign: 'center' }}
                        title={
                           <Avatar 
                              size={70} 
                              style={{ display: 'inline-block', marginBottom: '10px' }} 
                              src="/gen5.jpeg" 
                           />
                        }
                        description="Victor S."
                     />
                  </Card>
               </div>

               <div className={styles.cardWrp}>
                  <Card
                     className={styles.cardStyle}
                     extra={<a href="#">Via Twitter</a>}
                     cover={
                        <p style={{ marginTop: '1rem', padding: '8px' }}>
                           This is the content lorem ipsum ...
                        </p>
                     }
                  >
                     <Meta
                        style={{ textAlign: 'center' }}
                        title={
                           <Avatar 
                              size={70} 
                              style={{ display: 'inline-block', marginBottom: '10px' }} 
                              src="/gen4.jpeg" 
                           />
                        }
                        description="Omer Steph"
                     />
                  </Card>
               </div>
            </Carousel>
         </section>
         
      </section>
   );
}

export default Testimonials;
