// Global variables for data management
let excelData = [];
let filteredData = [];
let regionsData = {};
let tasksData = {};
let currentCharts = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    initializeInteractivity();
    initializeAnimations();
});

function initializeEventListeners() {
    // File upload handlers
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadSection = document.getElementById('uploadSection');
    
    fileInput.addEventListener('change', handleFileSelection);
    uploadBtn.addEventListener('click', processExcelFile);
    uploadSection.addEventListener('dragover', handleDragOver);
    uploadSection.addEventListener('dragleave', handleDragLeave);
    uploadSection.addEventListener('drop', handleDrop);

    // Filter handlers
    document.getElementById('refreshData').addEventListener('click', applyFilters);

    // Tab handlers
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', handleTabClick);
    });

    // Table handlers
    document.getElementById('searchFilter').addEventListener('input', filterTable);
    document.getElementById('columnFilter').addEventListener('change', filterTable);

    // Export handlers
    document.getElementById('generateReport').addEventListener('click', generateReport);
}

function initializeInteractivity() {
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const selectedFile = document.getElementById('selectedFile');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');
    
    // Tab functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.dataset.tab;
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(target + '-tab').classList.add('active');
        });
    });
    
    // File input handling
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            fileName.textContent = file.name;
            fileSize.textContent = `(${formatFileSize(file.size)})`;
            selectedFile.style.display = 'flex';
            uploadBtn.disabled = false;
        }
    });
    
    // Refresh button animation
    document.getElementById('refreshData').addEventListener('click', function() {
        const icon = this.querySelector('i');
        icon.style.animation = 'spin 1s ease-in-out';
        setTimeout(() => {
            icon.style.animation = '';
        }, 1000);
    });
    
    // Add hover effects to glass cards
    const glassCards = document.querySelectorAll('.glass-card');
    glassCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Export button functionality
    document.getElementById('generateReport').addEventListener('click', function() {
        const originalText = this.innerHTML;
        this.innerHTML = '<span class="loading-spinner"></span> Generating...';
        this.disabled = true;
        
        setTimeout(() => {
            this.innerHTML = originalText;
            this.disabled = false;
            
            // Show success message
            const successMsg = document.createElement('div');
            successMsg.className = 'success-message';
            successMsg.textContent = 'Report generated successfully!';
            successMsg.style.display = 'block';
            this.parentNode.appendChild(successMsg);
            
            setTimeout(() => {
                successMsg.remove();
            }, 3000);
        }, 2000);
    });
    
    // Add search functionality simulation
    const searchInput = document.getElementById('searchFilter');
    searchInput.addEventListener('input', function() {
        const searchIcon = document.createElement('i');
        searchIcon.className = 'fas fa-search';
        searchIcon.style.position = 'absolute';
        searchIcon.style.right = '10px';
        searchIcon.style.top = '50%';
        searchIcon.style.transform = 'translateY(-50%)';
        searchIcon.style.color = 'var(--neon-cyan)';
        
        if (this.value && !this.parentNode.querySelector('.fas.fa-search')) {
            this.parentNode.style.position = 'relative';
            this.parentNode.appendChild(searchIcon);
        }
    });
}

function initializeAnimations() {
    // Add floating animation to upload icon
    const uploadIcon = document.querySelector('.upload-icon');
    if (uploadIcon) {
        uploadIcon.classList.add('pulse');
    }
    
    // Simulate data loading with animations
    function animateElements() {
        const elements = document.querySelectorAll('.glass-card');
        elements.forEach((el, index) => {
            setTimeout(() => {
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                
                setTimeout(() => {
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }, 100);
            }, index * 150);
        });
    }
    
    // Initialize animations
    animateElements();
    
    // Add dynamic background particles
    function createParticle() {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.width = '2px';
        particle.style.height = '2px';
        particle.style.background = 'rgba(0, 255, 255, 0.3)';
        particle.style.borderRadius = '50%';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '-1';
        particle.style.left = Math.random() * 100 + 'vw';
        particle.style.top = '100vh';
        particle.style.animation = 'floatUp 10s linear infinite';
        
        document.body.appendChild(particle);
        
        setTimeout(() => {
            particle.remove();
        }, 10000);
    }
    
    // Create floating particles
    setInterval(createParticle, 2000);
    
    // Add CSS for particle animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes floatUp {
            0% {
                transform: translateY(0) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) rotate(360deg);
                opacity: 0;
            }
        }
        
        @keyframes spin {
            0% {
                transform: rotate(0deg);
            }
            100% {
                transform: rotate(360deg);
            }
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.1);
            }
            100% {
                transform: scale(1);
            }
        }
        
        .loading-spinner {
            display: inline-block;
            width: 12px;
            height: 12px;
            border: 2px solid #rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }
    `;
    document.head.appendChild(style);
}

function handleFileSelection(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
            document.getElementById('fileInput').files = files;
            processFile(file);
        } else {
            showError('Please select an Excel file (.xlsx or .xls)');
        }
    }
}

function processFile(file) {
    if (file.size > 10 * 1024 * 1024) {
        showError('File size must be less than 10MB');
        return;
    }

    showFileInfo(file);
}

function showFileInfo(file) {
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const selectedFile = document.getElementById('selectedFile');
    
    fileName.textContent = file.name;
    fileSize.textContent = `(${formatFileSize(file.size)})`;
    selectedFile.style.display = 'block';
    
    document.getElementById('uploadBtn').disabled = false;
}

function processExcelFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        showError('Please select an Excel file first!');
        return;
    }

    showProgress();
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            const firstSheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[firstSheetName];
            
            // Convert to JSON
            const jsonData = XLSX.utils.sheet_to_json(worksheet);
            
            if (jsonData.length === 0) {
                showError('No data found in the Excel file!');
                return;
            }
            
            // Store the data
            excelData = jsonData;
            filteredData = [...jsonData];
            
            // Process data for regions and tasks
            processData(jsonData);
            
            // Hide progress and show results
            setTimeout(() => {
                hideProgress();
                showDataSections();
                showSuccess('Data processed successfully!');
                
                // Update UI with processed data
                updateSummaryCards();
                updateCharts();
                updateDataTable();
                populateFilterOptions();
                updateAnalysisSections();
            }, 1500);
            
        } catch (error) {
            hideProgress();
            showError('Error processing Excel file: ' + error.message);
            console.error(error);
        }
    };
    reader.readAsArrayBuffer(file);
}

// Process data into regions and tasks
function processData(data) {
    regionsData = {};
    tasksData = {};
    
    data.forEach(row => {
        // Normalize keys to lowercase for case insensitivity
        const keys = Object.keys(row);
        const normalizedRow = {};
        keys.forEach(key => {
            normalizedRow[key.toLowerCase()] = row[key];
        });
        
        const region = normalizedRow['region'] || 'Unspecified';
        const task = normalizedRow['task assignment'] || normalizedRow['task'] || 'Unspecified';
        
        // Count by region
        if (!regionsData[region]) {
            regionsData[region] = { count: 0, tasks: {} };
        }
        regionsData[region].count++;
        
        // Count by task
        if (!tasksData[task]) {
            tasksData[task] = 0;
        }
        tasksData[task]++;
        
        // Count task by region
        if (!regionsData[region].tasks[task]) {
            regionsData[region].tasks[task] = 0;
        }
        regionsData[region].tasks[task]++;
    });
}

function showProgress() {
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');
    
    progressBar.style.display = 'block';
    
    // Simulate progress
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 100) {
            progress = 100;
            clearInterval(interval);
        }
        progressFill.style.width = progress + '%';
    }, 100);
}

function hideProgress() {
    document.getElementById('progressBar').style.display = 'none';
    document.getElementById('progressFill').style.width = '0%';
}

function showDataSections() {
    // Show all the dynamic sections
    document.getElementById('dataControls').style.display = 'block';
    document.getElementById('summarySection').style.display = 'block';
    document.getElementById('chartsSection').style.display = 'block';
    document.getElementById('analysisSection').style.display = 'block';
    document.getElementById('dataTableSection').style.display = 'block';
    document.getElementById('exportSection').style.display = 'block';
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // Hide success message if shown
    document.getElementById('successMessage').style.display = 'none';
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

function showSuccess(message) {
    const successDiv = document.getElementById('successMessage');
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    
    // Hide error message if shown
    document.getElementById('errorMessage').style.display = 'none';
    
    // Auto hide after 3 seconds
    setTimeout(() => {
        successDiv.style.display = 'none';
    }, 3000);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i]);
}

// Update summary cards
function updateSummaryCards() {
    const summaryGrid = document.getElementById('summaryGrid');
    summaryGrid.innerHTML = '';
    
    // Total tasks card
    const totalTasks = filteredData.length;
    summaryGrid.appendChild(createSummaryCard('Total Tasks', totalTasks, 'fas fa-tasks'));
    
    // Total regions card
    const totalRegions = Object.keys(regionsData).length;
    summaryGrid.appendChild(createSummaryCard('Total Regions', totalRegions, 'fas fa-map-marker-alt'));
    
    // Top regions cards
    Object.entries(regionsData).forEach(([region, data]) => {
        summaryGrid.appendChild(createSummaryCard(region, data.count, 'fas fa-building'));
    });
}

// Create a summary card
function createSummaryCard(title, value, icon) {
    const card = document.createElement('div');
    card.className = 'summary-card';
    card.innerHTML = `
        <h3><i class="${icon}"></i> ${title}</h3>
        <div class="stat-number">${value}</div>
        <div class="stat-text">Tasks</div>
    `;
    return card;
}

// Update charts
function updateCharts() {
    // Destroy existing charts
    currentCharts.forEach(chart => chart.destroy());
    currentCharts = [];
    
    const chartsGrid = document.getElementById('chartsGrid');
    chartsGrid.innerHTML = '';
    
    // Regions distribution chart
    chartsGrid.appendChild(createChartCard('Tasks by Region', 'bar', getRegionsChartData()));
    
    // Task types distribution chart
    chartsGrid.appendChild(createChartCard('Task Types Distribution', 'pie', getTasksChartData()));
    
    // Tasks by region chart
    chartsGrid.appendChild(createChartCard('Tasks by Region and Type', 'bar', getTasksByRegionChartData()));
}

// Create chart card
function createChartCard(title, type, data) {
    const card = document.createElement('div');
    card.className = 'chart-card';
    card.innerHTML = `<h3>${title}</h3>`;
    
    const canvas = document.createElement('canvas');
    const container = document.createElement('div');
    container.className = 'chart-container';
    container.appendChild(canvas);
    card.appendChild(container);
    
    // Render chart after DOM insertion
    setTimeout(() => {
        const ctx = canvas.getContext('2d');
        const chart = new Chart(ctx, {
            type: type,
            data: {
                labels: data.labels,
                datasets: [{
                    label: data.label,
                    data: data.values,
                    backgroundColor: getChartColors(data.values.length),
                    borderColor: '#fff',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
        currentCharts.push(chart);
    }, 100);
    
    return card;
}

// Get chart colors
function getChartColors(count) {
    const colors = [
        '#667eea', '#764ba2', '#5a67d8', '#4c51bf', '#6b46c1',
        '#553c9a', '#44337a', '#e53e3e', '#dd6b20', '#38a169',
        '#319795', '#3182ce', '#5a67d8', '#805ad5', '#d53f8c'
    ];
    return colors.slice(0, count);
}

// Get regions chart data
function getRegionsChartData() {
    const labels = Object.keys(regionsData);
    const values = labels.map(region => regionsData[region].count);
    
    return {
        labels: labels,
        values: values,
        label: 'Tasks Count'
    };
}

// Get tasks chart data
function getTasksChartData() {
    const labels = Object.keys(tasksData);
    const values = labels.map(task => tasksData[task]);
    
    return {
        labels: labels,
        values: values,
        label: 'Tasks Count'
    };
}

// Get tasks by region chart data
function getTasksByRegionChartData() {
    const regions = Object.keys(regionsData);
    const tasks = Object.keys(tasksData);
    const datasets = [];
    
    tasks.forEach(task => {
        const data = regions.map(region => {
            return regionsData[region].tasks[task] || 0;
        });
        
        datasets.push({
            label: task,
            data: data,
            backgroundColor: getChartColors(1)[0]
        });
    });
    
    return {
        labels: regions,
        datasets: datasets,
        type: 'bar',
        options: {
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true
                }
            }
        }
    };
}

// Populate filter options
function populateFilterOptions() {
    const regionFilter = document.getElementById('regionFilter');
    const taskFilter = document.getElementById('taskFilter');
    const columnFilter = document.getElementById('columnFilter');
    
    // Clear existing options
    regionFilter.innerHTML = '<option value="">All Regions</option>';
    taskFilter.innerHTML = '<option value="">All Tasks</option>';
    columnFilter.innerHTML = '<option value="">All Columns</option>';
    
    // Add regions
    Object.keys(regionsData).forEach(region => {
        const option = document.createElement('option');
        option.value = region;
        option.textContent = region;
        regionFilter.appendChild(option);
    });
    
    // Add tasks
    Object.keys(tasksData).forEach(task => {
        const option = document.createElement('option');
        option.value = task;
        option.textContent = task;
        taskFilter.appendChild(option);
    });
    
    // Add columns for table filtering
    if (excelData.length > 0) {
        Object.keys(excelData[0]).forEach(column => {
            const option = document.createElement('option');
            option.value = column;
            option.textContent = column;
            columnFilter.appendChild(option);
        });
    }
}

// Apply filters
function applyFilters() {
    const region = document.getElementById('regionFilter').value;
    const task = document.getElementById('taskFilter').value;
    
    filteredData = excelData.filter(row => {
        const rowRegion = (row['Region'] || row['region'] || '').toString().toLowerCase();
        const rowTask = (row['Task Assignment'] || row['task assignment'] || row['Task'] || row['task'] || '').toString().toLowerCase();
        
        const regionMatch = !region || rowRegion === region.toLowerCase();
        const taskMatch = !task || rowTask === task.toLowerCase();
        
        return regionMatch && taskMatch;
    });
    
    // Update data for regions and tasks based on filtered data
    processData(filteredData);
    
    // Update UI
    updateSummaryCards();
    updateCharts();
    updateDataTable();
    updateAnalysisSections();
    
    showSuccess('Filters applied successfully!');
}

// Update data table
function updateDataTable() {
    const tableContainer = document.getElementById('dataTableContainer');
    tableContainer.innerHTML = '';
    
    if (filteredData.length === 0) {
        tableContainer.innerHTML = '<p>No data available with current filters</p>';
        return;
    }
    
    const table = document.createElement('table');
    table.className = 'data-table';
    
    // Create table header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    Object.keys(filteredData[0]).forEach(key => {
        const th = document.createElement('th');
        th.textContent = key;
        headerRow.appendChild(th);
    });
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Create table body
    const tbody = document.createElement('tbody');
    
    filteredData.forEach(row => {
        const tr = document.createElement('tr');
        
        Object.values(row).forEach(value => {
            const td = document.createElement('td');
            td.textContent = value;
            tr.appendChild(td);
        });
        
        tbody.appendChild(tr);
    });
    
    table.appendChild(tbody);
    tableContainer.appendChild(table);
}

// Filter table
function filterTable() {
    const searchText = document.getElementById('searchFilter').value.toLowerCase();
    const column = document.getElementById('columnFilter').value;
    
    if (!searchText) {
        // If no search text, show all data
        filteredData = [...excelData];
        updateDataTable();
        return;
    }
    
    filteredData = excelData.filter(row => {
        if (column) {
            // Search in specific column
            const value = row[column] ? row[column].toString().toLowerCase() : '';
            return value.includes(searchText);
        } else {
            // Search in all columns
            return Object.values(row).some(value => 
                value && value.toString().toLowerCase().includes(searchText)
            );
        }
    });
    
    updateDataTable();
}

// Handle tab clicks
function handleTabClick(event) {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Remove active class from all buttons and contents
    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));
    
    // Add active class to clicked button
    event.currentTarget.classList.add('active');
    
    // Show corresponding content
    const tabName = event.currentTarget.getAttribute('data-tab');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

// Update analysis sections
function updateAnalysisSections() {
    updateRegionsAnalysis();
    updateTasksAnalysis();
}

// Update regions analysis
function updateRegionsAnalysis() {
    const regionsAnalysis = document.getElementById('regionsAnalysis');
    regionsAnalysis.innerHTML = '';
    
    Object.entries(regionsData).forEach(([region, data]) => {
        const card = document.createElement('div');
        card.className = 'region-task-card';
        
        let tasksHtml = '';
        Object.entries(data.tasks).forEach(([task, count]) => {
            tasksHtml += `
                <div class="task-item">
                    <span>${task}</span>
                    <span>${count}</span>
                </div>
            `;
        });
        
        card.innerHTML = `
            <h4>${region} (Total: ${data.count})</h4>
            ${tasksHtml}
        `;
        
        regionsAnalysis.appendChild(card);
    });
}

// Update tasks analysis
function updateTasksAnalysis() {
    const tasksAnalysis = document.getElementById('tasksAnalysis');
    tasksAnalysis.innerHTML = '';
    
    const taskCard = document.createElement('div');
    taskCard.className = 'region-task-card';
    
    let tasksHtml = '';
    Object.entries(tasksData).forEach(([task, count]) => {
        tasksHtml += `
            <div class="task-item">
                <span>${task}</span>
                <span>${count}</span>
            </div>
        `;
    });
    
    taskCard.innerHTML = `
        <h4>Task Distribution (Total: ${filteredData.length})</h4>
        ${tasksHtml}
    `;
    
    tasksAnalysis.appendChild(taskCard);
}

// Generate reports
function generateReport() {
    const reportType = document.getElementById('reportType').value;
    
    try {
        // Create workbook
        const wb = XLSX.utils.book_new();
        
        // Add summary sheet
        const summaryData = [
            ['Report Type', 'Excel Data Analyzer Report'],
            ['Generated At', new Date().toLocaleString()],
            ['Total Tasks', filteredData.length],
            ['Total Regions', Object.keys(regionsData).length],
            ['','']
        ];
        
        const summarySheet = XLSX.utils.aoa_to_sheet(summaryData);
        XLSX.utils.book_append_sheet(wb, summarySheet, 'Summary');
        
        // Add regions data sheet
        const regionsSheetData = [['Region', 'Task Count']];
        Object.entries(regionsData).forEach(([region, data]) => {
            regionsSheetData.push([region, data.count]);
        });
        const regionsSheet = XLSX.utils.aoa_to_sheet(regionsSheetData);
        XLSX.utils.book_append_sheet(wb, regionsSheet, 'Regions');
        
        // Add tasks data sheet
        const tasksSheetData = [['Task Type', 'Count']];
        Object.entries(tasksData).forEach(([task, count]) => {
            tasksSheetData.push([task, count]);
        });
        const tasksSheet = XLSX.utils.aoa_to_sheet(tasksSheetData);
        XLSX.utils.book_append_sheet(wb, tasksSheet, 'Tasks');
        
        // Add detailed data sheet
        const detailedSheet = XLSX.utils.json_to_sheet(filteredData);
        XLSX.utils.book_append_sheet(wb, detailedSheet, 'Detailed Data');
        
        // Export workbook
        XLSX.writeFile(wb, 'Excel_Analysis_Report.xlsx');
        showSuccess('Report generated successfully!');
        
    } catch (error) {
        showError('Error generating report: ' + error.message);
    }
}