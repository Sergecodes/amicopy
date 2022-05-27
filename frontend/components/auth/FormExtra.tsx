import Link from 'next/link'
import { Checkbox } from 'antd';
import type { CheckboxChangeEvent } from 'antd/es/checkbox';


const FormExtra: React.FC = () => {
   return (
      <div className="flex items-center justify-between">
         <div className="flex items-center">
            <input
               id="remember-me"
               name="remember-me"
               type="checkbox"
               className="h-4 w-4 text-siteBlue focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
               Remember me
            </label>
         </div>

         <div className="text-sm">
            <Checkbox className="font-medium text-siteBlue hover:text-blue-500">
               <Link href="#">
                  <a>Forgot your password?</a>
               </Link>
            </Checkbox>
         </div>
      </div>
   )
}

export default FormExtra;
