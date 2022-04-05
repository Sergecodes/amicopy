import { FaRegWindowMinimize } from 'react-icons/fa'
import Image from 'next/image'
import Link from 'next/link'
import styles from './styles.module.css'


const MobileNavbar: React.FunctionComponent<{ loggedIn: boolean, onBarClick: React.MouseEventHandler }> = (props) => {
  return (
    <section className={`flex md:hidden ${styles.mobNavSection}`}>
        <div className={styles.menuBars}>
          <button onClick={props.onBarClick} className={styles.menuBarsButton}>
            <span>
              <FaRegWindowMinimize style={{marginBottom: '-5px'}} />
              <FaRegWindowMinimize />
            </span>
          </button>
        </div>
        <div>
          <Image alt="amicopy logo" src="/merakist-l5if0iQfV4c-unsplash.jpg" width={80} height={30} />
        </div>
        <div>
          {props.loggedIn ? 
          null
          : 
          <Link href="/">
            <a>Log in</a>
          </Link>
          }
        </div>
    </section>

  );
}


export default MobileNavbar;
