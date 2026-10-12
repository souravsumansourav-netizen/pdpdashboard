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
  const { data, error } = await supabase.rpc('get_category_drilldown', {
      p_category: 'Coin',
      p_platform: 'combined',
      p_start_date: '2020-01-01',
      p_end_date: '2030-01-01'
  });
  
  if (error) {
      console.log("Error:", error);
      return;
  }
  
  console.log(`Total products returned for Coin: ${data.length}`);
  const notCoin = data.filter(d => !d.product_identifier.toLowerCase().includes('coin') && !d.product_identifier.toLowerCase().includes('bar') && !d.product_identifier.toLowerCase().includes('vedhani') && !d.product_identifier.toLowerCase().includes('ginni') && !d.product_identifier.toLowerCase().includes('purity') && !d.product_identifier.toLowerCase().includes('gram'));
  console.log("Products that don't look like coins:");
  notCoin.slice(0, 10).forEach(d => console.log(d.product_identifier));
}
test();
