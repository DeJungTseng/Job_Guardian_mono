
import type { AppProps } from 'next/app';
import { MyRuntimeProvider } from '../MyRuntimeProvider';
import '../globals.css';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <MyRuntimeProvider>
      <Component {...pageProps} />
    </MyRuntimeProvider>
  );
}

export default MyApp;
