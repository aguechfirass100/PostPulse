import { NextRequest, NextResponse } from 'next/server';

export async function POST(
  request: NextRequest,
  { params }: { params: { provider: string } }
) {
  const { provider } = params;
  
  // Get the request body
  const body = await request.json();
  
  // Forward the request to the backend
  // const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const response = await fetch("http://localhost:8000/api/auth/signup", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  
  // If the response is not ok, return an error
  if (!response.ok) {
    const error = await response.json();
    return NextResponse.json(error, { status: response.status });
  }
  
  // Return the response
  const data = await response.json();
  return NextResponse.json(data);
}