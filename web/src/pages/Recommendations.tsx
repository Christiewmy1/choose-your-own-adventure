import type { AdvisingResult, DashboardResults, StudentProfile } from '../types';

interface RecommendationsProps {
  profile: StudentProfile;
  results: DashboardResults | null;
  error: string;
  onEditProfile: () => void;
}

const renderResultCard = (result: AdvisingResult, variantClass: string) => (
  <article className={`card result-card ${variantClass}`}>
    <h3>{result.title}</h3>
    <p className="small-copy">{result.summary}</p>

    <div className="result-section">
      <h4>Main suggestions</h4>
      <ul className="result-list">
        {result.recommendations.map((item, index) => (
          <li key={`${result.title}-rec-${index}`}>{item}</li>
        ))}
      </ul>
    </div>

    {result.evidence.length > 0 && (
      <div className="result-section">
        <h4>Why these suggestions</h4>
        <ul className="result-list muted-list">
          {result.evidence.map((item, index) => (
            <li key={`${result.title}-ev-${index}`}>{item}</li>
          ))}
        </ul>
      </div>
    )}

    {result.cautions.length > 0 && (
      <div className="result-section caution-box">
        <h4>Keep in mind</h4>
        <ul className="result-list">
          {result.cautions.map((item, index) => (
            <li key={`${result.title}-caution-${index}`}>{item}</li>
          ))}
        </ul>
      </div>
    )}
  </article>
);

const formatProfileSubtitle = (profile: StudentProfile) => {
  const goals = profile.careerGoals || 'your current goals';
  return `These UWB-focused results are based on ${profile.major || 'your program'}, your ${profile.standing.toLowerCase()} standing, and goals like ${goals}.`;
};

const Recommendations = ({ profile, results, error, onEditProfile }: RecommendationsProps) => {
  if (error) {
    return (
      <section className="section-panel card">
        <div className="recommendation-header">
          <div>
            <span className="eyebrow">Result connection issue</span>
            <h2>HuskyAdvisor could not load live recommendations.</h2>
            <p>{error}</p>
          </div>
          <button className="button-secondary" type="button" onClick={onEditProfile}>
            Adjust profile
          </button>
        </div>
      </section>
    );
  }

  if (!results) {
    return null;
  }

  return (
    <section className="section-panel card">
      <div className="recommendation-header">
        <div>
          <span className="eyebrow">Your tailored results</span>
          <h2>Course and company alignment for {profile.major || 'your path'}</h2>
          <p>{formatProfileSubtitle(profile)}</p>
        </div>
        <button className="button-secondary" type="button" onClick={onEditProfile}>
          Adjust profile
        </button>
      </div>

      <div className="results-grid">
        {renderResultCard(results.recommendations, 'result-primary')}
        {renderResultCard(results.companies, 'result-secondary')}
        {renderResultCard(results.internshipPrep, 'result-secondary')}
        {renderResultCard(results.roadmap, 'result-secondary')}
      </div>
    </section>
  );
};

export default Recommendations;
