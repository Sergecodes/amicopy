import Link from 'next/link'
import Image from 'next/image'


type Props = {
   heading: string;
   paragraph: string;
   linkName: string;
   linkUrl?: string;
}

const Header: React.FC<Props> = (props) => {
   return (
      <div className="mb-10">
         <div className="flex justify-center">
            <Image src="/logo.png" height="3.5rem" width="3.5rem" alt="amicopy logo" />
         </div>
         <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            {props.heading}
         </h2>
         <p className="mt-2 text-center text-sm text-gray-600 mt-5">
            {props.paragraph} {' '}
            <Link href={props.linkUrl || "#"}>
               <a className="font-medium text-siteBlue hover:text-blue-500">
                  {props.linkName}
               </a>  
            </Link>
         </p>
      </div>
   );
}

export default Header;

