import fs from 'fs';
import { createClient } from '@supabase/supabase-js';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, v] = line.split('=');
  if (k && v) env[k.trim()] = v.trim();
});

const supabase = createClient(env['VITE_SUPABASE_URL'], env['VITE_SUPABASE_ANON_KEY']);

const sql = `
CREATE TABLE IF NOT EXISTS weekly_performance_metrics (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  week_label text NOT NULL,
  week_start_date date NOT NULL,
  category text,
  searches bigint DEFAULT 0,
  visit_percentage numeric DEFAULT 0,
  purchase_percentage numeric DEFAULT 0,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now())
);
`;

async function run() {
  const { data, error } = await supabase.rpc('exec_sql', { sql_query: sql });
  if (error) {
    console.error('Error creating table:', error);
  } else {
    console.log('Table created successfully', data);
  }
}

run();
