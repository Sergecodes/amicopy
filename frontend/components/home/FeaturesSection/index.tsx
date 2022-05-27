import styles from './styles.module.css'
import SectionIntro from '../../Layout/SectionIntro'
import { FaReact, FaHistory } from 'react-icons/fa'
import { RiChatPrivateLine } from 'react-icons/ri'
import { SiSpringsecurity, SiAuthy } from 'react-icons/si'
import { MdOutlinePhonelink, MdOutlinePhonelinkLock, MdPhonelink } from 'react-icons/md'


const Feature: React.FC<{ 
   className?: string,
   icon: React.ReactNode, 
   title: string, 
   description: string 
}> = (props) => {

   return (
      <div className={`${props.className || ''} ${styles.featureWrp}`}>
         <div className={`text-center mb-2 text-3xl`}>
            <span className={`inline-block ${styles.iconWrp}`}>{props.icon}</span>
         </div>
         <h3 className={`font-bold text-center capitalize mb-3 text-lg ${styles.title}`}>
            {props.title}
         </h3>
         <p className={`text-center ${styles.description}`}>
            {props.description}
         </p>
      </div>
   )
}


const FeaturesSection: React.FC = () => {

   return (
      <section>
         <SectionIntro heading='Distinct features' />

         <section className={`grid grid-cols-12 md:grid-cols-12 gap-y-10 ${styles.featuresParent}`}>
            <Feature 
               className="px-4 col-span-12 sm:col-span-6 md:col-span-4"
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
               className="px-4 col-span-12 sm:col-span-6 md:col-span-4"
               title="Unique private sessions" 
               icon={<RiChatPrivateLine style={{ fontSize: '2.5rem' }} />}
               description="
                  Each session has a unique code. Moreover, you decide who joins the session.
                  You are also free to remove devices and block a session from new devices.
               "
            />
            <Feature 
               className="px-4 col-span-12 sm:col-span-6 md:col-span-4"
               title="No boundaries" 
               icon={<FaReact />}
               description="
                  There's no physical boundary as to where devices can be; devices can 
                  be in any location. Also, it's blazing fast!
               "
            />
            <Feature 
               className="px-4 col-span-12 sm:col-span-6 md:col-span-4"
               title="Guaranteed security" 
               icon={<SiSpringsecurity />}
               description="
                  You can view all past sessions and transactions in a single click.
                  Because we are there, you do not need to remember your data. Information 
                  is what's useful and we help you keep in touch with it!
               "
            />
            <Feature 
               className="px-4 col-span-12 sm:col-span-6 md:col-span-4"
               title="Consistent history" 
               icon={<FaHistory />}
               description="
                  In addition to the default security, you can add a custom code that 
                  will be required for new users. Users without this code won't be granted 
                  access.
               "
            />
            <Feature 
               className="px-4 col-span-12 sm:col-span-6 md:col-span-4"
               title="2FA" 
               icon={<MdOutlinePhonelinkLock />}
               description="
                  Because we understand how important your data is, we also provide 
                  Two Factor Authentication. This is an extra mile of security which 
                  prevents others from impersonating you without your permission.
               "
            />
            {/* <Feature 
               className="px-4 sm:px-36 md:px-4 col-span-12 md:col-span-4"
               title="No boundaries" 
               icon={<FaReact />}
               description="
                  There's no physical boundary as to where devices can be; devices can 
                  be in any location. Also, it's blazing fast!
               "
            />
            <Feature 
               className="px-4 col-span-12 sm:col-span-6"
               title="Guaranteed security" 
               icon={<SiSpringsecurity />}
               description="
                  In addition to the default security, you can add a custom code that 
                  will be required for new users. Users without this code won't be granted 
                  access.
               "
            />
            <Feature 
               className="px-4 col-span-12 sm:col-span-6"
               title="2FA" 
               icon={<MdOutlinePhonelinkLock />}
               description="
                  Because we understand how important your data is, we also provide 
                  Two Factor Authentication. This is an extra mile of security which 
                  prevents others from impersonating you without your permission.
               "
            /> */}
         </section>
      </section>
   );
}

export default FeaturesSection;
