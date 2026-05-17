import type { StudentProfile, Recommendation } from '../types';

interface RecommendationsProps {
  profile: StudentProfile;
  onEditProfile: () => void;
}

const buildCourses = (profile: StudentProfile): Recommendation[] => {
  const normalizedMajor = profile.major.toLowerCase();
  const isTech = /informat|computer|data|software/.test(normalizedMajor);
  const isBusiness = /business|marketing|finance|management/.test(normalizedMajor);
  const isDesign = /design|ux|ui|media/.test(normalizedMajor);

  if (isTech) {
    return [
      {
        title: 'INFO 340 – Human-Computer Interaction',
        description: 'Strengthen user-centered design and interaction skills for software product teams.',
        reason: 'Husky technical roles often combine data, product, and UX thinking.',
      },
      {
        title: 'INFO 335 – Data Visualization',
        description: 'Learn to interpret and present data clearly with visual tools and storytelling.',
        reason: 'Skills here closely match analytics and product role expectations.',
      },
      {
        title: 'INFO 360 – Software Development',
        description: 'Advance your software project experience with team-based development practices.',
        reason: 'Practical programming experience is a strong indicator for internships.',
      },
    ];
  }

  if (isBusiness) {
    return [
      {
        title: 'BUS 360 – Entrepreneurship',
        description: 'Explore business models, pitch development, and innovation frameworks.',
        reason: 'Great for students pursuing startup or consulting pathways.',
      },
      {
        title: 'MKTG 326 – Digital Strategy',
        description: 'Build marketing plans for digital products and brand storytelling.',
        reason: 'Supports career goals in marketing, product, and communications.',
      },
      {
        title: 'ADMS 311 – Strategic Management',
        description: 'Practice strategic decision-making in team-based business scenarios.',
        reason: 'Strong preparation for leadership roles in corporate settings.',
      },
    ];
  }

  if (isDesign) {
    return [
      {
        title: 'INFO 340 – Human-Computer Interaction',
        description: 'Build hands-on design and prototyping skills for digital experiences.',
        reason: 'Bridges product design work with technical team expectations.',
      },
      {
        title: 'INFO 437 – Visual Communication',
        description: 'Learn the principles of visual storytelling and digital media design.',
        reason: 'A strong fit for creative and UX-focused career goals.',
      },
      {
        title: 'INFO 445 – Social Media Design',
        description: 'Discover how design supports brand engagement and user interaction online.',
        reason: 'Useful for roles that blend design, content, and brand strategy.',
      },
    ];
  }

  return [
    {
      title: 'INFO 200 – Intranet Systems and Services',
      description: 'Get grounded in information systems and collaborative workflows.',
      reason: 'A solid foundation for many UWB majors and career pathways.',
    },
    {
      title: 'INFO 220 – Computing in the Community',
      description: 'Study computing projects that address real-world community challenges.',
      reason: 'Demonstrates applied learning and social impact experience.',
    },
    {
      title: 'INFO 330 – Information Experience Design',
      description: 'Explore how people interact with information and digital interfaces.',
      reason: 'Great preparation for roles that need both technical and communication skills.',
    },
  ];
};

const buildCompanies = (profile: StudentProfile) => {
  const baseGoals = profile.careerGoals.toLowerCase();
  const suggestions = [
    {
      company: 'Amazon',
      focus: 'Technical operations, data, and software product strategy.',
      alignment: baseGoals.includes('data') || baseGoals.includes('software') ? 'Strong' : 'Moderate',
    },
    {
      company: 'Microsoft',
      focus: 'Cloud services, AI, and inclusive design across product teams.',
      alignment: baseGoals.includes('cloud') || baseGoals.includes('software') ? 'Strong' : 'Good',
    },
    {
      company: 'T-Mobile',
      focus: 'Customer experience, digital services, and technology transformation.',
      alignment: baseGoals.includes('customer') || baseGoals.includes('service') ? 'Strong' : 'Moderate',
    },
  ];

  return suggestions;
};

const Recommendations = ({ profile, onEditProfile }: RecommendationsProps) => {
  const courseList = buildCourses(profile);
  const companyList = buildCompanies(profile);

  return (
    <section className="section-panel card">
      <div className="recommendation-header">
        <div>
          <span className="eyebrow">Your tailored results</span>
          <h2>Course and company alignment for {profile.major || 'your path'}</h2>
          <p>
            These suggestions are based on your current standing and career direction. Use them to inform your next semester and career conversations.
          </p>
        </div>
        <button className="button-secondary" type="button" onClick={onEditProfile}>
          Adjust profile
        </button>
      </div>

      <div className="summary-grid">
        <article className="card recommendation-card">
          <h3>Recommended courses</h3>
          <p className="small-copy">Classes to consider for the next 1–2 semesters.</p>
          <div className="course-list">
            {courseList.map((course, index) => (
              <div className="course-item" key={`${course.title}-${index}`}>
                <h4>{course.title}</h4>
                <p>{course.description}</p>
                <div className="course-reason">{course.reason}</div>
              </div>
            ))}
          </div>
        </article>

        <article className="card alignment-card">
          <h3>Company alignment</h3>
          <p className="small-copy">Companies to explore based on your goals and UWB interests.</p>
          <div className="company-list">
            {companyList.map(({ company, focus, alignment }) => (
              <div className="company-item" key={company}>
                <div className="company-header">
                  <span className="company-name">{company}</span>
                  <span className={`alignment-badge badge-${alignment.toLowerCase()}`}>{alignment}</span>
                </div>
                <p>{focus}</p>
              </div>
            ))}
          </div>
        </article>
      </div>
    </section>
  );
};

export default Recommendations;
