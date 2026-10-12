import { supabase } from './src/config/supabaseClient.js';
import { processNewMatches } from './src/utils/matchingLogic.js';

async function fix() {
    console.log('Fetching unique identifiers from product_metrics...');
    
    // We can't do SELECT DISTINCT via JS easily for 600k rows without running into limits,
    // so let's just clear the bridge table, and then select everything from product_metrics in chunks
    // and pass it to processNewMatches which handles grouping!
    
    console.log('Clearing sku_attribute_bridge...');
    // We have to clear it manually in the DB or via API if possible.
    // PostgREST doesn't allow truncate without a filter.
    // Let's just pass {product_identifier, category} into processNewMatches.
    // Since processNewMatches checks existingBridgeMap, we MUST clear it first.
    
    // I'll execute a direct delete if possible.
    await supabase.from('sku_attribute_bridge').delete().neq('product_identifier', '000000');
    console.log('Cleared bridge table.');

    let count = 0;
    const CHUNK = 5000;
    
    while(true) {
        const { data, error } = await supabase
            .from('product_metrics')
            .select('product_identifier, category')
            .range(count, count + CHUNK - 1);
            
        if(error) {
            console.error(error);
            break;
        }
        
        if(!data || data.length === 0) break;
        
        // Map to expected format
        const products = data.map(d => ({
            identifier: d.product_identifier,
            category: d.category
        }));
        
        console.log(`Processing chunk ${count} to ${count + CHUNK}, size: ${products.length}`);
        await processNewMatches(products);
        
        count += CHUNK;
    }
    
    console.log('Done! Finished processing ' + count + ' rows.');
}

fix();
