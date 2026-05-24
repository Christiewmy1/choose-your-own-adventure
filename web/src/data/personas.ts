import type { StudentProfile } from '../types';

export interface SamplePersona {
  id: string;
  label: string;
  description: string;
  profile: StudentProfile;
}

export const samplePersonas: SamplePersona[] = [
  {
    id: 'junior_csse_boeing',
    label: 'Avery — CSSE / Boeing',
    description: 'Junior CSSE student targeting aerospace systems software.',
    profile: {
      major: 'CSSE',
      standing: 'Junior',
      completedCourses: 'CSS 142, CSS 143, CSS 301, CSS 342, CSS 360',
      careerGoals: 'embedded systems, software engineering, aerospace',
      targetCompanies: 'Boeing',
    },
  },
  {
    id: 'sophomore_app_cloud',
    label: 'Jordan — Applied Computing / Microsoft',
    description: 'Sophomore exploring cloud and web development paths.',
    profile: {
      major: 'Applied Computing',
      standing: 'Sophomore',
      completedCourses: 'BIS 200, CSS 142, CSS 143',
      careerGoals: 'cloud computing, web development, data systems',
      targetCompanies: 'Microsoft Redmond',
    },
  },
  {
    id: 'junior_ee_embedded',
    label: 'Sam — EE / T-Mobile',
    description: 'Junior EE student focused on embedded and firmware work.',
    profile: {
      major: 'Electrical Engineering',
      standing: 'Junior',
      completedCourses: 'MATH 124, MATH 125, PHYS 121, EE 271',
      careerGoals: 'embedded systems, firmware, robotics',
      targetCompanies: 'T-Mobile',
    },
  },
  {
    id: 'senior_csse_quality',
    label: 'Taylor — CSSE / Amazon',
    description: 'Senior CSSE student preparing for QA and backend roles.',
    profile: {
      major: 'CSSE',
      standing: 'Senior',
      completedCourses: 'CSS 301, CSS 342, CSS 360, CSS 430, CSS 432',
      careerGoals: 'quality assurance, backend engineering, reliable systems',
      targetCompanies: 'Amazon Bellevue',
    },
  },
  {
    id: 'junior_me_robotics',
    label: 'Riley — Mechanical Engineering / Boeing',
    description: 'Junior ME student interested in robotics and aerospace hardware.',
    profile: {
      major: 'Mechanical Engineering',
      standing: 'Junior',
      completedCourses: 'MATH 124, MATH 125, PHYS 121, ME 123, ME 230',
      careerGoals: 'robotics, mechanical design, aerospace',
      targetCompanies: 'Boeing',
    },
  },
  {
    id: 'sophomore_business_analytics',
    label: 'Casey — Business / Amazon',
    description: 'Sophomore exploring business systems and analytics paths.',
    profile: {
      major: 'Business Administration',
      standing: 'Sophomore',
      completedCourses: 'BIS 111, BIS 200, CSS 123',
      careerGoals: 'analytics, business intelligence, data systems',
      targetCompanies: 'Amazon Bellevue',
    },
  },
  {
    id: 'junior_compeng_embedded',
    label: 'Morgan — Computer Engineering / T-Mobile',
    description: 'Junior computer engineering student focused on embedded systems.',
    profile: {
      major: 'Computer Engineering',
      standing: 'Junior',
      completedCourses: 'CSS 132, CSS 133, EE 215, EE 271',
      careerGoals: 'embedded systems, firmware, hardware-software integration',
      targetCompanies: 'T-Mobile',
    },
  },
  {
    id: 'junior_data_science_research',
    label: 'Quinn — Data Science / Fred Hutch',
    description: 'Junior data science student interested in research and health data.',
    profile: {
      major: 'Data Science',
      standing: 'Junior',
      completedCourses: 'CSS 123, STMATH 124, STMATH 125, B BIO 180',
      careerGoals: 'machine learning, research computing, health data',
      targetCompanies: 'Fred Hutch',
    },
  },
  {
    id: 'sophomore_it_security',
    label: 'Jamie — Information Technology / AT&T',
    description: 'Sophomore IT student exploring infrastructure and security operations.',
    profile: {
      major: 'Information Technology',
      standing: 'Sophomore',
      completedCourses: 'BIS 111, BIS 200, BIS 221, CSS 110',
      careerGoals: 'infrastructure, security operations, networking',
      targetCompanies: 'AT&T Bothell',
    },
  },
];
