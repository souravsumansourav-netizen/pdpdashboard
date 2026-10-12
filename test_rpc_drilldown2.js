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
  console.log("Fetching drilldown for Coin...");
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
  const withEarring = data.filter(d => d.product_identifier.toLowerCase().includes('earring'));
  const withNecklace = data.filter(d => d.product_identifier.toLowerCase().includes('necklace'));
  console.log("With Earring:", withEarring.length);
  console.log("With Necklace:", withNecklace.length);
  
  if (withEarring.length > 0) console.log("Example:", withEarring[0]);
  if (withNecklace.length > 0) console.log("Example:", withNecklace[0]);
}
test();
