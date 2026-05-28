import type { AdvisingResult, DashboardResults, StudentProfile } from './types';

const DEFAULT_LOCAL_API = 'http://127.0.0.1:8010';
const DEFAULT_PUBLIC_API = 'https://choose-your-own-adventure-bay.vercel.app';
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  (typeof window !== 'undefined' &&
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? DEFAULT_LOCAL_API
    : DEFAULT_PUBLIC_API);
const COURSE_CODE_PATTERN = /\b([A-Z]{2,6}|[A-Z]\s+[A-Z]{2,6})\s*-?\s*(\d{3})\b/g;

interface ProfilePayload {
  major: string;
  class_standing: StudentProfile['standing'];
  completed_courses: string[];
  career_goals: string[];
  target_companies: string[];
}

const normalizeList = (value: string) =>
  value
    .split(/[\n,;]+/)
    .map(item => item.trim())
    .filter(Boolean);

const extractCourseCodes = (value: string) => {
  const normalizedValue = value.toUpperCase();
  const matches = Array.from(normalizedValue.matchAll(COURSE_CODE_PATTERN));
  if (matches.length > 0) {
    return matches.map(([, dept, number]) => `${dept.toUpperCase().replace(/\s+/g, ' ').trim()} ${number}`);
  }

  return normalizeList(value);
};

const toPayload = (profile: StudentProfile): ProfilePayload => ({
  major: profile.major.trim(),
  class_standing: profile.standing,
  completed_courses: extractCourseCodes(profile.completedCourses),
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
