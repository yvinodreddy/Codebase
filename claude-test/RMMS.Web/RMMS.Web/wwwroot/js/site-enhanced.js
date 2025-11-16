/* ================================================================
   RMMS Web Application - Enhanced JavaScript
   Version: 1.0
   Date: 2025-10-01
   Description: DataTables initialization and responsive behaviors
   ================================================================ */

(function ($) {
    'use strict';

    // ============================================================
    // DATATABLE INITIALIZATION
    // ============================================================

    /**
     * Initialize DataTables with Microsoft-style configuration
     * Enabled with client-side pagination and sorting for all grids
     */
    function initializeDataTables() {
        console.info('Initializing DataTables with pagination and sorting...');

        // Check if DataTable plugin is available
        if (!$.fn.DataTable) {
            console.warn('DataTables plugin not loaded');
            return;
        }

        // Find all tables with class 'ms-datatable'
        $('.ms-datatable').each(function () {
            var $table = $(this);

            // Skip if already initialized - destroy and reinitialize to prevent errors
            if ($.fn.DataTable.isDataTable($table)) {
                $table.DataTable().destroy();
            }

            // Get custom options from data attributes
            var pageLength = $table.data('page-length') || 16;
            var ordering = $table.data('ordering') !== false;
            var searching = $table.data('searching') !== false;
            var paging = $table.data('paging') !== false;

            // Initialize DataTable
            var dataTable = $table.DataTable({
                // Display settings
                pageLength: pageLength,
                lengthMenu: [[10, 16, 25, 50, 100, -1], [10, 16, 25, 50, 100, "All"]],

                // Feature control
                ordering: ordering,
                searching: searching,
                paging: paging,
                info: true,
                autoWidth: false,

                // Responsive settings
                responsive: {
                    details: {
                        type: 'column',
                        target: 'tr'
                    }
                },

                // Column definitions
                columnDefs: [
                    {
                        // Set first column as high priority
                        responsivePriority: 1,
                        targets: 0
                    },
                    {
                        // Set last column (usually actions) as high priority
                        responsivePriority: 2,
                        targets: -1
                    }
                ],

                // DOM layout
                dom: "<'dataTables_top'<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>>" +
                     "<'ms-table-container'tr>" +
                     "<'dataTables_bottom'<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>>",

                // Language customization
                language: {
                    search: "Search:",
                    searchPlaceholder: "Type to search...",
                    lengthMenu: "Show _MENU_ entries",
                    info: "Showing _START_ to _END_ of _TOTAL_ entries",
                    infoEmpty: "Showing 0 to 0 of 0 entries",
                    infoFiltered: "(filtered from _MAX_ total entries)",
                    paginate: {
                        first: "First",
                        last: "Last",
                        next: "Next",
                        previous: "Previous"
                    },
                    emptyTable: "No data available in table",
                    zeroRecords: "No matching records found"
                },

                // State saving
                stateSave: true,
                stateDuration: 60 * 60 * 24, // 24 hours

                // Order by first column descending by default
                order: [[0, 'desc']],

                // Callbacks
                drawCallback: function (settings) {
                    // Re-initialize tooltips after draw
                    initializeTooltips();
                },

                initComplete: function (settings, json) {
                    // Add custom class to wrapper
                    $(this).closest('.dataTables_wrapper').addClass('ms-datatable-wrapper');
                }
            });

            // Add export buttons if enabled
            if ($table.data('export') === true) {
                new $.fn.dataTable.Buttons(dataTable, {
                    buttons: [
                        {
                            extend: 'copy',
                            text: '<i class="fas fa-copy"></i> Copy',
                            className: 'ms-btn ms-btn-secondary ms-btn-sm'
                        },
                        {
                            extend: 'excel',
                            text: '<i class="fas fa-file-excel"></i> Excel',
                            className: 'ms-btn ms-btn-success ms-btn-sm'
                        },
                        {
                            extend: 'pdf',
                            text: '<i class="fas fa-file-pdf"></i> PDF',
                            className: 'ms-btn ms-btn-danger ms-btn-sm'
                        },
                        {
                            extend: 'print',
                            text: '<i class="fas fa-print"></i> Print',
                            className: 'ms-btn ms-btn-secondary ms-btn-sm'
                        }
                    ]
                });

                dataTable.buttons().container()
                    .prependTo($table.closest('.dataTables_wrapper').find('.dataTables_top'));
            }
        });
    }

    // ============================================================
    // FORM ENHANCEMENTS
    // ============================================================

    /**
     * Initialize form validation styling
     */
    function initializeFormValidation() {
        $('form').on('submit', function () {
            $(this).find('.ms-form-control').each(function () {
                var $input = $(this);

                // Check HTML5 validity
                if (this.checkValidity && !this.checkValidity()) {
                    $input.addClass('is-invalid');
                } else {
                    $input.removeClass('is-invalid').addClass('is-valid');
                }
            });
        });

        // Real-time validation
        $('.ms-form-control').on('blur', function () {
            var $input = $(this);

            if (this.checkValidity && !this.checkValidity()) {
                $input.addClass('is-invalid');
            } else {
                $input.removeClass('is-invalid');
            }
        });

        // Remove validation on input
        $('.ms-form-control').on('input', function () {
            $(this).removeClass('is-invalid is-valid');
        });
    }

    // ============================================================
    // NAVIGATION ENHANCEMENTS
    // ============================================================

    /**
     * Mobile navigation toggle
     */
    function initializeMobileNav() {
        $('.ms-navbar-toggle').on('click', function () {
            var $collapse = $('.ms-navbar-collapse');
            $collapse.toggleClass('show');

            // Update aria attributes
            var expanded = $collapse.hasClass('show');
            $(this).attr('aria-expanded', expanded);
        });

        // Close mobile menu when clicking outside
        $(document).on('click', function (e) {
            var $navbar = $('.ms-navbar');
            if (!$navbar.is(e.target) && $navbar.has(e.target).length === 0) {
                $('.ms-navbar-collapse').removeClass('show');
                $('.ms-navbar-toggle').attr('aria-expanded', 'false');
            }
        });
    }

    // ============================================================
    // TOOLTIPS
    // ============================================================

    /**
     * Initialize Bootstrap tooltips
     */
    function initializeTooltips() {
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }

    // ============================================================
    // CARD INTERACTIONS
    // ============================================================

    /**
     * Card hover effects
     */
    function initializeCardEffects() {
        $('.ms-card-interactive').on('click', function () {
            var href = $(this).data('href');
            if (href) {
                window.location.href = href;
            }
        });
    }

    // ============================================================
    // STICKY HEADER
    // ============================================================

    /**
     * Sticky navigation on scroll
     */
    function initializeStickyHeader() {
        var $navbar = $('.ms-navbar');
        var navbarOffset = $navbar.offset() ? $navbar.offset().top : 0;

        $(window).on('scroll', function () {
            if ($(window).scrollTop() > navbarOffset) {
                $navbar.addClass('sticky').css('box-shadow', '0 6.4px 14.4px rgba(0,0,0,0.132)');
            } else {
                $navbar.removeClass('sticky').css('box-shadow', '0 1.6px 3.6px rgba(0,0,0,0.132)');
            }
        });
    }

    // ============================================================
    // CONFIRM DIALOGS
    // ============================================================

    /**
     * Confirmation dialog for delete actions
     */
    function initializeConfirmDialogs() {
        $('[data-confirm]').on('click', function (e) {
            var message = $(this).data('confirm') || 'Are you sure you want to proceed?';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    }

    // ============================================================
    // AUTO-CALCULATION HELPERS
    // ============================================================

    /**
     * Initialize auto-calculation on forms
     * Usage: Add data-calc="sum" data-calc-fields="field1,field2" data-calc-target="result"
     */
    function initializeAutoCalculation() {
        $('[data-calc]').each(function () {
            var $target = $(this);
            var calcType = $target.data('calc');
            var fields = ($target.data('calc-fields') || '').split(',');
            var targetField = $target.data('calc-target');

            if (!targetField || fields.length === 0) return;

            var $targetInput = $('#' + targetField);

            // Calculate function
            var calculate = function () {
                var values = [];
                var valid = true;

                fields.forEach(function (field) {
                    var val = parseFloat($('#' + field.trim()).val()) || 0;
                    if (isNaN(val)) valid = false;
                    values.push(val);
                });

                if (!valid) return;

                var result = 0;
                switch (calcType) {
                    case 'sum':
                        result = values.reduce(function (a, b) { return a + b; }, 0);
                        break;
                    case 'multiply':
                        result = values.reduce(function (a, b) { return a * b; }, 1);
                        break;
                    case 'subtract':
                        result = values[0] - values[1];
                        break;
                    case 'divide':
                        result = values[1] !== 0 ? values[0] / values[1] : 0;
                        break;
                }

                $targetInput.val(result.toFixed(2));
            };

            // Bind to input fields
            fields.forEach(function (field) {
                $('#' + field.trim()).on('input change', calculate);
            });
        });
    }

    // ============================================================
    // DATE PICKER INITIALIZATION
    // ============================================================

    /**
     * Initialize date pickers with proper format
     */
    function initializeDatePickers() {
        $('input[type="date"]').each(function () {
            // Add placeholder if not present
            if (!$(this).attr('placeholder')) {
                $(this).attr('placeholder', 'YYYY-MM-DD');
            }
        });
    }

    // ============================================================
    // LOADING INDICATOR
    // ============================================================

    /**
     * Show loading indicator on form submit
     */
    function initializeLoadingIndicator() {
        $('form').on('submit', function () {
            var $form = $(this);

            // Don't show loader if form is invalid
            if (!this.checkValidity || this.checkValidity()) {
                var $submitBtn = $form.find('button[type="submit"], input[type="submit"]');
                $submitBtn.prop('disabled', true);
                $submitBtn.html('<i class="fas fa-spinner fa-spin"></i> Processing...');

                // Re-enable after 5 seconds as fallback
                setTimeout(function () {
                    $submitBtn.prop('disabled', false);
                    $submitBtn.html($submitBtn.data('original-text') || 'Submit');
                }, 5000);
            }
        });
    }

    // ============================================================
    // RESPONSIVE TABLE HELPERS
    // ============================================================

    /**
     * Add horizontal scroll hint for tables
     */
    function initializeTableScrollHint() {
        $('.ms-table-responsive').each(function () {
            var $container = $(this);
            var $table = $container.find('table');

            if ($table.width() > $container.width()) {
                $container.addClass('has-scroll');

                // Add scroll hint
                if (!$container.find('.scroll-hint').length) {
                    $container.append('<div class="scroll-hint"><i class="fas fa-arrow-left"></i> Scroll <i class="fas fa-arrow-right"></i></div>');
                }
            }
        });
    }

    // ============================================================
    // UTILITIES
    // ============================================================

    /**
     * Format number with Indian number system (lakhs/crores)
     */
    window.formatIndianNumber = function (num) {
        var x = num.toString();
        var lastThree = x.substring(x.length - 3);
        var otherNumbers = x.substring(0, x.length - 3);
        if (otherNumbers != '')
            lastThree = ',' + lastThree;
        return otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThree;
    };

    /**
     * Format currency (INR)
     */
    window.formatCurrency = function (amount) {
        return '₹' + window.formatIndianNumber(amount);
    };

    /**
     * Debounce function for search inputs
     */
    window.debounce = function (func, wait) {
        var timeout;
        return function executedFunction() {
            var context = this;
            var args = arguments;
            var later = function () {
                clearTimeout(timeout);
                func.apply(context, args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    };

    // ============================================================
    // DOCUMENT READY
    // ============================================================

    $(document).ready(function () {
        console.log('RMMS Enhanced JavaScript initialized');

        // Initialize all components
        initializeDataTables();
        initializeFormValidation();
        initializeMobileNav();
        initializeTooltips();
        initializeCardEffects();
        initializeStickyHeader();
        initializeConfirmDialogs();
        initializeAutoCalculation();
        initializeDatePickers();
        initializeLoadingIndicator();
        initializeTableScrollHint();

        // Add smooth scrolling
        $('a[href^="#"]').on('click', function (e) {
            var target = $(this.getAttribute('href'));
            if (target.length) {
                e.preventDefault();
                $('html, body').stop().animate({
                    scrollTop: target.offset().top - 80
                }, 500);
            }
        });

        // Print button handler
        $('.btn-print').on('click', function (e) {
            e.preventDefault();
            window.print();
        });

        // Back to top button
        if ($('.back-to-top').length) {
            $(window).scroll(function () {
                if ($(this).scrollTop() > 100) {
                    $('.back-to-top').fadeIn();
                } else {
                    $('.back-to-top').fadeOut();
                }
            });

            $('.back-to-top').click(function () {
                $('html, body').animate({ scrollTop: 0 }, 500);
                return false;
            });
        }
    });

    // ============================================================
    // WINDOW RESIZE HANDLER
    // ============================================================

    var resizeTimeout;
    $(window).on('resize', function () {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function () {
            // Reinitialize table scroll hints
            initializeTableScrollHint();

            // Trigger DataTables responsive recalculation
            if ($.fn.DataTable) {
                $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
            }
        }, 250);
    });

})(jQuery);

/* ================================================================
   END OF ENHANCED JAVASCRIPT
   ================================================================ */
