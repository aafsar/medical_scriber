import { useState, useEffect } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import type { PatientInfo } from '../../types';
import Button from '../ui/Button';
import TextInput from '../ui/TextInput';
import Select from '../ui/Select';

interface SidebarProps {
  patientInfo: PatientInfo;
  onSave: (info: PatientInfo) => void;
  specialties: string[];
  mode: string;
}

export default function Sidebar({ patientInfo, onSave, specialties, mode }: SidebarProps) {
  const [form, setForm] = useState<PatientInfo>(patientInfo);
  const [saved, setSaved] = useState(false);
  const [attempted, setAttempted] = useState(false);

  useEffect(() => {
    setForm(patientInfo);
  }, [patientInfo]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setAttempted(true);
    if (!form.name.trim()) return;
    onSave(form);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const update = (field: keyof PatientInfo, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <div className="h-full bg-sidebar p-4 flex flex-col">
      <form onSubmit={handleSubmit} className="space-y-3">
        <h2 className="text-sm font-semibold text-ink uppercase tracking-wide">Patient Information</h2>
        <TextInput
          label="Patient Name"
          value={form.name}
          onChange={(e) => update('name', e.target.value)}
          error={attempted && !form.name.trim()}
          required
        />
        <TextInput
          label="Date of Birth"
          type={mode === 'demo' ? 'text' : 'date'}
          value={form.date_of_birth}
          onChange={(e) => update('date_of_birth', e.target.value)}
        />
        <TextInput
          label="Date of Service"
          type={mode === 'demo' ? 'text' : 'date'}
          value={form.date_of_service}
          onChange={(e) => update('date_of_service', e.target.value)}
        />
        <TextInput
          label="Referring Physician"
          value={form.referring_physician}
          onChange={(e) => update('referring_physician', e.target.value)}
        />
        <Select
          label="Specialty"
          options={specialties}
          value={form.specialty}
          onChange={(e) => update('specialty', e.target.value)}
        />
        <Button type="submit" fullWidth>
          Save Patient Info
        </Button>
        <AnimatePresence>
          {saved && (
            <motion.div
              initial={{ opacity: 0, y: -4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="flex items-center justify-center gap-1.5 text-xs text-success"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Patient info saved.
            </motion.div>
          )}
        </AnimatePresence>
      </form>

      {patientInfo.name && (
        <div className="mt-4 pt-4 border-t border-gray/30">
          <p className="text-sm font-semibold text-ink">Current Patient: {patientInfo.name}</p>
          {patientInfo.specialty && (
            <p className="text-xs text-gray">{patientInfo.specialty}</p>
          )}
        </div>
      )}
    </div>
  );
}
