import { useRef, useEffect } from 'react';
import useAudioRecorder from '../../hooks/useAudioRecorder';
import WaveformVisualizer from './WaveformVisualizer';
import Button from '../ui/Button';
import Select from '../ui/Select';
import Alert from '../ui/Alert';

interface AudioInputProps {
  mode: string;
  provider: string;
  onProviderChange: (provider: string) => void;
  onAudioReady: (blob: Blob, filename: string) => void;
}

export default function AudioInput({ mode, provider, onProviderChange, onAudioReady }: AudioInputProps) {
  const { isRecording, audioBlob, duration, error, audioStream, startRecording, stopRecording } = useAudioRecorder();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const lastBlobRef = useRef<Blob | null>(null);

  const handleRecord = async () => {
    if (isRecording) {
      stopRecording();
    } else {
      await startRecording();
    }
  };

  // When recording finishes, pass blob up (only once per new blob)
  useEffect(() => {
    if (audioBlob && audioBlob !== lastBlobRef.current) {
      lastBlobRef.current = audioBlob;
      onAudioReady(audioBlob, 'recording.webm');
    }
  }, [audioBlob, onAudioReady]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onAudioReady(file, file.name);
    }
  };

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-4">
        {mode === 'dev' && (
          <>
            <Select
              label="Provider"
              options={['Deepgram', 'ElevenLabs']}
              value={provider}
              onChange={(e) => onProviderChange(e.target.value)}
              className="w-auto"
            />
          </>
        )}
      </div>

      {/* Record UI */}
      <div className="space-y-2">
        <Button
          onClick={handleRecord}
          variant={isRecording ? 'secondary' : 'primary'}
          fullWidth
        >
          {isRecording ? 'Stop Recording' : 'Start Recording'}
        </Button>

        {isRecording && (
          <WaveformVisualizer stream={audioStream} isRecording={isRecording} duration={duration} />
        )}
      </div>

      {/* Upload UI (dev only) */}
      {mode === 'dev' && (
        <div>
          <p className="text-sm text-gray mb-1">Or upload an audio file:</p>
          <input
            ref={fileInputRef}
            type="file"
            accept="audio/*"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-teal file:text-cream hover:file:bg-teal-dark file:cursor-pointer cursor-pointer"
          />
        </div>
      )}

      {error && <Alert type="error">{error}</Alert>}
    </div>
  );
}
