import re

with open('src/components/CategoryDrillDownPage.css', 'r') as f:
    content = f.read()

# Replace modal overlay with page container
old_overlay = """.drilldown-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.75);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.drilldown-modal-content {
  background-color: #1a1a24;
  width: 95%;
  max-width: 1400px;
  height: 90vh;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  border: 1px solid #333;
}

.drilldown-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background-color: #2a2a36;
  border-bottom: 1px solid #333;
}

.drilldown-modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #fff;
}

.close-button {
  background: none;
  border: none;
  color: #a0aec0;
  font-size: 2rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.close-button:hover {
  color: #fff;
}

.drilldown-modal-body {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}"""

new_page = """.drilldown-page-container {
  min-height: 100vh;
  background-color: #1a1a24;
  color: #fff;
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.drilldown-page-content {
  width: 100%;
  max-width: 1400px;
  display: flex;
  flex-direction: column;
}

.drilldown-page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #333;
  margin-bottom: 2rem;
}

.drilldown-page-header h2 {
  margin: 0;
  font-size: 2rem;
  color: #fff;
}

.drilldown-page-body {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}"""

content = content.replace(old_overlay, new_page)

with open('src/components/CategoryDrillDownPage.css', 'w') as f:
    f.write(content)
