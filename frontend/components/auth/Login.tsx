import { useState } from "react";
import { useRouter } from 'next/router';
import { message, Result, Spin } from 'antd';
import Input from "./Input";
import FormExtra from './FormExtra'
import FormAction from './FormAction'


const fields = [
   {
      labelText: "Email address",
      labelFor: "email",
      id: "email",
      name: "email",
      type: "email",
      isRequired: true,
      placeholder: "Email address"   
   },
   {
      labelText: "Password",
      labelFor: "password",
      id: "password",
      name: "password",
      type: "password",
      isRequired: true,
      placeholder: "Password"   
   }
]

type State = {
   // key can be "email" or "password" i.e id of field
   [key: string]: string;
}

let fieldsState: State = {};
fields.forEach(field => fieldsState[field.id] = '');


const Login: React.FC = () => {
   const [loginState, setLoginState] = useState<State>(fieldsState);
   const [inProgress, setInProgress] = useState(false);
   const router = useRouter();

   const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setLoginState({ ...loginState, [e.target.id]: e.target.value });
   }

   const handleSubmit = (e: React.FormEvent<HTMLElement>) => {
      e.preventDefault();
      setInProgress(true);

      authenticateUser();
   }

   // Handle Login API Integration here
   const authenticateUser = () => {
      // Authentication not ok
      // setInProgress(false);
      // message.error({ 
      //    content: 'Account not found, verify your email and password', 
      //    duration: 8 
      // });

      // Authentication ok
      // setInProgress(false);
      // Go to login page
      // router.push('/login');
   }

   return (
      <Spin spinning={inProgress} size="large">
         <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <div className="">
               {fields.map(field =>
                  <Input
                     key={field.id}
                     handleChange={handleChange}
                     value={loginState[field.id]}
                     labelText={field.labelText}
                     labelFor={field.labelFor}
                     id={field.id}
                     name={field.name}
                     type={field.type}
                     isRequired={field.isRequired}
                     placeholder={field.placeholder}
                  />
               )}
            </div>
            <FormExtra/>
            <FormAction handleSubmit={handleSubmit} text="Login" />
         </form>
      </Spin>
   )
}

export default Login;
