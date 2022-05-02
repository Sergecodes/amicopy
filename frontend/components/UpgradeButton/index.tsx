import Link from 'next/link'


const UpgradeBtn: React.FunctionComponent<{ style?: React.CSSProperties }> = (props) => {
  return (
    <Link href="/">
      <a style={props.style || {}}>
        <button>Upgrade</button>
      </a>
    </Link>
  );

}


export default UpgradeBtn;
