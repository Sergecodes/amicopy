import { useState } from "react";
import Input from "./Input";
import FormExtra from './FormExtra';
import FormAction from './FormAction';
import { GrSend } from 'react-icons/gr';
import { message, Result, Spin } from 'antd';
import isLength from 'validator/lib/isLength';
import isEmail from 'validator/lib/isEmail';
import isNumeric from 'validator/lib/isNumeric';

// type Field = {
//    labelText: string;
//    labelFor: "string";
//    id: "username" | "email" | "password";
//    name: string;
// }

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
   },
]

type State = {
   // [key in "email" | "password" | 'username']: string;
   [key: string]: string;
};

let fieldsState: State = {};
fields.forEach(field => fieldsState[field.id] = '');


const Signup: React.FC = () => {
   const [signupState, setSignupState] = useState<State>(fieldsState);
   const [confirmationSent, setConfirmationSent] = useState(false);
   const [inProgress, setInProgress] = useState(false);
   // const [formErrors, setFormErrors] = useState<string[]>([]);

   const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setSignupState({ ...signupState, [e.target.id]: e.target.value });
   };

   const handleSubmit = (e: React.FormEvent<HTMLElement>) => {
      e.preventDefault();
      setInProgress(true);

      const { email, username, password } = signupState;
      let errors: string[] = [];

      // Validate email
      if (!isEmail(email)) {
         errors.push("The email you entered is not a valid email address");
      }

      // Validate username
      if (!isLength(username, { min: 3, max: 36 })) {
         errors.push("Invalid username, your username should be between 3 and 36 characters");
      }

      // Validate password
      if (!isLength(password, { min: 8 }) || isNumeric(password)) {
         errors.push(
            "Your password should have at least 8 characters and should not be entirely numeric"
         );
      }

      if (errors.length === 0) {
         // Call api
         registerUser();
      } else {
         // Display error notification 
         setInProgress(false);
         message.error({ content: errors.join('<br/>'), duration: 8 });
      }
   };


   /** Handle Signup API Integration */
   const registerUser = () => {
      // If we're here then frontend validation is completed and OK
      // Remember loading message is still showing
      let registered = false;

      // Send confirmation email
      // setConfirmationSent(true);
      // ...

      // Remove spinner
      // setInProgress(false);
   };


   // const resendConfirmationEmail = () => {
   //    // Check limit (use local storage )
   // };

   return (
      <>
         {!confirmationSent ?
            <Spin spinning={inProgress} delay={400} size="large">
               <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                  <div className="">
                     {fields.map(field =>
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
                     )}
                  </div>
                  <FormExtra />
                  <FormAction handleSubmit={handleSubmit} text="Sign up" />
               </form>
            </Spin>
            :
            <Result
               icon={<GrSend color="#40a9ff" />}
               title="Confirmation email sent!"
               subTitle={`
                  A confirmation email has been sent to ${signupState['email']}. <br/> 
                  Click on the link in that email to confirm your account.
               `}
               // extra={
               //    <span>
               //       Didn{"'"}t receive any email? &nbsp;
               //       <Button 
               //          type="link" 
               //          className="border-b-1 border-dashed" 
               //          onClick={resendConfirmationEmail} 
               //       >
               //          Resend email
               //       </Button>
               //    </span>
               // }
            />
         }
      </>
   );
}

export default Signup;
