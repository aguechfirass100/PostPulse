'use client';

import React from 'react';
import ProtectedRoute from '../../components/ProtectedRoute';
import { useAuth } from '../contexts/AuthContext';
import Link from 'next/link';

const Dashboard = () => {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <h1 className="text-xl font-bold text-indigo-600">Image Generation App</h1>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <Link
                    href="/dashboard"
                    className="border-indigo-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Dashboard
                  </Link>
                  <Link
                    href="/generate"
                    className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Generate Image
                  </Link>
                  <Link
                    href="/profile"
                    className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Profile
                  </Link>
                </div>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:items-center">
                <div className="ml-3 relative">
                  <div className="flex items-center space-x-3">
                    {user?.profilePicture ? (
                      <img
                        className="h-8 w-8 rounded-full"
                        src={user.profilePicture}
                        alt={user.name}
                      />
                    ) : (
                      <div className="h-8 w-8 rounded-full bg-indigo-600 flex items-center justify-center text-white">
                        {user?.name.charAt(0).toUpperCase()}
                      </div>
                    )}
                    <span className="text-sm text-gray-700">{user?.name}</span>
                    <button
                      onClick={handleLogout}
                      className="text-sm text-red-600 hover:text-red-800"
                    >
                      Logout
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <div className="py-10">
          <header>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            </div>
          </header>
          <main>
            <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
              <div className="px-4 py-8 sm:px-0">
                <div className="border-4 border-dashed border-gray-200 rounded-lg p-6">
                  <h2 className="text-xl font-semibold mb-4">Welcome, {user?.name}!</h2>
                  <p className="text-gray-600">
                    You're now logged in to the Image Generation App. Use the navigation above to generate images or update your profile.
                  </p>
                  
                  <div className="mt-6 border-t border-gray-200 pt-6">
                    <h3 className="text-lg font-medium">Your account details:</h3>
                    <ul className="mt-2 text-gray-600">
                      <li><strong>Email:</strong> {user?.email}</li>
                      {/* <li><strong>Sign-up method:</strong> {user?.provider?.charAt(0).toUpperCase() + user?.provider?.slice(1) || 'Email/Password'}</li> */}
                      <li><strong>Account created:</strong> {user?.createdAt ? new Date(user.createdAt).toLocaleString() : 'Unknown'}</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default Dashboard;