import fs from 'fs';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, v] = line.split('=');
  if (k && v) env[k.trim()] = v.trim();
});

async function check() {
  const url = `${env['VITE_SUPABASE_URL']}/rest/v1/sku_attribute_master?select=base_sku`,
        res = await fetch(url, { headers: { apikey: env['VITE_SUPABASE_ANON_KEY'], 'Prefer': 'count=exact' }});
  console.log(res.headers.get('content-range'));
}
check();
