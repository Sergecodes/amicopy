import Link from 'next/link'


const UpgradeBtn: React.FunctionComponent<{ 
  style?: React.CSSProperties, 
  className?: string 
}> = (props) => {
  return (
    <Link href="/pricing">
      <a className={props.className || ''} style={props.style || {}}>
        <button>Pricing</button>
      </a>
    </Link>
  );

}


export default UpgradeBtn;
