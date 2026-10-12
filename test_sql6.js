import fs from 'fs';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, v] = line.split('=');
  if (k && v) env[k.trim()] = v.trim();
});

async function check() {
  const url = `${env['VITE_SUPABASE_URL']}/rest/v1/rpc/get_attribute_breakdown`;
  console.log('Sending request to RPC 2...');
  const start = Date.now();
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'apikey': env['VITE_SUPABASE_ANON_KEY'],
      'Authorization': `Bearer ${env['VITE_SUPABASE_ANON_KEY']}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      p_month: 'Overall',
      p_category: 'All',
      p_platform: 'combined',
      p_attribute_key: 'METAL'
    })
  });
  console.log('Time:', Date.now() - start, 'ms. Status:', res.status);
  if(res.status !== 200) {
      console.log('Response:', await res.text());
  }
}
check();
