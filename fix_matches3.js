import fs from 'fs';
import { createClient } from '@supabase/supabase-js';

const envFile = fs.readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [k, ...v] = line.split('=');
  if (k && v.length > 0) env[k.trim()] = v.join('=').trim();
});

const supabase = createClient(env['VITE_SUPABASE_URL'], env['VITE_SUPABASE_ANON_KEY']);
const categoryMapping = JSON.parse(fs.readFileSync('./src/config/category_mapping.json', 'utf8'));

// Jaro-Winkler
function jaroWinkler(s1, s2) {
    if (s1 === s2) return 1.0;
    const len1 = s1.length;
    const len2 = s2.length;
    if (len1 === 0 || len2 === 0) return 0.0;
    const matchDistance = Math.floor(Math.max(len1, len2) / 2) - 1;
    const s1Matches = new Array(len1).fill(false);
    const s2Matches = new Array(len2).fill(false);
    let matches = 0, transpositions = 0;
    for (let i = 0; i < len1; i++) {
        const start = Math.max(0, i - matchDistance), end = Math.min(i + matchDistance + 1, len2);
        for (let j = start; j < end; j++) {
            if (s2Matches[j]) continue;
            if (s1[i] !== s2[j]) continue;
            s1Matches[i] = true; s2Matches[j] = true; matches++; break;
        }
    }
    if (matches === 0) return 0.0;
    let k = 0;
    for (let i = 0; i < len1; i++) {
        if (!s1Matches[i]) continue;
        while (!s2Matches[k]) k++;
        if (s1[i] !== s2[k]) transpositions++; k++;
    }
    transpositions = transpositions / 2.0;
    const m = matches, jaro = (m / len1 + m / len2 + (m - transpositions) / m) / 3.0;
    let prefix = 0;
    const maxPrefix = Math.min(4, Math.min(len1, len2));
    for (let i = 0; i < maxPrefix; i++) { if (s1[i] === s2[i]) prefix++; else break; }
    return jaro + (prefix * 0.1 * (1.0 - jaro));
}

const normalize = (str) => {
    if (!str) return '';
    return String(str).trim().toLowerCase().replace(/\s+/g, ' ');
};
const getMappedCategory = (rawCat) => {
    const norm = normalize(rawCat);
    return normalize(categoryMapping[norm] || rawCat);
};

async function fix() {
    console.log('Fetching all metrics...');
    const uniqueMap = new Map();
    let count = 0;
    while(true) {
        const { data } = await supabase.from('product_metrics').select('product_identifier, category').range(count, count + 999);
        if(!data || data.length === 0) break;
        data.forEach(p => uniqueMap.set(p.product_identifier, p.category));
        count += 1000;
    }
    const uniqueIdentifiers = Array.from(uniqueMap.keys());
    console.log('Found', uniqueIdentifiers.length, 'unique products.');

    console.log('Fetching master SKUs...');
    const masterData = [];
    count = 0;
    while(true) {
        const { data } = await supabase.from('sku_attribute_master').select('base_sku, category').range(count, count + 999);
        if(!data || data.length === 0) break;
        masterData.push(...data);
        count += 1000;
    }
    
    const masterList = masterData.map(m => ({
        base_sku: m.base_sku,
        norm_sku: normalize(m.base_sku),
        mapped_cat: getMappedCategory(m.category)
    }));

    const newBridgeRows = [];
    console.log('Matching...');
    let mCount = 0;
    for (const rawId of uniqueIdentifiers) {
        const normId = normalize(rawId);
        const mappedProdCat = getMappedCategory(uniqueMap.get(rawId));
        
        let bestMatch = null, bestTier = 'Unmatched', bestConf = 0;
        const validMasters = masterList.filter(m => m.mapped_cat === mappedProdCat || mappedProdCat === 'unmapped' || mappedProdCat === '');

        if (validMasters.length > 0) {
            const exactMatch = validMasters.find(m => m.norm_sku === normId);
            if (exactMatch) {
                bestMatch = exactMatch; bestTier = 'Exact'; bestConf = 1.0;
            } else {
                const prefixMatches = validMasters.filter(m => normId.startsWith(m.norm_sku) || m.norm_sku.startsWith(normId));
                if (prefixMatches.length > 0) {
                    bestMatch = prefixMatches.reduce((a, b) => a.norm_sku.length > b.norm_sku.length ? a : b);
                    bestTier = 'Prefix'; bestConf = 0.95;
                } else {
                    let maxScore = 0, topFuzzyMatch = null;
                    for (const master of validMasters) {
                        const score = jaroWinkler(normId, master.norm_sku);
                        if (score > maxScore) { maxScore = score; topFuzzyMatch = master; }
                    }
                    if (maxScore > 0.85 && topFuzzyMatch) {
                        bestMatch = topFuzzyMatch; bestTier = 'Fuzzy'; bestConf = parseFloat(maxScore.toFixed(3));
                    }
                }
            }
        }

        newBridgeRows.push({
            product_identifier: rawId,
            base_sku: bestMatch ? bestMatch.base_sku : null,
            match_tier: bestTier,
            confidence: bestConf
        });
        mCount++;
        if(mCount % 5000 === 0) console.log('Matched', mCount);
    }

    console.log('Clearing old bridge rows...');
    await supabase.from('sku_attribute_bridge').delete().neq('product_identifier', 'NONE');
    
    console.log('Inserting', newBridgeRows.length, 'new bridge rows...');
    for (let i = 0; i < newBridgeRows.length; i += 1000) {
        const chunk = newBridgeRows.slice(i, i + 1000);
        await supabase.from('sku_attribute_bridge').upsert(chunk, { onConflict: 'product_identifier' });
        console.log(`Inserted ${i + chunk.length} / ${newBridgeRows.length}`);
    }
    console.log('Done!');
}

fix();
