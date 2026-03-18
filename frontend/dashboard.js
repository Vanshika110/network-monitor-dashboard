const socket = io();

// Protocol chart setup
const protoCtx = document.getElementById('protoChart').getContext('2d');
const protoChart = new Chart(protoCtx, {
  type: 'doughnut',
  data: {
    labels: [],
    datasets: [{
      data: [],
      backgroundColor: ['#58a6ff', '#56d364', '#f78166', '#d2a8ff'],
      borderWidth: 0
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        labels: { color: '#e6edf3', font: { size: 12 } }
      }
    }
  }
});

// Update dashboard with live data
socket.on('stats_update', (data) => {
  // Update stat cards
  document.getElementById('total-packets').textContent = 
    data.total_packets.toLocaleString();
  document.getElementById('total-bytes').textContent = 
    (data.total_bytes / 1024).toFixed(1) + ' KB';
  document.getElementById('proto-count').textContent = 
    Object.keys(data.protocols).length;

  // Update protocol chart
  const labels = Object.keys(data.protocols);
  const values = Object.values(data.protocols);
  protoChart.data.labels = labels;
  protoChart.data.datasets[0].data = values;
  protoChart.update('none');

  // Update top IPs
  const ipList = document.getElementById('top-ips');
  ipList.innerHTML = data.top_ips.map(([ip, count]) => `
    <li>
      <span class="ip">${ip}</span>
      <span class="count">${count} pkts</span>
    </li>
  `).join('');
});
```

### `.env.example`
```
SECRET_KEY=your-secret-key-here
INTERFACE=eth0