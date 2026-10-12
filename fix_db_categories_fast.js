import fs from 'fs';
import { createClient } from '@supabase/supabase-js';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, ...v] = line.split('=');
  if (k && v.length > 0) env[k.trim()] = v.join('=').trim();
});

const supabase = createClient(env['VITE_SUPABASE_URL'], env['VITE_SUPABASE_ANON_KEY']);

async function fixDB() {
    console.log("Updating Earrings...");
    let { data: eData, error: eErr } = await supabase.from('product_metrics')
        .update({ category: 'Earrings' })
        .eq('category', 'Coin')
        .ilike('product_identifier', '%earring%');
    console.log("Earrings updated", eErr);

    console.log("Updating Necklace...");
    let { data: nData, error: nErr } = await supabase.from('product_metrics')
        .update({ category: 'Necklace' })
        .eq('category', 'Coin')
        .ilike('product_identifier', '%necklace%');
    console.log("Necklace updated", nErr);
    
    console.log("Updating Pendant...");
    let { data: pData, error: pErr } = await supabase.from('product_metrics')
        .update({ category: 'Pendant' })
        .eq('category', 'Coin')
        .ilike('product_identifier', '%pendant%');
    console.log("Pendant updated", pErr);
    
    // For Unmapped as well
    console.log("Updating Unmapped Earrings...");
    await supabase.from('product_metrics')
        .update({ category: 'Earrings' })
        .eq('category', 'Unmapped')
        .ilike('product_identifier', '%earring%');

    console.log("Updating Unmapped Necklace...");
    await supabase.from('product_metrics')
        .update({ category: 'Necklace' })
        .eq('category', 'Unmapped')
        .ilike('product_identifier', '%necklace%');
        
    console.log("Done");
}
fixDB();
