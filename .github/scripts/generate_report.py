#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json
import re
import os
from datetime import datetime

def get_description(name):
    desc_map = {
        'AuthCommandTest': 'User authentication validation',
        'CreateCommandTest': 'File creation operations',
        'WriteCommandTest': 'File write operations',
        'ReadCommandTest': 'File read operations',
        'AppendCommandTest': 'File append operations',
        'DeleteCommandTest': 'File deletion operations',
        'RenameCommandTest': 'File rename operations',
        'ListCommandTest': 'Directory listing operations',
        'InfoCommandTest': 'File information retrieval',
        'CpuLoadCommandTest': 'CPU load monitoring',
    }
    return desc_map.get(name, name + ' test suite')

def parse_xml():
    tree = ET.parse('test_results/results.xml')
    root = tree.getroot()
    test_suites = []
    chart_labels = []
    chart_passed = []
    chart_failed = []
    for testsuite in root.findall('.//testsuite'):
        name = testsuite.get('name', 'Unknown')
        tests = int(testsuite.get('tests', 0))
        failures = int(testsuite.get('failures', 0))
        errors = int(testsuite.get('errors', 0))
        passed = tests - failures - errors
        test_cases = []
        for testcase in testsuite.findall('testcase'):
            tc_name = testcase.get('name', 'Unknown')
            tc_status = 'FAILED' if testcase.find('failure') is not None else 'PASSED'
            test_cases.append({'name': tc_name, 'status': tc_status})
        status = 'PASSED' if failures == 0 and errors == 0 else 'FAILED'
        test_suites.append({
            'name': name,
            'description': get_description(name),
            'tests': tests,
            'passed': passed,
            'failed': failures + errors,
            'status': status,
            'test_cases': test_cases
        })
        short_name = name.replace('CommandTest', '').replace('Test', '')
        chart_labels.append(short_name)
        chart_passed.append(passed)
        chart_failed.append(failures + errors)
    return {
        'test_suites': test_suites,
        'chart_labels': chart_labels,
        'chart_passed': chart_passed,
        'chart_failed': chart_failed,
        'total_suites': len(test_suites)
    }

def parse_text():
    with open('test_output.txt', 'r') as f:
        content = f.read()
    test_suites = []
    chart_labels = []
    chart_passed = []
    chart_failed = []
    suite_pat = r'
$$
----------
$$ \d+ tests? from (\w+)'
    suites = re.findall(suite_pat, content)
    suites = list(dict.fromkeys(suites))
    for suite_name in suites:
        run_pat = r'
$$
 RUN      
$$ ' + suite_name + r'\.(\w+)'
        ok_pat = r'
$$
       OK 
$$ ' + suite_name + r'\.(\w+)'
        fail_pat = r'
$$
  FAILED  
$$ ' + suite_name + r'\.(\w+)'
        runs = re.findall(run_pat, content)
        oks = re.findall(ok_pat, content)
        fails = re.findall(fail_pat, content)
        passed = len(oks)
        failed = len(fails)
        total = len(runs) if runs else passed + failed
        status = 'PASSED' if failed == 0 else 'FAILED'
        test_cases = []
        for tc in runs:
            tc_status = 'PASSED' if tc in oks else 'FAILED'
            test_cases.append({'name': tc, 'status': tc_status})
        test_suites.append({
            'name': suite_name,
            'description': get_description(suite_name),
            'tests': total,
            'passed': passed,
            'failed': failed,
            'status': status,
            'test_cases': test_cases
        })
        short_name = suite_name.replace('CommandTest', '').replace('Test', '')
        chart_labels.append(short_name)
        chart_passed.append(passed)
        chart_failed.append(failed)
    return {
        'test_suites': test_suites,
        'chart_labels': chart_labels,
        'chart_passed': chart_passed,
        'chart_failed': chart_failed,
        'total_suites': len(test_suites)
    }

def generate_html(test_data, lp, fp, lc, lt, fc, ft, gp, gf, gt):
    nc = round(100 - lp, 1)
    cd = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    fcls = 'metric-bad' if gf > 0 else 'metric-good'
    shtml = ''
    for i, s in enumerate(test_data['test_suites']):
        scls = 'status-passed' if s['status'] == 'PASSED' else 'status-failed'
        shtml += '<tr class="expandable" onclick="toggleDetails(' + str(i) + ')">'
        shtml += '<td><span class="toggle-icon" id="icon-' + str(i) + '">[+]</span>' + s['name'] + '</td>'
        shtml += '<td>' + s['description'] + '</td>'
        shtml += '<td style="text-align:center;">' + str(s['passed']) + '/' + str(s['tests']) + '</td>'
        shtml += '<td style="text-align:center;" class="' + scls + '">' + s['status'] + '</td></tr>'
        tchtml = '<ul class="test-case-list">'
        for tc in s['test_cases']:
            tccls = 'status-passed' if tc['status'] == 'PASSED' else 'status-failed'
            tchtml += '<li><span class="' + tccls + '">[' + tc['status'] + ']</span> ' + tc['name'] + '</li>'
        tchtml += '</ul>'
        shtml += '<tr id="details-' + str(i) + '" class="test-details"><td colspan="4">' + tchtml + '</td></tr>'
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ClientServerSystem - CI Report</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body{font-family:Arial,sans-serif;background:#f9f9f9;margin:40px}
h1,h2,h3,h4{color:#2c3e50}
.section{background:#fff;padding:20px;margin-bottom:25px;border-radius:6px;box-shadow:0 0 6px rgba(0,0,0,.1)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:30px}
canvas{max-width:100%;height:300px!important}
.footer{color:#777;font-size:.9em;margin-top:30px}
.metrics{font-size:1.1em;margin-bottom:20px}
.metrics p{margin:8px 0}
.metric-value{font-weight:bold}
.metric-good{color:#27ae60}
.metric-bad{color:#e74c3c}
.summary-box{display:inline-block;padding:15px 25px;margin:10px;background:#ecf0f1;border-radius:8px;text-align:center}
.summary-box .value{font-size:2em;font-weight:bold;color:#2c3e50}
.summary-box .label{font-size:0.9em;color:#7f8c8d}
.feature-list{columns:2;column-gap:40px}
.feature-list li{margin-bottom:8px}
.tech-badge{display:inline-block;padding:5px 12px;margin:4px;background:#3498db;color:white;border-radius:15px;font-size:0.9em}
.architecture-diagram{background:#f8f9fa;padding:20px;border-radius:8px;text-align:center;margin:20px 0}
.arch-box{display:inline-block;padding:15px 25px;margin:10px;background:#3498db;color:white;border-radius:8px;min-width:120px}
.arch-box.client{background:#9b59b6}
.arch-box.server{background:#27ae60}
.arch-box.common{background:#e67e22}
.arch-arrow{font-size:2em;color:#7f8c8d;margin:0 10px}
pre{background:#2c3e50;color:#ecf0f1;padding:15px;border-radius:6px;overflow-x:auto}
table{width:100%;border-collapse:collapse;margin-top:15px}
th{background:#3498db;color:white;padding:12px;text-align:left}
td{padding:10px;border-bottom:1px solid #ddd}
.status-passed{color:#27ae60;font-weight:bold}
.status-failed{color:#e74c3c;font-weight:bold}
.test-case-list{margin:5px 0;padding-left:20px;font-size:0.9em;color:#666}
.expandable{cursor:pointer}
.expandable:hover{background:#e8f4f8}
.test-details{display:none;background:#f8f9fa}
.test-details.show{display:table-row}
.toggle-icon{margin-right:8px}
</style>
</head>
<body>
<h1>ClientServerSystem</h1>
<h2>CI, Testing and Coverage Report</h2>
<div class="section">
<h3>Author Information</h3>
<p><strong>Name:</strong> Mohamed Waaer</p>
<p><strong>Email:</strong> mohamed.waer@coretech-innovations.com</p>
</div>
<div class="section">
<h3>Project Overview</h3>
<p><strong>ClientServerSystem</strong> is a robust Qt6-based client-server application for file management and system monitoring.</p>
<h4>Key Features</h4>
<ul class="feature-list">
<li><strong>File Operations:</strong> Create, Read, Write, Append, Delete, Rename</li>
<li><strong>Directory Management:</strong> List files and directories</li>
<li><strong>File Information:</strong> Retrieve detailed file metadata</li>
<li><strong>System Monitoring:</strong> Real-time CPU load monitoring</li>
<li><strong>Authentication:</strong> Secure user authentication system</li>
<li><strong>Command Parser:</strong> Flexible command parsing</li>
<li><strong>Path Validation:</strong> Secure path handling</li>
<li><strong>Response Handling:</strong> Structured response formatting</li>
</ul>
<h4>Architecture</h4>
<div class="architecture-diagram">
<div class="arch-box client">Client</div>
<span class="arch-arrow">&#8596;</span>
<div class="arch-box common">Common</div>
<span class="arch-arrow">&#8596;</span>
<div class="arch-box server">Server</div>
</div>
<h4>Technology Stack</h4>
<div><span class="tech-badge">C++17</span><span class="tech-badge">Qt 6.4</span><span class="tech-badge">GoogleTest</span><span class="tech-badge">CMake</span><span class="tech-badge">lcov</span><span class="tech-badge">GitHub Actions</span></div>
</div>
<div class="section">
<h3>Summary</h3>
<div style="text-align:center">
<div class="summary-box"><div class="value">__LP__%</div><div class="label">Line Coverage</div></div>
<div class="summary-box"><div class="value">__FP__%</div><div class="label">Function Coverage</div></div>
<div class="summary-box"><div class="value">__GP__/__GT__</div><div class="label">Tests Passed</div></div>
<div class="summary-box"><div class="value">__TS__</div><div class="label">Test Suites</div></div>
</div>
</div>
<div class="section">
<h3>Test Coverage Metrics</h3>
<div class="metrics">
<p>Line Coverage: <span class="metric-value">__LP__% (__LC__ of __LT__ lines)</span></p>
<p>Function Coverage: <span class="metric-value">__FP__% (__FC__ of __FT__ functions)</span></p>
</div>
<div class="grid"><div><canvas id="coveragePie"></canvas></div><div><canvas id="coverageBar"></canvas></div></div>
</div>
<div class="section">
<h3>Test Results</h3>
<div class="metrics">
<p>Total: <span class="metric-value">__GT__</span></p>
<p>Passed: <span class="metric-value metric-good">__GP__</span></p>
<p>Failed: <span class="metric-value __FCLS__">__GF__</span></p>
</div>
<h4>Test Suites (Click to expand)</h4>
<table><thead><tr><th>Test Suite</th><th>Description</th><th style="text-align:center">Tests</th><th style="text-align:center">Status</th></tr></thead>
<tbody>__SHTML__</tbody></table>
<div class="grid" style="margin-top:25px"><div><canvas id="testsPie"></canvas></div><div><canvas id="testsBar"></canvas></div></div>
</div>
<div class="section">
<h3>Build Information</h3>
<table>
<tr><td><strong>Build System</strong></td><td>QMake/CMake</td></tr>
<tr><td><strong>Compiler</strong></td><td>GCC 13.x</td></tr>
<tr><td><strong>Qt Version</strong></td><td>Qt 6.4.2</td></tr>
<tr><td><strong>Test Framework</strong></td><td>GoogleTest</td></tr>
<tr><td><strong>Coverage Tool</strong></td><td>lcov/gcov</td></tr>
<tr><td><strong>CI Platform</strong></td><td>GitHub Actions</td></tr>
<tr><td><strong>Platform</strong></td><td>Ubuntu 24.04</td></tr>
<tr><td><strong>Generated</strong></td><td>__CD__</td></tr>
</table>
</div>
<script>
var testData=__TD__;
var linePercent=__LPJ__;
var funcPercent=__FPJ__;
var notCovered=__NC__;
var gtestPassed=__GPJ__;
var gtestFailed=__GFJ__;
function toggleDetails(i){var d=document.getElementById('details-'+i);d.classList.toggle('show');var ic=document.getElementById('icon-'+i);ic.textContent=d.classList.contains('show')?'[-]':'[+]';}
new Chart(document.getElementById('coveragePie'),{type:'pie',data:{labels:['Covered ('+linePercent.toFixed(1)+'%)','Not Covered ('+notCovered.toFixed(1)+'%)'],datasets:[{data:[linePercent,notCovered],backgroundColor:['#4DD0E1','#FF9F40']}]},options:{responsive:true,plugins:{title:{display:true,text:'Line Coverage'},legend:{position:'bottom'}}}});
new Chart(document.getElementById('coverageBar'),{type:'bar',data:{labels:['Line','Function'],datasets:[{label:'Coverage',data:[linePercent,funcPercent],backgroundColor:['#4DD0E1','#36A2EB']}]},options:{responsive:true,plugins:{title:{display:true,text:'Coverage by Type'}},scales:{y:{beginAtZero:true,max:100}}}});
new Chart(document.getElementById('testsPie'),{type:'doughnut',data:{labels:['Passed ('+gtestPassed+')','Failed ('+gtestFailed+')'],datasets:[{data:[gtestPassed,Math.max(gtestFailed,0.1)],backgroundColor:['#4BC0C0','#FF6384']}]},options:{responsive:true,plugins:{title:{display:true,text:'Test Results'},legend:{position:'bottom'}}}});
new Chart(document.getElementById('testsBar'),{type:'bar',data:{labels:testData.chart_labels,datasets:[{label:'Passed',data:testData.chart_passed,backgroundColor:'#4BC0C0'},{label:'Failed',data:testData.chart_failed,backgroundColor:'#FF6384'}]},options:{responsive:true,plugins:{title:{display:true,text:'Tests by Suite'}},scales:{x:{stacked:true},y:{stacked:true,beginAtZero:true}}}});
</script>
<div class="footer"><p>Generated by GitHub Actions CI</p></div>
</body>
</html>'''
    html = html.replace('__LP__', str(round(lp, 1)))
    html = html.replace('__FP__', str(round(fp, 1)))
    html = html.replace('__LC__', str(lc))
    html = html.replace('__LT__', str(lt))
    html = html.replace('__FC__', str(fc))
    html = html.replace('__FT__', str(ft))
    html = html.replace('__GP__', str(gp))
    html = html.replace('__GF__', str(gf))
    html = html.replace('__GT__', str(gt))
    html = html.replace('__TS__', str(test_data['total_suites']))
    html = html.replace('__FCLS__', fcls)
    html = html.replace('__CD__', cd)
    html = html.replace('__SHTML__', shtml)
    html = html.replace('__TD__', json.dumps(test_data))
    html = html.replace('__LPJ__', str(lp))
    html = html.replace('__FPJ__', str(fp))
    html = html.replace('__NC__', str(nc))
    html = html.replace('__GPJ__', str(gp))
    html = html.replace('__GFJ__', str(gf))
    return html

def main():
    if os.path.exists('test_results/results.xml'):
        print('Parsing XML...')
        test_data = parse_xml()
    else:
        print('Parsing text...')
        test_data = parse_text()
    lp = float(os.environ.get('LINE_PERCENT', '0'))
    fp = float(os.environ.get('FUNC_PERCENT', '0'))
    lc = os.environ.get('LINES_COVERED', '0')
    lt = os.environ.get('LINES_TOTAL', '0')
    fc = os.environ.get('FUNCS_COVERED', '0')
    ft = os.environ.get('FUNCS_TOTAL', '0')
    gp = int(os.environ.get('GTEST_PASSED', '0'))
    gf = int(os.environ.get('GTEST_FAILED', '0'))
    gt = int(os.environ.get('GTEST_TOTAL', '0'))
    html = generate_html(test_data, lp, fp, lc, lt, fc, ft, gp, gf, gt)
    with open('REPORT.html', 'w') as f:
        f.write(html)
    print('Report generated!')
    print('Line Coverage: ' + str(lp) + '%')
    print('Function Coverage: ' + str(fp) + '%')
    print('Tests: ' + str(gp) + '/' + str(gt))

if __name__ == '__main__':
    main()
