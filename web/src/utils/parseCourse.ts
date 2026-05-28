const courseCodePattern = /^([A-Z]{2,4}\s?\d{3}[A-Z]?)\s+(.+)$/;

export interface ParsedCourseRecommendation {
  code: string | null;
  title: string;
  description: string;
  raw: string;
}

export const extractCourseCode = (text: string): string | null => {
  const match = text.match(/\b([A-Z]{2,4}\s?\d{3}[A-Z]?)\b/);
  return match ? match[1].replace(/\s+/g, ' ') : null;
};

export const parseCourseRecommendation = (item: string): ParsedCourseRecommendation => {
  const code = extractCourseCode(item);
  if (!code) {
    return { code: null, title: item, description: '', raw: item };
  }

  const afterCode = item.slice(item.indexOf(code) + code.length).trim();
  const colonIndex = afterCode.indexOf(':');
  if (colonIndex >= 0) {
    return {
      code,
      title: afterCode.slice(0, colonIndex).trim(),
      description: afterCode.slice(colonIndex + 1).trim(),
      raw: item,
    };
  }

  const titleMatch = afterCode.match(courseCodePattern);
  if (titleMatch) {
    return {
      code: titleMatch[1].replace(/\s+/g, ' '),
      title: titleMatch[2].trim(),
      description: '',
      raw: item,
    };
  }

  return {
    code,
    title: afterCode,
    description: '',
    raw: item,
  };
};

export const findCautionForCourse = (code: string | null, cautions: string[]): string | undefined => {
  if (!code) {
    return undefined;
  }
  return cautions.find(caution => caution.includes(code));
};
