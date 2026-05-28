export const majorOptions = [
  'CSSE',
  'Applied Computing',
  'Electrical Engineering',
  'Mechanical Engineering',
  'Business Administration',
  'Computer Engineering',
  'Data Science',
  'Information Technology',
] as const;

export const fieldHelp = {
  major: 'Choose the major you are in or the one you are considering.',
  standing: 'This helps the system keep recommendations realistic for your stage.',
  completedCourses: 'Add courses you already finished so they are not recommended again.',
  careerGoals: 'Describe the kind of role, field, or skills you want to build toward.',
  targetCompanies: 'Optional, but helpful if you want more specific guidance.',
} as const;

export const disclaimerText =
  'HuskyAdvisor provides planning support for UW Bothell students. Results are not official degree approval, live job listings, or an internship board. Confirm prerequisites and graduation requirements with official UWB resources.';

export const loadingMessages = [
  'Reviewing your completed coursework…',
  'Matching courses to your career goals…',
  'Finding regional company alignment…',
  'Building your internship prep plan…',
  'Drafting your quarter roadmap…',
] as const;

export const PROFILE_STORAGE_KEY = 'huskyadvisor-profile';
