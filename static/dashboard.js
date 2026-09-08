// Dashboard functionality

// Update stats in real-time
function updateStats() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-scans').textContent = data.scans_completed;
            document.getElementById('total-vulns').textContent = data.vulnerabilities_found;
            document.getElementById('active-modules').textContent = data.modules;
        })
        .catch(error => console.error('Error updating stats:', error));
}

// Execute scan
function executeScan() {
    const target = document.getElementById('scan-target').value;
    const scanType = document.getElementById('scan-type').value;
    
    if (!target) {
        alert('Please enter a target');
        return;
    }
    
    fetch('/api/scan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            target: target,
            scan_type: scanType
        })
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data);
    })
    .catch(error => console.error('Scan failed:', error));
}

// Display scan results
function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    
    let html = '<h4>Scan Results</h4>';
    html += `<p>Target: ${results.target}</p>`;
    html += `<p>Type: ${results.scan_type}</p>`;
    html += `<p>Vulnerabilities: ${results.total_found}</p>`;
    
    if (results.vulnerabilities && results.vulnerabilities.length > 0) {
        html += '<ul>';
        results.vulnerabilities.forEach(vuln => {
            html += `<li class="severity-${vuln.severity}">${vuln.title}</li>`;
        });
        html += '</ul>';
    }
    
    resultsDiv.innerHTML = html;
}

// Auto-update every 30 seconds
setInterval(updateStats, 30000);

// Initial update
document.addEventListener('DOMContentLoaded', updateStats);
