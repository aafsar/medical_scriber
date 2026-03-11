import type { Utterance } from '../../types';
import TranscriptLine from './TranscriptLine';

interface TranscriptViewProps {
  utterances: Utterance[];
  speakerMap: Record<number, string>;
}

export default function TranscriptView({ utterances, speakerMap }: TranscriptViewProps) {
  return (
    <div className="max-h-[50vh] overflow-y-auto rounded-lg border border-gray/20 bg-white p-2">
      {utterances.map((u, i) => (
        <TranscriptLine
          key={i}
          utterance={u}
          role={speakerMap[u.speaker] || `Speaker ${u.speaker}`}
        />
      ))}
    </div>
  );
}
