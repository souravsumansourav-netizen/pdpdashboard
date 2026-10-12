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
  const { data, error } = await supabase.rpc('refresh_material_metrics');
  console.log("RPC result:", error || "Success");

  const { data: viewData, error: viewError } = await supabase.from('category_material_metrics').select('*').limit(5);
  console.log("View data (first 5):", viewData?.length, viewError);
  
  const { data: dates, error: dateError } = await supabase.from('category_material_metrics').select('upload_date');
  if (dates) {
     const uniqueDates = [...new Set(dates.map(d => d.upload_date))];
     console.log("Unique dates in view:", uniqueDates);
  }
}
check();
