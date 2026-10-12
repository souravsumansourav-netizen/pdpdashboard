import fs from 'fs';
import { createClient } from '@supabase/supabase-js';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, v] = line.split('=');
  if (k && v) env[k.trim()] = v.trim();
});

const supabase = createClient(env['VITE_SUPABASE_URL'], env['VITE_SUPABASE_ANON_KEY']);

async function run() {
  const { data, error } = await supabase.rpc('get_category_drilldown', {
    p_category: 'Earrings',
    p_platform: 'combined',
    p_start_date: '2025-01-01',
    p_end_date: '2025-12-31'
  });
  console.log('Error:', error);
  if (data) {
    console.log(`Success! Retrieved ${data.length} SKUs.`);
    if (data.length > 0) {
      console.log('Sample SKU:', data[0]);
    }
  }
}

run();
