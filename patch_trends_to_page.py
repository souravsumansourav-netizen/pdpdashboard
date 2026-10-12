import re

with open('src/components/TrendsDashboard.jsx', 'r') as f:
    content = f.read()

# 1. Remove import
content = content.replace("import { CategoryDrillDownModal } from './CategoryDrillDownModal';\n", "")

# 2. Remove states related to DrillDownModal
content = content.replace("const [drillDownCategory, setDrillDownCategory] = useState(null);\n  const [isDrillDownOpen, setIsDrillDownOpen] = useState(false);", "")

# 3. Change tr click logic
old_tr_click = """                        <tr 
                          key={idx} 
                          style={{ cursor: 'pointer' }}
                          onClick={() => {
                            setDrillDownCategory(row.category);
                            setIsDrillDownOpen(true);
                          }}
                          className="clickable-row"
                        >"""

new_tr_click = """                        <tr 
                          key={idx} 
                          style={{ cursor: 'pointer' }}
                          onClick={() => {
                            const url = `/category/${encodeURIComponent(row.category)}?start=${activeStartMonth}&end=${activeEndMonth}&platform=${selectedPlatform}`;
                            window.open(url, '_blank');
                          }}
                          className="clickable-row"
                        >"""

content = content.replace(old_tr_click, new_tr_click)

# 4. Remove Modal component rendering at the end
old_modal_render = """      <CategoryDrillDownModal 
        isOpen={isDrillDownOpen} 
        onClose={() => setIsDrillDownOpen(false)}
        category={drillDownCategory}
        platform={selectedPlatform}
        startDate={[activeStartMonth, activeEndMonth].sort()[0]}
        endDate={[activeStartMonth, activeEndMonth].sort()[1]}
      />"""

content = content.replace(old_modal_render, "")

with open('src/components/TrendsDashboard.jsx', 'w') as f:
    f.write(content)
