interface TopNavProps {
  currentPage: 'landing' | 'profile' | 'results';
  onHome: () => void;
  onStart: () => void;
}

const TopNav = ({ currentPage, onHome, onStart }: TopNavProps) => {
  return (
    <header className="top-nav">
      <div className="brand-line">
        <button className="brand-link" onClick={onHome} type="button">
          HuskyAdvisor
        </button>
        <span>UWB course planning for Husky careers</span>
      </div>

      <nav className="nav-actions">
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
