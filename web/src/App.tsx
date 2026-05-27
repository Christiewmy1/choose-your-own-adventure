import { useState } from 'react';
import { fetchDashboardResults } from './api';
import LandingPage from './pages/LandingPage';
import ProfileForm from './pages/ProfileForm';
import Recommendations from './pages/Recommendations';
import TopNav from './components/TopNav';
import LoadingSpinner from './components/LoadingSpinner';
import type { DashboardResults, StudentProfile } from './types';

const defaultProfile: StudentProfile = {
  major: '',
  standing: 'Freshman',
  completedCourses: '',
  careerGoals: '',
  targetCompanies: '',
};

function App() {
  const [page, setPage] = useState<'landing' | 'profile' | 'results'>('landing');
  const [profile, setProfile] = useState<StudentProfile>(defaultProfile);
  const [results, setResults] = useState<DashboardResults | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [resultError, setResultError] = useState('');

  const goToLanding = () => {
    setPage('landing');
    setError('');
    setResultError('');
  };

  const goToProfile = () => {
    setPage('profile');
    setError('');
    setResultError('');
  };

  const handleProfileSubmit = async (nextProfile: StudentProfile) => {
    if (!nextProfile.major.trim() || !nextProfile.careerGoals.trim()) {
      setError('Please share your major and your main career goal.');
      return;
    }

    setProfile(nextProfile);
    setError('');
    setResultError('');
    setPage('results');
    setIsLoading(true);
    setResults(null);

    try {
      const nextResults = await fetchDashboardResults(nextProfile);
      setResults(nextResults);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Could not load HuskyAdvisor results.';
      setResultError(
        `${message} If you are testing locally, make sure the HuskyAdvisor API is running on port 8010. If you are using the public site, the deployed backend may be unavailable.`
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleEditProfile = () => {
    setPage('profile');
    setError('');
  };

  return (
    <div className="app-shell">
      <TopNav
        currentPage={page}
        onHome={goToLanding}
        onStart={goToProfile}
      />

      <main className="page-content">
        {page === 'landing' && <LandingPage onStart={goToProfile} />}

        {page === 'profile' && (
          <ProfileForm
            profile={profile}
            error={error}
            onSubmit={handleProfileSubmit}
            onBack={goToLanding}
          />
        )}

        {page === 'results' && (
          <section className="results-shell">
            {isLoading ? (
              <div className="status-panel">
                <LoadingSpinner />
                <p>Crunching your plan with UWB-focused recommendations...</p>
              </div>
            ) : (
              <Recommendations
                profile={profile}
                results={results}
                error={resultError}
                onEditProfile={handleEditProfile}
              />
            )}
          </section>
        )}
      </main>

      <footer className="site-footer">
        <p>HuskyAdvisor is built for UWB students looking to align academics with career momentum.</p>
      </footer>
    </div>
  );
}

export default App;
