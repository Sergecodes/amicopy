import { RiMenu5Fill } from 'react-icons/ri'
import Image from 'next/image'
import Link from 'next/link'
import { Divider } from '@chakra-ui/react'
import { Switch } from 'antd'
import { FaCloudSun } from 'react-icons/fa'
import { BsSun } from 'react-icons/bs'
import styles from './styles.module.css'


const MobileNavbar: React.FunctionComponent<{ 
  loggedIn: boolean, 
  onBarClick: React.MouseEventHandler 
}> = (props) => {
  return (
    <section className={`flex ${styles.mobNavSection}`}>
        <div className={styles.menuBars}>
          <button onClick={props.onBarClick} className={styles.menuBarsButton}>
            {/* <span>
              <FaRegWindowMinimize style={{marginBottom: '-5px'}} />
              <FaRegWindowMinimize />
            </span> */}
            <span><RiMenu5Fill /></span>
          </button>
        </div>
        <div>
          <Link href="/">
            <a>
              <Image alt="amicopy logo" src="/logo.png" width={140} height={50} />
            </a>
          </Link>
        </div>
        <div className="flex">
          {props.loggedIn ? 
            <Link href="/">
              <a className={styles.rightLink}>My profile</a>
            </Link>
            : 
            <Link href="/">
              <a className={styles.rightLink}>Sign in</a>
            </Link>
          }
          <span style={{ height: '28px' }}>
            <Divider orientation='vertical' style={{ borderColor: '#bbb' }} />
          </span>
          <div className='ml-4'>
            <Switch
              checkedChildren={<BsSun />}
              unCheckedChildren={<FaCloudSun />}
              style={{ height: '25px', minWidth: '48px' }}
              defaultChecked
            />
          </div>
        </div>
    </section>

  );
}


export default MobileNavbar;
