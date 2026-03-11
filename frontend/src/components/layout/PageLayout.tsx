import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import AppHeader from './AppHeader';

interface PageLayoutProps {
  sidebar: React.ReactNode;
  children: React.ReactNode;
  nav?: React.ReactNode;
}

export default function PageLayout({ sidebar, children, nav }: PageLayoutProps) {
  const [drawerOpen, setDrawerOpen] = useState(false);

  return (
    <div className="min-h-screen flex flex-col">
      <a href="#main-content" className="skip-to-content">Skip to content</a>
      <AppHeader
        onMenuClick={() => setDrawerOpen((o) => !o)}
        showMenu={!!sidebar}
        drawerOpen={drawerOpen}
      />

      {nav && (
        <nav className="bg-cream border-b border-gray/20 px-4 md:px-6 py-2 flex gap-4">
          {nav}
        </nav>
      )}

      <div className="flex flex-1 overflow-hidden">
        {/* Desktop sidebar */}
        {sidebar && (
          <aside
            className="hidden md:block w-[280px] shrink-0 overflow-y-auto border-r border-gray/20"
            aria-label="Patient information"
          >
            {sidebar}
          </aside>
        )}

        {/* Mobile drawer */}
        <AnimatePresence>
          {sidebar && drawerOpen && (
            <>
              <motion.div
                className="fixed inset-0 bg-black/40 z-40 md:hidden"
                onClick={() => setDrawerOpen(false)}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.2 }}
              />
              <motion.aside
                className="fixed left-0 top-0 h-full w-[280px] z-50 md:hidden overflow-y-auto shadow-xl"
                aria-label="Patient information"
                initial={{ x: '-100%' }}
                animate={{ x: 0 }}
                exit={{ x: '-100%' }}
                transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              >
                <div className="relative">
                  <button
                    onClick={() => setDrawerOpen(false)}
                    className="absolute top-3 right-3 z-10 p-2.5 rounded-full hover:bg-gray/10 text-ink"
                    aria-label="Close menu"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  {sidebar}
                </div>
              </motion.aside>
            </>
          )}
        </AnimatePresence>

        {/* Main content */}
        <main id="main-content" className="flex-1 overflow-y-auto p-4 md:p-8 max-w-4xl mx-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
