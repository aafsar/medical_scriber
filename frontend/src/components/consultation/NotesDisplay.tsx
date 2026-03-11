import { useState, useCallback } from 'react';
import { NOTE_SECTIONS } from '../../types';
import type { ConsultationNotes } from '../../types';
import NoteSection from './NoteSection';
import PatientInfoNote from './PatientInfoNote';

interface NotesDisplayProps {
  notes: ConsultationNotes;
  latency?: number;
}

export default function NotesDisplay({ notes, latency }: NotesDisplayProps) {
  const [openSections, setOpenSections] = useState<Record<string, boolean>>(() => {
    const initial: Record<string, boolean> = {};
    NOTE_SECTIONS.forEach(([key]) => {
      if (key === 'patient_information') {
        initial[key] = true;
      } else {
        const content = (notes[key] as string) || 'Not discussed';
        initial[key] = content !== 'Not discussed';
      }
    });
    return initial;
  });

  const allOpen = NOTE_SECTIONS.every(([key]) => openSections[key]);

  const toggleAll = useCallback(() => {
    const newState: Record<string, boolean> = {};
    const setTo = !allOpen;
    NOTE_SECTIONS.forEach(([key]) => {
      newState[key] = setTo;
    });
    setOpenSections(newState);
  }, [allOpen]);

  const toggleSection = useCallback((key: string) => {
    setOpenSections((prev) => ({ ...prev, [key]: !prev[key] }));
  }, []);

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        {latency !== undefined && (
          <p className="text-xs text-gray-light">Notes generated in {latency.toFixed(1)}s</p>
        )}
        <button
          onClick={toggleAll}
          className="text-xs text-teal hover:text-teal-dark font-medium ml-auto"
        >
          {allOpen ? 'Collapse All' : 'Expand All'}
        </button>
      </div>
      {NOTE_SECTIONS.map(([key, label]) => {
        if (key === 'patient_information') {
          const info = typeof notes[key] === 'object' ? (notes[key] as Record<string, string>) : {};
          return (
            <PatientInfoNote
              key={key}
              info={info}
              isOpen={openSections[key] ?? true}
              onToggle={() => toggleSection(key)}
            />
          );
        }
        return (
          <NoteSection
            key={key}
            label={label}
            content={(notes[key] as string) || 'Not discussed'}
            isOpen={openSections[key] ?? false}
            onToggle={() => toggleSection(key)}
          />
        );
      })}
    </div>
  );
}
