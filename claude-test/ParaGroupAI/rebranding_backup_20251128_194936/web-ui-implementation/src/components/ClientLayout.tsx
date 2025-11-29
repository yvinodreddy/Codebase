'use client';

import { ThemeProvider } from '@/contexts/ThemeContext';
import { ReactNode } from 'react';

export function ClientLayout({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      {children}
    </ThemeProvider>
  );
}
