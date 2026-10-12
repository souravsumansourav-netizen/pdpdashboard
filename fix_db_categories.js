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
    let count = 0;
    while(true) {
        const { data } = await supabase.from('product_metrics').select('id, product_identifier, category').range(count, count + 999);
        if(!data || data.length === 0) break;
        
        for (const row of data) {
            const lowerName = row.product_identifier.toLowerCase();
            let newCat = row.category;
            
            if (row.category === 'Coin' || row.category === 'Unmapped') {
                if (lowerName.includes('earring')) newCat = 'Earrings';
                else if (lowerName.includes('necklace')) newCat = 'Necklace';
                else if (lowerName.includes('pendant')) newCat = 'Pendant';
                else if (lowerName.includes('ring') && !lowerName.includes('earring')) newCat = 'Ring';
                else if (lowerName.includes('bangle')) newCat = 'Bangle';
                else if (lowerName.includes('bracelet')) newCat = 'Bracelet';
            }
            
            if (newCat !== row.category) {
                console.log(`Updating ${row.product_identifier} from ${row.category} to ${newCat}`);
                await supabase.from('product_metrics').update({ category: newCat }).eq('id', row.id);
            }
        }
        count += 1000;
    }
    console.log("DB fix complete.");
}
fixDB();
