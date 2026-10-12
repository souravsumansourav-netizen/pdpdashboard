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
    .select('product_identifier')
    .eq('category', 'Coin');
    
  if(data) {
    const uniques = [...new Set(data.map(d => d.product_identifier))];
    console.log("Total unique coins:", uniques.length);
    const withEarring = uniques.filter(u => u.toLowerCase().includes('earring'));
    const withNecklace = uniques.filter(u => u.toLowerCase().includes('necklace'));
    console.log("With Earring:", withEarring.length);
    console.log("With Necklace:", withNecklace.length);
    if(withEarring.length > 0) console.log("Example:", withEarring[0]);
  }
}
test();
