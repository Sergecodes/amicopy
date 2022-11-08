import '../styles/tailwindImports.css'
import '../styles/globals.css'
import type { AppProps } from 'next/app'
// import { useState } from 'react';
import { ChakraProvider } from '@chakra-ui/react'
import { createContext } from 'react';
// import { IUser } from '../types';


export const DataContext = createContext({
  siteData: {
    // theme: "light"
  },
  user: {}
});


export default function MyApp({ Component, pageProps }: AppProps) {
  // const [user, setUser] = useState<IUser | null>(null);
  // todo: https://nextjs.org/docs/authentication
  const user = {};
  // const siteData = { theme: "light" };
  const siteData = {};

  return (
    <ChakraProvider>
      <DataContext.Provider value={{ user, siteData }}>
        <Component {...pageProps} />
      </DataContext.Provider>
    </ChakraProvider>
  )
}

