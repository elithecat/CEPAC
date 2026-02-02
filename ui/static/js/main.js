/**
 * CEPAC UI - Main JavaScript
 * Handles tab navigation, form management, and API communication
 */

// Global state
let currentParams = {};

// DOM ready
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    initializeToolbar();
    initializeCollapsibles();
    loadParameters();
});

/**
 * Tab Navigation
 */
function initializeTabs() {
    const tabItems = document.querySelectorAll('.tab-item');
    const tabContents = document.querySelectorAll('.tab-content');

    tabItems.forEach(item => {
        item.addEventListener('click', function() {
            const tabId = this.dataset.tab;

            // Update active states
            tabItems.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            this.classList.add('active');
            document.getElementById('tab-' + tabId).classList.add('active');
        });
    });
}

/**
 * Toolbar Actions
 */
function initializeToolbar() {
    // Validate button
    document.getElementById('btn-validate').addEventListener('click', validateParameters);

    // Run button
    document.getElementById('btn-run').addEventListener('click', runModel);

    // Import button
    document.getElementById('btn-import').addEventListener('click', function() {
        document.getElementById('file-input').click();
    });

    // File input change
    document.getElementById('file-input').addEventListener('change', importFile);

    // Export button
    document.getElementById('btn-export').addEventListener('click', exportFile);

    // Reset button
    document.getElementById('btn-reset').addEventListener('click', resetParameters);
}

/**
 * Collapsible Sections
 */
function initializeCollapsibles() {
    document.querySelectorAll('.collapsible-header').forEach(header => {
        header.addEventListener('click', function() {
            const section = this.parentElement;
            section.classList.toggle('collapsed');
        });
    });
}

/**
 * Parameter Management
 */
function loadParameters() {
    showLoading('Loading parameters...');

    fetch('/api/params')
        .then(response => response.json())
        .then(params => {
            currentParams = params;
            populateForm(params);
            hideLoading();
        })
        .catch(error => {
            hideLoading();
            showToast('Error loading parameters: ' + error, 'error');
        });
}

function populateForm(params) {
    // Iterate through all form inputs with data-tab attribute
    document.querySelectorAll('[data-tab][data-param]').forEach(input => {
        const tab = input.dataset.tab;
        const param = input.dataset.param;
        const index = input.dataset.index;
        const subparam = input.dataset.subparam;
        const subindex = input.dataset.subindex;

        if (!params[tab]) return;

        let value;

        if (index !== undefined && subparam !== undefined) {
            // Nested array with subparam: params[tab][param][index][subparam]
            const arr = params[tab][param];
            if (arr && arr[index]) {
                if (subindex !== undefined && Array.isArray(arr[index][subparam])) {
                    value = arr[index][subparam][subindex];
                } else {
                    value = arr[index][subparam];
                }
            }
        } else if (index !== undefined) {
            // Array access: params[tab][param][index]
            const arr = params[tab][param];
            if (Array.isArray(arr)) {
                value = arr[index];
            }
        } else {
            // Direct access: params[tab][param]
            value = params[tab][param];
        }

        if (value !== undefined) {
            setInputValue(input, value);
        }
    });

    // Set up change handlers
    document.querySelectorAll('[data-tab][data-param]').forEach(input => {
        input.addEventListener('change', handleInputChange);
    });
}

function setInputValue(input, value) {
    if (input.type === 'checkbox') {
        input.checked = Boolean(value);
    } else if (input.type === 'number') {
        input.value = value;
    } else {
        input.value = value;
    }
}

function handleInputChange(event) {
    const input = event.target;
    const tab = input.dataset.tab;
    const param = input.dataset.param;
    const index = input.dataset.index;
    const subparam = input.dataset.subparam;
    const subindex = input.dataset.subindex;

    let value;
    if (input.type === 'checkbox') {
        value = input.checked;
    } else if (input.type === 'number') {
        value = parseFloat(input.value) || 0;
    } else {
        value = input.value;
    }

    // Update local state
    if (!currentParams[tab]) currentParams[tab] = {};

    if (index !== undefined && subparam !== undefined) {
        if (!currentParams[tab][param]) currentParams[tab][param] = [];
        if (!currentParams[tab][param][index]) currentParams[tab][param][index] = {};
        if (subindex !== undefined) {
            if (!currentParams[tab][param][index][subparam]) {
                currentParams[tab][param][index][subparam] = [];
            }
            currentParams[tab][param][index][subparam][subindex] = value;
        } else {
            currentParams[tab][param][index][subparam] = value;
        }
    } else if (index !== undefined) {
        if (!currentParams[tab][param]) currentParams[tab][param] = [];
        currentParams[tab][param][index] = value;
    } else {
        currentParams[tab][param] = value;
    }

    // Debounced save to server
    debouncedSave();
}

// Debounce save operations
let saveTimeout = null;
function debouncedSave() {
    if (saveTimeout) clearTimeout(saveTimeout);
    saveTimeout = setTimeout(saveParameters, 500);
}

function saveParameters() {
    fetch('/api/params', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentParams)
    })
    .catch(error => {
        console.error('Error saving parameters:', error);
    });
}

/**
 * Validation
 */
function validateParameters() {
    showLoading('Validating...');

    fetch('/api/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(result => {
        hideLoading();

        if (result.valid) {
            let message = 'All parameters valid';
            if (result.warnings && result.warnings.length > 0) {
                message += '\n\nWarnings:\n- ' + result.warnings.join('\n- ');
            }
            showToast(message, 'success');
        } else {
            showToast('Validation errors:\n- ' + result.errors.join('\n- '), 'error');
        }
    })
    .catch(error => {
        hideLoading();
        showToast('Validation error: ' + error, 'error');
    });
}

/**
 * Model Execution
 */
function runModel() {
    showLoading('Running model... This may take a while.');

    fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(result => {
        hideLoading();
        displayResults(result);

        if (result.success) {
            showToast('Model completed successfully', 'success');
            // Switch to results tab
            document.querySelector('[data-tab="results"]').click();
        } else {
            showToast('Model execution failed: ' + result.message, 'error');
        }
    })
    .catch(error => {
        hideLoading();
        showToast('Error running model: ' + error, 'error');
    });
}

function displayResults(result) {
    // Update status
    const status = document.getElementById('results-status');
    if (result.success) {
        status.innerHTML = '<p style="color: #48bb78;">Model completed successfully.</p>';
    } else {
        status.innerHTML = '<p style="color: #e53e3e;">Model execution failed.</p>';
    }

    // Display output sections
    if (result.output) {
        document.getElementById('results-output-section').style.display = 'block';
        document.getElementById('results-output').textContent = result.output;
    }

    if (result.cout) {
        document.getElementById('results-cout-section').style.display = 'block';
        document.getElementById('results-cout').textContent = result.cout;
    }

    if (result.popstats) {
        document.getElementById('results-popstats-section').style.display = 'block';
        document.getElementById('results-popstats').textContent = result.popstats;
    }

    if (result.trace) {
        document.getElementById('results-trace-section').style.display = 'block';
        document.getElementById('results-trace').textContent = result.trace;
    }

    if (result.message) {
        document.getElementById('results-message-section').style.display = 'block';
        document.getElementById('results-message').textContent = result.message;
    }
}

/**
 * Reset Parameters
 */
function resetParameters() {
    if (!confirm('Reset all parameters to defaults? This cannot be undone.')) {
        return;
    }

    showLoading('Resetting...');

    fetch('/api/params/reset', { method: 'POST' })
        .then(response => response.json())
        .then(result => {
            loadParameters();
            showToast('Parameters reset to defaults', 'success');
        })
        .catch(error => {
            hideLoading();
            showToast('Error resetting: ' + error, 'error');
        });
}

/**
 * UI Helpers
 */
function showLoading(text) {
    const overlay = document.getElementById('loading-overlay');
    const loadingText = overlay.querySelector('.loading-text');
    loadingText.textContent = text || 'Processing...';
    overlay.classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.add('hidden');
}

function showToast(message, type) {
    const toast = document.getElementById('message-toast');
    toast.textContent = message;
    toast.className = 'toast ' + (type || '');
    toast.classList.remove('hidden');

    setTimeout(() => {
        toast.classList.add('hidden');
    }, 5000);
}
