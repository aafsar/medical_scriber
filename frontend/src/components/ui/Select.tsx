import { useId } from 'react';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: string[];
}

export default function Select({ label, options, className = '', id: externalId, ...props }: SelectProps) {
  const generatedId = useId();
  const selectId = externalId || generatedId;

  return (
    <div>
      {label && (
        <label htmlFor={selectId} className="block text-sm font-medium text-ink mb-1">
          {label}
        </label>
      )}
      <select
        id={selectId}
        className={`w-full rounded-lg border border-gray/30 bg-white px-3 py-3 md:py-2 text-sm text-ink focus:outline-none focus:ring-2 focus:ring-teal/50 ${className}`}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {opt}
          </option>
        ))}
      </select>
    </div>
  );
}
