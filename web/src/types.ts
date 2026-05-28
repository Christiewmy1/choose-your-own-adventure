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
  ai_trace?: {
    recommendation_engine: string;
    llm_enhancement: string;
    llm_model: string | null;
    data_ingestion: string;
    retrieval_readiness: string;
    fallback_mode: boolean;
    decision_inputs: string[];
  };
}

export interface DashboardResults {
  recommendations: AdvisingResult;
  companies: AdvisingResult;
  internshipPrep: AdvisingResult;
  roadmap: AdvisingResult;
}
