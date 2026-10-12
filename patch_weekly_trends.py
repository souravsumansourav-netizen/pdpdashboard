import re

with open("src/components/WeeklyTrendsDashboard.jsx", "r") as f:
    code = f.read()

# 1. Add total computations
totals_hooks = """
  // Totals calculations
  const tabularTotals = useMemo(() => {
    let t = { views: 0, cart_adds: 0, purchases: 0, fis_users: 0 };
    filteredData.forEach(d => {
      t.views += d.views || 0;
      t.cart_adds += d.cart_adds || 0;
      t.purchases += d.purchases || 0;
      t.fis_users += d.fis_users || 0;
    });
    t.pdp_to_cart_rate = t.views > 0 ? t.cart_adds / t.views : 0;
    t.overall_conv_rate = t.views > 0 ? t.purchases / t.views : 0;
    t.fis_intent_rate = t.views > 0 ? t.fis_users / t.views : 0;
    return t;
  }, [filteredData]);

  const weeklyCatTotals = useMemo(() => {
    let t = { views: 0, cart_adds: 0, purchases: 0, fis_users: 0 };
    weeklyCategoryData.forEach(c => {
      t.views += c.views || 0;
      t.cart_adds += c.cart_adds || 0;
      t.purchases += c.purchases || 0;
      t.fis_users += c.fis_users || 0;
    });
    t.pdp_to_cart_rate = t.views > 0 ? t.cart_adds / t.views : 0;
    t.overall_conv_rate = t.views > 0 ? t.purchases / t.views : 0;
    t.fis_intent_rate = t.views > 0 ? t.fis_users / t.views : 0;
    t.overall_intent_rate = t.views > 0 ? (t.cart_adds + t.fis_users) / t.views : 0;
    return t;
  }, [weeklyCategoryData]);

  const compTotals = useMemo(() => {
    let a = { views: 0, cart_adds: 0, purchases: 0, fis_users: 0 };
    let b = { views: 0, cart_adds: 0, purchases: 0, fis_users: 0 };
    categoryComparisonData.forEach(c => {
      a.views += c.viewsA || 0; a.cart_adds += c.cartAddsA || 0; a.purchases += c.purchasesA || 0; a.fis_users += c.fisUsersA || 0;
      b.views += c.viewsB || 0; b.cart_adds += c.cartAddsB || 0; b.purchases += c.purchasesB || 0; b.fis_users += c.fisUsersB || 0;
    });
    const aPdp = a.views > 0 ? a.cart_adds / a.views : 0; const aConv = a.views > 0 ? a.purchases / a.views : 0;
    const bPdp = b.views > 0 ? b.cart_adds / b.views : 0; const bConv = b.views > 0 ? b.purchases / b.views : 0;
    
    return {
       viewsPct: a.views > 0 ? (b.views - a.views)/a.views : 0,
       cartAddsPct: a.cart_adds > 0 ? (b.cart_adds - a.cart_adds)/a.cart_adds : 0,
       purchasesPct: a.purchases > 0 ? (b.purchases - a.purchases)/a.purchases : 0,
       fisUsersPct: a.fis_users > 0 ? (b.fis_users - a.fis_users)/a.fis_users : 0,
       pdpToCartDiff: bPdp - aPdp,
       convRateDiff: bConv - aConv
    };
  }, [categoryComparisonData]);

  const trendMatrixTotals = useMemo(() => {
    if(!trendMatrixData.latest4Weeks || trendMatrixData.latest4Weeks.length === 0) return { map: {}, sparklineData: [] };
    const latest5Weeks = weeks.slice(-5);
    const tMapAll = {};
    latest5Weeks.forEach(w => { tMapAll[w] = { views:0, cart_adds:0, purchases:0, fis_users:0, total_intent:0 }; });
    
    trendMatrixData.categories.forEach(cat => {
       latest5Weeks.forEach(w => {
          const c = trendMatrixData.map[cat] && trendMatrixData.map[cat][w];
          if(c) {
             tMapAll[w].views += c.views||0; tMapAll[w].cart_adds += c.cart_adds||0; 
             tMapAll[w].purchases += c.purchases||0; tMapAll[w].fis_users += c.fis_users||0;
             tMapAll[w].total_intent += c.total_intent||0;
          }
       });
    });
    
    trendMatrixData.latest4Weeks.forEach(w => {
       const curr = tMapAll[w];
       const prevW = latest5Weeks[latest5Weeks.indexOf(w)-1];
       const prev = prevW ? tMapAll[prevW] : null;
       curr.wow_views = (prev && prev.views>0) ? (curr.views - prev.views)/prev.views : 0;
       curr.wow_cart = (prev && prev.cart_adds>0) ? (curr.cart_adds - prev.cart_adds)/prev.cart_adds : 0;
       curr.wow_purch = (prev && prev.purchases>0) ? (curr.purchases - prev.purchases)/prev.purchases : 0;
       curr.wow_fis = (prev && prev.fis_users>0) ? (curr.fis_users - prev.fis_users)/prev.fis_users : 0;
       curr.wow_total_intent = (prev && prev.total_intent>0) ? (curr.total_intent - prev.total_intent)/prev.total_intent : 0;
    });
    
    const sparklineData = trendMatrixData.latest4Weeks.map(w => ({ name: w, views: tMapAll[w].views }));
    return { map: tMapAll, sparklineData };
  }, [trendMatrixData, weeks]);
"""

code = code.replace("const toggleExpand = (category) => {", totals_hooks + "\n  const toggleExpand = (category) => {")


# 2. Update trendMatrixData to include total_intent
trend_matrix_replacement = """
       c.views += row.views || 0;
       c.cart_adds += row.cart_adds || 0;
       c.purchases += row.purchases || 0;
       c.fis_users += row.fis_users || 0;
       c.total_intent = c.cart_adds + c.fis_users;
    });
    
    // Calculate WoW % and build Sparkline array
    Object.keys(byCategory).forEach(cat => {
       latest4Weeks.forEach(w => {
          const c = byCategory[cat][w];
          const prevW = latest5Weeks[latest5Weeks.indexOf(w) - 1];
          const prev = prevW ? byCategory[cat][prevW] : null;
          
          c.wow_views = (prev && prev.views > 0) ? (c.views - prev.views) / prev.views : 0;
          c.wow_cart = (prev && prev.cart_adds > 0) ? (c.cart_adds - prev.cart_adds) / prev.cart_adds : 0;
          c.wow_purch = (prev && prev.purchases > 0) ? (c.purchases - prev.purchases) / prev.purchases : 0;
          c.wow_fis = (prev && prev.fis_users > 0) ? (c.fis_users - prev.fis_users) / prev.fis_users : 0;
          c.wow_total_intent = (prev && prev.total_intent > 0) ? (c.total_intent - prev.total_intent) / prev.total_intent : 0;
       });
"""
code = re.sub(r'c\.views \+= row\.views \|\| 0;.*?c\.wow_fis = \([^;]*;', trend_matrix_replacement, code, flags=re.DOTALL)

with open("src/components/WeeklyTrendsDashboard.jsx", "w") as f:
    f.write(code)
