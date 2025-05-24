'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';

export default function OAuthClient() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [status, setStatus] = useState('Initializing OAuth flow...');
  const [error, setError] = useState('');

  useEffect(() => {
    const provider = searchParams.get('provider');
    const code = searchParams.get('code');
    const state = searchParams.get('state');
    const action = searchParams.get('action') || 'login';

    if (!provider) {
      setError('No OAuth provider specified');
      return;
    }

    if (action === 'redirect') {
      initiateOAuth(provider);
    } else if (code && state) {
      handleOAuthCallback(provider, code, state);
    } else {
      setError('Invalid OAuth parameters');
    }
  }, [searchParams]);

  const initiateOAuth = async (provider: string) => {
    try {
      setStatus(`Initiating ${provider} login...`);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/${provider}/login`);
      const data = await response.json();

      if (data.redirect_url) {
        window.location.href = data.redirect_url;
      } else {
        setError(`Failed to get redirect URL from ${provider}`);
      }
    } catch (error) {
      setError(`Error initiating ${provider} login: ${error instanceof Error ? error.message : String(error)}`);
    }
  };

  const handleOAuthCallback = async (provider: string, code: string, state: string) => {
    try {
      setStatus(`Processing ${provider} login...`);
      const callbackUrlObj = new URL(window.location.href);

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/${provider}/callback${callbackUrlObj.search}`);
      const data = await response.json();

      if (data.token && data.user) {
        localStorage.setItem('authToken', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        setStatus('Login successful! Redirecting...');
        setTimeout(() => {
          router.push('/dashboard');
        }, 1000);
      } else if (data.error) {
        setError(`Authentication error: ${data.error}`);
      } else {
        setError('Failed to authenticate with the server');
      }
    } catch (error) {
      setError(`Error during ${provider} callback: ${error instanceof Error ? error.message : String(error)}`);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4 bg-gray-50">
      <div className="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
        <div className="text-center">
          <h1 className="text-2xl font-bold">OAuth Authentication</h1>
          {!error ? (
            <div className="mt-4">
              <p className="text-gray-600">{status}</p>
              <div className="mt-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
              </div>
            </div>
          ) : (
            <div className="mt-4">
              <p className="text-red-500">{error}</p>
              <div className="mt-4">
                <Link href="/login" className="text-blue-500 hover:text-blue-700 underline">
                  Return to login
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
