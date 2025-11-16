/**
 * RMMS Professional - Production-Grade JavaScript Helpers
 * Phase 1 Implementation: Professional UI/UX Enhancements
 * Created: October 21, 2025
 */

// ================================================================
// CONFIGURATION
// ================================================================

// Toastr Configuration
toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": true,
    "progressBar": true,
    "positionClass": "toast-top-right",
    "preventDuplicates": true,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};

// SweetAlert2 Theme Configuration
const SwalTheme = Swal.mixin({
    customClass: {
        confirmButton: 'btn btn-primary btn-lg mx-2',
        cancelButton: 'btn btn-secondary btn-lg mx-2',
        denyButton: 'btn btn-danger btn-lg mx-2'
    },
    buttonsStyling: false,
    reverseButtons: true
});

// ================================================================
// RMMS OBJECT - Namespace for all RMMS functions
// ================================================================

window.RMMS = window.RMMS || {};

// ================================================================
// TOAST NOTIFICATIONS
// ================================================================

RMMS.Toast = {
    /**
     * Show success toast notification
     * @param {string} message - Message to display
     * @param {string} title - Optional title
     */
    success: function(message, title = 'Success') {
        toastr.success(message, title);
    },

    /**
     * Show info toast notification
     * @param {string} message - Message to display
     * @param {string} title - Optional title
     */
    info: function(message, title = 'Info') {
        toastr.info(message, title);
    },

    /**
     * Show warning toast notification
     * @param {string} message - Message to display
     * @param {string} title - Optional title
     */
    warning: function(message, title = 'Warning') {
        toastr.warning(message, title);
    },

    /**
     * Show error toast notification
     * @param {string} message - Message to display
     * @param {string} title - Optional title
     */
    error: function(message, title = 'Error') {
        toastr.error(message, title);
    }
};

// ================================================================
// SWEETALERT2 - PROFESSIONAL ALERTS
// ================================================================

RMMS.Alert = {
    /**
     * Confirm delete action
     * @param {Object} options - Configuration object
     * @returns {Promise} - SweetAlert2 promise
     */
    confirmDelete: function(options = {}) {
        const defaults = {
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'No, cancel',
            customClass: {
                confirmButton: 'btn btn-danger btn-lg mx-2',
                cancelButton: 'btn btn-secondary btn-lg mx-2'
            }
        };

        return SwalTheme.fire({ ...defaults, ...options });
    },

    /**
     * Show success message
     * @param {Object} options - Configuration object
     */
    success: function(options = {}) {
        const defaults = {
            title: 'Success!',
            text: 'Operation completed successfully',
            icon: 'success',
            confirmButtonText: 'OK'
        };

        return SwalTheme.fire({ ...defaults, ...options });
    },

    /**
     * Show error message
     * @param {Object} options - Configuration object
     */
    error: function(options = {}) {
        const defaults = {
            title: 'Error!',
            text: 'Something went wrong. Please try again.',
            icon: 'error',
            confirmButtonText: 'OK'
        };

        return SwalTheme.fire({ ...defaults, ...options });
    },

    /**
     * Show info message
     * @param {Object} options - Configuration object
     */
    info: function(options = {}) {
        const defaults = {
            title: 'Information',
            text: '',
            icon: 'info',
            confirmButtonText: 'OK'
        };

        return SwalTheme.fire({ ...defaults, ...options });
    },

    /**
     * Show warning message
     * @param {Object} options - Configuration object
     */
    warning: function(options = {}) {
        const defaults = {
            title: 'Warning',
            text: '',
            icon: 'warning',
            confirmButtonText: 'OK'
        };

        return SwalTheme.fire({ ...defaults, ...options });
    },

    /**
     * Show confirmation dialog
     * @param {Object} options - Configuration object
     */
    confirm: function(options = {}) {
        const defaults = {
            title: 'Are you sure?',
            text: '',
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Yes',
            cancelButtonText: 'No'
        };

        return SwalTheme.fire({ ...defaults, ...options });
    },

    /**
     * Show loading indicator
     * @param {string} title - Loading message
     */
    loading: function(title = 'Processing...') {
        Swal.fire({
            title: title,
            allowOutsideClick: false,
            allowEscapeKey: false,
            allowEnterKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
    },

    /**
     * Close current alert
     */
    close: function() {
        Swal.close();
    }
};

// ================================================================
// FORM HELPERS
// ================================================================

RMMS.Form = {
    /**
     * Show loading state on submit button
     * @param {jQuery} $button - Button element
     */
    showLoading: function($button) {
        $button.prop('disabled', true);
        $button.data('original-text', $button.html());
        $button.html('<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processing...');
    },

    /**
     * Hide loading state on submit button
     * @param {jQuery} $button - Button element
     */
    hideLoading: function($button) {
        $button.prop('disabled', false);
        $button.html($button.data('original-text'));
    },

    /**
     * Validate form before submission
     * @param {jQuery} $form - Form element
     * @returns {boolean} - Valid or not
     */
    validate: function($form) {
        // Add Bootstrap validation classes
        $form.addClass('was-validated');
        return $form[0].checkValidity();
    },

    /**
     * Reset form and remove validation classes
     * @param {jQuery} $form - Form element
     */
    reset: function($form) {
        $form[0].reset();
        $form.removeClass('was-validated');
    }
};

// ================================================================
// DELETE CONFIRMATION HELPER
// ================================================================

/**
 * Global delete confirmation
 * @param {string} url - Delete URL
 * @param {string} itemName - Name of item being deleted
 * @param {Function} onSuccess - Callback on successful delete
 */
RMMS.confirmDelete = function(url, itemName = 'this item', onSuccess) {
    RMMS.Alert.confirmDelete({
        title: `Delete ${itemName}?`,
        text: `Are you sure you want to delete ${itemName}? This action cannot be undone.`
    }).then((result) => {
        if (result.isConfirmed) {
            // Show loading
            RMMS.Alert.loading('Deleting...');

            // Perform delete
            $.ajax({
                url: url,
                type: 'POST',
                data: {
                    __RequestVerificationToken: $('input[name="__RequestVerificationToken"]').val()
                },
                success: function(response) {
                    RMMS.Alert.close();
                    RMMS.Alert.success({
                        title: 'Deleted!',
                        text: `${itemName} has been deleted successfully.`
                    }).then(() => {
                        if (onSuccess) {
                            onSuccess(response);
                        } else {
                            location.reload();
                        }
                    });
                },
                error: function(xhr) {
                    RMMS.Alert.close();
                    RMMS.Alert.error({
                        title: 'Error!',
                        text: xhr.responseText || 'Failed to delete. Please try again.'
                    });
                }
            });
        }
    });
};

// ================================================================
// AJAX HELPERS
// ================================================================

RMMS.Ajax = {
    /**
     * POST request with loading and error handling
     * @param {Object} options - Configuration
     */
    post: function(options) {
        const defaults = {
            url: '',
            data: {},
            loadingMessage: 'Processing...',
            successMessage: 'Operation completed successfully',
            errorMessage: 'An error occurred. Please try again.',
            onSuccess: null,
            onError: null
        };

        const config = { ...defaults, ...options };

        RMMS.Alert.loading(config.loadingMessage);

        $.ajax({
            url: config.url,
            type: 'POST',
            data: config.data,
            success: function(response) {
                RMMS.Alert.close();
                RMMS.Toast.success(config.successMessage);

                if (config.onSuccess) {
                    config.onSuccess(response);
                }
            },
            error: function(xhr) {
                RMMS.Alert.close();
                RMMS.Toast.error(xhr.responseText || config.errorMessage);

                if (config.onError) {
                    config.onError(xhr);
                }
            }
        });
    }
};

// ================================================================
// INITIALIZATION
// ================================================================

$(document).ready(function() {
    console.log('🚀 RMMS Professional Loaded - Phase 1');

    // Initialize AOS (Animate On Scroll)
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        mirror: false
    });

    // Initialize Select2 on all select elements with class 'select2'
    $('.select2').select2({
        theme: 'bootstrap-5',
        width: '100%'
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle delete buttons with data-delete-url attribute
    $(document).on('click', '[data-delete-url]', function(e) {
        e.preventDefault();
        const $this = $(this);
        const url = $this.data('delete-url');
        const itemName = $this.data('item-name') || 'this item';

        RMMS.confirmDelete(url, itemName);
    });

    // Show success message from TempData
    if (window.tempDataSuccess) {
        RMMS.Toast.success(window.tempDataSuccess);
    }

    // Show error message from TempData
    if (window.tempDataError) {
        RMMS.Toast.error(window.tempDataError);
    }

    // Add form submit loading state
    $('form[data-loading]').on('submit', function() {
        const $form = $(this);
        const $submitBtn = $form.find('button[type="submit"]');

        if (RMMS.Form.validate($form)) {
            RMMS.Form.showLoading($submitBtn);
        }
    });

    console.log('✅ All professional features initialized');
});

// ================================================================
// EXAMPLE USAGE IN VIEWS
// ================================================================

/*

// Toast Notifications:
RMMS.Toast.success('Record saved successfully!');
RMMS.Toast.info('Processing your request...');
RMMS.Toast.warning('Low stock alert!');
RMMS.Toast.error('Failed to save record');

// SweetAlert2 Confirmations:
RMMS.Alert.confirmDelete({
    title: 'Delete Farmer?',
    text: 'This will also delete all associated records'
}).then((result) => {
    if (result.isConfirmed) {
        // Delete logic
    }
});

// Success Alert:
RMMS.Alert.success({
    title: 'Saved!',
    text: 'Production batch created successfully'
});

// Simple Delete (auto-handled):
<button class="btn btn-danger"
        data-delete-url="/Farmers/Delete/123"
        data-item-name="Farmer John Doe">
    <i class="fas fa-trash"></i> Delete
</button>

// Advanced Select2:
<select class="form-select select2" name="FarmerId">
    <option>Choose Farmer...</option>
</select>

// Animated Elements:
<div data-aos="fade-up">Content will fade up on scroll</div>

*/
