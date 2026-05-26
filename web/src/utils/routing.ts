import type { StudentProfile } from '../types';

export type AppPage = 'landing' | 'profile' | 'results';

export const pageToHash = (page: AppPage) => {
  if (page === 'landing') {
    return '#/';
  }
  return `#/${page}`;
};

export const hashToPage = (hash: string): AppPage => {
  if (hash.startsWith('#/profile')) {
    return 'profile';
  }
  if (hash.startsWith('#/results')) {
    return 'results';
  }
  return 'landing';
};

export const exampleProfiles: { label: string; profile: StudentProfile }[] = [
  {
    label: 'Junior CSSE → Boeing',
    profile: {
      major: 'CSSE',
      standing: 'Junior',
      completedCourses: 'CSS 142, CSS 143, CSS 301, CSS 342, CSS 360',
      careerGoals: 'embedded systems, software engineering, aerospace',
      targetCompanies: 'Boeing',
    },
  },
  {
    label: 'Undecided → embedded systems',
    profile: {
      major: 'Computer Engineering',
      standing: 'Sophomore',
      completedCourses: 'CSS 132, CSS 133, EE 215',
      careerGoals: 'embedded systems, firmware, robotics',
      targetCompanies: 'SpaceX Starlink',
    },
  },
  {
    label: 'Internship-ready planning',
    profile: {
      major: 'Applied Computing',
      standing: 'Junior',
      completedCourses: 'CSS 142, CSS 143, CSS 360, CSS 370',
      careerGoals: 'cloud computing, web development, backend',
      targetCompanies: 'Microsoft Redmond',
    },
  },
];
