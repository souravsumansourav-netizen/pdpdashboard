import fs from 'fs';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, v] = line.split('=');
  if (k && v) env[k.trim()] = v.trim();
});

async function check() {
  const url = `${env['VITE_SUPABASE_URL']}/rest/v1/category_metrics?select=upload_date&limit=1`;
  const start = Date.now();
  const res = await fetch(url, {
    headers: {
      'apikey': env['VITE_SUPABASE_ANON_KEY'],
      'Authorization': `Bearer ${env['VITE_SUPABASE_ANON_KEY']}`
    }
  });
  console.log('category_metrics time:', Date.now() - start, 'ms');
  
  const url2 = `${env['VITE_SUPABASE_URL']}/rest/v1/sku_attribute_master?select=attributes&limit=1`;
  const start2 = Date.now();
  const res2 = await fetch(url2, {
    headers: {
      'apikey': env['VITE_SUPABASE_ANON_KEY'],
      'Authorization': `Bearer ${env['VITE_SUPABASE_ANON_KEY']}`
    }
  });
  console.log('sku_attribute_master time:', Date.now() - start2, 'ms');
}
check();
