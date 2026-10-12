CREATE TABLE IF NOT EXISTS weekly_performance_metrics (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  upload_date date NOT NULL, -- The start date of the week (e.g. 2024-07-01)
  week_label text NOT NULL, -- E.g. "1-7th July"
  platform text,
  category text,
  material_type text,
  views bigint DEFAULT 0,
  cart_adds bigint DEFAULT 0,
  purchases bigint DEFAULT 0,
  fis_users bigint DEFAULT 0,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now())
);
