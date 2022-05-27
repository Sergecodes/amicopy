import { useState } from "react";
import Input from "./Input";
import FormExtra from './FormExtra'
import FormAction from './FormAction'


const fields = [
   {
      labelText: "Email address",
      labelFor: "email-address",
      id: "email-address",
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

   const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setLoginState({ ...loginState, [e.target.id]: e.target.value });
   }

   const handleSubmit = (e: React.FormEvent<HTMLElement>) => {
      e.preventDefault();
      authenticateUser();
   }

   // Handle Login API Integration here
   const authenticateUser = () => {

   }

   return (
      <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
         <div className="">
            {
               fields.map(field =>
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
               )
            }
         </div>
         <FormExtra/>
         <FormAction handleSubmit={handleSubmit} text="Login" />
      </form>
   )
}

export default Login;
