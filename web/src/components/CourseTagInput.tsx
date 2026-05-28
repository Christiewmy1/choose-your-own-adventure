import TagInput from './TagInput';
import { courseCatalog } from '../data/courseCatalog';

interface CourseTagInputProps {
  id: string;
  label: string;
  help?: string;
  value: string;
  error?: string;
  onChange: (value: string) => void;
  onAddCommon?: () => void;
  commonLabel?: string;
}

const courseSuggestions = courseCatalog.map(course => course.code);

const CourseTagInput = ({
  id,
  label,
  help,
  value,
  error,
  onChange,
  onAddCommon,
  commonLabel,
}: CourseTagInputProps) => {
  const selected = new Set(
    value
      .split(',')
      .map(item => item.trim())
      .filter(Boolean)
  );

  const getTitle = (code: string) => courseCatalog.find(course => course.code === code)?.title;

  return (
    <div className="course-tag-input">
      <TagInput
        id={id}
        label={label}
        help={help}
        value={value}
        suggestions={courseSuggestions}
        placeholder="Type a course code, e.g. CSS 342"
        error={error}
        onChange={onChange}
      />
      {onAddCommon && (
        <button type="button" className="button-ghost" onClick={onAddCommon}>
          {commonLabel ?? 'Add common courses for major'}
        </button>
      )}
      <div className="selected-course-preview">
        {Array.from(selected).slice(0, 4).map(code => (
          <span key={code} className="small-copy">
            {code}{getTitle(code) ? ` — ${getTitle(code)}` : ''}
          </span>
        ))}
      </div>
    </div>
  );
};

export default CourseTagInput;
