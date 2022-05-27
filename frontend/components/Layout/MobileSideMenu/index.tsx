import Link from 'next/link'
import classnames from 'classnames'
import { Divider } from '@chakra-ui/react'
import styles from './styles.module.css'
import UpgradeBtn from '../UpgradeButton'
import { AiOutlinePlus, AiOutlineLogin, AiOutlineLogout } from 'react-icons/ai'
import { BiGitMerge } from 'react-icons/bi'
import { BsViewList } from 'react-icons/bs'
import { FaUserCog, FaUserPlus } from 'react-icons/fa'


const MobileSideMenu: React.FC<{
    show: boolean,
    loggedIn: boolean
}> = (props) => {
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
                            <span className={styles.sessionsSpan}>Sessions</span>
                        </label>
                        <input type="checkbox" id="sessionCheckbox" className={styles.sessionCheckbox} />

                        <ul className={styles.sideNavInnerUl}>
                            <li>
                                <Link href='/'><a><AiOutlinePlus /> New session</a></Link>
                            </li>
                            <li>
                                <Link href='/'><a><BiGitMerge /> Join a session</a></Link>
                            </li>
                            <li>
                                <Link href='/'><a><BsViewList /> View sessions</a></Link>
                            </li>
                        </ul>
                    </li>
                    <li className={styles.sideNavLi}>
                        <UpgradeBtn />
                    </li>
                    <li className={styles.sideNavLi}>
                        <div className={styles.accountDiv}>
                            {props.loggedIn ?
                                <>
                                    <span>
                                        <Link href="#">
                                            <a>
                                                <FaUserCog className="mr-1" style={{ verticalAlign: 'text-top' }} />
                                                Profile
                                            </a>
                                        </Link>
                                    </span>
                                    <span style={{ height: '20px', margin: '0 15px' }}>
                                        <Divider orientation='vertical' style={{ borderColor: '#bbb' }} />
                                    </span>
                                    <span>
                                        <Link href="#">
                                            <a style={{ color: 'var(--pink)' }}>
                                                <AiOutlineLogout className="mr-1" style={{ verticalAlign: 'text-top' }} />
                                                Sign out
                                            </a>
                                        </Link>
                                    </span>
                                </> :
                                <>
                                    <span>
                                        <Link href="/signup">
                                            <a style={{ color: 'var(--blue)' }}>
                                                <FaUserPlus className="mr-1" style={{ verticalAlign: 'text-top' }} />
                                                Sign up
                                            </a>
                                        </Link>
                                    </span>
                                    <span style={{ height: '20px', margin: '0 15px' }}>
                                        <Divider orientation='vertical' style={{ borderColor: '#bbb' }} />
                                    </span>
                                    <span>
                                        <Link href="/login">
                                            <a>
                                                <AiOutlineLogin className="mr-1" style={{ verticalAlign: 'text-top' }} />
                                                Sign in
                                            </a>
                                        </Link>
                                    </span>
                                </>
                            }
                        </div>
                    </li>
                </ul>
            </nav>
        </section>

    );
}


export default MobileSideMenu;
