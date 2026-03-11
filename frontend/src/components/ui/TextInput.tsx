import { useId } from 'react';

interface TextInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: boolean;
}

export default function TextInput({ label, error, className = '', id: externalId, ...props }: TextInputProps) {
  const generatedId = useId();
  const inputId = externalId || generatedId;

  return (
    <div>
      {label && (
        <label htmlFor={inputId} className="block text-sm font-medium text-ink mb-1">
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={`w-full rounded-lg border bg-white px-3 py-3 md:py-2 text-sm text-ink focus:outline-none focus:ring-2 focus:ring-teal/50 ${error ? 'border-error' : 'border-gray/30'} ${className}`}
        {...props}
      />
    </div>
  );
}
