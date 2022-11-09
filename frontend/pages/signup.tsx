import type { NextPage } from 'next';
import Header from '../components/auth/Header';
import Signup from '../components/auth/Signup';
import Layout from '../components/Layout'
import { useContext } from 'react'
import { DataContext } from './_app'
import { isEmptyObject } from '../utils';


const SignupPage: NextPage = () => {
   const { user } = useContext(DataContext);

   return (
      <Layout title="Signup" loggedIn={!(isEmptyObject(user))}>
         <div className="min-h-full h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8">
               <Header
                  heading="Sign up to create an account"
                  paragraph="Already have an account? "
                  linkName="Login"
                  linkUrl="/login"
               />
               <Signup />
            </div>
         </div>
      </Layout>
   );
}

export default SignupPage;
