document.addEventListener('DOMContentLoaded', () => {
    let jobs = [];
    let currentView = 'grid'; // 'grid' or 'list'

    // DOM Elements
    const jobGrid = document.getElementById('job-grid');
    const totalCountEl = document.getElementById('total-count');
    const appliedCountEl = document.getElementById('applied-count');
    const pendingCountEl = document.getElementById('pending-count');
    const resultsCountEl = document.getElementById('results-count');
    
    // Filter Elements
    const searchInput = document.getElementById('search-input');
    const typeFilter = document.getElementById('type-filter');
    const chanceFilter = document.getElementById('chance-filter');
    const categoryFilter = document.getElementById('category-filter');
    const statusFilter = document.getElementById('status-filter');
    const resetBtn = document.getElementById('reset-btn');
    
    // View Toggles
    const gridViewBtn = document.getElementById('grid-view-btn');
    const listViewBtn = document.getElementById('list-view-btn');

    // Fetch Jobs Data
    fetch('jobs.json')
        .then(response => response.json())
        .then(data => {
            jobs = data;
            initializeStatuses();
            updateStats();
            renderJobs();
        })
        .catch(err => {
            console.error('Error loading jobs:', err);
            jobGrid.innerHTML = `<div class="loading-spinner">Failed to load jobs. Please make sure jobs.json exists.</div>`;
        });

    // Initialize statuses in localStorage if not already present
    function initializeStatuses() {
        jobs.forEach((job, index) => {
            const key = `job-status-${index}-${job.company.replace(/\s+/g, '-')}`;
            if (!localStorage.getItem(key)) {
                localStorage.setItem(key, 'Not Applied');
            }
        });
    }

    // Get status from localStorage
    function getJobStatus(job, index) {
        const key = `job-status-${index}-${job.company.replace(/\s+/g, '-')}`;
        return localStorage.getItem(key) || 'Not Applied';
    }

    // Set status in localStorage
    function setJobStatus(job, index, status) {
        const key = `job-status-${index}-${job.company.replace(/\s+/g, '-')}`;
        localStorage.setItem(key, status);
        updateStats();
        renderJobs(); // Re-render to apply new filters if active
    }

    // Update Stats Summary Header
    function updateStats() {
        let total = jobs.length;
        let applied = 0;
        let pending = 0;

        jobs.forEach((job, index) => {
            const status = getJobStatus(job, index);
            if (status === 'Applied' || status === 'Interviewing' || status === 'Offered') {
                applied++;
            } else {
                pending++;
            }
        });

        totalCountEl.textContent = total;
        appliedCountEl.textContent = applied;
        pendingCountEl.textContent = pending;
    }

    // Filter Logic
    function getFilteredJobs() {
        const query = searchInput.value.toLowerCase().trim();
        const type = typeFilter.value;
        const chance = chanceFilter.value;
        const category = categoryFilter.value;
        const statusVal = statusFilter.value;

        return jobs.filter((job, index) => {
            const status = getJobStatus(job, index);
            
            // Search Query Filter
            const matchesQuery = !query || 
                job.title.toLowerCase().includes(query) || 
                job.company.toLowerCase().includes(query) || 
                job.fits.toLowerCase().includes(query) || 
                job.tip.toLowerCase().includes(query);

            // Employment Type Filter
            const matchesType = type === 'all' || job.employment === type;

            // Selection Chance Filter
            const matchesChance = chance === 'all' || job.chance === chance;

            // Category Filter
            const matchesCategory = category === 'all' || job.category === category;

            // Application Status Filter
            const matchesStatus = statusVal === 'all' || 
                (statusVal === 'Not Applied' && status === 'Not Applied') ||
                (statusVal === status);

            return matchesQuery && matchesType && matchesChance && matchesCategory && matchesStatus;
        });
    }

    // Render Job Cards
    function renderJobs() {
        const filtered = getFilteredJobs();
        resultsCountEl.textContent = `Showing ${filtered.length} of ${jobs.length} jobs`;

        if (filtered.length === 0) {
            jobGrid.innerHTML = `<div class="loading-spinner">No jobs match your search filters. Try resetting filters.</div>`;
            return;
        }

        jobGrid.innerHTML = '';

        filtered.forEach(job => {
            // Find the original index of this job in the full list
            const originalIndex = jobs.findIndex(j => j.company === job.company && j.title === job.title);
            const status = getJobStatus(job, originalIndex);

            // Create Card Element
            const card = document.createElement('div');
            card.className = `job-card ${currentView === 'list' ? 'list-card' : ''}`;
            
            // Build inner HTML
            card.innerHTML = `
                <div class="card-top">
                    <div class="badge-row">
                        <span class="badge badge-category" data-cat="${job.category}">${job.category}</span>
                        <span class="badge badge-employment ${job.employment === 'Part-time' ? 'part-time' : ''}">${job.employment}</span>
                        <span class="badge badge-chance ${job.chance === 'Extremely High' ? 'extremely-high' : ''}">${job.chance} Chance</span>
                    </div>
                    <h3>${job.title}</h3>
                    <div class="job-company">${job.company}</div>
                </div>

                <div class="card-body">
                    <p class="fit-text"><strong>Why it fits:</strong> ${job.fits}</p>
                    <p class="tip-text"><strong>Strategy Tip:</strong> ${job.tip}</p>
                </div>

                <div class="card-bottom">
                    <a href="${job.url}" target="_blank" class="apply-btn">Apply Now ↗</a>
                    <select class="status-dropdown" data-status="${status}" data-index="${originalIndex}">
                        <option value="Not Applied" ${status === 'Not Applied' ? 'selected' : ''}>Not Applied</option>
                        <option value="Applied" ${status === 'Applied' ? 'selected' : ''}>Applied</option>
                        <option value="Interviewing" ${status === 'Interviewing' ? 'selected' : ''}>Interviewing</option>
                        <option value="Offered" ${status === 'Offered' ? 'selected' : ''}>Offered 🎉</option>
                        <option value="Rejected" ${status === 'Rejected' ? 'selected' : ''}>Rejected</option>
                    </select>
                </div>
            `;

            // Append Card
            jobGrid.appendChild(card);
        });

        // Add Event Listeners to Dropdowns
        document.querySelectorAll('.status-dropdown').forEach(dropdown => {
            dropdown.addEventListener('change', (e) => {
                const index = parseInt(e.target.getAttribute('data-index'));
                const newStatus = e.target.value;
                const job = jobs[index];
                setJobStatus(job, index, newStatus);
            });
        });
    }

    // Filter Change Event Listeners
    searchInput.addEventListener('input', renderJobs);
    typeFilter.addEventListener('change', renderJobs);
    chanceFilter.addEventListener('change', renderJobs);
    categoryFilter.addEventListener('change', renderJobs);
    statusFilter.addEventListener('change', renderJobs);

    // Reset Button Event Listener
    resetBtn.addEventListener('click', () => {
        searchInput.value = '';
        typeFilter.value = 'all';
        chanceFilter.value = 'all';
        categoryFilter.value = 'all';
        statusFilter.value = 'all';
        renderJobs();
    });

    // View Toggles
    gridViewBtn.addEventListener('click', () => {
        currentView = 'grid';
        jobGrid.classList.remove('list-view');
        gridViewBtn.classList.add('active');
        listViewBtn.classList.remove('active');
        renderJobs();
    });

    listViewBtn.addEventListener('click', () => {
        currentView = 'list';
        jobGrid.classList.add('list-view');
        listViewBtn.classList.add('active');
        gridViewBtn.classList.remove('active');
        renderJobs();
    });
});
