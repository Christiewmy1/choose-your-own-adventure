import type { AdvisingResult, DashboardResults, StudentProfile } from '../types';

const normalizeText = (value: string) => value.toLowerCase();

const splitList = (value: string) =>
  value
    .split(/[\n,;]+/)
    .map(item => item.trim())
    .filter(Boolean);

const hasAny = (value: string, keywords: string[]) => {
  const normalized = normalizeText(value);
  return keywords.some(keyword => normalized.includes(keyword));
};

const courseTrackFor = (profile: StudentProfile) => {
  const context = `${profile.major} ${profile.careerGoals} ${profile.targetCompanies}`;

  if (hasAny(context, ['data', 'analytics', 'visualization', 'dashboard', 'healthcare'])) {
    return {
      courses: [
        'CSS 475 Database Systems: Strengthens data modeling and query skills for analytics-heavy work.',
        'BIS 315 Understanding Statistics: Builds evidence-based reasoning for dashboards and decision support.',
        'CSS 486 Human-Computer Interaction: Helps turn data and software into usable student- or client-facing tools.',
      ],
      focus: 'data and analytics',
    };
  }

  if (hasAny(context, ['embedded', 'aerospace', 'hardware', 'firmware', 'boeing'])) {
    return {
      courses: [
        'CSS 427 Embedded Systems: Matches embedded, firmware, and aerospace software goals.',
        'CSS 430 Operating Systems: Builds systems foundations for low-level engineering roles.',
        'EE 454 Digital Signal Processing: Supports hardware/software work in engineering environments.',
      ],
      focus: 'embedded and aerospace systems',
    };
  }

  if (hasAny(context, ['security', 'cyber', 't-mobile', 'privacy'])) {
    return {
      courses: [
        'CSS 310 Information Assurance and Cybersecurity: Builds security fundamentals for infrastructure roles.',
        'CSS 430 Operating Systems: Connects systems internals to security and reliability work.',
        'CSS 436 Cloud Computing: Supports secure cloud service design and deployment.',
      ],
      focus: 'security and cloud infrastructure',
    };
  }

  return {
    courses: [
      'CSS 436 Cloud Computing: Aligns with cloud, backend, and platform engineering goals.',
      'CSS 481 Web Programming and Applications: Builds practical full-stack application experience.',
      'CSS 497 CSSE Capstone: Turns prior coursework into a substantial portfolio-ready team project.',
    ],
    focus: 'cloud and software engineering',
  };
};

const result = (
  title: string,
  summary: string,
  recommendations: string[],
  evidence: string[],
  cautions: string[],
  profile: StudentProfile,
  context: string
): AdvisingResult => ({
  title,
  summary,
  recommendations,
  evidence,
  cautions,
  ai_trace: {
    recommendation_engine: 'browser demo fallback using the same profile fields and pathway assumptions',
    llm_enhancement: 'not used in fallback mode',
    llm_model: null,
    data_ingestion: 'fallback references the same curated UWB/company data story but does not fetch live data',
    retrieval_readiness: 'fallback does not query retrieval documents',
    fallback_mode: true,
    decision_inputs: [
      `context=${context}`,
      `major=${profile.major || 'not specified'}`,
      `standing=${profile.standing}`,
      `career_goals=${profile.careerGoals || 'not specified'}`,
      `target_companies=${profile.targetCompanies || 'none'}`,
    ],
  },
});

export const buildFallbackDashboardResults = (profile: StudentProfile): DashboardResults => {
  const completed = splitList(profile.completedCourses);
  const track = courseTrackFor(profile);
  const target = splitList(profile.targetCompanies)[0] || 'regional tech employers';

  return {
    recommendations: result(
      'Demo-Safe Course Recommendations',
      `This fallback uses the same UWB-focused planning assumptions as the main app to keep the demo usable if the live API is temporarily unreachable. The strongest detected track is ${track.focus}.`,
      track.courses,
      [
        `${profile.major || 'The selected pathway'} was matched against the stated goals: ${profile.careerGoals || 'not specified'}.`,
        completed.length > 0
          ? `Completed-course input was captured (${completed.length} item${completed.length === 1 ? '' : 's'}) and should be excluded by the live engine.`
          : 'No completed courses were provided, so this fallback favors broadly useful next-step courses.',
        'Fallback output is intentionally labeled so it does not overclaim live API certainty.',
      ],
      [
        'Use the live API results for final advising-quality output when available.',
        'Confirm prerequisites and graduation requirements with official UW Bothell resources.',
      ],
      profile,
      'course fallback'
    ),
    companies: result(
      'Demo-Safe Company Alignment',
      `This fallback connects the profile to likely regional employer themes while preserving the project distinction between planning support and live job postings.`,
      [
        `${target}: compare desired roles against courses, projects, and internship timelines before applying.`,
        'Microsoft Redmond: strong fit for cloud, platform engineering, developer tools, and AI-adjacent software work.',
        'Boeing: strong fit for aerospace software, embedded systems, reliability, and large-scale engineering workflows.',
      ],
      [
        'Company recommendations are based on pathway tags, not scraped live job openings.',
        'The full backend uses the 140-company dataset for richer matching when reachable.',
      ],
      ['This is not a live internship board; students should still verify current openings.'],
      profile,
      'company fallback'
    ),
    internshipPrep: result(
      'Demo-Safe Internship Prep',
      'The fallback keeps the demo moving with practical preparation steps that map coursework to portfolio evidence.',
      [
        `Build one portfolio project connected to ${track.focus}.`,
        'Create a one-page resume section that explains course projects, tools, and measurable outcomes.',
        'Practice explaining one technical decision, one tradeoff, and one debugging story from a course or project.',
      ],
      [
        'Internship guidance is generated from the student profile rather than a generic chatbot prompt.',
        'The live backend adds company-specific playbooks and stronger roadmap matching.',
      ],
      ['Students should validate deadlines through Handshake, company sites, and UWB career resources.'],
      profile,
      'internship fallback'
    ),
    roadmap: result(
      'Demo-Safe Quarter Roadmap',
      'This fallback gives a defensible planning sequence while making clear that official advising confirmation is still required.',
      [
        `Next quarter: prioritize one course connected to ${track.focus} and confirm prerequisites.`,
        'Following quarter: add a project-heavy course or capstone-style experience to strengthen portfolio evidence.',
        'Before internship season: refresh resume, prepare project explanations, and verify target company postings.',
      ],
      [
        'Roadmap sequencing is approximate and meant for planning conversation, not official degree clearance.',
        'The live backend replaces completed template courses and uses pathway-specific roadmap templates.',
      ],
      ['Final course sequencing must be checked against official catalog, schedule, and advisor guidance.'],
      profile,
      'roadmap fallback'
    ),
  };
};
