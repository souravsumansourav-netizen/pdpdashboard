import re

with open('src/components/CategoryDrillDownModal.jsx', 'r') as f:
    content = f.read()

# 1. Add state for activeLayer2
content = content.replace(
    "const [threshold, setThreshold] = useState(50);",
    "const [threshold, setThreshold] = useState(50);\n  const [activeLayer2, setActiveLayer2] = useState(null);"
)

# 2. Modify concentrationSummary to return skus
old_calc = """      for (const row of sorted) {
        runningSum += row[metric];
        count++;
        if (runningSum >= target) break;
      }
      
      return { 
        count, 
        totalSkus: sorted.length, 
        share: (runningSum / total) * 100 
      };"""

new_calc = """      const skus = [];
      for (const row of sorted) {
        runningSum += row[metric];
        count++;
        skus.push(row);
        if (runningSum >= target) break;
      }
      
      return { 
        count, 
        totalSkus: sorted.length, 
        share: (runningSum / total) * 100,
        skus
      };"""

content = content.replace(old_calc, new_calc)

# 3. Add FIS useMemos
old_cart_memos = """  const wastedViewsCart = useMemo(() => {
    return data.filter(d => d.opp_score_cart && d.opp_score_cart < 0)
               .sort((a, b) => a.opp_score_cart - b.opp_score_cart)
               .slice(0, 50);
  }, [data]);"""

new_cart_memos = """  const wastedViewsCart = useMemo(() => {
    return data.filter(d => d.opp_score_cart && d.opp_score_cart < 0)
               .sort((a, b) => a.opp_score_cart - b.opp_score_cart)
               .slice(0, 50);
  }, [data]);

  const underexposedFis = useMemo(() => {
    return data.filter(d => d.opp_score_fis && d.opp_score_fis > 0)
               .sort((a, b) => b.opp_score_fis - a.opp_score_fis)
               .slice(0, 50);
  }, [data]);
  
  const wastedViewsFis = useMemo(() => {
    return data.filter(d => d.opp_score_fis && d.opp_score_fis < 0)
               .sort((a, b) => a.opp_score_fis - b.opp_score_fis)
               .slice(0, 50);
  }, [data]);"""

content = content.replace(old_cart_memos, new_cart_memos)

# 4. Make cards clickable
old_cards = """                  <div className="summary-card">
                    <h4>Views</h4>
                    <p><strong>{concentrationSummary.views.count}</strong> of {concentrationSummary.views.totalSkus} SKUs</p>
                    <p className="subtext">({formatPercent(concentrationSummary.views.count / concentrationSummary.views.totalSkus)}) account for ~{threshold}% of views</p>
                  </div>
                  <div className="summary-card">
                    <h4>Cart Adds</h4>
                    <p><strong>{concentrationSummary.cart.count}</strong> of {concentrationSummary.cart.totalSkus} SKUs</p>
                    <p className="subtext">({formatPercent(concentrationSummary.cart.count / concentrationSummary.cart.totalSkus)}) account for ~{threshold}% of cart adds</p>
                  </div>
                  <div className="summary-card">
                    <h4>FIS Users</h4>
                    <p><strong>{concentrationSummary.fis.count}</strong> of {concentrationSummary.fis.totalSkus} SKUs</p>
                    <p className="subtext">({formatPercent(concentrationSummary.fis.count / concentrationSummary.fis.totalSkus)}) account for ~{threshold}% of FIS</p>
                  </div>"""

new_cards = """                  <div className={`summary-card clickable ${activeLayer2 === 'views' ? 'active' : ''}`} onClick={() => setActiveLayer2(activeLayer2 === 'views' ? null : 'views')}>
                    <h4>Views</h4>
                    <p><strong>{concentrationSummary.views.count}</strong> of {concentrationSummary.views.totalSkus} SKUs</p>
                    <p className="subtext">({formatPercent(concentrationSummary.views.count / concentrationSummary.views.totalSkus)}) account for ~{threshold}% of views</p>
                  </div>
                  <div className={`summary-card clickable ${activeLayer2 === 'cart' ? 'active' : ''}`} onClick={() => setActiveLayer2(activeLayer2 === 'cart' ? null : 'cart')}>
                    <h4>Cart Adds</h4>
                    <p><strong>{concentrationSummary.cart.count}</strong> of {concentrationSummary.cart.totalSkus} SKUs</p>
                    <p className="subtext">({formatPercent(concentrationSummary.cart.count / concentrationSummary.cart.totalSkus)}) account for ~{threshold}% of cart adds</p>
                  </div>
                  <div className={`summary-card clickable ${activeLayer2 === 'fis' ? 'active' : ''}`} onClick={() => setActiveLayer2(activeLayer2 === 'fis' ? null : 'fis')}>
                    <h4>FIS Users</h4>
                    <p><strong>{concentrationSummary.fis.count}</strong> of {concentrationSummary.fis.totalSkus} SKUs</p>
                    <p className="subtext">({formatPercent(concentrationSummary.fis.count / concentrationSummary.fis.totalSkus)}) account for ~{threshold}% of FIS</p>
                  </div>"""

content = content.replace(old_cards, new_cards)

# 5. Add Layer 2 render block
layer2_block = """
              {activeLayer2 && (
                <div className="drilldown-section layer2-drilldown">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h3>Top {activeLayer2 === 'views' ? 'Views' : activeLayer2 === 'cart' ? 'Cart Adds' : 'FIS Users'} Contributors ({concentrationSummary[activeLayer2].skus.length} SKUs)</h3>
                    <button onClick={() => setActiveLayer2(null)} style={{ padding: '0.2rem 0.5rem', cursor: 'pointer' }}>Close</button>
                  </div>
                  <div className="table-wrapper">
                    <table className="trends-table">
                      <thead>
                        <tr>
                          <th>Product ID</th>
                          <th>Product Name</th>
                          <th>Views</th>
                          <th>Cart Adds</th>
                          <th>Purchases</th>
                          <th>FIS Users</th>
                        </tr>
                      </thead>
                      <tbody>
                        {concentrationSummary[activeLayer2].skus.map(row => (
                          <tr key={row.product_identifier}>
                            <td>{row.base_sku || row.product_identifier}</td>
                            <td>{row.product_name || 'Unknown'}</td>
                            <td>{row.views}</td>
                            <td>{row.cart_adds}</td>
                            <td>{row.purchases}</td>
                            <td>{row.fis_users}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
"""

# Insert Layer 2 right after summary-cards block
content = content.replace(
    '</div>\n              </div>\n\n              {anomalies.length > 0 && (',
    '</div>\n              </div>\n' + layer2_block + '\n              {anomalies.length > 0 && ('
)


# 6. Add FIS Opp sections
fis_opps = """
              <div className="drilldown-section">
                <h3>Underexposed Opportunities (FIS)</h3>
                <p className="section-desc">High FIS conversion, barely seen. Push visibility.</p>
                <div className="table-wrapper">
                  <table className="trends-table">
                    <thead>
                      <tr>
                        <th>Product ID</th>
                        <th>Product Name</th>
                        <th>Views</th>
                        <th>FIS Users</th>
                        <th>Wilson Adj. Rate</th>
                        <th>Opp Score</th>
                      </tr>
                    </thead>
                    <tbody>
                      {underexposedFis.map(row => (
                        <tr key={row.product_identifier}>
                          <td>{row.base_sku || row.product_identifier}</td>
                          <td>{row.product_name || 'Unknown'}</td>
                          <td>{row.views}</td>
                          <td>{row.fis_users}</td>
                          <td>{formatPercent(row.wilson_fis_rate)}</td>
                          <td style={{color: '#10b981'}}>+{formatPercent(row.opp_score_fis)}</td>
                        </tr>
                      ))}
                      {underexposedFis.length === 0 && (
                        <tr><td colSpan="6" style={{textAlign: 'center'}}>No significant opportunities found.</td></tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="drilldown-section">
                <h3>Wasted Views (FIS)</h3>
                <p className="section-desc">Seen a lot, very low FIS engagement.</p>
                <div className="table-wrapper">
                  <table className="trends-table">
                    <thead>
                      <tr>
                        <th>Product ID</th>
                        <th>Product Name</th>
                        <th>Views</th>
                        <th>FIS Users</th>
                        <th>Wilson Adj. Rate</th>
                        <th>Opp Score</th>
                      </tr>
                    </thead>
                    <tbody>
                      {wastedViewsFis.map(row => (
                        <tr key={row.product_identifier}>
                          <td>{row.base_sku || row.product_identifier}</td>
                          <td>{row.product_name || 'Unknown'}</td>
                          <td>{row.views}</td>
                          <td>{row.fis_users}</td>
                          <td>{formatPercent(row.wilson_fis_rate)}</td>
                          <td style={{color: '#ef4444'}}>{formatPercent(row.opp_score_fis)}</td>
                        </tr>
                      ))}
                      {wastedViewsFis.length === 0 && (
                        <tr><td colSpan="6" style={{textAlign: 'center'}}>No significant wasted views found.</td></tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
"""

content = content.replace(
    '</>\n          )}\n        </div>',
    fis_opps + '\n            </>\n          )}\n        </div>'
)

with open('src/components/CategoryDrillDownModal.jsx', 'w') as f:
    f.write(content)
