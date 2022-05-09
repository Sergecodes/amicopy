import '../styles/tailwindImports.css'
import '../styles/globals.css'
import type { AppProps } from 'next/app'
// import { useState } from 'react';
import { ChakraProvider } from '@chakra-ui/react'
// import { IUser } from '../types';


function MyApp({ Component, pageProps }: AppProps) {
  // const [user, setUser] = useState<IUser | null>(null);
  // todo: https://nextjs.org/docs/authentication

  return (
    <ChakraProvider>
      <Component {...pageProps} />
    </ChakraProvider>
  )
}

export default MyApp
