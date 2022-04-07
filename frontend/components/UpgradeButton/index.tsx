import Link from 'next/link'


const UpgradeBtn: React.FunctionComponent = () => {
  return (
    <Link href="/">
      <a>
        <button>Upgrade</button>
      </a>
    </Link>
  );

}


export default UpgradeBtn;
