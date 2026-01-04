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
    
    # Find all test suites
    suite_pattern = r'
$$
----------
$$ \d+ tests? from (\w+)'
    suites = re.findall(suite_pattern, content)
    suites = list(dict.fromkeys(suites))
    
    for suite_name in suites:
        run_pattern = r'
$$
 RUN      
$$ ' + suite_name + r'\.(\w+)'
        ok_pattern = r'
$$
       OK 
$$ ' + suite_name + r'\.(\w+)'
        fail_pattern = r'
$$
  FAILED  
$$ ' + suite_name + r'\.(\w+)'
        
        runs = re.findall(run_pattern, content)
        oks = re.findall(ok_pattern, content)
        fails = re.findall(fail_pattern, content)
        
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

def generate_html(test_data, line_percent, func_percent, lines_covered, lines_total,
                  funcs_covered, funcs_total, gtest_passed, gtest_failed, gtest_total):
    
    not_covered = round(100 - line_percent, 1)
    current_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    failed_class = 'metric-bad' if gtest_failed > 0 else 'metric-good'
    
    # Generate test suites table rows
    suites_html = ''
    for i, suite in enumerate(test_data['test_suites']):
        status_class = 'status-passed' if suite['status'] == 'PASSED' else 'status-failed'
        
        # Main row
        suites_html += f'''<tr class="expandable" onclick="toggleDetails({i})">
            <td><span class="toggle-icon" id="icon-{i}">[+]</span>{suite['name']}</td>
            <td>{suite['description']}</td>
            <td style="text-align: center;">{suite['passed']}/{suite['tests']}</td>
            <td style="text-align: center;" class="{status_class}">{suite['status']}</td>
        </tr>'''
        
        # Details row
        test_cases_html = '<ul class="test-case-list">'
        for tc in suite['test_cases']:
            tc_class = 'status-passed' if tc['status'] == 'PASSED' else 'status-failed'
            test_cases_html += f'<li><span class="{tc_class}">[{tc["status"]}]</span> {tc["name"]}</li>'
        test_cases_html += '</ul>'
        
        suites_html += f'''<tr id="details-{i}" class="test-details">
            <td colspan="4">{test_cases_html}</td>
        </tr>'''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ClientServerSystem - CI and Coverage Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f9f9f9; margin: 40px; }}
        h1, h2, h3, h4 {{ color: #2c3e50; }}
        .section {{ background: #fff; padding: 20px; margin-bottom: 25px; border-radius: 6px; box-shadow: 0 0 6px rgba(0,0,0,.1); }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
        canvas {{ max-width: 100%; height: 300px !important; }}
        .footer {{ color: #777; font-size: .9em; margin-top: 30px; }}
        .metrics {{ font-size: 1.1em; margin-bottom: 20px; }}
        .metrics p {{ margin: 8px 0; }}
        .metric-value {{ font-weight: bold; }}
        .metric-good {{ color: #27ae60; }}
        .metric-bad {{ color: #e74c3c; }}
        .summary-box {{ display: inline-block; padding: 15px 25px; margin: 10px; background: #ecf0f1; border-radius: 8px; text-align: center; }}
        .summary-box .value {{ font-size: 2em; font-weight: bold; color: #2c3e50; }}
        .summary-box .label {{ font-size: 0.9em; color: #7f8c8d; }}
        .feature-list {{ columns: 2; column-gap: 40px; }}
        .feature-list li {{ margin-bottom: 8px; }}
        .tech-badge {{ display: inline-block; padding: 5px 12px; margin: 4px; background: #3498db; color: white; border-radius: 15px; font-size: 0.9em; }}
        .architecture-diagram {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; }}
        .arch-box {{ display: inline-block; padding: 15px 25px; margin: 10px; background: #3498db; color: white; border-radius: 8px; min-width: 120px; }}
        .arch-box.client {{ background: #9b59b6; }}
        .arch-box.server {{ background: #27ae60; }}
        .arch-box.common {{ background: #e67e22; }}
        .arch-arrow {{ font-size: 2em; color: #7f8c8d; margin: 0 10px; }}
        pre {{ background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 6px; overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th {{ background: #3498db; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:nth-child(even):not(.test-details) {{ background: #f9f9f9; }}
        .status-passed {{ color: #27ae60; font-weight: bold; }}
        .status-failed {{ color: #e74c3c; font-weight: bold; }}
        .test-case-list {{ margin: 5px 0; padding-left: 20px; font-size: 0.9em; color: #666; }}
        .expandable {{ cursor: pointer; }}
        .expandable:hover {{ background: #e8f4f8; }}
        .test-details {{ display: none; background: #f8f9fa; }}
        .test-details.show {{ display: table-row; }}
        .toggle-icon {{ margin-right: 8px; }}
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
    <p><strong>ClientServerSystem</strong> is a robust Qt6-based client-server application designed for efficient file management and system monitoring operations.</p>
    
    <h4>Key Features</h4>
    <ul class="feature-list">
        <li><strong>File Operations:</strong> Create, Read, Write, Append, Delete, Rename files</li>
        <li><strong>Directory Management:</strong> List files and directories</li>
        <li><strong>File Information:</strong> Retrieve detailed file metadata</li>
        <li><strong>System Monitoring:</strong> Real-time CPU load monitoring</li>
        <li><strong>Authentication:</strong> Secure user authentication system</li>
        <li><strong>Command Parser:</strong> Flexible command parsing and validation</li>
        <li><strong>Path Validation:</strong> Secure path handling and validation</li>
        <li><strong>Response Handling:</strong> Structured response formatting</li>
    </ul>

    <h4>Architecture</h4>
    <div class="architecture-diagram">
        <div class="arch-box client">Client</div>
        <span class="arch-arrow">&#8596;</span>
        <div class="arch-box common">Common Library</div>
        <span class="arch-arrow">&#8596;</span>
        <div class="arch-box server">Server</div>
    </div>

    <h4>Technology Stack</h4>
    <div style="margin-top: 15px;">
        <span class="tech-badge">C++17</span>
        <span class="tech-badge">Qt 6.4</span>
        <span class="tech-badge">GoogleTest</span>
        <span class="tech-badge">CMake/QMake</span>
        <span class="tech-badge">lcov</span>
        <span class="tech-badge">GitHub Actions</span>
    </div>

    <h4>Project Structure</h4>
    <pre>ClientServerSystem/
|-- client/              # Client application
|-- server/              # Server application
|-- common/              # Shared library
|-- tests/gtest/         # GoogleTest test suites
+-- ClientServerSystem.pro</pre>
</div>

<div class="section">
    <h3>Summary</h3>
    <div style="text-align: center;">
        <div class="summary-box">
            <div class="value">{line_percent:.1f}%</div>
            <div class="label">Line Coverage</div>
        </div>
        <div class="summary-box">
            <div class="value">{func_percent:.1f}%</div>
            <div class="label">Function Coverage</div>
        </div>
        <div class="summary-box">
            <div class="value">{gtest_passed}/{gtest_total}</div>
            <div class="label">Tests Passed</div>
        </div>
        <div class="summary-box">
            <div class="value">{test_data['total_suites']}</div>
            <div class="label">Test Suites</div>
        </div>
    </div>
</div>

<div class="section">
    <h3>Test Coverage Metrics</h3>
    <div class="metrics">
        <p>Line Coverage: <span class="metric-value">{line_percent:.1f}% ({lines_covered} of {lines_total} lines)</span></p>
        <p>Function Coverage: <span class="metric-value">{func_percent:.1f}% ({funcs_covered} of {funcs_total} functions)</span></p>
    </div>
    <div class="grid">
        <div><canvas id="coveragePie"></canvas></div>
        <div><canvas id="coverageBar"></canvas></div>
    </div>
</div>

<div class="section">
    <h3>Test Results</h3>
    <div class="metrics">
        <p>Total Tests: <span class="metric-value">{gtest_total}</span></p>
        <p>Passed: <span class="metric-value metric-good">{gtest_passed}</span></p>
        <p>Failed: <span class="metric-value {failed_class}">{gtest_failed}</span></p>
    </div>
    
    <h4>Test Suites (Click to expand)</h4>
    <table>
        <thead>
            <tr>
                <th>Test Suite</th>
                <th>Description</th>
                <th style="text-align: center;">Tests</th>
                <th style="text-align: center;">Status</th>
            </tr>
        </thead>
        <tbody>
            {suites_html}
        </tbody>
    </table>

    <div class="grid" style="margin-top: 25px;">
        <div><canvas id="testsPie"></canvas></div>
        <div><canvas id="testsBar"></canvas></div>
    </div>
</div>

<div class="section">
    <h3>Build Information</h3>
    <table>
        <tr><td><strong>Build System</strong></td><td>QMake / CMake</td></tr>
        <tr><td><strong>Compiler</strong></td><td>GCC 13.x</td></tr>
        <tr><td><strong>Qt Version</strong></td><td>Qt 6.4.2</td></tr>
        <tr><td><strong>Test Framework</strong></td><td>GoogleTest</td></tr>
        <tr><td><strong>Coverage Tool</strong></td><td>lcov / gcov</td></tr>
        <tr><td><strong>CI Platform</strong></td><td>GitHub Actions</td></tr>
        <tr><td><strong>Platform</strong></td><td>Ubuntu 24.04 (x86_64)</td></tr>
        <tr><td><strong>Report Generated</strong></td><td>{current_date}</td></tr>
    </table>
</div>

<script>
    var testData = {json.dumps(test_data)};
    var linePercent = {line_percent};
    var funcPercent = {func_percent};
    var notCovered = {not_covered};
    var gtestPassed = {gtest_passed};
    var gtestFailed = {gtest_failed};

    function toggleDetails(index) {{
        var details = document.getElementById('details-' + index);
        details.classList.toggle('show');
        var icon = document.getElementById('icon-' + index);
        icon.textContent = details.classList.contains('show') ? '[-]' : '[+]';
    }}

    new Chart(document.getElementById('coveragePie'), {{
        type: 'pie',
        data: {{
            labels: ['Covered (' + linePercent.toFixed(1) + '%)', 'Not Covered (' + notCovered.toFixed(1) + '%)'],
            datasets: [{{ data: [linePercent, notCovered], backgroundColor: ['#4DD0E1', '#FF9F40'] }}]
        }},
        options: {{ responsive: true, plugins: {{ title: {{ display: true, text: 'Line Coverage' }}, legend: {{ position: 'bottom' }} }} }}
    }});

    new Chart(document.getElementById('coverageBar'), {{
        type: 'bar',
        data: {{
            labels: ['Line Coverage', 'Function Coverage'],
            datasets: [{{ label: 'Coverage', data: [linePercent, funcPercent], backgroundColor: ['#4DD0E1', '#36A2EB'] }}]
        }},
        options: {{ responsive: true, plugins: {{ title: {{ display: true, text: 'Coverage by Type' }} }}, scales: {{ y: {{ beginAtZero: true, max: 100 }} }} }}
    }});

    new Chart(document.getElementById('testsPie'), {{
        type: 'doughnut',
        data: {{
            labels: ['Passed (' + gtestPassed + ')', 'Failed (' + gtestFailed + ')'],
            datasets: [{{ data: [gtestPassed, Math.max(gtestFailed, 0.1)], backgroundColor: ['#4BC0C0', '#FF6384'] }}]
        }},
        options: {{ responsive: true, plugins: {{ title: {{ display: true, text: 'Test Results' }}, legend: {{ position: 'bottom' }} }} }}
    }});

    new Chart(document.getElementById('testsBar'), {{
        type: 'bar',
        data: {{
            labels: testData.chart_labels,
            datasets: [
                {{ label: 'Passed', data: testData.chart_passed, backgroundColor: '#4BC0C0' }},
                {{ label: 'Failed', data: testData.chart_failed, backgroundColor: '#FF6384' }}
            ]
        }},
        options: {{ responsive: true, plugins: {{ title: {{ display: true, text: 'Tests by Suite' }} }}, scales: {{ x: {{ stacked: true }}, y: {{ stacked: true, beginAtZero: true }} }} }}
    }});
</script>

<div class="footer">
    <p>Generated automatically by GitHub Actions CI</p>
    <p>ClientServerSystem - A Qt6-based Client-Server File Management System</p>
</div>

</body>
</html>'''
    
    return html

def main():
    # Parse test results
    if os.path.exists('test_results/results.xml'):
        test_data = parse_xml()
    else:
        test_data = parse_text()
    
    # Get environment variables
    line_percent = float(os.environ.get('LINE_PERCENT', '0'))
    func_percent = float(os.environ.get('FUNC_PERCENT', '0'))
    lines_covered = os.environ.get('LINES_COVERED', '0')
    lines_total = os.environ.get('LINES_TOTAL', '0')
    funcs_covered = os.environ.get('FUNCS_COVERED', '0')
    funcs_total = os.environ.get('FUNCS_TOTAL', '0')
    gtest_passed = int(os.environ.get('GTEST_PASSED', '0'))
    gtest_failed = int(os.environ.get('GTEST_FAILED', '0'))
    gtest_total = int(os.environ.get('GTEST_TOTAL', '0'))
    
    # Generate HTML
    html = generate_html(
        test_data, line_percent, func_percent, lines_covered, lines_total,
        funcs_covered, funcs_total, gtest_passed, gtest_failed, gtest_total
    )
    
    # Write report
    with open('REPORT.html', 'w') as f:
        f.write(html)
    
    print('Report generated successfully!')
    print(f'Line Coverage: {line_percent}%')
    print(f'Function Coverage: {func_percent}%')
    print(f'Tests: {gtest_passed}/{gtest_total} passed')
    print(f'Test Suites: {test_data["total_suites"]}')

if __name__ == '__main__':
    main()