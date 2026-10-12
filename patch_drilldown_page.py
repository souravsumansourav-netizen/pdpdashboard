import re

with open('src/components/CategoryDrillDownPage.jsx', 'r') as f:
    content = f.read()

# 1. Imports and component declaration
old_imports = """import React, { useState, useEffect, useMemo } from 'react';
import { supabase } from '../config/supabaseClient';
import { formatPercent } from '../utils/formatters';
import './CategoryDrillDownModal.css';

export const CategoryDrillDownModal = ({ isOpen, onClose, category, platform, startDate, endDate }) => {"""

new_imports = """import React, { useState, useEffect, useMemo } from 'react';
import { useParams, useSearchParams, useNavigate } from 'react-router-dom';
import { supabase } from '../config/supabaseClient';
import { formatPercent } from '../utils/formatters';
import './CategoryDrillDownPage.css';

export const CategoryDrillDownPage = () => {
  const { categoryName } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  
  const category = categoryName ? decodeURIComponent(categoryName) : '';
  const platform = searchParams.get('platform') || 'combined';
  const startDate = searchParams.get('start') || '';
  const endDate = searchParams.get('end') || '';"""

content = content.replace(old_imports, new_imports)

# 2. Fix the initial fetch condition
content = content.replace(
    "if (!isOpen) return;",
    "if (!category) return;"
)
content = content.replace("[isOpen, category", "[category")

# 3. Add global sorting states and helpers
# Insert right after `const [activeLayer2, setActiveLayer2] = useState(null);`
old_state = "const [activeLayer2, setActiveLayer2] = useState(null);"
new_state = """const [activeLayer2, setActiveLayer2] = useState(null);

  // Sorting states for different tables
  const [sortConfigL2, setSortConfigL2] = useState({ key: 'views', direction: 'desc' });
  const [sortConfigUnderexposedCart, setSortConfigUnderexposedCart] = useState({ key: 'opp_score_cart', direction: 'desc' });
  const [sortConfigWastedCart, setSortConfigWastedCart] = useState({ key: 'opp_score_cart', direction: 'asc' });
  const [sortConfigUnderexposedFis, setSortConfigUnderexposedFis] = useState({ key: 'opp_score_fis', direction: 'desc' });
  const [sortConfigWastedFis, setSortConfigWastedFis] = useState({ key: 'opp_score_fis', direction: 'asc' });

  const getSortIndicator = (config, key) => {
    if (config.key !== key) return null;
    return config.direction === 'asc' ? ' ↑' : ' ↓';
  };

  const handleSort = (config, setConfig, key) => {
    let direction = 'desc';
    if (config.key === key && config.direction === 'desc') {
      direction = 'asc';
    }
    setConfig({ key, direction });
  };
  
  const applySort = (arr, config) => {
    return [...arr].sort((a, b) => {
      const aVal = a[config.key] ?? 0;
      const bVal = b[config.key] ?? 0;
      if (aVal < bVal) return config.direction === 'asc' ? -1 : 1;
      if (aVal > bVal) return config.direction === 'asc' ? 1 : -1;
      return 0;
    });
  };"""
content = content.replace(old_state, new_state)

# 4. Remove `if (!isOpen) return null;`
content = content.replace("if (!isOpen) return null;", "")

# 5. Fix HTML structure (remove modal overlay, add full-page styling)
old_return = """  return (
    <div className="drilldown-modal-overlay">
      <div className="drilldown-modal-content">
        <div className="drilldown-modal-header">
          <h2>Category Drill-Down: {category}</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        
        <div className="drilldown-modal-body">"""

new_return = """  return (
    <div className="drilldown-page-container">
      <div className="drilldown-page-content">
        <div className="drilldown-page-header">
          <h2>Category Drill-Down: {category}</h2>
          <button className="back-button" onClick={() => navigate(-1)} style={{ padding: '0.4rem 1rem', background: '#3b82f6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>← Back to Trends</button>
        </div>
        
        <div className="drilldown-page-body">"""
content = content.replace(old_return, new_return)

# 6. Apply sorting to memos
content = content.replace(
    ".sort((a, b) => b.opp_score_cart - a.opp_score_cart)\n               .slice(0, 50); // top 50 for sanity\n  }, [data]);",
    "// Sorting is applied dynamically at render time to allow table column clicks\n               ;\n  }, [data]);"
)
content = content.replace(
    ".sort((a, b) => a.opp_score_cart - b.opp_score_cart)\n               .slice(0, 50);\n  }, [data]);",
    ";\n  }, [data]);"
)
content = content.replace(
    ".sort((a, b) => b.opp_score_fis - a.opp_score_fis)\n               .slice(0, 50);\n  }, [data]);",
    ";\n  }, [data]);"
)
content = content.replace(
    ".sort((a, b) => a.opp_score_fis - b.opp_score_fis)\n               .slice(0, 50);\n  }, [data]);",
    ";\n  }, [data]);"
)

# Render variables with sorts applied
sort_render_vars = """
  const sortedLayer2 = useMemo(() => {
    if (!activeLayer2 || !concentrationSummary) return [];
    return applySort(concentrationSummary[activeLayer2].skus, sortConfigL2);
  }, [activeLayer2, concentrationSummary, sortConfigL2]);

  const sortedUnderexposedCart = useMemo(() => applySort(underexposedCart, sortConfigUnderexposedCart).slice(0, 50), [underexposedCart, sortConfigUnderexposedCart]);
  const sortedWastedViewsCart = useMemo(() => applySort(wastedViewsCart, sortConfigWastedCart).slice(0, 50), [wastedViewsCart, sortConfigWastedCart]);
  const sortedUnderexposedFis = useMemo(() => applySort(underexposedFis, sortConfigUnderexposedFis).slice(0, 50), [underexposedFis, sortConfigUnderexposedFis]);
  const sortedWastedViewsFis = useMemo(() => applySort(wastedViewsFis, sortConfigWastedFis).slice(0, 50), [wastedViewsFis, sortConfigWastedFis]);
"""
content = content.replace(
    "return (\n    <div className=\"drilldown-page-container\">",
    sort_render_vars + "\n  return (\n    <div className=\"drilldown-page-container\">"
)

# 7. Update Tables HTML for Layer 2
old_l2_thead = """                      <thead>
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
                        {concentrationSummary[activeLayer2].skus.map(row => ("""

new_l2_thead = """                      <thead>
                        <tr>
                          <th onClick={() => handleSort(sortConfigL2, setSortConfigL2, 'base_sku')} style={{cursor:'pointer', userSelect:'none'}}>Product ID{getSortIndicator(sortConfigL2, 'base_sku')}</th>
                          <th onClick={() => handleSort(sortConfigL2, setSortConfigL2, 'product_name')} style={{cursor:'pointer', userSelect:'none'}}>Product Name{getSortIndicator(sortConfigL2, 'product_name')}</th>
                          <th onClick={() => handleSort(sortConfigL2, setSortConfigL2, 'views')} style={{cursor:'pointer', userSelect:'none'}}>Views{getSortIndicator(sortConfigL2, 'views')}</th>
                          <th onClick={() => handleSort(sortConfigL2, setSortConfigL2, 'cart_adds')} style={{cursor:'pointer', userSelect:'none'}}>Cart Adds{getSortIndicator(sortConfigL2, 'cart_adds')}</th>
                          <th onClick={() => handleSort(sortConfigL2, setSortConfigL2, 'purchases')} style={{cursor:'pointer', userSelect:'none'}}>Purchases{getSortIndicator(sortConfigL2, 'purchases')}</th>
                          <th onClick={() => handleSort(sortConfigL2, setSortConfigL2, 'fis_users')} style={{cursor:'pointer', userSelect:'none'}}>FIS Users{getSortIndicator(sortConfigL2, 'fis_users')}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {sortedLayer2.map(row => ("""
content = content.replace(old_l2_thead, new_l2_thead)

# 8. Underexposed Cart
old_ucart = """                  <table className="trends-table">
                    <thead>
                      <tr>
                        <th>Product ID</th>
                        <th>Product Name</th>
                        <th>Views</th>
                        <th>Cart Adds</th>
                        <th>FIS Users</th>
                        <th>Wilson Adj. Rate</th>
                        <th>Opp Score</th>
                      </tr>
                    </thead>
                    <tbody>
                      {underexposedCart.map(row => ("""

new_ucart = """                  <table className="trends-table">
                    <thead>
                      <tr>
                        <th onClick={() => handleSort(sortConfigUnderexposedCart, setSortConfigUnderexposedCart, 'base_sku')} style={{cursor:'pointer', userSelect:'none'}}>Product ID{getSortIndicator(sortConfigUnderexposedCart, 'base_sku')}</th>
                        <th onClick={() => handleSort(sortConfigUnderexposedCart, setSortConfigUnderexposedCart, 'product_name')} style={{cursor:'pointer', userSelect:'none'}}>Product Name{getSortIndicator(sortConfigUnderexposedCart, 'product_name')}</th>
                        <th onClick={() => handleSort(sortConfigUnderexposedCart, setSortConfigUnderexposedCart, 'views')} style={{cursor:'pointer', userSelect:'none'}}>Views{getSortIndicator(sortConfigUnderexposedCart, 'views')}</th>
                        <th onClick={() => handleSort(sortConfigUnderexposedCart, setSortConfigUnderexposedCart, 'cart_adds')} style={{cursor:'pointer', userSelect:'none'}}>Cart Adds{getSortIndicator(sortConfigUnderexposedCart, 'cart_adds')}</th>
                        <th onClick={() => handleSort(sortConfigUnderexposedCart, setSortConfigUnderexposedCart, 'fis_users')} style={{cursor:'pointer', userSelect:'none'}}>FIS Users{getSortIndicator(sortConfigUnderexposedCart, 'fis_users')}</th>
                        <th onClick={() => handleSort(sortConfigUnderexposedCart, setSortConfigUnderexposedCart, 'wilson_cart_rate')} style={{cursor:'pointer', userSelect:'none'}}>Wilson Adj. Rate{getSortIndicator(sortConfigUnderexposedCart, 'wilson_cart_rate')}</th>
                        <th onClick={() => handleSort(sortConfigUnderexposedCart, setSortConfigUnderexposedCart, 'opp_score_cart')} style={{cursor:'pointer', userSelect:'none'}}>Opp Score{getSortIndicator(sortConfigUnderexposedCart, 'opp_score_cart')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {sortedUnderexposedCart.map(row => ("""
content = content.replace(old_ucart, new_ucart)

# 9. Wasted Cart
old_wcart = """                  <table className="trends-table">
                    <thead>
                      <tr>
                        <th>Product ID</th>
                        <th>Product Name</th>
                        <th>Views</th>
                        <th>Cart Adds</th>
                        <th>FIS Users</th>
                        <th>Wilson Adj. Rate</th>
                        <th>Opp Score</th>
                      </tr>
                    </thead>
                    <tbody>
                      {wastedViewsCart.map(row => ("""
new_wcart = """                  <table className="trends-table">
                    <thead>
                      <tr>
                        <th onClick={() => handleSort(sortConfigWastedCart, setSortConfigWastedCart, 'base_sku')} style={{cursor:'pointer', userSelect:'none'}}>Product ID{getSortIndicator(sortConfigWastedCart, 'base_sku')}</th>
                        <th onClick={() => handleSort(sortConfigWastedCart, setSortConfigWastedCart, 'product_name')} style={{cursor:'pointer', userSelect:'none'}}>Product Name{getSortIndicator(sortConfigWastedCart, 'product_name')}</th>
                        <th onClick={() => handleSort(sortConfigWastedCart, setSortConfigWastedCart, 'views')} style={{cursor:'pointer', userSelect:'none'}}>Views{getSortIndicator(sortConfigWastedCart, 'views')}</th>
                        <th onClick={() => handleSort(sortConfigWastedCart, setSortConfigWastedCart, 'cart_adds')} style={{cursor:'pointer', userSelect:'none'}}>Cart Adds{getSortIndicator(sortConfigWastedCart, 'cart_adds')}</th>
                        <th onClick={() => handleSort(sortConfigWastedCart, setSortConfigWastedCart, 'fis_users')} style={{cursor:'pointer', userSelect:'none'}}>FIS Users{getSortIndicator(sortConfigWastedCart, 'fis_users')}</th>
                        <th onClick={() => handleSort(sortConfigWastedCart, setSortConfigWastedCart, 'wilson_cart_rate')} style={{cursor:'pointer', userSelect:'none'}}>Wilson Adj. Rate{getSortIndicator(sortConfigWastedCart, 'wilson_cart_rate')}</th>
                        <th onClick={() => handleSort(sortConfigWastedCart, setSortConfigWastedCart, 'opp_score_cart')} style={{cursor:'pointer', userSelect:'none'}}>Opp Score{getSortIndicator(sortConfigWastedCart, 'opp_score_cart')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {sortedWastedViewsCart.map(row => ("""
content = content.replace(old_wcart, new_wcart)

# 10. Underexposed FIS
old_ufis = """                  <table className="trends-table">
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
                      {underexposedFis.map(row => ("""
new_ufis = """                  <table className="trends-table">
                    <thead>
                      <tr>
                        <th onClick={() => handleSort(sortConfigUnderexposedFis, setSortConfigUnderexposedFis, 'base_sku')} style={{cursor:'pointer', userSelect:'none'}}>Product ID{getSortIndicator(sortConfigUnderexposedFis, 'base_sku')}</th>
                        <th onClick={() => handleSort(sortConfigUnderexposedFis, setSortConfigUnderexposedFis, 'product_name')} style={{cursor:'pointer', userSelect:'none'}}>Product Name{getSortIndicator(sortConfigUnderexposedFis, 'product_name')}</th>
                        <th onClick={() => handleSort(sortConfigUnderexposedFis, setSortConfigUnderexposedFis, 'views')} style={{cursor:'pointer', userSelect:'none'}}>Views{getSortIndicator(sortConfigUnderexposedFis, 'views')}</th>
                        <th onClick={() => handleSort(sortConfigUnderexposedFis, setSortConfigUnderexposedFis, 'fis_users')} style={{cursor:'pointer', userSelect:'none'}}>FIS Users{getSortIndicator(sortConfigUnderexposedFis, 'fis_users')}</th>
                        <th onClick={() => handleSort(sortConfigUnderexposedFis, setSortConfigUnderexposedFis, 'wilson_fis_rate')} style={{cursor:'pointer', userSelect:'none'}}>Wilson Adj. Rate{getSortIndicator(sortConfigUnderexposedFis, 'wilson_fis_rate')}</th>
                        <th onClick={() => handleSort(sortConfigUnderexposedFis, setSortConfigUnderexposedFis, 'opp_score_fis')} style={{cursor:'pointer', userSelect:'none'}}>Opp Score{getSortIndicator(sortConfigUnderexposedFis, 'opp_score_fis')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {sortedUnderexposedFis.map(row => ("""
content = content.replace(old_ufis, new_ufis)

# 11. Wasted FIS
old_wfis = """                  <table className="trends-table">
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
                      {wastedViewsFis.map(row => ("""
new_wfis = """                  <table className="trends-table">
                    <thead>
                      <tr>
                        <th onClick={() => handleSort(sortConfigWastedFis, setSortConfigWastedFis, 'base_sku')} style={{cursor:'pointer', userSelect:'none'}}>Product ID{getSortIndicator(sortConfigWastedFis, 'base_sku')}</th>
                        <th onClick={() => handleSort(sortConfigWastedFis, setSortConfigWastedFis, 'product_name')} style={{cursor:'pointer', userSelect:'none'}}>Product Name{getSortIndicator(sortConfigWastedFis, 'product_name')}</th>
                        <th onClick={() => handleSort(sortConfigWastedFis, setSortConfigWastedFis, 'views')} style={{cursor:'pointer', userSelect:'none'}}>Views{getSortIndicator(sortConfigWastedFis, 'views')}</th>
                        <th onClick={() => handleSort(sortConfigWastedFis, setSortConfigWastedFis, 'fis_users')} style={{cursor:'pointer', userSelect:'none'}}>FIS Users{getSortIndicator(sortConfigWastedFis, 'fis_users')}</th>
                        <th onClick={() => handleSort(sortConfigWastedFis, setSortConfigWastedFis, 'wilson_fis_rate')} style={{cursor:'pointer', userSelect:'none'}}>Wilson Adj. Rate{getSortIndicator(sortConfigWastedFis, 'wilson_fis_rate')}</th>
                        <th onClick={() => handleSort(sortConfigWastedFis, setSortConfigWastedFis, 'opp_score_fis')} style={{cursor:'pointer', userSelect:'none'}}>Opp Score{getSortIndicator(sortConfigWastedFis, 'opp_score_fis')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {sortedWastedViewsFis.map(row => ("""
content = content.replace(old_wfis, new_wfis)

with open('src/components/CategoryDrillDownPage.jsx', 'w') as f:
    f.write(content)
