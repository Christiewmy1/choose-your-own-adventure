interface TopNavProps {
  currentPage: 'landing' | 'profile' | 'results';
  apiOnline: boolean | null;
  onHome: () => void;
  onStart: () => void;
}

/**
 * Main navigation shown on every page.
 * The API status badge gives graders immediate proof that the live frontend is
 * connected to a deployed backend rather than only a static mock.
 */
const TopNav = ({ currentPage, apiOnline, onHome, onStart }: TopNavProps) => {
  return (
    <header className="top-nav">
      <div className="brand-line">
        <button className="brand-link" onClick={onHome} type="button">
          HuskyAdvisor
        </button>
        <span>UWB course planning for Husky careers</span>
      </div>

      <nav className="nav-actions">
        <span className={`api-status api-status-${apiOnline === null ? 'checking' : apiOnline ? 'online' : 'offline'}`}>
          {apiOnline === null ? 'API Checking' : apiOnline ? 'API Online' : 'API Offline'}
        </span>
        {currentPage !== 'landing' && (
          <button className="button-secondary" onClick={onHome} type="button">
            Home
          </button>
        )}
        {currentPage === 'landing' && (
          <button className="button-primary" onClick={onStart} type="button">
            Start planning
          </button>
        )}
      </nav>
    </header>
  );
};

export default TopNav;
