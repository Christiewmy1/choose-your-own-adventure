interface LandingPageProps {
  onStart: () => void;
}

const LandingPage = ({ onStart }: LandingPageProps) => (
  <section className="section-hero">
    <div className="container-inner">
      <div className="section-row hero-grid">
        <div>
          <span className="eyebrow">UW Bothell • Husky advising</span>
          <h1>Choose the right classes, build the right connections, and move toward your career.</h1>
          <p>
            HuskyAdvisor is a UWB student-facing planning tool that turns your major, completed coursework,
            and career goals into recommended classes and company alignment insights.
          </p>
          <div className="hero-actions">
            <button className="button-primary" onClick={onStart} type="button">
              Start your plan
            </button>
          </div>
        </div>

        <div className="hero-panel card">
          <h2>What you get</h2>
          <ul>
            <li>Personalized course recommendations for your UWB major.</li>
            <li>Career goal alignment with real company paths.</li>
            <li>Clear next steps for spring and summer planning.</li>
          </ul>
        </div>
      </div>

      <div className="section-row feature-section">
        <div className="feature-card card">
          <h3>UWB-first advice</h3>
          <p>Recommendations are shaped around the Husky experience, Bothell curriculum, and regional career options.</p>
        </div>
        <div className="feature-card card">
          <h3>Career alignment</h3>
          <p>See how recommended classes support career goals like software, data, design, and consulting.</p>
        </div>
        <div className="feature-card card">
          <h3>Fast and clear</h3>
          <p>Enter your major and courses once, then get a results dashboard that helps you plan next steps.</p>
        </div>
      </div>
    </div>
  </section>
);

export default LandingPage;
