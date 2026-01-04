#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json
import re
import os
from datetime import datetime

DESC_MAP = {
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

def get_desc(name):
    return DESC_MAP.get(name, name + ' test suite')

def parse_xml():
    tree = ET.parse('test_results/results.xml')
    root = tree.getroot()
    suites, labels, passed_list, failed_list = [], [], [], []
    for ts in root.findall('.//testsuite'):
        name = ts.get('name', 'Unknown')
        tests = int(ts.get('tests', 0))
        fail = int(ts.get('failures', 0)) + int(ts.get('errors', 0))
        pas = tests - fail
        cases = []
        for tc in ts.findall('testcase'):
            tcn = tc.get('name', 'Unknown')
            tcs = 'FAILED' if tc.find('failure') is not None else 'PASSED'
            cases.append({'name': tcn, 'status': tcs})
        suites.append({'name': name, 'description': get_desc(name), 'tests': tests, 'passed': pas, 'failed': fail, 'status': 'PASSED' if fail == 0 else 'FAILED', 'test_cases': cases})
        labels.append(name.replace('CommandTest', '').replace('Test', ''))
        passed_list.append(pas)
        failed_list.append(fail)
    return {'test_suites': suites, 'chart_labels': labels, 'chart_passed': passed_list, 'chart_failed': failed_list, 'total_suites': len(suites)}

def parse_text():
    with open('test_output.txt', 'r') as f:
        txt = f.read()
    suites, labels, passed_list, failed_list = [], [], [], []
    # Find suite names
    for line in txt.split('\n'):
        if '[----------]' in line and 'from' in line:
            parts = line.split('from')
            if len(parts) > 1:
                sname = parts[1].strip().split()[0] if parts[1].strip() else None
                if sname and sname not in [s['name'] for s in suites]:
                    # Count tests for this suite
                    cases = []
                    pas, fail = 0, 0
                    for l2 in txt.split('\n'):
                        if '[ RUN      ]' in l2 and sname + '.' in l2:
                            tcname = l2.split(sname + '.')[1].strip() if sname + '.' in l2 else 'Unknown'
                            cases.append({'name': tcname, 'status': 'PASSED'})
                        if '[       OK ]' in l2 and sname + '.' in l2:
                            pas += 1
                        if '[  FAILED  ]' in l2 and sname + '.' in l2:
                            fail += 1
                            for c in cases:
                                tcn = l2.split(sname + '.')[1].strip().split()[0] if sname + '.' in l2 else ''
                                if c['name'] == tcn:
                                    c['status'] = 'FAILED'
                    total = pas + fail
                    suites.append({'name': sname, 'description': get_desc(sname), 'tests': total, 'passed': pas, 'failed': fail, 'status': 'PASSED' if fail == 0 else 'FAILED', 'test_cases': cases})
                    labels.append(sname.replace('CommandTest', '').replace('Test', ''))
                    passed_list.append(pas)
                    failed_list.append(fail)
    return {'test_suites': suites, 'chart_labels': labels, 'chart_passed': passed_list, 'chart_failed': failed_list, 'total_suites': len(suites)}

def gen_html(td, lp, fp, lc, lt, fc, ft, gp, gf, gt):
    nc = round(100 - lp, 1)
    dt = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    fcls = 'metric-bad' if gf > 0 else 'metric-good'
    rows = ''
    for i, s in enumerate(td['test_suites']):
        sc = 'status-passed' if s['status'] == 'PASSED' else 'status-failed'
        rows += '<tr class="expandable" onclick="toggleDetails(' + str(i) + ')"><td><span class="toggle-icon" id="icon-' + str(i) + '">[+]</span>' + s['name'] + '</td><td>' + s['description'] + '</td><td style="text-align:center">' + str(s['passed']) + '/' + str(s['tests']) + '</td><td style="text-align:center" class="' + sc + '">' + s['status'] + '</td></tr>'
        tcl = '<ul class="tcl">'
        for tc in s['test_cases']:
            tcc = 'status-passed' if tc['status'] == 'PASSED' else 'status-failed'
            tcl += '<li><span class="' + tcc + '">[' + tc['status'] + ']</span> ' + tc['name'] + '</li>'
        tcl += '</ul>'
        rows += '<tr id="details-' + str(i) + '" class="test-details"><td colspan="4">' + tcl + '</td></tr>'
    
    h = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>CI Report</title>'
    h += '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
    h += '<style>'
    h += 'body{font-family:Arial,sans-serif;background:#f9f9f9;margin:40px}'
    h += 'h1,h2,h3,h4{color:#2c3e50}'
    h += '.section{background:#fff;padding:20px;margin-bottom:25px;border-radius:6px;box-shadow:0 0 6px rgba(0,0,0,.1)}'
    h += '.grid{display:grid;grid-template-columns:1fr 1fr;gap:30px}'
    h += 'canvas{max-width:100%;height:300px!important}'
    h += '.metrics{font-size:1.1em;margin-bottom:20px}'
    h += '.metrics p{margin:8px 0}'
    h += '.metric-value{font-weight:bold}'
    h += '.metric-good{color:#27ae60}'
    h += '.metric-bad{color:#e74c3c}'
    h += '.summary-box{display:inline-block;padding:15px 25px;margin:10px;background:#ecf0f1;border-radius:8px;text-align:center}'
    h += '.summary-box .value{font-size:2em;font-weight:bold;color:#2c3e50}'
    h += '.summary-box .label{font-size:0.9em;color:#7f8c8d}'
    h += '.feature-list{columns:2;column-gap:40px}'
    h += '.feature-list li{margin-bottom:8px}'
    h += '.tech-badge{display:inline-block;padding:5px 12px;margin:4px;background:#3498db;color:white;border-radius:15px;font-size:0.9em}'
    h += '.arch-diagram{background:#f8f9fa;padding:20px;border-radius:8px;text-align:center;margin:20px 0}'
    h += '.arch-box{display:inline-block;padding:15px 25px;margin:10px;color:white;border-radius:8px;min-width:120px}'
    h += '.arch-client{background:#9b59b6}'
    h += '.arch-server{background:#27ae60}'
    h += '.arch-common{background:#e67e22}'
    h += '.arch-arrow{font-size:2em;color:#7f8c8d;margin:0 10px}'
    h += 'table{width:100%;border-collapse:collapse;margin-top:15px}'
    h += 'th{background:#3498db;color:white;padding:12px;text-align:left}'
    h += 'td{padding:10px;border-bottom:1px solid #ddd}'
    h += '.status-passed{color:#27ae60;font-weight:bold}'
    h += '.status-failed{color:#e74c3c;font-weight:bold}'
    h += '.tcl{margin:5px 0;padding-left:20px;font-size:0.9em;color:#666}'
    h += '.expandable{cursor:pointer}'
    h += '.expandable:hover{background:#e8f4f8}'
    h += '.test-details{display:none;background:#f8f9fa}'
    h += '.test-details.show{display:table-row}'
    h += '.toggle-icon{margin-right:8px}'
    h += '.footer{color:#777;font-size:.9em;margin-top:30px}'
    h += '</style></head><body>'
    
    h += '<h1>ClientServerSystem</h1>'
    h += '<h2>CI, Testing and Coverage Report</h2>'
    
    h += '<div class="section"><h3>Author</h3>'
    h += '<p><strong>Name:</strong> Mohamed Waaer</p>'
    h += '<p><strong>Email:</strong> mohamed.waer@coretech-innovations.com</p></div>'
    
    h += '<div class="section"><h3>Project Overview</h3>'
    h += '<p><strong>ClientServerSystem</strong> is a Qt6-based client-server application for file management and system monitoring.</p>'
    h += '<h4>Key Features</h4><ul class="feature-list">'
    h += '<li><strong>File Operations:</strong> Create, Read, Write, Append, Delete, Rename</li>'
    h += '<li><strong>Directory Management:</strong> List files and directories</li>'
    h += '<li><strong>File Information:</strong> Retrieve file metadata</li>'
    h += '<li><strong>System Monitoring:</strong> CPU load monitoring</li>'
    h += '<li><strong>Authentication:</strong> Secure user authentication</li>'
    h += '<li><strong>Command Parser:</strong> Flexible command parsing</li>'
    h += '<li><strong>Path Validation:</strong> Secure path handling</li>'
    h += '<li><strong>Response Handling:</strong> Structured responses</li>'
    h += '</ul>'
    h += '<h4>Architecture</h4>'
    h += '<div class="arch-diagram">'
    h += '<div class="arch-box arch-client">Client</div>'
    h += '<span class="arch-arrow">&#8596;</span>'
    h += '<div class="arch-box arch-common">Common</div>'
    h += '<span class="arch-arrow">&#8596;</span>'
    h += '<div class="arch-box arch-server">Server</div>'
    h += '</div>'
    h += '<h4>Technology Stack</h4><div>'
    h += '<span class="tech-badge">C++17</span>'
    h += '<span class="tech-badge">Qt 6.4</span>'
    h += '<span class="tech-badge">GoogleTest</span>'
    h += '<span class="tech-badge">CMake</span>'
    h += '<span class="tech-badge">lcov</span>'
    h += '<span class="tech-badge">GitHub Actions</span>'
    h += '</div></div>'
    
    h += '<div class="section"><h3>Summary</h3><div style="text-align:center">'
    h += '<div class="summary-box"><div class="value">' + str(round(lp,1)) + '%</div><div class="label">Line Coverage</div></div>'
    h += '<div class="summary-box"><div class="value">' + str(round(fp,1)) + '%</div><div class="label">Function Coverage</div></div>'
    h += '<div class="summary-box"><div class="value">' + str(gp) + '/' + str(gt) + '</div><div class="label">Tests Passed</div></div>'
    h += '<div class="summary-box"><div class="value">' + str(td['total_suites']) + '</div><div class="label">Test Suites</div></div>'
    h += '</div></div>'
    
    h += '<div class="section"><h3>Coverage Metrics</h3>'
    h += '<div class="metrics">'
    h += '<p>Line Coverage: <span class="metric-value">' + str(round(lp,1)) + '% (' + str(lc) + ' of ' + str(lt) + ' lines)</span></p>'
    h += '<p>Function Coverage: <span class="metric-value">' + str(round(fp,1)) + '% (' + str(fc) + ' of ' + str(ft) + ' functions)</span></p>'
    h += '</div>'
    h += '<div class="grid"><div><canvas id="covPie"></canvas></div><div><canvas id="covBar"></canvas></div></div>'
    h += '</div>'
    
    h += '<div class="section"><h3>Test Results</h3>'
    h += '<div class="metrics">'
    h += '<p>Total: <span class="metric-value">' + str(gt) + '</span></p>'
    h += '<p>Passed: <span class="metric-value metric-good">' + str(gp) + '</span></p>'
    h += '<p>Failed: <span class="metric-value ' + fcls + '">' + str(gf) + '</span></p>'
    h += '</div>'
    h += '<h4>Test Suites (Click to expand)</h4>'
    h += '<table><thead><tr><th>Suite</th><th>Description</th><th style="text-align:center">Tests</th><th style="text-align:center">Status</th></tr></thead>'
    h += '<tbody>' + rows + '</tbody></table>'
    h += '<div class="grid" style="margin-top:25px"><div><canvas id="testPie"></canvas></div><div><canvas id="testBar"></canvas></div></div>'
    h += '</div>'
    
    h += '<div class="section"><h3>Build Info</h3><table>'
    h += '<tr><td><strong>Build System</strong></td><td>QMake/CMake</td></tr>'
    h += '<tr><td><strong>Compiler</strong></td><td>GCC 13.x</td></tr>'
    h += '<tr><td><strong>Qt</strong></td><td>Qt 6.4.2</td></tr>'
    h += '<tr><td><strong>Test Framework</strong></td><td>GoogleTest</td></tr>'
    h += '<tr><td><strong>Coverage</strong></td><td>lcov/gcov</td></tr>'
    h += '<tr><td><strong>CI</strong></td><td>GitHub Actions</td></tr>'
    h += '<tr><td><strong>Platform</strong></td><td>Ubuntu 24.04</td></tr>'
    h += '<tr><td><strong>Generated</strong></td><td>' + dt + '</td></tr>'
    h += '</table></div>'
    
    h += '<script>'
    h += 'var td=' + json.dumps(td) + ';'
    h += 'var lp=' + str(lp) + ',fp=' + str(fp) + ',nc=' + str(nc) + ',gp=' + str(gp) + ',gf=' + str(gf) + ';'
    h += 'function toggleDetails(i){var d=document.getElementById("details-"+i);d.classList.toggle("show");document.getElementById("icon-"+i).textContent=d.classList.contains("show")?"[-]":"[+]";}'
    h += 'new Chart(document.getElementById("covPie"),{type:"pie",data:{labels:["Covered ("+lp.toFixed(1)+"%)","Not Covered ("+nc.toFixed(1)+"%)"],datasets:[{data:[lp,nc],backgroundColor:["#4DD0E1","#FF9F40"]}]},options:{responsive:true,plugins:{title:{display:true,text:"Line Coverage"},legend:{position:"bottom"}}}});'
    h += 'new Chart(document.getElementById("covBar"),{type:"bar",data:{labels:["Line","Function"],datasets:[{label:"Coverage",data:[lp,fp],backgroundColor:["#4DD0E1","#36A2EB"]}]},options:{responsive:true,scales:{y:{beginAtZero:true,max:100}}}});'
    h += 'new Chart(document.getElementById("testPie"),{type:"doughnut",data:{labels:["Passed ("+gp+")","Failed ("+gf+")"],datasets:[{data:[gp,Math.max(gf,0.1)],backgroundColor:["#4BC0C0","#FF6384"]}]},options:{responsive:true,plugins:{legend:{position:"bottom"}}}});'
    h += 'new Chart(document.getElementById("testBar"),{type:"bar",data:{labels:td.chart_labels,datasets:[{label:"Passed",data:td.chart_passed,backgroundColor:"#4BC0C0"},{label:"Failed",data:td.chart_failed,backgroundColor:"#FF6384"}]},options:{responsive:true,scales:{x:{stacked:true},y:{stacked:true,beginAtZero:true}}}});'
    h += '</script>'
    
    h += '<div class="footer"><p>Generated by GitHub Actions CI</p></div>'
    h += '</body></html>'
    return h

def main():
    if os.path.exists('test_results/results.xml'):
        print('Parsing XML...')
        td = parse_xml()
    else:
        print('Parsing text...')
        td = parse_text()
    
    lp = float(os.environ.get('LINE_PERCENT', '0'))
    fp = float(os.environ.get('FUNC_PERCENT', '0'))
    lc = os.environ.get('LINES_COVERED', '0')
    lt = os.environ.get('LINES_TOTAL', '0')
    fc = os.environ.get('FUNCS_COVERED', '0')
    ft = os.environ.get('FUNCS_TOTAL', '0')
    gp = int(os.environ.get('GTEST_PASSED', '0'))
    gf = int(os.environ.get('GTEST_FAILED', '0'))
    gt = int(os.environ.get('GTEST_TOTAL', '0'))
    
    html = gen_html(td, lp, fp, lc, lt, fc, ft, gp, gf, gt)
    
    with open('REPORT.html', 'w') as f:
        f.write(html)
    
    print('Report generated!')
    print('Line Coverage: ' + str(lp) + '%')
    print('Function Coverage: ' + str(fp) + '%')
    print('Tests: ' + str(gp) + '/' + str(gt))
    print('Suites: ' + str(td['total_suites']))

if __name__ == '__main__':
    main()
