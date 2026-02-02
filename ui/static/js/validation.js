/**
 * CEPAC UI - Parameter Validation
 * Client-side validation functions for form inputs
 */

/**
 * Validate a single input field
 */
function validateInput(input) {
    const tab = input.dataset.tab;
    const param = input.dataset.param;
    const value = input.type === 'checkbox' ? input.checked :
                  input.type === 'number' ? parseFloat(input.value) :
                  input.value;

    const errors = [];

    // Type-specific validation
    if (input.type === 'number') {
        if (isNaN(value)) {
            errors.push('Must be a valid number');
        }

        const min = input.min !== '' ? parseFloat(input.min) : null;
        const max = input.max !== '' ? parseFloat(input.max) : null;

        if (min !== null && value < min) {
            errors.push(`Must be at least ${min}`);
        }
        if (max !== null && value > max) {
            errors.push(`Must be at most ${max}`);
        }
    }

    // Parameter-specific validation
    const validator = paramValidators[`${tab}.${param}`];
    if (validator) {
        const paramErrors = validator(value, input);
        errors.push(...paramErrors);
    }

    // Update UI
    if (errors.length > 0) {
        input.classList.add('invalid');
        input.title = errors.join('\n');
    } else {
        input.classList.remove('invalid');
        input.title = '';
    }

    return errors;
}

/**
 * Parameter-specific validators
 */
const paramValidators = {
    'runspecs.numCohorts': (value) => {
        const errors = [];
        if (value <= 0) {
            errors.push('Cohort size must be positive');
        }
        if (value < 1000) {
            // This is a warning, not an error
        }
        return errors;
    },

    'runspecs.discountFactor': (value) => {
        const errors = [];
        if (value < 0) {
            errors.push('Discount factor cannot be negative');
        }
        if (value > 0.2) {
            // Warning: unusually high discount rate
        }
        return errors;
    },

    'cohort.initialCD4Mean': (value) => {
        const errors = [];
        if (value <= 0) {
            errors.push('Initial CD4 mean must be positive');
        }
        return errors;
    },

    'cohort.initialCD4StdDev': (value) => {
        const errors = [];
        if (value < 0) {
            errors.push('Standard deviation cannot be negative');
        }
        return errors;
    },

    'cohort.maleGenderDistribution': (value) => {
        const errors = [];
        if (value < 0 || value > 1) {
            errors.push('Proportion must be between 0 and 1');
        }
        return errors;
    },

    'treatment.clinicVisitInterval': (value) => {
        const errors = [];
        if (value < 1) {
            errors.push('Visit interval must be at least 1 month');
        }
        return errors;
    }
};

/**
 * Validate all inputs in a tab
 */
function validateTab(tabId) {
    const tabContent = document.getElementById('tab-' + tabId);
    if (!tabContent) return [];

    const allErrors = [];
    tabContent.querySelectorAll('[data-tab][data-param]').forEach(input => {
        const errors = validateInput(input);
        if (errors.length > 0) {
            allErrors.push({
                param: `${input.dataset.tab}.${input.dataset.param}`,
                errors: errors
            });
        }
    });

    return allErrors;
}

/**
 * Validate all parameters
 */
function validateAllInputs() {
    const allErrors = [];

    document.querySelectorAll('[data-tab][data-param]').forEach(input => {
        const errors = validateInput(input);
        if (errors.length > 0) {
            allErrors.push({
                param: `${input.dataset.tab}.${input.dataset.param}`,
                errors: errors
            });
        }
    });

    return allErrors;
}

/**
 * Check if distributions sum to 1 (or close to 1)
 */
function validateDistribution(inputs, tolerance = 0.001) {
    let sum = 0;
    inputs.forEach(input => {
        sum += parseFloat(input.value) || 0;
    });

    return Math.abs(sum - 1.0) <= tolerance;
}

/**
 * Initialize validation on form load
 */
document.addEventListener('DOMContentLoaded', function() {
    // Add blur validation to all inputs
    document.querySelectorAll('[data-tab][data-param]').forEach(input => {
        input.addEventListener('blur', function() {
            validateInput(this);
        });
    });
});
