import styles from './styles.module.css'
import { useState } from 'react'
import MobileMenu from '../MobileSideMenu'
import MobileNavbar from '../MobileNavbar'
import DesktopNavbar from '../DesktopNavbar'


const Header: React.FunctionComponent<{ loggedIn: boolean }> = (props) => {
  const [showMenu, setShowMenu] = useState(false);

  const handleNavBarClick: React.MouseEventHandler = () => setShowMenu(!showMenu);
  
  return (
    <header className={`${styles.header}`}>
      <MobileNavbar loggedIn={props.loggedIn} onBarClick={handleNavBarClick} />
      <MobileMenu show={showMenu} />

      <DesktopNavbar loggedIn={props.loggedIn} />
      
    </header>
  );
}


export default Header;
