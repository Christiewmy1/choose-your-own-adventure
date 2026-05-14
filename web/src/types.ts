export interface StudentProfile {
  major: string;
  standing: 'Freshman' | 'Sophomore' | 'Junior' | 'Senior' | 'Graduate';
  completedCourses: string;
  careerGoals: string;
}

export interface Recommendation {
  title: string;
  description: string;
  reason: string;
}
