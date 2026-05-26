import { useState } from 'react';
import type { AdvisingResult, DashboardResults, StudentProfile } from '../types';
import DisclaimerBanner from '../components/DisclaimerBanner';
import { formatResultsForCopy } from '../utils/formatResults';
import { findCautionForCourse, parseCourseRecommendation } from '../utils/parseCourse';

interface RecommendationsProps {
  profile: StudentProfile;
  results: DashboardResults | null;
  error: string;
  onEditProfile: () => void;
  onRetry?: () => void;
}

type ResultTab = 'courses' | 'companies' | 'internship' | 'roadmap';

const tabConfig: {
  id: ResultTab;
  label: string;
  icon: string;
  key: keyof DashboardResults;
}[] = [
  { id: 'courses', label: 'Courses', icon: '📚', key: 'recommendations' },
  { id: 'companies', label: 'Companies', icon: '🏢', key: 'companies' },
  { id: 'internship', label: 'Internship Prep', icon: '🎯', key: 'internshipPrep' },
  { id: 'roadmap', label: 'Roadmap', icon: '🗓️', key: 'roadmap' },
];

const alignmentBadges = ['badge-strong', 'badge-good', 'badge-moderate'];

const groupInternshipItems = (items: string[]) => {
  const groups = {
    courses: [] as string[],
    projects: [] as string[],
    skills: [] as string[],
    other: [] as string[],
  };

  for (const item of items) {
    const lower = item.toLowerCase();
    if (/\b[A-Z]{2,4}\s?\d{3}/.test(item) || lower.includes('course') || lower.includes('css ') || lower.includes('ee ')) {
      groups.courses.push(item);
    } else if (lower.includes('project') || lower.includes('portfolio') || lower.includes('build')) {
      groups.projects.push(item);
    } else if (lower.includes('skill') || lower.includes('practice') || lower.includes('focus')) {
      groups.skills.push(item);
    } else {
      groups.other.push(item);
    }
  }

  return groups;
};

const groupRoadmapItems = (items: string[]) => {
  const quarterOrder = ['winter', 'spring', 'summer', 'autumn', 'fall', 'quarter'];
  const buckets: { label: string; items: string[] }[] = quarterOrder.map(label => ({
    label: label.charAt(0).toUpperCase() + label.slice(1),
    items: [],
  }));
  const general: string[] = [];

  for (const item of items) {
    const lower = item.toLowerCase();
    const index = quarterOrder.findIndex(quarter => lower.includes(quarter));
    if (index >= 0) {
      buckets[index].items.push(item);
    } else {
      general.push(item);
    }
  }

  const filled = buckets.filter(bucket => bucket.items.length > 0);
  if (general.length > 0) {
    filled.push({ label: 'General plan', items: general });
  }

  return filled.length > 0 ? filled : [{ label: 'Quarter plan', items }];
};

const ProfileSummary = ({ profile }: { profile: StudentProfile }) => {
  const courseCount = profile.completedCourses
    .split(',')
    .map(item => item.trim())
    .filter(Boolean).length;

  return (
    <div className="profile-summary">
      <span className="summary-chip">{profile.major || 'Undeclared major'}</span>
      <span className="summary-chip">{profile.standing}</span>
      {courseCount > 0 && <span className="summary-chip">{courseCount} courses completed</span>}
    </div>
  );
};

const renderCourseCards = (items: string[], cautions: string[]) => (
  <div className="course-card-grid">
    {items.map((item, index) => {
      const parsed = parseCourseRecommendation(item);
      const caution = findCautionForCourse(parsed.code, cautions);
      return (
        <article key={`course-card-${index}`} className="course-card">
          <div className="course-card-header">
            {parsed.code && <span className="course-code-badge">{parsed.code}</span>}
            <h5>{parsed.title}</h5>
          </div>
          {parsed.description && <p className="small-copy">{parsed.description}</p>}
          {caution && (
            <p className="course-card-caution">
              <strong>Keep in mind:</strong> {caution}
            </p>
          )}
        </article>
      );
    })}
  </div>
);

const renderCompanyList = (items: string[]) => (
  <ul className="result-list structured-list">
    {items.map((item, index) => (
      <li key={`company-${index}`} className="company-item">
        <div className="company-header">
          <span className="company-name">{item.split(':')[0]}</span>
          <span className={`alignment-badge ${alignmentBadges[index % alignmentBadges.length]}`}>
            {index === 0 ? 'Strong fit' : index === 1 ? 'Good fit' : 'Moderate fit'}
          </span>
        </div>
        {item.includes(':') && <p className="small-copy">{item.split(':').slice(1).join(':').trim()}</p>}
        {!item.includes(':') && <p className="small-copy">Regional company alignment based on your goals.</p>}
      </li>
    ))}
  </ul>
);

const renderInternshipPrep = (items: string[]) => {
  const groups = groupInternshipItems(items);

  return (
    <div className="grouped-results">
      {groups.courses.length > 0 && (
        <div className="result-section">
          <h4>Courses to prioritize</h4>
          <ul className="result-list">{groups.courses.map((item, i) => <li key={i}>{item}</li>)}</ul>
        </div>
      )}
      {groups.projects.length > 0 && (
        <div className="result-section">
          <h4>Project ideas</h4>
          <ul className="result-list">{groups.projects.map((item, i) => <li key={i}>{item}</li>)}</ul>
        </div>
      )}
      {groups.skills.length > 0 && (
        <div className="result-section">
          <h4>Skills to build</h4>
          <ul className="result-list">{groups.skills.map((item, i) => <li key={i}>{item}</li>)}</ul>
        </div>
      )}
      {groups.other.length > 0 && (
        <div className="result-section">
          <h4>Additional steps</h4>
          <ul className="result-list">{groups.other.map((item, i) => <li key={i}>{item}</li>)}</ul>
        </div>
      )}
    </div>
  );
};

const renderRoadmap = (items: string[]) => {
  const groups = groupRoadmapItems(items);

  return (
    <div className="timeline-results">
      {groups.map(group => (
        <div key={group.label} className="timeline-block">
          <h4>{group.label}</h4>
          <ul className="result-list">
            {group.items.map((item, index) => (
              <li key={`${group.label}-${index}`}>{item}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

const renderResultBody = (tab: ResultTab, result: AdvisingResult) => {
  switch (tab) {
    case 'courses':
      return renderCourseCards(result.recommendations, result.cautions);
    case 'companies':
      return renderCompanyList(result.recommendations);
    case 'internship':
      return renderInternshipPrep(result.recommendations);
    case 'roadmap':
      return renderRoadmap(result.recommendations);
    default:
      return null;
  }
};

const sectionDescriptions: Record<ResultTab, string> = {
  courses: 'Course recommendations based on your profile, completed coursework, and UWB-focused planning data.',
  companies:
    'This section connects your academic path to regional companies. It is not a live job board, but it helps you understand which classes and skills fit likely career directions.',
  internship:
    'This plan turns your goals into next steps by highlighting useful courses, project ideas, and skill areas before internship season.',
  roadmap: 'A quarter-by-quarter planning view to help you sequence coursework and preparation over time.',
};

const Recommendations = ({ profile, results, error, onEditProfile, onRetry }: RecommendationsProps) => {
  const [activeTab, setActiveTab] = useState<ResultTab>('courses');
  const [copyMessage, setCopyMessage] = useState('');

  const handleCopy = async () => {
    if (!results) {
      return;
    }
    const text = formatResultsForCopy(profile, results);
    try {
      await navigator.clipboard.writeText(text);
      setCopyMessage('Plan copied to clipboard.');
    } catch {
      setCopyMessage('Could not copy automatically — select and copy manually.');
    }
    window.setTimeout(() => setCopyMessage(''), 2500);
  };

  if (error) {
    return (
      <section className="section-panel card">
        <div className="recommendation-header">
          <div>
            <span className="eyebrow">Result connection issue</span>
            <h2>HuskyAdvisor could not load live recommendations.</h2>
            <p>{error}</p>
            <div className="local-api-help">
              <p className="small-copy">
                <strong>Running locally?</strong> Start the API in a separate terminal:
              </p>
              <code>.venv/bin/uvicorn api.main:app --host 127.0.0.1 --port 8000</code>
            </div>
          </div>
          <div className="header-actions">
            {onRetry && (
              <button className="button-primary" type="button" onClick={onRetry}>
                Retry
              </button>
            )}
            <button className="button-secondary" type="button" onClick={onEditProfile}>
              Adjust profile
            </button>
          </div>
        </div>
      </section>
    );
  }

  if (!results) {
    return null;
  }

  const activeConfig = tabConfig.find(tab => tab.id === activeTab) ?? tabConfig[0];
  const activeResult = results[activeConfig.key];

  return (
    <section className="section-panel card results-page">
      <div className="recommendation-header">
        <div>
          <span className="eyebrow">Your tailored results</span>
          <h2>Your HuskyAdvisor recommendations</h2>
          <p>
            These recommendations are based on your profile, completed coursework, and HuskyAdvisor&apos;s
            UW Bothell-focused planning data.
          </p>
        </div>
        <div className="header-actions">
          <button className="button-secondary" type="button" onClick={handleCopy}>
            Copy plan
          </button>
          <button className="button-secondary" type="button" onClick={onEditProfile}>
            Adjust profile
          </button>
        </div>
      </div>

      {copyMessage && <p className="copy-feedback">{copyMessage}</p>}

      <ProfileSummary profile={profile} />

      <div className="profile-detail-bar">
        <span><strong>Goals:</strong> {profile.careerGoals || 'Not specified'}</span>
        {profile.targetCompanies && (
          <span><strong>Target:</strong> {profile.targetCompanies}</span>
        )}
      </div>

      <DisclaimerBanner />

      <div className="results-overview">
        {tabConfig.map(tab => {
          const section = results[tab.key];
          return (
            <button
              key={tab.id}
              type="button"
              className={`overview-card${activeTab === tab.id ? ' overview-card-active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <span className="overview-icon">{tab.icon}</span>
              <span className="overview-label">{tab.label}</span>
              <span className="overview-count">{section.recommendations.length} items</span>
              <span className="small-copy overview-title">{section.title}</span>
            </button>
          );
        })}
      </div>

      <div className="results-tabs" role="tablist" aria-label="Recommendation sections">
        {tabConfig.map(tab => (
          <button
            key={tab.id}
            type="button"
            role="tab"
            aria-selected={activeTab === tab.id}
            className={`tab-button${activeTab === tab.id ? ' tab-button-active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span className="tab-icon" aria-hidden="true">{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </div>

      <article className="card result-card result-primary tab-panel" role="tabpanel">
        <h3>{activeResult.title}</h3>
        <p className="small-copy">{activeResult.summary}</p>
        <p className="section-description">{sectionDescriptions[activeTab]}</p>

        <div className="result-section">
          <h4>{activeTab === 'courses' ? 'Recommended courses' : 'Main suggestions'}</h4>
          {renderResultBody(activeTab, activeResult)}
        </div>

        {activeResult.evidence.length > 0 && (
          <div className="result-section evidence-box">
            <h4>Why these suggestions</h4>
            <ul className="result-list muted-list">
              {activeResult.evidence.map((item, index) => (
                <li key={`evidence-${index}`}>{item}</li>
              ))}
            </ul>
          </div>
        )}

        {activeTab !== 'courses' && activeResult.cautions.length > 0 && (
          <div className="result-section caution-box">
            <h4>Keep in mind</h4>
            <ul className="result-list">
              {activeResult.cautions.map((item, index) => (
                <li key={`caution-${index}`}>{item}</li>
              ))}
            </ul>
          </div>
        )}
      </article>
    </section>
  );
};

export default Recommendations;
