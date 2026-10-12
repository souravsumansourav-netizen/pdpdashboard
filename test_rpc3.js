import fs from 'fs';
import { createClient } from '@supabase/supabase-js';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, v] = line.split('=');
  if (k && v) env[k.trim()] = v.trim();
});

const supabase = createClient(env['VITE_SUPABASE_URL'], env['VITE_SUPABASE_ANON_KEY']);

async function check() {
  const { data, error } = await supabase.rpc('get_dashboard_filters');
  console.log('Error 1:', error);
  
  const { data: d2, error: e2 } = await supabase.rpc('get_attribute_breakdown', {
    p_month: 'Overall',
    p_category: 'All',
    p_platform: 'combined',
    p_attribute_key: 'METAL'
  });
  console.log('Error 2:', e2);
}
check();
