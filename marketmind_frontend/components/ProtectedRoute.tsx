'use client';

import React, { ReactNode } from 'react';
import { useAuth } from '../app/contexts/AuthContext';
import { useRouter } from 'next/navigation';

interface ProtectedRouteProps {
  children: ReactNode;
  redirectTo?: string;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  redirectTo = '/login' 
}) => {
  const { user, loading } = useAuth();
  const router = useRouter();
  
  // If auth is still loading, show a loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }
  
  // If no user is logged in, redirect to the login page
  if (!user) {
    // We use setTimeout to ensure this happens after component rendering
    // This is a workaround for React Suspense/hydration in Next.js
    setTimeout(() => {
      router.push(redirectTo);
    }, 0);
    
    // Return null or a loading state while redirecting
    return null;
  }
  
  // If the user is authenticated, render the protected content
  return <>{children}</>;
};

export default ProtectedRoute;