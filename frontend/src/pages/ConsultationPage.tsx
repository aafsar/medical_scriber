import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import type { PatientInfo, AppConfig, HealthStatus } from '../types';
import useConsultation from '../hooks/useConsultation';
import PageLayout from '../components/layout/PageLayout';
import Sidebar from '../components/layout/Sidebar';
import SectionHeader from '../components/ui/SectionHeader';
import Button from '../components/ui/Button';
import Spinner from '../components/ui/Spinner';
import Alert from '../components/ui/Alert';
import ProgressBar from '../components/consultation/ProgressBar';
import AudioInput from '../components/consultation/AudioInput';
import AudioPlayer from '../components/consultation/AudioPlayer';
import TranscriptView from '../components/consultation/TranscriptView';
import SpeakerToggle from '../components/consultation/SpeakerToggle';
import NotesDisplay from '../components/consultation/NotesDisplay';
import DownloadButton from '../components/consultation/DownloadButton';

interface ConsultationPageProps {
  config: AppConfig;
  health: HealthStatus | null;
  nav?: React.ReactNode;
}

const emptyPatient: PatientInfo = {
  name: '',
  date_of_birth: '',
  date_of_service: new Date().toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' }),
  referring_physician: '',
  specialty: '',
};

const sectionVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3, ease: 'easeOut' as const } },
};

export default function ConsultationPage({ config, health, nav }: ConsultationPageProps) {
  const [patientInfo, setPatientInfo] = useState<PatientInfo>(
    config.demo_patient || emptyPatient,
  );
  const { state, dispatch, transcribe, generateNotes, setSpeakerMap } = useConsultation();

  useEffect(() => {
    if (config.demo_patient) {
      setPatientInfo(config.demo_patient);
    }
  }, [config.demo_patient]);

  const handleAudioReady = (blob: Blob, filename: string) => {
    dispatch({ type: 'SET_AUDIO', blob, filename });
  };

  // API key warnings
  const missingKeys: string[] = [];
  if (health) {
    if (config.mode === 'dev' && !health.api_keys.deepgram) missingKeys.push('Deepgram');
    if (!health.api_keys.elevenlabs) missingKeys.push('ElevenLabs');
    if (!health.api_keys.anthropic) missingKeys.push('Anthropic');
  }

  const sidebar = (
    <Sidebar
      patientInfo={patientInfo}
      onSave={setPatientInfo}
      specialties={config.specialties}
      mode={config.mode}
    />
  );

  return (
    <PageLayout sidebar={sidebar} nav={nav}>
      <ProgressBar
        hasAudio={!!state.audioBlob}
        hasTranscript={state.utterances.length > 0}
        isGenerating={state.isGenerating}
        hasNotes={!!state.notes}
      />

      {missingKeys.length > 0 && (
        <div className="mb-4">
          <Alert type="warning">
            Missing API keys: <strong>{missingKeys.join(', ')}</strong>. Add them to your <code>.env</code> file.
          </Alert>
        </div>
      )}

      {/* Section 1: Audio Input */}
      <motion.section
        className="mb-6"
        initial="hidden"
        animate="visible"
        variants={sectionVariants}
      >
        <SectionHeader number={1} title="Audio Input" />
        <AudioInput
          mode={config.mode}
          provider={state.provider}
          onProviderChange={(p) => dispatch({ type: 'SET_PROVIDER', provider: p })}
          onAudioReady={handleAudioReady}
        />
        <AudioPlayer blob={state.audioBlob} />
        {state.audioBlob && (
          <div className="mt-3">
            <Button
              fullWidth
              onClick={transcribe}
              loading={state.isTranscribing}
              disabled={state.isTranscribing}
            >
              Transcribe
            </Button>
          </div>
        )}
        {state.isTranscribing && <Spinner message="Transcribing audio..." />}
        {state.error && !state.isTranscribing && !state.isGenerating && (
          <div className="mt-2">
            <Alert type="error" onDismiss={() => dispatch({ type: 'CLEAR_ERROR' })}>
              {state.error}
            </Alert>
          </div>
        )}
      </motion.section>

      {/* Section 2: Transcript */}
      <AnimatePresence>
        {state.utterances.length > 0 && (
          <motion.section
            className="mb-6"
            initial="hidden"
            animate="visible"
            exit="hidden"
            variants={sectionVariants}
          >
            <SectionHeader number={2} title="Transcript" />
            {config.mode === 'dev' && (
              <p className="text-xs text-gray-light mb-2">
                Transcribed in {state.transcribeLatency.toFixed(1)}s via {state.provider}
              </p>
            )}
            <SpeakerToggle
              detectedDoctorSpeaker={state.detectedDoctorSpeaker}
              onToggle={setSpeakerMap}
              mode={config.mode}
            />
            <TranscriptView utterances={state.utterances} speakerMap={state.speakerMap} />

            {/* Section 3: Generate Notes */}
            <motion.div
              className="mt-6"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.15 }}
            >
              <SectionHeader number={3} title="Generate Notes" />
              <Button
                fullWidth
                onClick={() => generateNotes(patientInfo)}
                loading={state.isGenerating}
                disabled={state.isGenerating}
              >
                Generate Notes
              </Button>
              {state.isGenerating && <Spinner message="Generating consultation notes..." />}
              {state.error && state.isGenerating && (
                <div className="mt-2">
                  <Alert type="error" onDismiss={() => dispatch({ type: 'CLEAR_ERROR' })}>
                    {state.error}
                  </Alert>
                </div>
              )}
            </motion.div>
          </motion.section>
        )}
      </AnimatePresence>

      {/* Section 4: Notes + Download */}
      <AnimatePresence>
        {state.notes && (
          <motion.section
            className="mb-6"
            initial="hidden"
            animate="visible"
            exit="hidden"
            variants={sectionVariants}
          >
            <SectionHeader number={4} title="Consultation Notes" />
            <NotesDisplay notes={state.notes} latency={state.notesLatency} />
            <div className="mt-4">
              <DownloadButton notes={state.notes} patientInfo={patientInfo} />
            </div>
          </motion.section>
        )}
      </AnimatePresence>
    </PageLayout>
  );
}
