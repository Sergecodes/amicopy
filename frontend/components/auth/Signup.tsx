import { useState } from "react";
import Input from "./Input";
import FormExtra from './FormExtra';
import FormAction from './FormAction';


const fields = [
   {
      labelText: "Username",
      labelFor: "username",
      id: "username",
      name: "username",
      type: "text",
      isRequired: true,
      placeholder: "Username"   
   },
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
   },
   // {
   //    labelText: "Confirm Password",
   //    labelFor: "confirm-password",
   //    id: "confirm-password",
   //    name: "confirm-password",
   //    type: "password",
   //    isRequired: true,
   //    placeholder: "Confirm Password"   
   // }
]

type State = {
   // key can be "email" or "password" i.e id of field
   [key: string]: string;
}

let fieldsState: State = {};
fields.forEach(field => fieldsState[field.id] = '');


const Signup: React.FC = () => {
   const [signupState, setSignupState] = useState<State>(fieldsState);

   const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setSignupState({ ...signupState, [e.target.id]: e.target.value });
   }

   const handleSubmit = (e: React.FormEvent<HTMLElement>) => {
      e.preventDefault();
      registerUser();
   }

   // Handle Signup API Integration here
   const registerUser = () => {

   }

   return (
      <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
         <div className="">
            {
               fields.map(field =>
                  <Input
                     key={field.id}
                     handleChange={handleChange}
                     value={signupState[field.id]}
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
         <FormAction handleSubmit={handleSubmit} text="Sign up" />
      </form>
   )
}

export default Signup;
