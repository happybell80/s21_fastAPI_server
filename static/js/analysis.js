document.addEventListener('DOMContentLoaded', function() {
  // Initialize components
  initSideMenu();
  initTabs();
  loadMetricsData();
  loadChartData();
  loadTableData();
  loadNewsData();
});

// Side menu toggle functionality
function initSideMenu() {
  const menuToggle = document.querySelector('.menu-toggle');
  const sideMenu = document.querySelector('.side-menu');
  const container = document.querySelector('.analysis-container');
  
  if (menuToggle && sideMenu && container) {
    menuToggle.addEventListener('click', function() {
      sideMenu.classList.toggle('collapsed');
      container.classList.toggle('expanded');
    });
  }
}

// Tab navigation
function initTabs() {
  const tabs = document.querySelectorAll('.tab-nav button');
  const contentSections = document.querySelectorAll('.content-section');
  
  if (tabs.length && contentSections.length) {
    tabs.forEach(tab => {
      tab.addEventListener('click', function() {
        // Remove active class from all tabs
        tabs.forEach(t => t.classList.remove('active'));
        
        // Add active class to clicked tab
        this.classList.add('active');
        
        // Hide all content sections
        contentSections.forEach(section => {
          section.style.display = 'none';
        });
        
        // Show selected content section
        const targetSection = document.querySelector(this.dataset.target);
        if (targetSection) {
          targetSection.style.display = 'block';
        }
      });
    });
    
    // Activate first tab by default
    if (tabs[0]) {
      tabs[0].click();
    }
  }
}

// Load metrics data from API
function loadMetricsData() {
  fetch('/api/analytics/metrics')
    .then(response => response.json())
    .then(data => {
      updateMetrics(data);
    })
    .catch(error => {
      console.error('Error loading metrics data:', error);
      // Use placeholder data if API fails
      updateMetrics(getPlaceholderMetrics());
    });
}

// Update metrics section with data
function updateMetrics(data) {
  const metricCards = document.querySelectorAll('.metric-card');
  
  if (data && metricCards.length) {
    metricCards.forEach(card => {
      const metricId = card.dataset.metric;
      const valueElement = card.querySelector('.metric-value');
      const changeElement = card.querySelector('.metric-change');
      
      if (valueElement && data[metricId]) {
        valueElement.textContent = data[metricId].value;
        
        if (changeElement && data[metricId].change) {
          const change = data[metricId].change;
          const isPositive = change > 0;
          
          changeElement.textContent = `${isPositive ? '+' : ''}${change}%`;
          changeElement.classList.add(isPositive ? 'positive' : 'negative');
        }
      }
    });
  }
}

// Load chart data from API
function loadChartData() {
  fetch('/api/analytics/charts')
    .then(response => response.json())
    .then(data => {
      if (data.marketTrends) createMarketTrendsChart(data.marketTrends);
      if (data.tokenDistribution) createTokenDistributionChart(data.tokenDistribution);
      if (data.tradingVolume) createTradingVolumeChart(data.tradingVolume);
      if (data.priceComparison) createPriceComparisonChart(data.priceComparison);
    })
    .catch(error => {
      console.error('Error loading chart data:', error);
      // Use placeholder data if API fails
      const placeholderData = getPlaceholderChartData();
      createMarketTrendsChart(placeholderData.marketTrends);
      createTokenDistributionChart(placeholderData.tokenDistribution);
      createTradingVolumeChart(placeholderData.tradingVolume);
      createPriceComparisonChart(placeholderData.priceComparison);
    });
}

// Create market trends line chart using D3.js
function createMarketTrendsChart(data) {
  const container = document.getElementById('market-trends-chart');
  if (!container) return;
  
  // Clear previous chart if any
  container.innerHTML = '';
  
  // Set dimensions and margins
  const margin = {top: 20, right: 30, bottom: 30, left: 40};
  const width = container.clientWidth - margin.left - margin.right;
  const height = 300 - margin.top - margin.bottom;
  
  // Create SVG
  const svg = d3.select(container)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  // X scale
  const x = d3.scaleTime()
    .domain(d3.extent(data, d => new Date(d.date)))
    .range([0, width]);
  
  // Y scale
  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value) * 1.1])
    .range([height, 0]);
  
  // Line generator
  const line = d3.line()
    .x(d => x(new Date(d.date)))
    .y(d => y(d.value))
    .curve(d3.curveMonotoneX);
  
  // Add X axis
  svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat(d3.timeFormat("%b %d")));
  
  // Add Y axis
  svg.append("g")
    .call(d3.axisLeft(y));
  
  // Add line path
  svg.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "#3498db")
    .attr("stroke-width", 2)
    .attr("d", line);
  
  // Add dots
  svg.selectAll(".dot")
    .data(data)
    .enter().append("circle")
    .attr("class", "dot")
    .attr("cx", d => x(new Date(d.date)))
    .attr("cy", d => y(d.value))
    .attr("r", 4)
    .attr("fill", "#3498db");
}

// Create token distribution pie chart using D3.js
function createTokenDistributionChart(data) {
  const container = document.getElementById('token-distribution-chart');
  if (!container) return;
  
  // Clear previous chart if any
  container.innerHTML = '';
  
  // Set dimensions
  const width = container.clientWidth;
  const height = 300;
  const radius = Math.min(width, height) / 2 - 40;
  
  // Create SVG
  const svg = d3.select(container)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);
  
  // Color scale
  const color = d3.scaleOrdinal()
    .domain(data.map(d => d.category))
    .range(["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6", "#1abc9c"]);
  
  // Pie generator
  const pie = d3.pie()
    .value(d => d.value)
    .sort(null);
  
  // Arc generator
  const arc = d3.arc()
    .innerRadius(radius * 0.5) // Make it a donut chart
    .outerRadius(radius);
  
  // Add arcs
  const arcs = svg.selectAll(".arc")
    .data(pie(data))
    .enter()
    .append("g")
    .attr("class", "arc");
  
  // Add path
  arcs.append("path")
    .attr("d", arc)
    .attr("fill", d => color(d.data.category))
    .attr("stroke", "white")
    .style("stroke-width", "2px");
  
  // Add labels
  const labelArc = d3.arc()
    .innerRadius(radius * 0.8)
    .outerRadius(radius * 0.8);
  
  arcs.append("text")
    .attr("transform", d => `translate(${labelArc.centroid(d)})`)
    .attr("dy", ".35em")
    .style("text-anchor", "middle")
    .style("font-size", "12px")
    .style("fill", "white")
    .text(d => d.data.category);
}

// Create trading volume bar chart using D3.js
function createTradingVolumeChart(data) {
  const container = document.getElementById('trading-volume-chart');
  if (!container) return;
  
  // Clear previous chart if any
  container.innerHTML = '';
  
  // Set dimensions and margins
  const margin = {top: 20, right: 30, bottom: 40, left: 50};
  const width = container.clientWidth - margin.left - margin.right;
  const height = 300 - margin.top - margin.bottom;
  
  // Create SVG
  const svg = d3.select(container)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  // X scale
  const x = d3.scaleBand()
    .domain(data.map(d => d.date))
    .range([0, width])
    .padding(0.2);
  
  // Y scale
  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value) * 1.1])
    .range([height, 0]);
  
  // Add X axis
  svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).tickFormat(d => d.slice(5)))
    .selectAll("text")
    .style("text-anchor", "end")
    .attr("dx", "-.8em")
    .attr("dy", ".15em")
    .attr("transform", "rotate(-45)");
  
  // Add Y axis
  svg.append("g")
    .call(d3.axisLeft(y));
  
  // Add bars
  svg.selectAll(".bar")
    .data(data)
    .enter()
    .append("rect")
    .attr("class", "bar")
    .attr("x", d => x(d.date))
    .attr("width", x.bandwidth())
    .attr("y", d => y(d.value))
    .attr("height", d => height - y(d.value))
    .attr("fill", "#3498db");
}

// Create price comparison line chart using D3.js
function createPriceComparisonChart(data) {
  const container = document.getElementById('price-comparison-chart');
  if (!container) return;
  
  // Clear previous chart if any
  container.innerHTML = '';
  
  // Set dimensions and margins
  const margin = {top: 20, right: 60, bottom: 30, left: 40};
  const width = container.clientWidth - margin.left - margin.right;
  const height = 300 - margin.top - margin.bottom;
  
  // Create SVG
  const svg = d3.select(container)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  // Process data
  const cryptos = Object.keys(data[0]).filter(key => key !== 'date');
  const formattedData = data.map(d => {
    return {
      date: new Date(d.date),
      ...cryptos.reduce((obj, crypto) => {
        obj[crypto] = +d[crypto];
        return obj;
      }, {})
    };
  });
  
  // X scale
  const x = d3.scaleTime()
    .domain(d3.extent(formattedData, d => d.date))
    .range([0, width]);
  
  // Y scale
  const y = d3.scaleLinear()
    .domain([
      d3.min(formattedData, d => Math.min(...cryptos.map(crypto => d[crypto]))) * 0.9,
      d3.max(formattedData, d => Math.max(...cryptos.map(crypto => d[crypto]))) * 1.1
    ])
    .range([height, 0]);
  
  // Color scale
  const color = d3.scaleOrdinal()
    .domain(cryptos)
    .range(["#3498db", "#e74c3c", "#2ecc71", "#f39c12"]);
  
  // Line generator
  const line = d3.line()
    .x(d => x(d.date))
    .y(d => y(d.value))
    .curve(d3.curveMonotoneX);
  
  // Add X axis
  svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat(d3.timeFormat("%b %d")));
  
  // Add Y axis
  svg.append("g")
    .call(d3.axisLeft(y));
  
  // Add lines
  cryptos.forEach(crypto => {
    const cryptoData = formattedData.map(d => ({
      date: d.date,
      value: d[crypto]
    }));
    
    svg.append("path")
      .datum(cryptoData)
      .attr("fill", "none")
      .attr("stroke", color(crypto))
      .attr("stroke-width", 2)
      .attr("d", line);
    
    // Add dots for the last point
    const lastPoint = cryptoData[cryptoData.length - 1];
    
    svg.append("circle")
      .attr("cx", x(lastPoint.date))
      .attr("cy", y(lastPoint.value))
      .attr("r", 4)
      .attr("fill", color(crypto));
    
    // Add label for the last point
    svg.append("text")
      .attr("x", x(lastPoint.date) + 10)
      .attr("y", y(lastPoint.value))
      .attr("dy", ".35em")
      .style("font-size", "12px")
      .style("fill", color(crypto))
      .text(crypto);
  });
}

// Load table data from API
function loadTableData() {
  fetch('/api/analytics/transactions')
    .then(response => response.json())
    .then(data => {
      updateTransactionsTable(data);
    })
    .catch(error => {
      console.error('Error loading table data:', error);
      // Use placeholder data if API fails
      updateTransactionsTable(getPlaceholderTableData());
    });
}

// Update transactions table with data
function updateTransactionsTable(data) {
  const tableBody = document.querySelector('.transactions-table tbody');
  if (!tableBody) return;
  
  // Clear previous data
  tableBody.innerHTML = '';
  
  // Add rows
  data.forEach(transaction => {
    const row = document.createElement('tr');
    
    // Create cells
    const idCell = document.createElement('td');
    idCell.textContent = transaction.id;
    
    const typeCell = document.createElement('td');
    typeCell.textContent = transaction.type;
    typeCell.classList.add(transaction.type.toLowerCase());
    
    const amountCell = document.createElement('td');
    amountCell.textContent = transaction.amount;
    
    const tokenCell = document.createElement('td');
    tokenCell.textContent = transaction.token;
    
    const statusCell = document.createElement('td');
    statusCell.textContent = transaction.status;
    statusCell.classList.add(transaction.status.toLowerCase());
    
    const dateCell = document.createElement('td');
    dateCell.textContent = transaction.date;
    
    // Add cells to row
    row.appendChild(idCell);
    row.appendChild(typeCell);
    row.appendChild(amountCell);
    row.appendChild(tokenCell);
    row.appendChild(statusCell);
    row.appendChild(dateCell);
    
    // Add row to table
    tableBody.appendChild(row);
  });
  
  // Update pagination
  updatePagination(data.length);
}

// Update pagination controls
function updatePagination(totalItems) {
  const paginationContainer = document.querySelector('.pagination');
  if (!paginationContainer) return;
  
  const itemsPerPage = 10;
  const totalPages = Math.ceil(totalItems / itemsPerPage);
  
  // Clear previous pagination
  paginationContainer.innerHTML = '';
  
  // Add previous button
  const prevButton = document.createElement('button');
  prevButton.textContent = '‹';
  prevButton.classList.add('pagination-btn');
  prevButton.disabled = true;
  paginationContainer.appendChild(prevButton);
  
  // Add page buttons
  for (let i = 1; i <= Math.min(totalPages, 5); i++) {
    const pageButton = document.createElement('button');
    pageButton.textContent = i;
    pageButton.classList.add('pagination-btn');
    
    if (i === 1) {
      pageButton.classList.add('active');
    }
    
    paginationContainer.appendChild(pageButton);
  }
  
  // Add next button
  const nextButton = document.createElement('button');
  nextButton.textContent = '›';
  nextButton.classList.add('pagination-btn');
  paginationContainer.appendChild(nextButton);
}

// Load news data from API
function loadNewsData() {
  fetch('/api/analytics/news')
    .then(response => response.json())
    .then(data => {
      updateNewsSection(data);
    })
    .catch(error => {
      console.error('Error loading news data:', error);
      // Use placeholder data if API fails
      updateNewsSection(getPlaceholderNewsData());
    });
}

// Update news section with data
function updateNewsSection(data) {
  const newsContainer = document.querySelector('.news-grid');
  if (!newsContainer) return;
  
  // Clear previous news
  newsContainer.innerHTML = '';
  
  // Add news cards
  data.forEach(newsItem => {
    const card = document.createElement('div');
    card.className = 'news-card';
    
    card.innerHTML = `
      <div class="news-card-header">
        <span class="news-source">${newsItem.source}</span>
        <span class="news-date">${newsItem.date}</span>
      </div>
      <h3 class="news-title">${newsItem.title}</h3>
      <p class="news-summary">${newsItem.summary}</p>
      <a href="${newsItem.url}" class="news-link" target="_blank">Read More</a>
    `;
    
    newsContainer.appendChild(card);
  });
}

// Placeholder data functions
function getPlaceholderMetrics() {
  return {
    totalUsers: { value: '32,456', change: 12.3 },
    activeTraders: { value: '8,754', change: 5.7 },
    tradingVolume: { value: '$24.5M', change: -3.2 },
    marketCap: { value: '$158.7B', change: 7.8 }
  };
}

function getPlaceholderChartData() {
  // Market trends data
  const marketTrends = [];
  const today = new Date();
  for (let i = 30; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    marketTrends.push({
      date: date.toISOString().split('T')[0],
      value: 10000 + Math.random() * 5000
    });
  }
  
  // Token distribution data
  const tokenDistribution = [
    { category: 'BTC', value: 45 },
    { category: 'ETH', value: 30 },
    { category: 'XRP', value: 10 },
    { category: 'SOL', value: 8 },
    { category: 'Others', value: 7 }
  ];
  
  // Trading volume data
  const tradingVolume = [];
  for (let i = 0; i < 12; i++) {
    const date = new Date(today);
    date.setMonth(date.getMonth() - 11 + i);
    const monthYear = date.toISOString().split('T')[0].substring(0, 7);
    tradingVolume.push({
      date: monthYear,
      value: 5000000 + Math.random() * 10000000
    });
  }
  
  // Price comparison data
  const priceComparison = [];
  for (let i = 30; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    priceComparison.push({
      date: date.toISOString().split('T')[0],
      BTC: 30000 + Math.random() * 5000,
      ETH: 2000 + Math.random() * 500,
      XRP: 0.5 + Math.random() * 0.2,
      SOL: 100 + Math.random() * 20
    });
  }
  
  return {
    marketTrends,
    tokenDistribution,
    tradingVolume,
    priceComparison
  };
}

function getPlaceholderTableData() {
  const transactions = [];
  const types = ['Buy', 'Sell', 'Transfer', 'Swap'];
  const tokens = ['BTC', 'ETH', 'XRP', 'SOL', 'USDT'];
  const statuses = ['Completed', 'Pending', 'Failed'];
  
  for (let i = 1; i <= 20; i++) {
    const today = new Date();
    const randomDays = Math.floor(Math.random() * 30);
    today.setDate(today.getDate() - randomDays);
    
    transactions.push({
      id: `TX${100000 + i}`,
      type: types[Math.floor(Math.random() * types.length)],
      amount: (Math.random() * 10).toFixed(4),
      token: tokens[Math.floor(Math.random() * tokens.length)],
      status: statuses[Math.floor(Math.random() * statuses.length)],
      date: today.toISOString().split('T')[0]
    });
  }
  
  return transactions;
}

function getPlaceholderNewsData() {
  return [
    {
      title: 'Bitcoin Surges Past $50K as Institutional Adoption Grows',
      summary: 'Bitcoin has surpassed the $50,000 mark for the first time in months as institutional investors continue to show interest in cryptocurrency.',
      source: 'CryptoNews',
      date: '2023-10-15',
      url: '#'
    },
    {
      title: 'New Regulatory Framework for Crypto Exchanges Announced',
      summary: 'The Securities and Exchange Commission has announced a new regulatory framework that aims to provide clarity for cryptocurrency exchanges.',
      source: 'Financial Times',
      date: '2023-10-12',
      url: '#'
    },
    {
      title: 'Ethereum 2.0 Upgrade Set to Launch Next Month',
      summary: 'The much-anticipated Ethereum 2.0 upgrade is scheduled to launch next month, promising improved scalability and reduced energy consumption.',
      source: 'Tech Insider',
      date: '2023-10-10',
      url: '#'
    },
    {
      title: 'DeFi Market Cap Reaches All-Time High of $150 Billion',
      summary: 'The total market capitalization of decentralized finance (DeFi) projects has reached an all-time high of $150 billion, reflecting growing investor confidence.',
      source: 'DeFi Pulse',
      date: '2023-10-08',
      url: '#'
    }
  ];
} 