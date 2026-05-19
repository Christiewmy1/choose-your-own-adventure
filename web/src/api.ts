import type { AdvisingResult, DashboardResults, StudentProfile } from './types';

const API_BASE_URL = 'http://127.0.0.1:8010';

interface ProfilePayload {
  major: string;
  class_standing: StudentProfile['standing'];
  completed_courses: string[];
  career_goals: string[];
  target_companies: string[];
}

const normalizeList = (value: string) =>
  value
    .split(',')
    .map(item => item.trim())
    .filter(Boolean);

const toPayload = (profile: StudentProfile): ProfilePayload => ({
  major: profile.major.trim(),
  class_standing: profile.standing,
  completed_courses: normalizeList(profile.completedCourses),
  career_goals: normalizeList(profile.careerGoals),
  target_companies: normalizeList(profile.targetCompanies),
});

async function postResult(path: string, profile: StudentProfile): Promise<AdvisingResult> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(toPayload(profile)),
  });

  if (!response.ok) {
    throw new Error(`API request failed for ${path} (${response.status}).`);
  }

  return response.json();
}

export async function fetchDashboardResults(profile: StudentProfile): Promise<DashboardResults> {
  const [recommendations, companies, internshipPrep, roadmap] = await Promise.all([
    postResult('/api/profile/recommendations', profile),
    postResult('/api/profile/companies', profile),
    postResult('/api/profile/internship-prep', profile),
    postResult('/api/profile/roadmap', profile),
  ]);

  return {
    recommendations,
    companies,
    internshipPrep,
    roadmap,
  };
}
