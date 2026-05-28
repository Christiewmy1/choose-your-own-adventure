import { useEffect, useState } from 'react';
import type { StudentProfile } from '../types';
import { fieldHelp, majorOptions } from '../constants';
import { samplePersonas } from '../data/personas';
import { careerGoalSuggestions, commonCoursesByMajor } from '../data/careerGoalSuggestions';
import { companyOptions } from '../data/companyOptions';
import CourseTagInput from '../components/CourseTagInput';
import TagInput from '../components/TagInput';

interface ProfileFormProps {
  profile: StudentProfile;
  error: string;
  fieldErrors?: Partial<Record<keyof StudentProfile, string>>;
  onSubmit: (profile: StudentProfile) => void;
  onBack: () => void;
}

const standingOptions: StudentProfile['standing'][] = [
  'Freshman',
  'Sophomore',
  'Junior',
  'Senior',
  'Graduate',
];

const FEATURED_PERSONA_COUNT = 3;

const mergeCourses = (existing: string, toAdd: string[]) => {
  const current = existing
    .split(',')
    .map(item => item.trim())
    .filter(Boolean);
  const merged = [...current];
  for (const code of toAdd) {
    if (!merged.includes(code)) {
      merged.push(code);
    }
  }
  return merged.join(', ');
};

const ProfileForm = ({ profile, error, fieldErrors = {}, onSubmit, onBack }: ProfileFormProps) => {
  const [localProfile, setLocalProfile] = useState(profile);
  const [selectedPersonaId, setSelectedPersonaId] = useState('');
  const [showAllPersonas, setShowAllPersonas] = useState(false);

  useEffect(() => {
    setLocalProfile(profile);
  }, [profile]);

  const updateField = (key: keyof StudentProfile, value: string) => {
    setLocalProfile(prev => ({
      ...prev,
      [key]: value,
    }));
  };

  const applyPersona = (personaId: string) => {
    const persona = samplePersonas.find(item => item.id === personaId);
    if (!persona) {
      return;
    }
    setSelectedPersonaId(personaId);
    setLocalProfile(persona.profile);
  };

  const addCommonCourses = () => {
    const courses = commonCoursesByMajor[localProfile.major] ?? [];
    if (courses.length === 0) {
      return;
    }
    updateField('completedCourses', mergeCourses(localProfile.completedCourses, courses));
  };

  const visiblePersonas = showAllPersonas ? samplePersonas : samplePersonas.slice(0, FEATURED_PERSONA_COUNT);

  return (
    <section className="section-panel card profile-panel">
      <div className="profile-header">
        <div>
          <span className="eyebrow">Your Husky profile</span>
          <h2>Tell us about your major, progress, and career direction.</h2>
          <p>We use this to generate course picks, company alignment, internship prep, and a quarter roadmap.</p>
        </div>
      </div>

      <div className="persona-section">
        <div className="persona-section-header">
          <div>
            <h3>Quick demos</h3>
            <p className="small-copy">Load a sample student to explore HuskyAdvisor instantly.</p>
          </div>
          {samplePersonas.length > FEATURED_PERSONA_COUNT && (
            <button type="button" className="button-ghost" onClick={() => setShowAllPersonas(prev => !prev)}>
              {showAllPersonas ? 'Show fewer' : `Show all ${samplePersonas.length}`}
            </button>
          )}
        </div>
        <div className="persona-grid">
          {visiblePersonas.map(persona => (
            <button
              key={persona.id}
              type="button"
              className={`persona-chip${selectedPersonaId === persona.id ? ' persona-chip-active' : ''}`}
              onClick={() => applyPersona(persona.id)}
            >
              <span className="persona-label">{persona.label}</span>
              <span className="persona-description">{persona.description}</span>
            </button>
          ))}
        </div>
      </div>

      {error && <div className="alert">{error}</div>}

      <form
        onSubmit={e => {
          e.preventDefault();
          onSubmit(localProfile);
        }}
        className="form-grid"
      >
        <h3 className="form-section-title full-width">Academics</h3>

        <div className={`input-group${fieldErrors.major ? ' has-error' : ''}`}>
          <label htmlFor="major">Major</label>
          <p className="field-help">{fieldHelp.major}</p>
          <select
            id="major"
            value={localProfile.major}
            onChange={e => updateField('major', e.target.value)}
            required
          >
            <option value="">Select a major</option>
            {majorOptions.map(option => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
          {fieldErrors.major && <p className="field-error">{fieldErrors.major}</p>}
          <p className="small-copy">Current prototype scope: UW Bothell CSSE, Applied Computing, Electrical Engineering, Computer Engineering, Data Visualization, and the technology-facing side of Business Administration.</p>
        </div>

        <div className="input-group">
          <label htmlFor="standing">Current standing</label>
          <p className="field-help">{fieldHelp.standing}</p>
          <select
            id="standing"
            value={localProfile.standing}
            onChange={e => updateField('standing', e.target.value)}
          >
            {standingOptions.map(option => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        <div className="full-width">
          <CourseTagInput
            id="completedCourses"
            label="Completed courses"
            help={fieldHelp.completedCourses}
            value={localProfile.completedCourses}
            onChange={value => updateField('completedCourses', value)}
            onAddCommon={localProfile.major ? addCommonCourses : undefined}
            commonLabel={
              localProfile.major
                ? `Add common ${localProfile.major} courses`
                : undefined
            }
            placeholder="List the classes you’ve already taken (e.g. CSS 142, CSS 143, CSS 301, MATH 124)."
          />
          <p className="small-copy">Best results come from UWB-style course histories such as CSS, EE, BIS, and related math courses.</p>
        </div>

        <h3 className="form-section-title full-width">Career direction</h3>

        <div className="full-width">
          <TagInput
            id="careerGoals"
            label="Career goals"
            help={fieldHelp.careerGoals}
            value={localProfile.careerGoals}
            suggestions={[...careerGoalSuggestions]}
            placeholder="Add goals like cloud, embedded, analytics"
            required
            error={fieldErrors.careerGoals}
            onChange={value => updateField('careerGoals', value)}
          />
        </div>

        <div className="input-group full-width">
          <label htmlFor="targetCompanies">Target company</label>
          <p className="field-help">{fieldHelp.targetCompanies}</p>
          <select
            id="targetCompanies"
            value={localProfile.targetCompanies}
            onChange={e => updateField('targetCompanies', e.target.value)}
          >
            <option value="">Optional — select a company</option>
            {companyOptions.map(company => (
              <option key={company} value={company}>
                {company}
              </option>
            ))}
          </select>
          <p className="small-copy">Current dataset includes 100+ companies across aerospace, cloud, security, healthcare, gaming, AI/data, and business-tech pathways.</p>
        </div>

        <div className="form-actions full-width">
          <button className="button-secondary" onClick={onBack} type="button">
            Back to landing
          </button>
          <button className="button-primary" type="submit">
            See recommendations
          </button>
        </div>
      </form>
    </section>
  );
};

export default ProfileForm;
