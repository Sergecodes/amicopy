import Link from 'next/link'


const UpgradeBtn: React.FunctionComponent<{ 
  style?: React.CSSProperties, 
  className?: string 
}> = (props) => {
  return (
    <Link href="/">
      <a className={props.className || ''} style={props.style || {}}>
        <button>Upgrade</button>
      </a>
    </Link>
  );

}


export default UpgradeBtn;
