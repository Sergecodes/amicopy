import styles from './styles.module.css'
import { useState } from 'react'
import { useColorModeValue } from '@chakra-ui/react'
import MobileMenu from '../MobileSideMenu'
import MobileNavbar from '../MobileNavbar'
import DesktopNavbar from '../DesktopNavbar'


const Header: React.FC<{ loggedIn: boolean }> = (props) => {
  const [showMenu, setShowMenu] = useState(false);
  let colorValue = useColorModeValue('white', 'rgb(26, 32, 44)');

  const handleNavBarClick: React.MouseEventHandler = () => setShowMenu(!showMenu);
  
  return (
    <header className={`${styles.header}`} style={{backgroundColor: colorValue}}>
      <MobileNavbar loggedIn={props.loggedIn} onBarClick={handleNavBarClick} />
      <MobileMenu show={showMenu} loggedIn={props.loggedIn} />

      <DesktopNavbar loggedIn={props.loggedIn} />
    </header>
  );
}


export default Header;
