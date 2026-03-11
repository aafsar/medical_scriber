import { useState } from 'react';
import type { ConsultationNotes, PatientInfo } from '../../types';
import { downloadBlob } from '../../api/client';
import Button from '../ui/Button';
import Alert from '../ui/Alert';

interface DownloadButtonProps {
  notes: ConsultationNotes;
  patientInfo?: PatientInfo;
}

export default function DownloadButton({ notes, patientInfo }: DownloadButtonProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDownload = async () => {
    setLoading(true);
    setError(null);
    try {
      const blob = await downloadBlob('/api/notes/pdf', { notes });

      const name = patientInfo?.name?.trim() || '';
      const dos = patientInfo?.date_of_service?.replace(/\//g, '-') || '';
      let filename: string;
      if (name) {
        const base = name.toLowerCase().replace(/\s+/g, '_');
        filename = dos ? `${base}_${dos}_consultation.pdf` : `${base}_consultation.pdf`;
      } else {
        filename = 'consultation_notes.pdf';
      }

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate PDF. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Button variant="download" fullWidth loading={loading} onClick={handleDownload}>
        Download Notes (PDF)
      </Button>
      {error && (
        <div className="mt-2">
          <Alert type="error" onDismiss={() => setError(null)}>
            {error}
          </Alert>
        </div>
      )}
    </div>
  );
}
