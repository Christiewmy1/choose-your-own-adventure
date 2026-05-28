import type { AppPage } from '../utils/routing';

interface ProgressStepperProps {
  currentStep: AppPage;
  onStepChange?: (step: AppPage) => void;
  canOpenResults?: boolean;
}

const steps: { id: AppPage; label: string }[] = [
  { id: 'landing', label: 'Home' },
  { id: 'profile', label: 'Profile' },
  { id: 'results', label: 'Results' },
];

const ProgressStepper = ({ currentStep, onStepChange, canOpenResults = false }: ProgressStepperProps) => {
  const activeIndex = steps.findIndex(step => step.id === currentStep);

  return (
    <nav className="progress-stepper" aria-label="Progress">
      {steps.map((step, index) => {
        const isComplete = index < activeIndex;
        const isActive = index === activeIndex;
        const isDisabled = step.id === 'results' && !canOpenResults && !isActive;
        const className = `step-item${isActive ? ' step-active' : ''}${isComplete ? ' step-complete' : ''}${isDisabled ? ' step-disabled' : ''}`;

        return (
          <button
            key={step.id}
            type="button"
            className={className}
            disabled={isDisabled}
            onClick={() => onStepChange?.(step.id)}
          >
            <span className="step-dot" aria-hidden="true">
              {isComplete ? '✓' : index + 1}
            </span>
            <span className="step-label">{step.label}</span>
          </button>
        );
      })}
    </nav>
  );
};

export default ProgressStepper;
