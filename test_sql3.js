import fs from 'fs';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, v] = line.split('=');
  if (k && v) env[k.trim()] = v.trim();
});

async function check() {
  const query = `
    SELECT DISTINCT jsonb_object_keys(attributes) AS key
    FROM (SELECT attributes FROM sku_attribute_master LIMIT 1000) AS sample
    ORDER BY key
  `;
  // I can't run this raw query directly. I have to use PostgREST or modify the RPC.
}
check();
