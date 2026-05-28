import type { StudentProfile } from '../types';
import { exampleProfiles } from '../utils/routing';

interface LandingPageProps {
  onStart: () => void;
  onTryExample: (profile: StudentProfile) => void;
}

const howItWorks = [
  {
    title: 'Student Profile Input',
    description: 'Enter major interest, completed courses, goals, and target companies.',
  },
  {
    title: 'FastAPI + HuskyAdvisorEngine',
    description: 'The backend scores courses, companies, internship prep, and roadmap tracks.',
  },
  {
    title: 'Ranked Results + AI Summary',
    description: 'Students see explainable recommendations, AI trace evidence, and next steps.',
  },
];

const whoThisHelps = [
  'A sophomore unsure between CSSE and Applied Computing',
  'A junior preparing for a Microsoft or JPMorgan Chase Technology internship',
  'A transfer student trying to avoid repeating completed courses',
  'A student comparing cloud, embedded, analytics, healthcare, or business-tech paths',
];

const userGuideSteps = [
  'Enter your major interest and completed courses.',
  'Browse ranked course and company recommendations.',
  'Read your personalized AI-generated roadmap summary and AI trace.',
];

const techStack = ['React', 'Vite', 'FastAPI', 'Python', 'Groq/Llama 3.3', 'Crawl4AI', 'GitHub Pages', 'Vercel'];

/**
 * Rubric-facing landing page.
 * It explains the UWB problem, scope, user guide, architecture, and tech stack
 * before a grader has to inspect the repository.
 */
const LandingPage = ({ onStart, onTryExample }: LandingPageProps) => (
  <section className="section-hero">
    <div className="container-inner">
      <div className="section-row hero-grid">
        <div>
          <span className="eyebrow">Built exclusively for UW Bothell</span>
          <h1>HuskyAdvisor helps UW Bothell students find the right major, courses, and internship path — all in one place.</h1>
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
          <div className="scope-stat-grid">
            <strong>6</strong><span>major pathways</span>
            <strong>122</strong><span>courses</span>
            <strong>140</strong><span>regional employers</span>
          </div>
        </div>
      </div>

      <div className="section-row grader-grid">
        <article className="card info-card">
          <span className="eyebrow">The problem</span>
          <h2>Advising information is scattered.</h2>
          <p>
            UWB students often piece together planning advice from catalog pages, degree sheets,
            schedule pages, career fair notes, and informal recommendations. HuskyAdvisor puts
            those signals into one explainable planning flow.
          </p>
        </article>
        <article className="card info-card">
          <span className="eyebrow">Who this helps</span>
          <h2>Real UWB student scenarios</h2>
          <ul className="clean-list">
            {whoThisHelps.map(item => <li key={item}>{item}</li>)}
          </ul>
        </article>
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
        <div className="architecture-flow full-width" aria-label="Architecture flow">
          <span>Student Profile Input</span>
          <span>FastAPI</span>
          <span>HuskyAdvisorEngine</span>
          <span>JSON Datasets</span>
          <span>Ranked Results + AI Summary</span>
        </div>
        {howItWorks.map((step, index) => (
          <div key={step.title} className="feature-card card">
            <span className="step-number">{index + 1}</span>
            <h3>{step.title}</h3>
            <p>{step.description}</p>
          </div>
        ))}
      </div>

      <div className="section-row grader-grid">
        <article className="card info-card">
          <span className="eyebrow">User guide</span>
          <h2>Three steps to use it</h2>
          <ol className="clean-list numbered-list">
            {userGuideSteps.map(item => <li key={item}>{item}</li>)}
          </ol>
        </article>
        <article className="card info-card">
          <span className="eyebrow">Tech stack</span>
          <h2>Built with modern web + AI tooling</h2>
          <div className="tech-stack-list">
            {techStack.map(item => <span key={item}>{item}</span>)}
          </div>
        </article>
      </div>
    </div>
  </section>
);

export default LandingPage;
