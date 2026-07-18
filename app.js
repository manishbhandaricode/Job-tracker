document.addEventListener('DOMContentLoaded', () => {
    // --- Authentication Logic ---
    const loginOverlay = document.getElementById('login-overlay');
    const loginPassword = document.getElementById('login-password');
    const loginBtn = document.getElementById('login-btn');
    const loginError = document.getElementById('login-error');

    const savedPwd = localStorage.getItem('admin_pwd');
    if (savedPwd) {
        verifyPassword(savedPwd, true);
    }

    loginBtn.addEventListener('click', () => {
        const pwd = loginPassword.value;
        if (pwd) verifyPassword(pwd, false);
    });

    async function verifyPassword(pwd, isAutoLogin) {
        if (!isAutoLogin) loginBtn.textContent = 'Verifying...';
        try {
            const res = await fetch('/api/authenticate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password: pwd })
            });
            const data = await res.json();
            if (res.ok) {
                localStorage.setItem('admin_pwd', pwd);
                loginOverlay.classList.add('hidden');
                initDashboard();
            } else {
                if (!isAutoLogin) {
                    loginError.textContent = data.error || 'Incorrect password';
                    loginError.style.display = 'block';
                } else {
                    localStorage.removeItem('admin_pwd');
                }
            }
        } catch (err) {
            if (!isAutoLogin) {
                loginError.textContent = 'Network error. Please try again.';
                loginError.style.display = 'block';
            }
        } finally {
            if (!isAutoLogin) loginBtn.textContent = 'Unlock Dashboard';
        }
    }

    function initDashboard() {
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
        const locationTypeFilter = document.getElementById('location-type-filter');
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

    // Generate a stable key independent of array index
    function getJobKey(job) {
        const c = (job.company || '').replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
        const t = (job.title || '').replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
        return `job-status-${c}-${t}`;
    }

    // Initialize statuses in localStorage if not already present
    function initializeStatuses() {
        jobs.forEach((job, index) => {
            // Check for legacy index-based key and migrate if exists
            const legacyKey = `job-status-${index}-${job.company.replace(/\s+/g, '-')}`;
            const newKey = getJobKey(job);
            
            if (localStorage.getItem(legacyKey)) {
                localStorage.setItem(newKey, localStorage.getItem(legacyKey));
                localStorage.removeItem(legacyKey); // Clean up old key
            }
            
            if (!localStorage.getItem(newKey)) {
                localStorage.setItem(newKey, 'Not Applied');
            }
        });
    }

    // Get status from localStorage
    function getJobStatus(job) {
        return localStorage.getItem(getJobKey(job)) || 'Not Applied';
    }

    // Set status in localStorage
    function setJobStatus(job, status) {
        localStorage.setItem(getJobKey(job), status);
        updateStats();
        renderJobs(); // Re-render to apply new filters if active
    }

    // Update Stats Summary Header
    function updateStats() {
        let total = jobs.length;
        let applied = 0;
        let pending = 0;

        jobs.forEach((job) => {
            const status = getJobStatus(job);
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
        const locType = locationTypeFilter ? locationTypeFilter.value : 'all';

        return jobs.filter((job) => {
            const status = getJobStatus(job);
            
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
                
            // Location Type Filter
            const matchesLocType = locType === 'all' || job.type === locType;

            return matchesQuery && matchesType && matchesChance && matchesCategory && matchesStatus && matchesLocType;
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

        filtered.forEach((job, idx) => {
            const status = getJobStatus(job);

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
                    <div class="company-date-row">
                        <div class="job-company">${job.company}</div>
                        <div class="job-date">Added: ${job.date_discovered || 'Legacy'}</div>
                    </div>
                    <div class="job-location" style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;">📍 ${job.location || 'India'} (${job.type || 'Remote'})</div>
                </div>

                <div class="card-body">
                    <p class="fit-text"><strong>Why it fits:</strong> ${job.fits}</p>
                    <p class="tip-text"><strong>Strategy Tip:</strong> ${job.tip}</p>
                </div>

                <div class="card-bottom">
                    <a href="${job.url}" target="_blank" class="apply-btn">Apply Now ↗</a>
                    <select class="status-dropdown" data-status="${status}" data-company="${job.company}" data-title="${job.title}">
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
                const company = e.target.getAttribute('data-company');
                const title = e.target.getAttribute('data-title');
                const newStatus = e.target.value;
                const job = jobs.find(j => j.company === company && j.title === title);
                if (job) {
                    setJobStatus(job, newStatus);
                }
            });
        });
    }

    // Filter Change Event Listeners
    searchInput.addEventListener('input', renderJobs);
    typeFilter.addEventListener('change', renderJobs);
    chanceFilter.addEventListener('change', renderJobs);
    categoryFilter.addEventListener('change', renderJobs);
    statusFilter.addEventListener('change', renderJobs);
    if(locationTypeFilter) locationTypeFilter.addEventListener('change', renderJobs);

    // Reset Button Event Listener
    resetBtn.addEventListener('click', () => {
        searchInput.value = '';
        typeFilter.value = 'all';
        chanceFilter.value = 'all';
        categoryFilter.value = 'all';
        statusFilter.value = 'all';
        if(locationTypeFilter) locationTypeFilter.value = 'all';
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
    } // end of initDashboard
});

// --- Settings Modal Logic ---
document.addEventListener('DOMContentLoaded', () => {
    const settingsBtn = document.getElementById('settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const savePrefsBtn = document.getElementById('save-prefs-btn');
    const prefKeywordsInput = document.getElementById('pref-keywords');
    const prefProfileInput = document.getElementById('pref-profile');
    const saveStatus = document.getElementById('save-status');

    let currentPreferences = { keywords: [], profile: '' };

    if (!settingsBtn) return; // safety check

    // Open modal and fetch current preferences
    settingsBtn.addEventListener('click', async () => {
        settingsModal.classList.add('active');
        saveStatus.textContent = 'Loading current preferences...';
        saveStatus.style.color = 'var(--text-muted)';
        
        try {
            const response = await fetch('preferences.json');
            if (response.ok) {
                currentPreferences = await response.json();
                prefKeywordsInput.value = currentPreferences.keywords.join(', ');
                prefProfileInput.value = currentPreferences.profile;
                saveStatus.textContent = '';
            } else {
                saveStatus.textContent = 'Could not load preferences.json';
            }
        } catch (error) {
            console.error(error);
            saveStatus.textContent = 'Error loading preferences locally.';
        }
    });

    // Close modal
    closeModalBtn.addEventListener('click', () => {
        settingsModal.classList.remove('active');
    });

    // Save preferences to Vercel API -> GitHub
    savePrefsBtn.addEventListener('click', async () => {
        const newKeywords = prefKeywordsInput.value.split(',').map(k => k.trim()).filter(k => k);
        const newProfile = prefProfileInput.value.trim();

        if (!newKeywords.length || !newProfile) {
            saveStatus.textContent = 'Fields cannot be empty.';
            saveStatus.style.color = '#f87171'; // red
            return;
        }

        savePrefsBtn.textContent = 'Saving...';
        savePrefsBtn.disabled = true;
        saveStatus.textContent = 'Pushing to GitHub...';
        saveStatus.style.color = 'var(--text-muted)';

        try {
            const res = await fetch('/api/update-preferences', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    profile: newProfile,
                    keywords: newKeywords,
                    password: localStorage.getItem('admin_pwd')
                })
            });

            const data = await res.json();
            
            if (res.ok) {
                saveStatus.textContent = '✅ Saved! AI is now using new rules.';
                saveStatus.style.color = '#4ade80'; // green
                setTimeout(() => { settingsModal.classList.remove('active'); }, 2000);
            } else {
                saveStatus.textContent = `❌ Error: ${data.error}`;
                saveStatus.style.color = '#f87171';
            }
        } catch (error) {
            saveStatus.textContent = `❌ Network Error: ${error.message}`;
            saveStatus.style.color = '#f87171';
        } finally {
            savePrefsBtn.textContent = 'Save to GitHub';
            savePrefsBtn.disabled = false;
        }
    });
});
