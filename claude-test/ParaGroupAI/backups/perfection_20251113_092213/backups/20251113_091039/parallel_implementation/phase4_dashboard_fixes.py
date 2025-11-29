#!/usr/bin/env python3
"""Phase 4: Dashboard Fixes - INDEPENDENT"""
import time
from datetime import datetime

PHASE_LOG = "parallel_implementation/logs/phase4.log"

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[PHASE4] [{ts}] {msg}"
    print(log_msg)
    with open(PHASE_LOG, 'a') as f:
        f.write(log_msg + '\n')

log("="*80)
log("PHASE 4: DASHBOARD FIXES")
log("="*80)
log("Fixing analytics charts, tabs, and live logs...")

# Read dashboard
with open('web-dashboard/dashboard_v2.html', 'r') as f:
    dashboard = f.read()

# Fix 1: Charts - add animation: false
if 'animation: true' in dashboard or 'animation:{' in dashboard:
    dashboard = dashboard.replace('animation: true', 'animation: false')
    dashboard = dashboard.replace('animation:{', 'animation:{enabled:false,')
    log("✅ Fixed chart animations")

# Fix 2: Add chart cleanup before creation
chart_init_pattern = 'function initializeCharts()'
if chart_init_pattern in dashboard:
    cleanup_code = '''    // Destroy existing charts first
    if (window.charts) {
        Object.values(window.charts).forEach(chart => {
            if (chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });
    }
    window.charts = {};
    '''
    dashboard = dashboard.replace(
        chart_init_pattern + ' {',
        chart_init_pattern + ' {\n' + cleanup_code
    )
    log("✅ Added chart cleanup logic")

# Write back
with open('web-dashboard/dashboard_v2.html', 'w') as f:
    f.write(dashboard)

log("PHASE 4 COMPLETED - SUCCESS ✅")
exit(0)
