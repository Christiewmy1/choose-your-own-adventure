import { useMemo, useState } from 'react';

interface TagInputProps {
  id: string;
  label: string;
  help?: string;
  value: string;
  suggestions: string[];
  placeholder?: string;
  required?: boolean;
  error?: string;
  onChange: (value: string) => void;
}

const splitTags = (value: string) =>
  value
    .split(',')
    .map(item => item.trim())
    .filter(Boolean);

const joinTags = (tags: string[]) => tags.join(', ');

const TagInput = ({
  id,
  label,
  help,
  value,
  suggestions,
  placeholder,
  required,
  error,
  onChange,
}: TagInputProps) => {
  const [inputValue, setInputValue] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const tags = splitTags(value);

  const filteredSuggestions = useMemo(() => {
    const query = inputValue.trim().toLowerCase();
    if (!query) {
      return suggestions.filter(item => !tags.includes(item)).slice(0, 8);
    }
    return suggestions
      .filter(item => !tags.includes(item) && item.toLowerCase().includes(query))
      .slice(0, 8);
  }, [inputValue, suggestions, tags]);

  const addTag = (tag: string) => {
    const normalized = tag.trim();
    if (!normalized || tags.includes(normalized)) {
      return;
    }
    onChange(joinTags([...tags, normalized]));
    setInputValue('');
    setShowSuggestions(false);
  };

  const removeTag = (tag: string) => {
    onChange(joinTags(tags.filter(item => item !== tag)));
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter' || event.key === ',') {
      event.preventDefault();
      if (inputValue.trim()) {
        addTag(inputValue);
      }
    }
    if (event.key === 'Backspace' && !inputValue && tags.length > 0) {
      onChange(joinTags(tags.slice(0, -1)));
    }
  };

  return (
    <div className={`input-group tag-input-group${error ? ' has-error' : ''}`}>
      <label htmlFor={id}>{label}</label>
      {help && <p className="field-help">{help}</p>}

      <div className="tag-input-shell" onClick={() => setShowSuggestions(true)}>
        {tags.map(tag => (
          <span key={tag} className="tag-chip">
            {tag}
            <button type="button" className="tag-remove" onClick={() => removeTag(tag)} aria-label={`Remove ${tag}`}>
              ×
            </button>
          </span>
        ))}
        <input
          id={id}
          className="tag-input-field"
          value={inputValue}
          placeholder={tags.length === 0 ? placeholder : 'Add another…'}
          onChange={e => {
            setInputValue(e.target.value);
            setShowSuggestions(true);
          }}
          onKeyDown={handleKeyDown}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => window.setTimeout(() => setShowSuggestions(false), 120)}
          required={required && tags.length === 0}
        />
      </div>

      {showSuggestions && filteredSuggestions.length > 0 && (
        <ul className="tag-suggestions" role="listbox">
          {filteredSuggestions.map(item => (
            <li key={item}>
              <button type="button" onMouseDown={e => e.preventDefault()} onClick={() => addTag(item)}>
                {item}
              </button>
            </li>
          ))}
        </ul>
      )}

      {error && <p className="field-error">{error}</p>}
    </div>
  );
};

export default TagInput;
