import Link from 'next/link'
import classnames from 'classnames'
import styles from './styles.module.css'
import UpgradeBtn from '../UpgradeButton'


const MobileSideMenu: React.FunctionComponent<{ show: boolean}> = (props) => {
  return (
    <section className={
    `w-full max-h-0 overflow-hidden ${classnames(
        styles.sideMenu, props.show && styles.slide
        )}
    `}
    >
        <nav className={styles.sideNav}>
            <ul className={styles.sideNavUl}>
                <li className={styles.sideNavLi}>
                    <Link href='/'><a>Home</a></Link>
                </li>
                <li className={styles.sideNavLi}>
                    <label htmlFor="sessionCheckbox">
                        <span>Sessions</span>
                    </label>               
                    <input type="checkbox" id="sessionCheckbox" className={styles.sessionCheckbox} /> 

                    <ul className={styles.sideNavInnerUl}>
                        <li>
                            <Link href='/'><a>New session</a></Link>
                        </li>
                        <li>
                            <Link href='/'><a>Join a session</a></Link>
                        </li>
                        <li>
                            <Link href='/'><a>View sessions</a></Link>
                        </li>
                    </ul>
                </li>
                <li className={styles.sideNavLi}>
                    <UpgradeBtn />
                </li>
            </ul>
        </nav>
    </section>

  );
}


export default MobileSideMenu;
