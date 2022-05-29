import Link from 'next/link'
import { Checkbox } from 'antd';


const FormExtra: React.FC = () => {
   return (
      <div className="flex items-center justify-between">
         <div className="flex items-center">
            <Checkbox name="remember-me">Remember me</Checkbox>
         </div>

         <div className="text-sm">
            <Link href="#">
               <a className="font-medium text-siteBlue hover:text-blue-500">
                  Forgot your password?
               </a>
            </Link>
         </div>
      </div>
   )
}

export default FormExtra;
