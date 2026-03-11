import type { Utterance } from '../../types';

interface TranscriptLineProps {
  utterance: Utterance;
  role: string;
}

export default function TranscriptLine({ utterance, role }: TranscriptLineProps) {
  const isDoctor = role === 'Doctor';
  const totalSeconds = Math.floor(utterance.start);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  return (
    <div
      className={`px-3 py-2.5 rounded-md mb-1 border-l-[3px] ${
        isDoctor
          ? 'border-l-teal bg-teal/5'
          : 'border-l-patient bg-patient/10'
      }`}
    >
      <span className="font-semibold text-sm">{role}</span>
      <span className="text-gray-light text-xs ml-2">
        [{String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}]
      </span>
      <p className="text-sm mt-0.5">{utterance.text}</p>
    </div>
  );
}
