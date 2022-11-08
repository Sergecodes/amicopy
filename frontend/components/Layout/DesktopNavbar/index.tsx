import Image from 'next/image'
import Link from 'next/link'
import { 
   Menu, MenuButton, useColorMode, MenuItem, MenuList, Divider
} from '@chakra-ui/react'
import { Switch, Button } from 'antd'
import styles from './styles.module.css'
import { AiOutlinePlus } from 'react-icons/ai'
import { BiGitMerge } from 'react-icons/bi'
import { FaCloudSun } from 'react-icons/fa'
import { BsViewList, BsSun } from 'react-icons/bs'
import UpgradeBtn from '../UpgradeButton'


const DesktopNavbar: React.FC<{ loggedIn: boolean }> = (props) => {
   const { colorMode, toggleColorMode } = useColorMode();

   return (
      <section className={`hidden ${styles.deskNavSection}`}>
         <div className={`w-1/4`}>
            <Link href='/'>
               <a>
                  <Image alt="amicopy logo" src="/logo.png" width={135} height={60} />
               </a>
            </Link>
         </div>
         <div className={`w-3/4 flex ${styles.navDiv}`}>
            <div>
               <UpgradeBtn style={{ fontSize: '1.1rem' }} />
            </div>
            <div className={props.loggedIn ? `mx-8` : `mx-12 ${styles.authLinksWrp}`}>
               {props.loggedIn ?
                  <Link href='/'>
                     <a className={styles.profileLink}>My profile</a>
                  </Link>
                  :
                  <>
                     <Link href='/login'><a>Login</a></Link>
                     <span className="mx-2 inline-block" style={{ transform: 'scale(1.4)' }}>
                        ~
                     </span>
                     <Link href='/signup'><a>Sign up</a></Link>
                  </>
               }     
            </div>
            <div className={styles.sessionMenuWrp}>
               <Menu>
                  <MenuButton className={styles.sessionBtn}>Sessions</MenuButton>
                  <MenuList>
                     <MenuItem 
                        style={{ color: 'var(--pink)', fontWeight: 600 }} 
                        icon={<AiOutlinePlus />}
                     >
                        <Link href='/'><a>New session</a></Link>
                     </MenuItem>
                     <MenuItem style={{ color: 'var(--pink)' }} icon={<BiGitMerge />}>
                        <Link href='/'><a>Join a session</a></Link>
                     </MenuItem>
                     <MenuItem icon={<BsViewList />}>
                        <Link href='/'><a>View sessions</a></Link>
                     </MenuItem>
                  </MenuList>
               </Menu>
            </div>
            <span className={styles.modeDividerWrp}>
               <Divider orientation='vertical' style={{ borderColor: '#bbb' }} />
            </span>
            <div className='ml-4'>
               <Switch
                  onChange={() => toggleColorMode()}
                  checkedChildren={<BsSun />}
                  unCheckedChildren={<FaCloudSun />}
                  style={{ height: '25px', minWidth: '48px' }}
                  defaultChecked={colorMode === 'light' ? true : false}
               />
            </div>
         </div>
      </section>
   );
}


export default DesktopNavbar;
