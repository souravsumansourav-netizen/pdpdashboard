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
  const { data, error } = await supabase.from('category_material_metrics').insert({
      upload_date: '2020-01-01',
      category: 'Test',
      platform: 'web',
      material_type: 'Gold',
      views: 1,
      cart_adds: 0,
      purchases: 0,
      fis_users: 0
  }).select();
  console.log("Insert result:", data, error);
}
check();
