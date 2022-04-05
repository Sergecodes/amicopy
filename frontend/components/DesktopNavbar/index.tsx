import Image from 'next/image'
import { Button, Menu, MenuButton, MenuItem, MenuList } from '@chakra-ui/react'
import Link from 'next/link'
import styles from './styles.module.css'
import { AiOutlinePlus } from 'react-icons/ai'
import { BiChevronDown, BiGitMerge } from 'react-icons/bi'
import { BsViewList } from 'react-icons/bs'


const DesktopNavbar: React.FunctionComponent<{ loggedIn: boolean }> = (props) => {
   return (
      <section className={`hidden md:flex px-5 ${styles.deskNavSection}`}>
         <div className={`w-1/4`}>
            <Image alt="amicopy logo" src="/merakist-l5if0iQfV4c-unsplash.jpg" width={80} height={30} />
         </div>
         <div className={`w-3/4 flex ${styles.navDiv}`}>
            <Link href='/'>
               <a>
               <button className={styles.upgradeButton}>Upgrade</button>
               </a>
            </Link>
            <span>
               {props.loggedIn ?
                  <></>
                  :
                  <>
                     <Link href='/'><a>Login</a></Link>
                     <span>/</span>
                     <Link href='/'><a>Sign up</a></Link>
                  </>
               }     
            </span>
            <div className={styles.sessionMenuWrapper}>
               <Menu>
                  <MenuButton as={Button} rightIcon={<BiChevronDown />}>
                  Sessions
               </MenuButton>
               <MenuList>
                  <MenuItem icon={<AiOutlinePlus />}>
                     New session
                  </MenuItem>
                  <MenuItem icon={<BiGitMerge />}>
                     Join a session
                  </MenuItem>
                  <MenuItem icon={<BsViewList />}>
                     View sessions
                  </MenuItem>
               </MenuList>
               </Menu>
            </div>
         </div>
      </section>
   );
}


export default DesktopNavbar;
