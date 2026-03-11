interface ProgressBarProps {
  hasAudio: boolean;
  hasTranscript: boolean;
  isGenerating: boolean;
  hasNotes: boolean;
}

const steps = [
  { label: 'Audio', shortLabel: 'Audio', key: 'audio' },
  { label: 'Transcript', shortLabel: 'Script', key: 'transcript' },
  { label: 'Generate', shortLabel: 'Gen', key: 'generate' },
  { label: 'Notes', shortLabel: 'Notes', key: 'notes' },
] as const;

export default function ProgressBar({ hasAudio, hasTranscript, isGenerating, hasNotes }: ProgressBarProps) {
  const getStepStatus = (key: string): 'completed' | 'active' | 'upcoming' => {
    switch (key) {
      case 'audio':
        return hasAudio ? 'completed' : 'active';
      case 'transcript':
        if (hasTranscript) return 'completed';
        return hasAudio ? 'active' : 'upcoming';
      case 'generate':
        if (hasNotes) return 'completed';
        if (isGenerating || hasTranscript) return 'active';
        return 'upcoming';
      case 'notes':
        if (hasNotes) return 'completed';
        return 'upcoming';
      default:
        return 'upcoming';
    }
  };

  return (
    <div className="mb-6">
      <div className="flex items-center justify-between">
        {steps.map((step, i) => {
          const status = getStepStatus(step.key);
          return (
            <div key={step.key} className="flex items-center flex-1 last:flex-none">
              <div className="flex flex-col items-center min-w-0">
                <div
                  className={`w-7 h-7 md:w-8 md:h-8 rounded-full flex items-center justify-center text-xs font-semibold transition-colors ${
                    status === 'completed'
                      ? 'bg-teal text-cream'
                      : status === 'active'
                        ? 'bg-teal-light text-teal border-2 border-teal'
                        : 'bg-gray/10 text-gray border border-gray/30'
                  }`}
                >
                  {status === 'completed' ? (
                    <svg className="w-3.5 h-3.5 md:w-4 md:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    i + 1
                  )}
                </div>
                <span
                  className={`text-[10px] md:text-xs mt-1 truncate max-w-full ${
                    status === 'upcoming' ? 'text-gray-light' : 'text-ink font-medium'
                  }`}
                >
                  <span className="hidden md:inline">{step.label}</span>
                  <span className="md:hidden">{step.shortLabel}</span>
                </span>
              </div>
              {i < steps.length - 1 && (
                <div
                  className={`flex-1 h-0.5 mx-1 md:mx-2 mt-[-1rem] ${
                    getStepStatus(steps[i + 1].key) !== 'upcoming' ? 'bg-teal' : 'bg-gray/20'
                  }`}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
