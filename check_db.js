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
  console.log('--- CATEGORY METRICS ---');
  const { data: catData, error: catError } = await supabase
    .from('category_metrics')
    .select('upload_date, platform, views, fis_users');
  
  if (catError) console.error(catError);
  else {
    const summary = {};
    catData.forEach(r => {
      const key = `${r.upload_date} | ${r.platform}`;
      if (!summary[key]) summary[key] = { rows: 0, views: 0, fis: 0 };
      summary[key].rows += 1;
      summary[key].views += r.views || 0;
      summary[key].fis += r.fis_users || 0;
    });
    console.table(summary);
  }

  console.log('\n--- PRODUCT METRICS ---');
  const { data: prodData, error: prodError } = await supabase
    .from('product_metrics')
    .select('upload_date, platform, views, fis_users');
  
  if (prodError) console.error(prodError);
  else {
    const summary = {};
    prodData.forEach(r => {
      const key = `${r.upload_date} | ${r.platform}`;
      if (!summary[key]) summary[key] = { rows: 0, views: 0, fis: 0 };
      summary[key].rows += 1;
      summary[key].views += r.views || 0;
      summary[key].fis += r.fis_users || 0;
    });
    console.table(summary);
  }
}
check();
