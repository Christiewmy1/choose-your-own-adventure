import type { StudentProfile } from '../types';
import { exampleProfiles } from '../utils/routing';

interface LandingPageProps {
  onStart: () => void;
  onTryExample: (profile: StudentProfile) => void;
}

const howItWorks = [
  {
    title: 'Share your profile',
    description: 'Add your major, completed courses, and career goals.',
  },
  {
    title: 'Get tailored guidance',
    description: 'See courses, company alignment, internship prep, and a roadmap.',
  },
  {
    title: 'Plan next steps',
    description: 'Use explainable recommendations to shape your UWB path.',
  },
];

const LandingPage = ({ onStart, onTryExample }: LandingPageProps) => (
  <section className="section-hero">
    <div className="container-inner">
      <div className="section-row hero-grid">
        <div>
          <span className="eyebrow">UW Bothell • Husky advising</span>
          <h1>Choose the right classes, build the right connections, and move toward your career.</h1>
          <p>
            HuskyAdvisor turns your major, completed coursework, and career goals into recommended classes,
            company alignment insights, and a quarter-by-quarter plan.
          </p>
          <div className="hero-actions">
            <button className="button-primary" onClick={onStart} type="button">
              Start planning
            </button>
            <button
              className="button-secondary"
              type="button"
              onClick={() => onTryExample(exampleProfiles[0].profile)}
            >
              Try Avery&apos;s demo
            </button>
          </div>
        </div>

        <div className="hero-panel card">
          <h2>What you get</h2>
          <ul>
            <li>Personalized course recommendations for your UWB major.</li>
            <li>Career goal alignment with regional company paths.</li>
            <li>Internship prep and quarter roadmap in one dashboard.</li>
          </ul>
        </div>
      </div>

      <div className="section-row example-section">
        <div className="card example-panel">
          <h2>Try an example question</h2>
          <p className="small-copy">Click to load a ready-made profile and jump straight into results.</p>
          <div className="example-button-grid">
            {exampleProfiles.map(example => (
              <button
                key={example.label}
                type="button"
                className="example-question-button"
                onClick={() => onTryExample(example.profile)}
              >
                {example.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="section-row how-it-works">
        <h2 className="section-title">How it works</h2>
        {howItWorks.map((step, index) => (
          <div key={step.title} className="feature-card card">
            <span className="step-number">{index + 1}</span>
            <h3>{step.title}</h3>
            <p>{step.description}</p>
          </div>
        ))}
      </div>
    </div>
  </section>
);

export default LandingPage;
