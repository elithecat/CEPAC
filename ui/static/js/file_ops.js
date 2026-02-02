/**
 * CEPAC UI - File Operations
 * Handles import and export of .in files
 */

/**
 * Import a .in file
 */
function importFile(event) {
    const file = event.target.files[0];
    if (!file) return;

    // Check file extension
    if (!file.name.endsWith('.in')) {
        showToast('Please select a .in file', 'warning');
        return;
    }

    showLoading('Importing ' + file.name + '...');

    const formData = new FormData();
    formData.append('file', file);

    fetch('/api/import', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        hideLoading();

        if (result.success) {
            // Update local state and form
            currentParams = result.params;
            populateForm(result.params);
            showToast('Imported ' + file.name, 'success');
        } else {
            showToast('Import failed: ' + result.message, 'error');
        }

        // Reset file input
        event.target.value = '';
    })
    .catch(error => {
        hideLoading();
        showToast('Import error: ' + error, 'error');
        event.target.value = '';
    });
}

/**
 * Export current parameters as .in file
 */
function exportFile() {
    showLoading('Generating .in file...');

    // Ensure latest parameters are saved first
    fetch('/api/params', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentParams)
    })
    .then(() => {
        // Now trigger download
        const link = document.createElement('a');
        link.href = '/api/export';
        link.download = ''; // Let server set filename
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        hideLoading();
        showToast('File exported successfully', 'success');
    })
    .catch(error => {
        hideLoading();
        showToast('Export error: ' + error, 'error');
    });
}

/**
 * Drag and drop support for import
 */
document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.querySelector('.tab-content-container');

    if (dropZone) {
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        // Highlight drop zone when item is dragged over
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });

        // Handle dropped files
        dropZone.addEventListener('drop', handleDrop, false);
    }
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    document.querySelector('.tab-content-container').classList.add('drag-highlight');
}

function unhighlight(e) {
    document.querySelector('.tab-content-container').classList.remove('drag-highlight');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;

    if (files.length > 0) {
        const file = files[0];
        if (file.name.endsWith('.in')) {
            // Trigger import
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);

            const fileInput = document.getElementById('file-input');
            fileInput.files = dataTransfer.files;

            // Trigger change event
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        } else {
            showToast('Please drop a .in file', 'warning');
        }
    }
}

/**
 * Quick export to clipboard (JSON format)
 */
function exportToClipboard() {
    const json = JSON.stringify(currentParams, null, 2);

    navigator.clipboard.writeText(json)
        .then(() => {
            showToast('Parameters copied to clipboard', 'success');
        })
        .catch(err => {
            showToast('Failed to copy to clipboard', 'error');
        });
}

/**
 * Import from clipboard (JSON format)
 */
function importFromClipboard() {
    navigator.clipboard.readText()
        .then(text => {
            try {
                const params = JSON.parse(text);
                currentParams = params;
                populateForm(params);
                saveParameters();
                showToast('Parameters imported from clipboard', 'success');
            } catch (e) {
                showToast('Invalid JSON in clipboard', 'error');
            }
        })
        .catch(err => {
            showToast('Failed to read from clipboard', 'error');
        });
}
