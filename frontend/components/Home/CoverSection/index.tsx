import { Button } from '@chakra-ui/react'
import styles from './styles.module.css'
import { AiOutlineUserAdd, AiOutlinePlus } from 'react-icons/ai'
import { BsChevronDoubleDown } from 'react-icons/bs'
import { BiGitMerge } from 'react-icons/bi'
import { theme } from '../../../constants'
import Link from 'next/link'


const CoverSection: React.FunctionComponent<{ loggedIn: boolean }> = (props) => {
   return (
      <section className={`flex items-center justify-center ${styles.container}`}>
         <div className={`text-center px-4 ${styles.sectionDiv}`}>
            <h1 className="mb-9">
               Copy & paste between multiple devices.
            </h1>
            <h2 className="mb-6">
               Easily copy, paste and transfer text and files from one device to another.
            </h2>
            {props.loggedIn ?
               <Link href="#" passHref={true}>
                  <Button 
                     as="a"
                     size="lg" 
                     bg={theme.colors.blue}
                     fontSize='.9rem'
                     color="#fff"
                     className={`mr-4`}
                     leftIcon={<AiOutlinePlus />}
                     _hover={{bg: theme.colors.blue, color: '#fff'}}
                     // _active={{}}
                     // _focus={{}}
                  >
                     CREATE SESSION
                  </Button>
               </Link> :
               <Button 
                  as="a"
                  size="lg" 
                  variant="outline" 
                  href="#howItWorks"
                  // color={theme.colors.pink}
                  color="#fff"
                  rightIcon={<BsChevronDoubleDown className={styles.downArrow} />}
                  className={`mr-4 ${styles.ctaButton}`}
                  _hover={{bg: theme.colors.pink, color: '#fff'}}
                  // _active={{}}
                  // _focus={{}}
               >
                  Explore
               </Button>
            }
            
            {props.loggedIn ?
               <Link href="#" passHref={true}>
                  <Button 
                     as="a"
                     size="lg" 
                     // variant="outline" 
                     fontSize='.9rem'
                     color={theme.colors.blue}
                     leftIcon={<BiGitMerge />}
                     // _hover={{bg: theme.colors.pink, color: '#fff'}}
                     // _active={{}}
                     // _focus={{}}
                  >
                     JOIN SESSION
                  </Button>
               </Link> :
               <Link href="#" passHref={true}>
                  <Button 
                     as="a"
                     size="lg" 
                     bg={theme.colors.blue}
                     fontSize='1rem'
                     color="#fff"
                     leftIcon={<AiOutlineUserAdd style={{fontSize: '18px'}} />}
                     // _hover={{color: '#fff'}}
                     // _active={{}}
                     // _focus={{}}
                  >
                     SIGN UP
                  </Button>
               </Link>
            }
         </div>
      </section>
   );
}

export default CoverSection;
