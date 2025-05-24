import { Suspense } from 'react';
import OAuthClient from './OAuthClient';

export default function OAuthPage() {
  return (
    <Suspense fallback={<div className="text-center p-8">Loading OAuth flow...</div>}>
      <OAuthClient />
    </Suspense>
  );
}
