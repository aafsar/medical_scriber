interface SpeakerToggleProps {
  detectedDoctorSpeaker: number;
  onToggle: (speakerMap: Record<number, string>) => void;
  mode: string;
}

export default function SpeakerToggle({ detectedDoctorSpeaker, onToggle }: SpeakerToggleProps) {
  const handleChange = (roleFor0: string) => {
    if (roleFor0 === 'Doctor') {
      onToggle({ 0: 'Doctor', 1: 'Patient' });
    } else {
      onToggle({ 0: 'Patient', 1: 'Doctor' });
    }
  };

  const defaultRoleFor0 = detectedDoctorSpeaker === 0 ? 'Doctor' : 'Patient';

  return (
    <div className="flex items-center gap-3 text-sm mb-3">
      <span className="text-gray">Speaker 0 is:</span>
      {['Doctor', 'Patient'].map((role) => (
        <label key={role} className="inline-flex items-center gap-1 cursor-pointer">
          <input
            type="radio"
            name="speakerRole"
            value={role}
            defaultChecked={role === defaultRoleFor0}
            onChange={() => handleChange(role)}
            className="accent-teal"
          />
          {role}
        </label>
      ))}
    </div>
  );
}
