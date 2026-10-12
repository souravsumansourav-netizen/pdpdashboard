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
    .limit(10);
    
  console.log("Error:", error);
  console.log("Product Metrics Data:", data);
  
  if (data && data.length > 0) {
      const identifiers = data.map(d => d.product_identifier);
      const { data: sabData, error: sabError } = await supabase
        .from('sku_attribute_bridge')
        .select('*')
        .in('product_identifier', identifiers);
        
      console.log("SAB Error:", sabError);
      console.log("SAB Data:", sabData);
      
      const baseSkus = sabData.map(d => d.base_sku).filter(Boolean);
      if (baseSkus.length > 0) {
          const { data: samData, error: samError } = await supabase
            .from('sku_attribute_master')
            .select('base_sku, category, attributes')
            .in('base_sku', baseSkus);
            
          console.log("SAM Error:", samError);
          console.log("SAM Data:", samData.map(d => ({base_sku: d.base_sku, category: d.category, title: d.attributes?.TITLE})));
      }
  }
}
test();
