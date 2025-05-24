export interface User {
    id: string;
    email: string;
    name: string;
    profilePicture?: string;
    provider?: 'local' | 'google' | 'facebook';
    createdAt: string;
    updatedAt: string;
  }