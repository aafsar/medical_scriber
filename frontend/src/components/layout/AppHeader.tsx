interface AppHeaderProps {
  onMenuClick?: () => void;
  showMenu?: boolean;
  drawerOpen?: boolean;
}

export default function AppHeader({ onMenuClick, showMenu, drawerOpen = false }: AppHeaderProps) {
  return (
    <header className="flex items-center justify-between px-4 md:px-6 py-3 border-b-2 border-teal bg-cream">
      <div className="flex items-center gap-3">
        {showMenu && (
          <button
            onClick={onMenuClick}
            className="md:hidden p-1 text-ink hover:text-teal active:scale-95 transition-transform"
            aria-label={drawerOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={drawerOpen}
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        )}
        <img src="/Angy_logo_color.png" alt="Angy logo" className="h-10 md:h-12" />
      </div>
      <div className="text-center flex-1">
        <h1 className="text-xl font-bold text-ink">Angy Voice</h1>
        <p className="text-xs text-gray">AI-powered medical consultation scriber</p>
      </div>
      <div className="w-10 md:w-12" />
    </header>
  );
}
