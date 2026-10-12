import fs from 'fs';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, v] = line.split('=');
  if (k && v) env[k.trim()] = v.trim();
});

async function check() {
  const url = `${env['VITE_SUPABASE_URL']}/rest/v1/rpc/get_dashboard_filters`;
  console.log('Fetching:', url);
  
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'apikey': env['VITE_SUPABASE_ANON_KEY'],
      'Authorization': `Bearer ${env['VITE_SUPABASE_ANON_KEY']}`,
      'Content-Type': 'application/json'
    }
  });
  
  const status = res.status;
  const text = await res.text();
  console.log('Status:', status);
  console.log('Response:', text);
}
check();
