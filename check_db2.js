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
  const { count: pmCount, error: pmErr } = await supabase.from('product_metrics').select('*', { count: 'exact', head: true });
  console.log('Product Metrics Count:', pmCount, pmErr || '');

  const { count: sabCount, error: sabErr } = await supabase.from('sku_attribute_bridge').select('*', { count: 'exact', head: true });
  console.log('Bridge Count:', sabCount, sabErr || '');

  const { count: samCount, error: samErr } = await supabase.from('sku_attribute_master').select('*', { count: 'exact', head: true });
  console.log('Master Count:', samCount, samErr || '');
}
check();
