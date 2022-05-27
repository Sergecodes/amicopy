import { useState } from 'react'
import { Button } from 'antd';
import { BsEyeSlash, BsEye } from 'react-icons/bs';


const fixedInputClass = `
   rounded-md appearance-none relative block w-full
   px-3 py-2 border border-gray-300 placeholder-gray-500
   text-gray-900 focus:outline-none focus:ring-siteBlue
   focus:border-siteBlue focus:z-10 sm:text-sm
`;

type Props = {
   handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
   value: string;
   labelText: string;
   labelFor: string;
   id: string;
   name: string;
   type: string;
   isRequired?: boolean;
   placeholder: string;
   customClass?: string;
}

const Input: React.FC<Props> = (props) => {
   const [showPassword, setShowPassword] = useState(false);

   const handleShowPassword = () => {
      setShowPassword(!showPassword);
   };

   return (
      <div className="my-5">
         <label htmlFor={props.labelFor} className="sr-only">
            {props.labelText}
         </label>
         <input
            onChange={props.handleChange}
            value={props.value}
            id={props.id}
            name={props.name}
            type={props.name === "password" && showPassword ? "text" : props.type}
            required={props.isRequired || false}
            className={fixedInputClass + props.customClass || ''}
            placeholder={props.placeholder}
         />
         {props.name === 'password' ?
            <Button 
               icon={showPassword ? <BsEye /> : <BsEyeSlash />} 
               onClick={handleShowPassword} 
               type="text" 
               style={{ 
                  position: 'absolute',
                  top: '2px',
                  right: '8px',
                  zIndex: '999'
               }}
            /> : <></>
         }
      </div>
   )
}

export default Input;

