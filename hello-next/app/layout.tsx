import { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div>
      <header>
        <nav>
          <a href="/">Home</a> | <a href="/about">About</a> | <a href="/contact">Contact</a>
        </nav>
      </header>
      <main>{children}</main>
      <footer>
        <p>© 2024 My Next.js App</p>
      </footer>
    </div>
  );
}
