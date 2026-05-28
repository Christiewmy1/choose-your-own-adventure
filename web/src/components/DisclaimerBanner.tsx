import { disclaimerText } from '../constants';

interface DisclaimerBannerProps {
  variant?: 'inline' | 'footer';
}

const DisclaimerBanner = ({ variant = 'inline' }: DisclaimerBannerProps) => (
  <aside className={`disclaimer-banner disclaimer-${variant}`} role="note">
    <strong>Planning support only.</strong> {disclaimerText}
  </aside>
);

export default DisclaimerBanner;
