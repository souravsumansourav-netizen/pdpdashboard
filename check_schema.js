import fs from 'fs';
import { createClient } from '@supabase/supabase-js';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, ...v] = line.split('=');
  if (k) env[k.trim()] = v.join('=').trim().replace(/["']/g, '');
});

const supabase = createClient(env.VITE_SUPABASE_URL, env.VITE_SUPABASE_ANON_KEY);

async function check() {
  const { data, error } = await supabase.rpc('exec_sql', { query: "SELECT matviewname, definition FROM pg_matviews WHERE matviewname = 'category_material_metrics'" });
  console.log("pg_matviews:", data, error);
  
  const { data: vData, error: vError } = await supabase.rpc('exec_sql', { query: "SELECT viewname, definition FROM pg_views WHERE viewname = 'category_material_metrics'" });
  console.log("pg_views:", vData, vError);
}
check();
