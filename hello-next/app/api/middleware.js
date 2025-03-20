import { NextResponse } from 'next/server';

export function middleware(req) {
  const authToken = req.cookies.get('authToken');

  if (!authToken) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  return NextResponse.next(); // Continue request
}

export const config = {
  matcher: '/dashboard/:path*', // Apply middleware only to /dashboard/*
};
