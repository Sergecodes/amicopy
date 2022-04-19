import styles from './styles.module.css'
import SectionIntro from '../SectionIntro'
import { ReactNode } from 'react';
import { FaReact, FaUsers } from 'react-icons/fa'
import { RiChatPrivateLine } from 'react-icons/ri'
import { SiSpringsecurity, SiAuthy } from 'react-icons/si'
import { MdOutlinePhonelink, MdOutlinePhonelinkLock, MdPhonelink } from 'react-icons/md'
import { Center, Divider, Show } from '@chakra-ui/react'


const Feature: React.FunctionComponent<{ 
   icon: ReactNode, 
   title: string, 
   description: string 
}> = (props) => {

   return (
      <div className={styles.featureWrp}>
         <div className={`text-center mb-2`}>
            <span className={`inline-block`}>{props.icon}</span>
         </div>
         <h3 className={`font-bold text-center capitalize mb-3 h3`}>
            {props.title}
         </h3>
         <p className={`text-center`}>
            {props.description}
         </p>
      </div>
   )
}


const FeaturesSection: React.FunctionComponent = () => {

   return (
      <section className={``}>
         <SectionIntro heading='Distinct features' />

         <section>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-y-12 mb-12 md:mb-0">
               <Feature 
                  title="Multiple devices & users" 
                  icon={<MdPhonelink />}
                  description="
                     Copy and paste from your mobile to your desktop and vice versa. 
                     You can add any number of devices to a copy-paste session and also 
                     invite other users. These users may also have multiple devices 
                     in the session.
                  "
               />
               <Feature 
                  title="Unique private sessions" 
                  icon={<RiChatPrivateLine />}
                  description="
                     Each session has a unique code. Moreover, you decide who joins the session.
                     You are also free to remove devices and block a session from new devices.
                  "
               />
               <Feature 
                  title="No boundaries" 
                  icon={<FaReact />}
                  description="
                     There's no physical boundary as to where devices can be; devices can 
                     be in any location. Also, it's blazing fast!
                  "
               />
            </div>
            <Show above="md">
               <Center width='50vw'>
                  <Divider />
               </Center>
            </Show>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-y-12">
               <Feature 
                  title="Guaranteed security" 
                  icon={<SiSpringsecurity />}
                  description="
                     In addition to the default security, you can add a custom code that 
                     will be required for new users. Users without this code won't be granted 
                     access.
                  "
               />
               <Feature 
                  title="2FA" 
                  icon={<MdOutlinePhonelinkLock />}
                  description="
                     Because we understand how important your data is, we also provide 
                     Two Factor Authentication. This is an extra mile of security which 
                     prevents others from impersonating you without your permission.
                  "
               />
            </div>
         </section>
         
      </section>
   );
}

export default FeaturesSection;
