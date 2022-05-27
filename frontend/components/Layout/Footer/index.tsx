import styles from './styles.module.css'
import Link from 'next/link'
import { Center } from '@chakra-ui/react'
import { FiMail, FiTwitter, FiFacebook } from 'react-icons/fi'
// import { FaFacebook, FaTwitter } from 'react-icons/fa'
import FeedbackForm from '../FeedbackForm'


const Footer: React.FC = () => {

   return (
      <footer className="">
         <section className={`grid grid-cols-12 md:grid-cols-12 gap-y-10 ${styles.main}`}>
            <ul className={`col-span-12 md:col-span-10 flex justify-center md:justify-start items-center ${styles.linksUl}`}>
               <li>
                  <Link href="#">
                     <a>Home</a>
                  </Link>
               </li>
               <li>
                  <Link href="/pricing">
                     <a>Pricing</a>
                  </Link>
               </li>
               <li>
                  <Link href="#">
                     <a>Privacy policy</a>
                  </Link>
               </li>
               <li>
                  <Link href="#">
                     <a>Terms &amp; conditions</a>
                  </Link>
               </li>
               <li><FeedbackForm /></li>
            </ul>
               
            <ul className={`col-span-12 md:col-span-2 flex justify-center md:justify-start items-center ${styles.socialsUl}`}>
               <li>
                  <a href="#">
                     <FiMail />
                     {/* <IconButton aria-label='amicopy facebook' icon={<FaFacebookF />} /> */}
                  </a>
               </li>
               <li>
                  <a href="#">
                     <FiTwitter />
                  </a>
               </li>
               <li>
                  <a href="#">
                     <FiFacebook />
                     {/* <IconButton aria-label='amicopy facebook' icon={<FaFacebookF />} /> */}
                  </a>
               </li>
            </ul>
         </section>

         <Center className="py-8 text-lg">
            Copyright &copy; {new Date().getFullYear()} - amicopy
         </Center>
      </footer>
   );
}

export default Footer;
