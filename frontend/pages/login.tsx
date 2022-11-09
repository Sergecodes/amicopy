import type { NextPage } from 'next';
import Header from '../components/auth/Header';
import Login from '../components/auth/Login';
import Layout from '../components/Layout'
import { useContext } from 'react'
import { DataContext } from './_app'
import { isEmptyObject } from '../utils';


const LoginPage: NextPage = () => {
   const { user } = useContext(DataContext);

   return (
      <Layout title="Pricing" loggedIn={!(isEmptyObject(user))}>
         <div className="min-h-full h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8">
               <Header
                  heading="Login to your account"
                  paragraph="Don't have an account yet? "
                  linkName="Signup"
                  linkUrl="/signup"
               />
               <Login />
            </div>
         </div>
      </Layout>
   );
}

export default LoginPage;
