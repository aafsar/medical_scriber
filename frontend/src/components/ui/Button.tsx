import { motion, AnimatePresence } from 'framer-motion';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'download';
  fullWidth?: boolean;
  loading?: boolean;
  children: React.ReactNode;
  disabled?: boolean;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
  onClick?: () => void;
}

export default function Button({
  variant = 'primary',
  fullWidth = false,
  loading = false,
  children,
  disabled,
  className = '',
  type = 'button',
  onClick,
}: ButtonProps) {
  const base =
    'inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2.5 font-medium text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-teal/50 disabled:opacity-50 disabled:cursor-not-allowed';

  const variants = {
    primary: 'bg-teal text-cream hover:bg-teal-dark',
    secondary: 'bg-sidebar text-ink hover:bg-gray/20 border border-gray/30',
    download: 'bg-teal text-cream hover:bg-teal-dark',
  };

  const width = fullWidth ? 'w-full' : '';

  return (
    <motion.button
      layout
      className={`${base} ${variants[variant]} ${width} ${className}`}
      disabled={disabled || loading}
      aria-busy={loading}
      type={type}
      onClick={onClick}
    >
      <AnimatePresence mode="wait">
        {loading && (
          <motion.svg
            key="spinner"
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.5 }}
            className="animate-spin h-4 w-4"
            viewBox="0 0 24 24"
            fill="none"
          >
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </motion.svg>
        )}
      </AnimatePresence>
      {loading ? 'Loading...' : children}
    </motion.button>
  );
}
