import { useEffect, useState } from 'react';
import LandingPage from './pages/LandingPage';
import ProfileForm from './pages/ProfileForm';
import Recommendations from './pages/Recommendations';
import TopNav from './components/TopNav';
import LoadingSpinner from './components/LoadingSpinner';
import type { StudentProfile } from './types';

const defaultProfile: StudentProfile = {
  major: '',
  standing: 'Freshman',
  completedCourses: '',
  careerGoals: '',
};

function App() {
  const [page, setPage] = useState<'landing' | 'profile' | 'results'>('landing');
  const [profile, setProfile] = useState<StudentProfile>(defaultProfile);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (page === 'results' && isLoading) {
      const timer = window.setTimeout(() => setIsLoading(false), 900);
      return () => window.clearTimeout(timer);
    }
  }, [page, isLoading]);

  const goToLanding = () => {
    setPage('landing');
    setError('');
  };

  const goToProfile = () => {
    setPage('profile');
    setError('');
  };

  const handleProfileSubmit = (nextProfile: StudentProfile) => {
    if (!nextProfile.major.trim() || !nextProfile.careerGoals.trim()) {
      setError('Please share your major and your main career goal.');
      return;
    }

    setProfile(nextProfile);
    setError('');
    setPage('results');
    setIsLoading(true);
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
              <Recommendations profile={profile} onEditProfile={handleEditProfile} />
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
