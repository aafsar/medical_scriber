import { motion, AnimatePresence } from 'framer-motion';
import { PATIENT_INFO_FIELDS } from '../../types';

interface PatientInfoNoteProps {
  info: Record<string, string>;
  isOpen: boolean;
  onToggle: () => void;
}

export default function PatientInfoNote({ info, isOpen, onToggle }: PatientInfoNoteProps) {
  return (
    <div className="border border-gray/20 rounded-lg overflow-hidden">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between px-4 py-2.5 bg-white cursor-pointer hover:bg-teal-light font-semibold text-sm select-none text-left transition-colors"
        aria-expanded={isOpen}
      >
        <span>Patient Information</span>
        <motion.svg
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
          className="w-4 h-4 text-gray shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </motion.svg>
      </button>
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2, ease: 'easeInOut' }}
            className="overflow-hidden"
          >
            <div className="px-4 py-3 bg-white border-t border-gray/10 space-y-1">
              {PATIENT_INFO_FIELDS.map(([key, label]) => {
                const value = info[key] || 'Not provided';
                return (
                  <div key={key} className="text-sm">
                    <span className="font-medium">{label}:</span>{' '}
                    {value === 'Not provided' ? (
                      <span className="text-gray">{value}</span>
                    ) : (
                      <span>{value}</span>
                    )}
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
