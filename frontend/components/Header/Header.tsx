import styles from './styles.module.css'
import { useState } from 'react'
import MobileMenu from '../MobileSideMenu'
import MobileNavbar from '../MobileNavbar'
import DesktopNavbar from '../DesktopNavbar'


const Header: React.FunctionComponent = () => {
  let isLoggedIn = false;
  const [showMenu, setShowMenu] = useState(false);

  const handleNavBarClick: React.MouseEventHandler = () => setShowMenu(!showMenu);
  
  return (
    <header className={`md:px-4 md:py-4 ${styles.header}`}>
      <MobileNavbar loggedIn={isLoggedIn} onBarClick={handleNavBarClick} />
      <MobileMenu show={showMenu} />

      <DesktopNavbar loggedIn={isLoggedIn} />
      
    </header>
  );
}


export default Header;
