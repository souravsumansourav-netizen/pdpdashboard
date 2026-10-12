import fs from 'fs';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, v] = line.split('=');
  if (k && v) env[k.trim()] = v.trim();
});

async function check() {
  const url = `${env['VITE_SUPABASE_URL']}/rest/v1/sku_attribute_master?select=category&limit=10`;
  const res = await fetch(url, {
    headers: {
      'apikey': env['VITE_SUPABASE_ANON_KEY'],
      'Authorization': `Bearer ${env['VITE_SUPABASE_ANON_KEY']}`
    }
  });
  console.log('master categories:', await res.json());

  const url2 = `${env['VITE_SUPABASE_URL']}/rest/v1/product_metrics?select=category&limit=10`;
  const res2 = await fetch(url2, {
    headers: {
      'apikey': env['VITE_SUPABASE_ANON_KEY'],
      'Authorization': `Bearer ${env['VITE_SUPABASE_ANON_KEY']}`
    }
  });
  console.log('product categories:', await res2.json());
}
check();
