export const PARISHES = [
  { id: '1', name: 'St. John Anglican Church', slug: 'st-john' },
  { id: '2', name: 'St. Mary Anglican Church', slug: 'st-mary' },
  { id: '3', name: 'Trinity Anglican Church', slug: 'trinity' },
  { id: '4', name: 'Christ Anglican Church', slug: 'christ' },
  { id: '5', name: 'St. Paul Anglican Church', slug: 'st-paul' },
  { id: '6', name: 'St. Peter Anglican Church', slug: 'st-peter' },
  { id: '7', name: 'All Saints Anglican Church', slug: 'all-saints' },
  { id: '8', name: 'St. James Anglican Church', slug: 'st-james' },
  { id: '9', name: 'St. Michael Anglican Church', slug: 'st-michael' },
  { id: '10', name: 'Holy Trinity Anglican Church', slug: 'holy-trinity' },
];

export const ROLES = {
  ADMIN: 'admin',
  GEN_PRESIDENT: 'gen_president',
  GEN_SEC: 'gen_sec',
  PARISH_PRESIDENT: 'parish_president',
  PARISH_SEC: 'parish_sec',
  PROVOST: 'provost',
  PRO: 'pro',
  VICE_PRESIDENT: 'vice_president',
  MEMBER: 'member',
};

export const EVENT_LEVELS = {
  ARCHDEACONRY: 'archdeaconry',
  DIOCESE: 'diocese',
  PARISH: 'parish',
};

export const POST_TYPES = {
  ANNOUNCEMENT: 'announcement',
  EVENT: 'event',
  NOTICE: 'notice',
  TESTIMONY: 'testimony',
};

export const CHAT_GROUPS = {
  GENERAL: 'general',
  PARISH: 'parish',
  PRESIDENTS: 'presidents',
};

export const QUARTERS = [
  { value: 1, label: 'Q1 (Jan - Mar)' },
  { value: 2, label: 'Q2 (Apr - Jun)' },
  { value: 3, label: 'Q3 (Jul - Sep)' },
  { value: 4, label: 'Q4 (Oct - Dec)' },
];

export const RECURRENCE_PATTERNS = [
  { value: 'weekly', label: 'Weekly' },
  { value: 'monthly', label: 'Monthly' },
  { value: 'yearly', label: 'Yearly' },
];
