import styles from './styles.module.css'
import Link from 'next/link'
import { IconButton } from '@chakra-ui/react'
import { FaFacebook, FaTwitter } from 'react-icons/fa'


const Footer: React.FunctionComponent = () => {

   return (
      <section className={`footer`}>
         <div className="grid grid-cols-1 md:grid-cols-2 gap-y-10">
            <div className={`${styles.linksDiv}`}>
               <ul className={`${styles.linksUl}`}>
                  <li>
                     <Link href="#">
                        <a>Home</a>
                     </Link>
                  </li>
                  <li>
                     <Link href="#">
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
               </ul>
            </div>
            <div className={`${styles.socialsDiv}`}>
               <ul>
                  <li>
                     <a href="#">
                        <FaTwitter />
                     </a>
                  </li>
                  <li>
                     <a href="#">
                        <FaFacebook />
                        {/* <IconButton aria-label='amicopy facebook' icon={<FaFacebookF />} /> */}
                     </a>
                  </li>
               </ul>
            </div>
         </div>
      </section>
   );
}

export default Footer;
