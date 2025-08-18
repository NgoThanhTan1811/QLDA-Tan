// Main JavaScript for Fruit Export Management System

$(document).ready(function () {
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

    // Auto-hide alerts after 5 seconds
    $('.alert:not(.alert-permanent)').delay(5000).fadeOut();

    // Confirm delete actions
    $('.btn-delete').click(function (e) {
        if (!confirm('Bạn có chắc chắn muốn xóa item này không?')) {
            e.preventDefault();
        }
    });

    // Number formatting
    $('.format-number').each(function () {
        var num = parseFloat($(this).text());
        if (!isNaN(num)) {
            $(this).text(num.toLocaleString('vi-VN'));
        }
    });

    // Currency formatting
    $('.format-currency').each(function () {
        var num = parseFloat($(this).text());
        if (!isNaN(num)) {
            $(this).text(num.toLocaleString('vi-VN') + ' đ');
        }
    });

    // Date formatting
    $('.format-date').each(function () {
        var dateStr = $(this).text();
        var date = new Date(dateStr);
        if (!isNaN(date.getTime())) {
            $(this).text(date.toLocaleDateString('vi-VN'));
        }
    });

    // Loading states for forms
    $('form').submit(function () {
        $(this).find('button[type="submit"]').prop('disabled', true).html(
            '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Đang xử lý...'
        );
    });

    // Dynamic search
    $('.search-input').on('input', function () {
        var searchTerm = $(this).val().toLowerCase();
        var targetTable = $(this).data('target');

        $(targetTable + ' tbody tr').each(function () {
            var rowText = $(this).text().toLowerCase();
            if (rowText.indexOf(searchTerm) === -1) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });
});

// Utility functions
const Utils = {
    // Format number with Vietnamese locale
    formatNumber: function (num) {
        return num.toLocaleString('vi-VN');
    },

    // Format currency
    formatCurrency: function (num) {
        return num.toLocaleString('vi-VN') + ' đ';
    },

    // Format date
    formatDate: function (dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleDateString('vi-VN');
    },

    // Show toast notification
    showToast: function (message, type = 'info') {
        const toastHtml = `
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">${message}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;

        if (!$('#toast-container').length) {
            $('body').append('<div id="toast-container" class="toast-container position-fixed top-0 end-0 p-3"></div>');
        }

        const $toast = $(toastHtml);
        $('#toast-container').append($toast);

        const toast = new bootstrap.Toast($toast[0]);
        toast.show();
    },

    // Confirm action
    confirm: function (message, callback) {
        if (confirm(message)) {
            callback();
        }
    },

    // AJAX form submission
    submitForm: function (form, successCallback) {
        const $form = $(form);
        const formData = new FormData(form);

        $.ajax({
            url: $form.attr('action'),
            method: $form.attr('method') || 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.success) {
                    Utils.showToast(response.message || 'Thao tác thành công!', 'success');
                    if (successCallback) successCallback(response);
                } else {
                    Utils.showToast(response.message || 'Có lỗi xảy ra!', 'danger');
                }
            },
            error: function () {
                Utils.showToast('Có lỗi kết nối xảy ra!', 'danger');
            }
        });
    }
};

// Chart configurations
const ChartConfig = {
    // Default chart options
    defaultOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                font: {
                    size: 16,
                    weight: 'bold'
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function (value) {
                        return value.toLocaleString('vi-VN');
                    }
                }
            }
        }
    },

    // Create revenue chart
    createRevenueChart: function (ctx, data) {
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Doanh thu',
                    data: data.data,
                    borderColor: 'rgb(44, 90, 160)',
                    backgroundColor: 'rgba(44, 90, 160, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                ...ChartConfig.defaultOptions,
                plugins: {
                    ...ChartConfig.defaultOptions.plugins,
                    title: {
                        ...ChartConfig.defaultOptions.plugins.title,
                        text: 'Doanh thu theo tháng'
                    }
                }
            }
        });
    },

    // Create orders chart
    createOrdersChart: function (ctx, data) {
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    backgroundColor: [
                        '#2c5aa0',
                        '#198754',
                        '#ffc107',
                        '#dc3545',
                        '#6c757d',
                        '#0dcaf0'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    },
                    title: {
                        display: true,
                        text: 'Đơn hàng theo trạng thái',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                }
            }
        });
    },

    // Create products chart
    createProductsChart: function (ctx, data) {
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Số lượng bán',
                    data: data.data,
                    backgroundColor: 'rgba(44, 90, 160, 0.8)',
                    borderColor: 'rgb(44, 90, 160)',
                    borderWidth: 1
                }]
            },
            options: {
                ...ChartConfig.defaultOptions,
                plugins: {
                    ...ChartConfig.defaultOptions.plugins,
                    title: {
                        ...ChartConfig.defaultOptions.plugins.title,
                        text: 'Sản phẩm bán chạy'
                    }
                },
                scales: {
                    ...ChartConfig.defaultOptions.scales,
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });
    }
};

// Export to global scope
window.Utils = Utils;
window.ChartConfig = ChartConfig;
