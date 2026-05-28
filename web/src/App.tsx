import { useEffect, useState } from 'react';
import { fetchDashboardResults } from './api';
import LandingPage from './pages/LandingPage';
import ProfileForm from './pages/ProfileForm';
import Recommendations from './pages/Recommendations';
import TopNav from './components/TopNav';
import LoadingSpinner from './components/LoadingSpinner';
import ProgressStepper from './components/ProgressStepper';
import DisclaimerBanner from './components/DisclaimerBanner';
import { loadingMessages, PROFILE_STORAGE_KEY } from './constants';
import type { DashboardResults, StudentProfile } from './types';
import { hashToPage, pageToHash, type AppPage } from './utils/routing';
import { buildFallbackDashboardResults } from './utils/fallbackResults';

const defaultProfile: StudentProfile = {
  major: '',
  standing: 'Freshman',
  completedCourses: '',
  careerGoals: '',
  targetCompanies: '',
};

const loadStoredProfile = (): StudentProfile => {
  try {
    const raw = localStorage.getItem(PROFILE_STORAGE_KEY);
    if (!raw) {
      return defaultProfile;
    }
    return { ...defaultProfile, ...JSON.parse(raw) } as StudentProfile;
  } catch {
    return defaultProfile;
  }
};

const LOCAL_API_HINT =
  ' Start the API locally with: PYTHONPATH=src uvicorn api.main:app --host 127.0.0.1 --port 8010';

function App() {
  const [page, setPage] = useState<AppPage>(() => hashToPage(window.location.hash));
  const [profile, setProfile] = useState<StudentProfile>(loadStoredProfile);
  const [results, setResults] = useState<DashboardResults | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMessageIndex, setLoadingMessageIndex] = useState(0);
  const [error, setError] = useState('');
  const [fieldErrors, setFieldErrors] = useState<Partial<Record<keyof StudentProfile, string>>>({});
  const [resultError, setResultError] = useState('');
  const [resultNotice, setResultNotice] = useState('');

  useEffect(() => {
    const onHashChange = () => setPage(hashToPage(window.location.hash));
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  useEffect(() => {
    const nextHash = pageToHash(page);
    if (window.location.hash !== nextHash) {
      window.location.hash = nextHash;
    }
  }, [page]);

  useEffect(() => {
    if (!isLoading) {
      return;
    }

    const interval = window.setInterval(() => {
      setLoadingMessageIndex(prev => (prev + 1) % loadingMessages.length);
    }, 1800);

    return () => window.clearInterval(interval);
  }, [isLoading]);

  const goToLanding = () => {
    setPage('landing');
    setError('');
    setFieldErrors({});
    setResultError('');
  };

  const goToProfile = () => {
    setPage('profile');
    setError('');
    setFieldErrors({});
    setResultError('');
  };

  const fetchResults = async (nextProfile: StudentProfile) => {
    setIsLoading(true);
    setResults(null);
    setResultError('');
    setResultNotice('');
    setLoadingMessageIndex(0);

    try {
      const nextResults = await fetchDashboardResults(nextProfile);
      setResults(nextResults);
    } catch (err) {
      const rawMessage = err instanceof Error ? err.message : 'Could not load HuskyAdvisor results.';
      const message =
        rawMessage === 'Failed to fetch'
          ? 'The live API request did not complete.'
          : rawMessage;
      setResults(buildFallbackDashboardResults(nextProfile));
      setResultNotice(
        `${message} Showing a clearly labeled demo-safe fallback so the presentation can continue. Retry will attempt the live API again.${LOCAL_API_HINT}`
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleProfileSubmit = async (nextProfile: StudentProfile) => {
    const nextFieldErrors: Partial<Record<keyof StudentProfile, string>> = {};
    if (!nextProfile.major.trim()) {
      nextFieldErrors.major = 'Select your major to continue.';
    }
    if (!nextProfile.careerGoals.trim()) {
      nextFieldErrors.careerGoals = 'Add at least one career goal.';
    }

    if (Object.keys(nextFieldErrors).length > 0) {
      setFieldErrors(nextFieldErrors);
      setError('Please complete the required fields below.');
      return;
    }

    setProfile(nextProfile);
    localStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(nextProfile));
    setError('');
    setFieldErrors({});
    setPage('results');
    await fetchResults(nextProfile);
  };

  const handleTryExample = async (exampleProfile: StudentProfile) => {
    setProfile(exampleProfile);
    localStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(exampleProfile));
    setError('');
    setFieldErrors({});
    setPage('results');
    await fetchResults(exampleProfile);
  };

  const handleRetry = async () => {
    await fetchResults(profile);
  };

  const handleEditProfile = () => {
    setPage('profile');
    setError('');
    setFieldErrors({});
  };

  const handleStepChange = (step: AppPage) => {
    if (step === 'results' && !results && !isLoading) {
      return;
    }
    setPage(step);
  };

  return (
    <div className="app-shell">
      <TopNav currentPage={page} onHome={goToLanding} onStart={goToProfile} />

      <div className="page-content">
        <ProgressStepper currentStep={page} onStepChange={handleStepChange} canOpenResults={Boolean(results)} />

        {page === 'landing' && (
          <LandingPage onStart={goToProfile} onTryExample={handleTryExample} />
        )}

        {page === 'profile' && (
          <ProfileForm
            profile={profile}
            error={error}
            fieldErrors={fieldErrors}
            onSubmit={handleProfileSubmit}
            onBack={goToLanding}
          />
        )}

        {page === 'results' && (
          <div className="results-shell">
            {isLoading ? (
              <div className="status-panel">
                <LoadingSpinner />
                <p>{loadingMessages[loadingMessageIndex]}</p>
                <p className="small-copy">Building your dashboard from the local HuskyAdvisor API…</p>
              </div>
            ) : (
              <Recommendations
                profile={profile}
                results={results}
                error={resultError}
                notice={resultNotice}
                onEditProfile={handleEditProfile}
                onRetry={handleRetry}
              />
            )}
          </div>
        )}
      </div>

      <footer className="site-footer">
        <DisclaimerBanner variant="footer" />
      </footer>
    </div>
  );
}

export default App;
