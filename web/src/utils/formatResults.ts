import type { DashboardResults } from '../types';
import type { StudentProfile } from '../types';

export const formatResultsForCopy = (profile: StudentProfile, results: DashboardResults): string => {
  const sections = [
    { title: 'Course Recommendations', data: results.recommendations },
    { title: 'Company Alignment', data: results.companies },
    { title: 'Internship Prep', data: results.internshipPrep },
    { title: 'Quarter Roadmap', data: results.roadmap },
  ];

  const lines = [
    'HuskyAdvisor Plan',
    `Major: ${profile.major}`,
    `Standing: ${profile.standing}`,
    `Goals: ${profile.careerGoals}`,
    profile.targetCompanies ? `Target: ${profile.targetCompanies}` : '',
    '',
  ].filter(Boolean);

  for (const section of sections) {
    lines.push(`## ${section.title}`);
    lines.push(section.data.summary);
    lines.push('');
    section.data.recommendations.forEach(item => lines.push(`- ${item}`));
    if (section.data.cautions.length > 0) {
      lines.push('');
      lines.push('Keep in mind:');
      section.data.cautions.forEach(item => lines.push(`- ${item}`));
    }
    lines.push('');
  }

  lines.push('Planning support only — confirm requirements with official UWB resources.');
  return lines.join('\n');
};

export const countCourses = (value: string) =>
  value
    .split(',')
    .map(item => item.trim())
    .filter(Boolean).length;
