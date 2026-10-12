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
    .eq('product_identifier', '22 Karat Yellow Gold Coin Drop Bridal Necklace Set');
    
  console.log("Check specific product:", data);
  
  const { data: coins, error: err2 } = await supabase
    .from('product_metrics')
    .select('product_identifier')
    .eq('category', 'Coin');
    
  if(coins) {
    const uniques = [...new Set(coins.map(d => d.product_identifier))];
    const withEarring = uniques.filter(u => u.toLowerCase().includes('earring'));
    const withNecklace = uniques.filter(u => u.toLowerCase().includes('necklace'));
    console.log("Remaining coins with Earring:", withEarring.length);
    console.log("Remaining coins with Necklace:", withNecklace.length);
  }
}
test();
