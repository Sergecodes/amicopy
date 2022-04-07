import Image from 'next/image'
import Link from 'next/link'
import { 
   Button, Menu, MenuButton, MenuGroup, 
   MenuDivider, MenuItem, MenuList, Divider
} from '@chakra-ui/react'
import { Switch } from 'antd'
import styles from './styles.module.css'
import { AiOutlinePlus } from 'react-icons/ai'
import { BiGitMerge } from 'react-icons/bi'
import { FaCloudSun } from 'react-icons/fa'
import { BsViewList, BsSun } from 'react-icons/bs'
import UpgradeBtn from '../UpgradeButton'


const DesktopNavbar: React.FunctionComponent<{ loggedIn: boolean }> = (props) => {
   return (
      <section className={`hidden md:flex px-5 ${styles.deskNavSection}`}>
         <div className={`w-1/4`}>
            <Image alt="amicopy logo" src="/merakist-l5if0iQfV4c-unsplash.jpg" width={80} height={30} />
         </div>
         <div className={`w-3/4 flex ${styles.navDiv}`}>
            <UpgradeBtn />
            <div>
               {props.loggedIn ?
                  <Menu>
                     <MenuButton as={Button} colorScheme='pink'>
                     Profile
                     </MenuButton>
                     <MenuList>
                        <MenuGroup title='Profile'>
                           <MenuItem>My Account</MenuItem>
                           <MenuItem>Payments </MenuItem>
                        </MenuGroup>
                        <MenuDivider />
                        <MenuGroup title='Help'>
                           <MenuItem>Docs</MenuItem>
                           <MenuItem>FAQ</MenuItem>
                        </MenuGroup>
                     </MenuList>
                  </Menu>
                  :
                  <>
                     <Link href='/'><a className="ml-3">Login</a></Link>
                     <span className="mx-2 inline-block" style={{transform: 'scale(1.4)'}}>
                        /
                     </span>
                     <Link href='/'><a>Sign up</a></Link>
                  </>
               }     
            </div>
            <div className={styles.sessionMenuWrapper}>
               <Menu>
                  <MenuButton className={styles.sessionBtn}>Sessions</MenuButton>
                  <MenuList>
                     <MenuItem icon={<AiOutlinePlus />}>
                        <Link href='/'><a>New session</a></Link>
                     </MenuItem>
                     <MenuItem icon={<BiGitMerge />}>
                        <Link href='/'><a>Join a session</a></Link>
                     </MenuItem>
                     <MenuItem icon={<BsViewList />}>
                        <Link href='/'><a>View sessions</a></Link>
                     </MenuItem>
                  </MenuList>
               </Menu>
            </div>
            <span className={styles.modeDividerWrp}>
               <Divider orientation='vertical' style={{borderColor: '#bbb'}} />
            </span>
            <div>
               <Switch
                  checkedChildren={<BsSun />}
                  unCheckedChildren={<FaCloudSun />}
                  style={{height: '25px', minWidth: '48px'}}
                  defaultChecked
               />
            </div>
         </div>
      </section>
   );
}


export default DesktopNavbar;
