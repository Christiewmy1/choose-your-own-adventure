export const companyOptions = [
  "Boeing",
  "Google Kirkland",
  "Amazon Bellevue",
  "T-Mobile",
  "Microsoft Redmond",
  "AT&T Bothell",
  "Nintendo of America",
  "SpaceX Starlink",
  "UW Medicine",
  "Providence",
  "Fred Hutch",
] as const;

export type CompanyOption = (typeof companyOptions)[number];
