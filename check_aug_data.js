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
  console.log("Fetching product_metrics for Aug 2026");
  const { data: augData, error: augError } = await supabase.from('product_metrics')
      .select('*')
      .eq('upload_date', '2026-08-01')
      .limit(5);
  console.log(augData, augError);

  console.log("Fetching category_material_metrics for Aug 2026");
  const { data: viewData, error: viewError } = await supabase.from('category_material_metrics')
      .select('*')
      .eq('upload_date', '2026-08-01')
      .limit(5);
  console.log(viewData, viewError);
}
check();
