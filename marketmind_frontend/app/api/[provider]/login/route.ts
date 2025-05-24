import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: { provider: string } }
) {
  const { provider } = params;
  
  // Configure OAuth parameters based on provider
  let authUrl, clientId, redirectUri, scope;
  
  if (provider === 'google') {
    clientId = process.env.GOOGLE_CLIENT_ID;
    redirectUri = `${process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'}/oauth/google`;
    scope = 'email profile';
    authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&response_type=code&scope=${encodeURIComponent(scope)}&access_type=offline&prompt=consent`;
  } else if (provider === 'facebook') {
    clientId = process.env.FACEBOOK_CLIENT_ID;
    redirectUri = `${process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'}/oauth/facebook`;
    scope = 'email public_profile';
    authUrl = `https://www.facebook.com/v12.0/dialog/oauth?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}`;
  } else {
    return NextResponse.json({ message: `Unsupported provider: ${provider}` }, { status: 400 });
  }
  
  // Redirect to the OAuth provider's authorization URL
  return NextResponse.redirect(authUrl);
}