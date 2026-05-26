export interface StudentProfile {
  major: string;
  standing: 'Freshman' | 'Sophomore' | 'Junior' | 'Senior' | 'Graduate';
  completedCourses: string;
  careerGoals: string;
  targetCompanies: string;
}

export interface AdvisingResult {
  title: string;
  summary: string;
  recommendations: string[];
  evidence: string[];
  cautions: string[];
}

export interface DashboardResults {
  recommendations: AdvisingResult;
  companies: AdvisingResult;
  internshipPrep: AdvisingResult;
  roadmap: AdvisingResult;
}
