import fs from 'fs';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, v] = line.split('=');
  if (k && v) env[k.trim()] = v.trim();
});

async function check() {
  const query = `
    WITH agg_pm AS (
        SELECT 
            pm.product_identifier,
            SUM(pm.views) as views,
            SUM(pm.cart_adds) as cart_adds,
            SUM(pm.purchases) as purchases,
            SUM(pm.fis_users) as fis_users
        FROM product_metrics pm
        WHERE ('Overall' = 'Overall' OR pm.upload_date::text = 'Overall')
          AND ('All' = 'All' OR pm.category = 'All')
          AND ('combined' = 'combined' OR pm.platform = 'combined')
        GROUP BY pm.product_identifier
    )
    SELECT COUNT(*) FROM agg_pm;
  `;
  // Again, I can't run raw SQL from fetch using PostgREST for arbitrary complex CTEs.
  // I need to create a temporary RPC or just update the actual RPC!
}
check();
