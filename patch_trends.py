import re

with open('src/components/TrendsDashboard.jsx', 'r') as f:
    content = f.read()

# 1. Imports
content = content.replace(
    "import { exportToCSV } from '../utils/exportUtils';",
    "import { exportToCSV } from '../utils/exportUtils';\nimport { CategoryDrillDownModal } from './CategoryDrillDownModal';"
)

# 2. State
content = content.replace(
    "const [selectedMonthTable, setSelectedMonthTable] = useState('');",
    """const [selectedStartMonth, setSelectedStartMonth] = useState('');
  const [selectedEndMonth, setSelectedEndMonth] = useState('');
  
  const [drillDownCategory, setDrillDownCategory] = useState(null);
  const [isDrillDownOpen, setIsDrillDownOpen] = useState(false);"""
)

# 3. Categories array
content = content.replace(
    "const cats = new Set(data.map(d => d.category));",
    "const cats = new Set(data.map(d => (!d.category || d.category === 'N/A') ? 'Uncategorized' : d.category));"
)

# 4. activeMonthTable & monthlyCategoryData
old_monthly_data = """  const activeMonthTable = selectedMonthTable || (months.length > 0 ? months[0] : '');
  const activeMaterialMonth = materialMonth || (months.length > 0 ? months[0] : '');

  const monthlyCategoryData = useMemo(() => {
    if (!activeMonthTable) return [];
    
    let filtered = data.filter(d => 
      d.upload_date === activeMonthTable && 
      d.platform === selectedPlatform && 
      d.category !== 'All'
    );

    if (excludedCategories.length > 0) {
      filtered = filtered.filter(d => !excludedCategories.includes(d.category));
    }
    
    const byCategory = {};
    filtered.forEach(row => {
      if (!byCategory[row.category]) {
        byCategory[row.category] = {
          category: row.category,
          views: 0,
          cart_adds: 0,
          purchases: 0,
          fis_users: 0,
        };
      }
      const c = byCategory[row.category];
      c.views += row.views || 0;
      c.cart_adds += row.cart_adds || 0;
      c.purchases += row.purchases || 0;
      c.fis_users += row.fis_users || 0;
    });"""

new_monthly_data = """  const activeStartMonth = selectedStartMonth || (months.length > 0 ? months[0] : '');
  const activeEndMonth = selectedEndMonth || (months.length > 0 ? months[0] : '');
  const activeMaterialMonth = materialMonth || (months.length > 0 ? months[0] : '');

  const monthlyCategoryData = useMemo(() => {
    if (!activeStartMonth || !activeEndMonth) return [];
    
    // Sort dates just in case start > end
    const sortedDates = [activeStartMonth, activeEndMonth].sort();
    const startDate = sortedDates[0];
    const endDate = sortedDates[1];

    let filtered = data.filter(d => 
      d.upload_date >= startDate && 
      d.upload_date <= endDate &&
      d.platform === selectedPlatform
    );

    const byCategory = {};
    filtered.forEach(row => {
      const cat = (!row.category || row.category === 'N/A') ? 'Uncategorized' : row.category;
      
      if (excludedCategories.length > 0 && excludedCategories.includes(cat)) return;
      
      if (!byCategory[cat]) {
        byCategory[cat] = {
          category: cat,
          views: 0,
          cart_adds: 0,
          purchases: 0,
          fis_users: 0,
        };
      }
      const c = byCategory[cat];
      c.views += row.views || 0;
      c.cart_adds += row.cart_adds || 0;
      c.purchases += row.purchases || 0;
      c.fis_users += row.fis_users || 0;
    });"""

content = content.replace(old_monthly_data, new_monthly_data)

# 5. UI dropdowns for table
old_filters = """              <div className="trends-filters" style={{ padding: '0.5rem 1rem' }}>
                <label>
                  <span>Month:</span>
                  <select 
                    value={activeMonthTable} 
                    onChange={(e) => setSelectedMonthTable(e.target.value)}
                    className="trends-select"
                  >
                    {months.map(m => <option key={m} value={m}>{m}</option>)}
                  </select>
                </label>
              </div>"""

new_filters = """              <div className="trends-filters" style={{ padding: '0.5rem 1rem', display: 'flex', gap: '1rem' }}>
                <label>
                  <span>Start Month:</span>
                  <select 
                    value={activeStartMonth} 
                    onChange={(e) => setSelectedStartMonth(e.target.value)}
                    className="trends-select"
                  >
                    {months.map(m => <option key={m} value={m}>{m}</option>)}
                  </select>
                </label>
                <label>
                  <span>End Month:</span>
                  <select 
                    value={activeEndMonth} 
                    onChange={(e) => setSelectedEndMonth(e.target.value)}
                    className="trends-select"
                  >
                    {months.map(m => <option key={m} value={m}>{m}</option>)}
                  </select>
                </label>
              </div>"""

content = content.replace(old_filters, new_filters)

# 6. Clickable table rows
old_tr = """                      {monthlyCategoryData.map((row, idx) => (
                        <tr key={idx}>
                          <td>{row.category}</td>"""

new_tr = """                      {monthlyCategoryData.map((row, idx) => (
                        <tr 
                          key={idx} 
                          style={{ cursor: 'pointer' }}
                          onClick={() => {
                            setDrillDownCategory(row.category);
                            setIsDrillDownOpen(true);
                          }}
                          className="clickable-row"
                        >
                          <td style={{ color: '#3b82f6', textDecoration: 'underline' }}>{row.category}</td>"""

content = content.replace(old_tr, new_tr)

# 7. Add DrillDownModal to render output
old_closing = """    </div>
  );
};"""

new_closing = """      <CategoryDrillDownModal 
        isOpen={isDrillDownOpen} 
        onClose={() => setIsDrillDownOpen(false)}
        category={drillDownCategory}
        platform={selectedPlatform}
        startDate={[activeStartMonth, activeEndMonth].sort()[0]}
        endDate={[activeStartMonth, activeEndMonth].sort()[1]}
      />
    </div>
  );
};"""

content = content.replace(old_closing, new_closing)

# Also fix the CSV download for category performance
content = content.replace(
    "`category_performance_${activeMonthTable || 'all'}.csv`",
    "`category_performance_${activeStartMonth}_to_${activeEndMonth}.csv`"
)

with open('src/components/TrendsDashboard.jsx', 'w') as f:
    f.write(content)
