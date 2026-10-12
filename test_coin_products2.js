import fs from 'fs';
import { createClient } from '@supabase/supabase-js';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, ...v] = line.split('=');
  if (k && v.length > 0) env[k.trim()] = v.join('=').trim();
});

const supabase = createClient(env['VITE_SUPABASE_URL'], env['VITE_SUPABASE_ANON_KEY']);

async function test() {
  const { data, error } = await supabase
    .from('product_metrics')
    .select('product_identifier, category')
    .eq('category', 'Coin')
    .ilike('product_identifier', '%Earring%')
    .limit(10);
    
  console.log("Earrings in Coin category:", data);

  const { data: data2, error: error2 } = await supabase
    .from('product_metrics')
    .select('product_identifier, category')
    .eq('category', 'Coin')
    .ilike('product_identifier', '%Necklace%')
    .limit(10);
    
  console.log("Necklace in Coin category:", data2);
}
test();
