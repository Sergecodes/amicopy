import { Steps } from 'antd'
import Image from 'next/image'
import styles from './styles.module.css'
import { useWindowSize } from '../../utils'
import SectionIntro from '../../components/SectionIntro'


const { Step } = Steps;

const HowItWorks: React.FunctionComponent = () => {
   const [width, height] = useWindowSize();

   let maxWidth = 810;  // step direction depends on max width
   console.log("rendered how it works");

   return (
      <section className={``}>
         <SectionIntro 
            heading='How it works' 
            span1='Create a session; a space where devices can communicate with each other,'
            span2='add devices to the session, et voilà! 👌'
         />
         
         <Steps direction={width > maxWidth ? 'horizontal' : 'vertical'} type="navigation">
            <Step 
               title={<h3 className={styles.stepTitle}>Create a session</h3>}
               subTitle={
                  <div className="mb-3 inline-block">
                     <Image 
                        src='/2008.i605.015_freelance_people_work_set-12.png' 
                        alt="woman on computer"
                        width={150}
                        height={150}
                     />
                  </div>
               }
               description={
                  <p>
                     Create a space for devices with which you want to enable copying and pasting.
                  </p>
               }
               status="process" 
            />
            <Step 
               title={<h3 className={styles.stepTitle}>Invite and add other devices</h3>}
               subTitle={
                  <div className="mb-3 inline-block">
                     <Image 
                        src='/8401.png' 
                        alt="computer desk"
                        width={150}
                        height={150}
                     />
                     <Image 
                        src='/business_woman_using_smartphone.png' 
                        alt="women using smartphone"
                        width={150}
                        height={150}
                     />
                  </div>
               }
               description={
                  <p>
                     Invite devices using an auto-generated and unique link. 
                     You choose which devices should join the session!
                  </p>
               }
               status="process" 
            />
         </Steps>
         <Steps type="navigation">
            <Step 
               className='third-step'
               title={<h3 className={styles.stepTitle}>Start sharing, copying and pasting</h3>}
               subTitle={
                  <div className="mb-3 inline-block">
                     <Image 
                        src='/Happy_people_communicating_via_social_network_on_mobile_screens.png' 
                        alt="people communicating via mobile phone"
                        width={150}
                        height={150}
                     />
                     {/* <Image 
                        src='/4884548.png' 
                        alt="people holding devices"
                        width={150}
                        height={150}
                     /> */}
                  </div>
               }
               description={
                  <p>
                     You can now copy & paste or share between these devices, 
                     or select the devices to send to.
                  </p>
               }
               status="process" 
            />
         </Steps>

         <style jsx global>{`
            .ant-steps-item-description {
               max-width: 300px !important;
               color: var(--text) !important;
               font-size: .97rem;
            }

            /* Add margin after bottom arrow */
            .ant-steps-navigation.ant-steps-vertical > .ant-steps-item {
               margin-bottom: 1rem;
            }
            
            .ant-steps-item-container {
               text-align: center !important;
               margin-bottom: 1rem;  /* add margin before bottom arrow */
            }
               
            /* Remove horizontal tracker bar */
            .ant-steps-item.ant-steps-item-active::before {
               width: 0 !important;
            }

            /* Replace 1 in last step with 3 */
            .third-step .ant-steps-icon {
               /* Use same color as background */
               color: #1890ff !important;
            }

            .third-step .ant-steps-icon::after {
               content: '3';
               color: white;
               margin-left: -8px;
            }

         `}</style>
      </section>
   );
}

export default HowItWorks;
