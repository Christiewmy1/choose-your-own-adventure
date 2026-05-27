import { useEffect, useState } from 'react';
import type { StudentProfile } from '../types';

interface ProfileFormProps {
  profile: StudentProfile;
  error: string;
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

const ProfileForm = ({ profile, error, onSubmit, onBack }: ProfileFormProps) => {
  const [localProfile, setLocalProfile] = useState(profile);

  useEffect(() => {
    setLocalProfile(profile);
  }, [profile]);

  const updateField = (key: keyof StudentProfile, value: string) => {
    setLocalProfile(prev => ({
      ...prev,
      [key]: value,
    }));
  };

  return (
    <section className="section-panel card profile-panel">
      <div className="profile-header">
        <div>
          <span className="eyebrow">Your Husky profile</span>
          <h2>Tell us about your major, progress, and career direction.</h2>
          <p>We’ll use this information to generate course recommendations and company alignment insights.</p>
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
        <div className="input-group">
          <label htmlFor="major">Major</label>
          <input
            id="major"
            value={localProfile.major}
            onChange={e => updateField('major', e.target.value)}
            placeholder="e.g. CSSE, Applied Computing, Electrical Engineering, Computer Engineering"
            required
          />
          <p className="small-copy">Current prototype scope: UW Bothell CSSE, Applied Computing, Electrical Engineering, Computer Engineering, Data Visualization, and the technology-facing side of Business Administration.</p>
        </div>

        <div className="input-group">
          <label htmlFor="standing">Current standing</label>
          <select
            id="standing"
            value={localProfile.standing}
            onChange={e => updateField('standing', e.target.value)}
          >
            {standingOptions.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </div>

        <div className="input-group full-width">
          <label htmlFor="completedCourses">Completed courses</label>
          <textarea
            id="completedCourses"
            value={localProfile.completedCourses}
            onChange={e => updateField('completedCourses', e.target.value)}
            placeholder="List the classes you’ve already taken (e.g. CSS 142, CSS 143, CSS 301, MATH 124)."
          />
          <p className="small-copy">Best results come from UWB-style course histories such as CSS, EE, BIS, and related math courses.</p>
        </div>

        <div className="input-group full-width">
          <label htmlFor="careerGoals">Career goals</label>
          <textarea
            id="careerGoals"
            value={localProfile.careerGoals}
            onChange={e => updateField('careerGoals', e.target.value)}
            placeholder="Use commas to list goals like systems, embedded, software engineering, cloud."
            required
          />
        </div>

        <div className="input-group full-width">
          <label htmlFor="targetCompanies">Target companies or field</label>
          <textarea
            id="targetCompanies"
            value={localProfile.targetCompanies}
            onChange={e => updateField('targetCompanies', e.target.value)}
            placeholder="Optional: Boeing, Snowflake, Deloitte, Nintendo of America, Seattle Children's"
          />
          <p className="small-copy">Current dataset includes 100+ companies across aerospace, cloud, security, healthcare, gaming, AI/data, and business-tech pathways.</p>
        </div>

        <div className="form-actions">
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
