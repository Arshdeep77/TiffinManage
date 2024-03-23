$(document).ready(function () {




    var getCustomersElement = document.getElementById('get-customers');

    var delCustomersElement = document.getElementById('delete-customers');
    var url = getCustomersElement.getAttribute('data-url');
    var delUrl = delCustomersElement.getAttribute('data-url');

    var staticData = [
        { "name": "John Doe", "email": "john@example.com", "phone": "1234567890", "service": "Service A", "payment": "$100", "start_date": "2022-01-01", "end_date": "2022-01-31" },
        { "name": "Jane Smith", "email": "jane@example.com", "phone": "9876543210", "service": "Service B", "payment": "$200", "start_date": "2022-02-01", "end_date": "2022-02-28" }
    ];


    $('#customer-table').DataTable({
        "ajax": {
            "url": url,
            "type": "GET",
            "dataSrc": ""
        },
        "columns": [
            {
                "data": null, "render": function (data, type, row, meta) {
                    // Render SNo column with row index starting from 1
                    return meta.row + 1;
                }
            },
            { "data": "name" },
            { "data": "phone" },
            { "data": "package" },
            { "data": "roti" },
            { "data": "dry" },
            { "data": "gravy" },
            { "data": "address" },
            { "data": "note" },
            { "data": "payment" },
            // { "data": "start_date" },
            { "data": "end_date" },

            {
                "data": null,
                "render": function (data, type, row) {

                    return '<div class="action-buttons btn-group-vertical">' +
                        '<button class="btn btn-primary btn-sm edit-btn mb-2" data-row=\'' + JSON.stringify(row) + '\'>Edit</button>' +
                        '<button class="btn btn-success btn-sm detail-btn mb-2" data-row=\'' + JSON.stringify(row) + '\'>Details</button>' +
                        '<button class="btn btn-danger btn-sm delete-btn mb-2" data-id="' + row.id + '">Delete</button>' +

                        '</div>';


                }
            }


        ],
        "createdRow": function (row, data, dataIndex) {
            // Apply CSS to cells with long text to allow word wrapping
            $('td', row).css('word-wrap', 'break-word');
        },
        columnDefs: [
            {

                targets: [7, 8], // Replace with the index of your address column
                render: function (data, type, row) {
                    if (type === 'display' && data) {
                        // Truncate the text if it is too long
                        var truncated = data.length > 10 ? data.substr(0, 10) + '...' : data;
                        // Return cell content with a Bootstrap tooltip
                        return '<span data-bs-toggle="tooltip" data-bs-placement="top" title="' + data + '">' + truncated + '</span>';
                    }
                    return data; // For other types, return the data unaltered
                },


            },


        ], drawCallback: function (settings) {
            // Initialize Bootstrap tooltips after each table draw event
            $('[data-bs-toggle="tooltip"]').tooltip();
        },
        "rowCallback": function (row, data, index) {
            var today = new Date();
            var expiryDate = new Date(data.end_date);
            today.setHours(0, 0, 0, 0);
            expiryDate.setHours(0, 0, 0, 0);


            // Calculate the difference in days
            var timeDiff = expiryDate.getTime() - today.getTime();
            var dayDiff = Math.floor(timeDiff / (1000 * 3600 * 24));

            if (dayDiff < 1) {
                console.log(today, data.end_date, dayDiff);
                // Expired
                $(row).css({
                    "background-color": "#F78F84", // Bootstrap's alert-danger background color
                    "color": "#721c24", // Bootstrap's alert-danger text color
                });
            }
            else if (dayDiff <= 2) {
                // Expiring in 5 days
                $(row).css({
                    "background-color": "#fff3cd", // Bootstrap's alert-warning background color
                    "color": "#856404", // Bootstrap's alert-warning text color
                });
            } else {
                // More than 5 days remaining
                $(row).css({
                    "background-color": "#d4edda", // Bootstrap's alert-success background color
                    "color": "#155724", // Bootstrap's alert-success text color
                });
            }
            console.log(data.name, dayDiff, data.payment);
            if (dayDiff >= 0 && data.payment == 0) {
                $(row).css({
                    "background-color": "#FFA768", // Bootstrap's alert-success background color
                    // Bootstrap's alert-success text color
                });
            }
        },

    });

    $('#customer-table').on('click', '.delete-btn', function () {
        var id = $(this).data('id'); // Get the ID from the data-id attribute of the delete button
        // Set the ID in the modal form action attribute
        var form = document.getElementById('deleteForm');

        form.action = delUrl + 'delete/' + id + '/';


        // Open the modal
        var modal = new bootstrap.Modal(document.getElementById('deleteModal'));
        modal.show();
    });
    $('#customer-table').on('click', '.edit-btn', function () {
        // Get the ID from the data-id attribute of the delete button
        // Set the ID in the modal form action attribute
        $('#addCustomerModalLabel').text('Update Customer');
        var form = document.getElementById('addCustomerForm');
        var formData = $(this).data('row');
        var id = formData.id;
        $('#name').val(formData.name);
        $('#address').val(formData.address);
        $('#note').val(formData.note);
        $('#drt').val(formData.dry);
        $('#gravy').val(formData.gravy);
        $('#roti').val(formData.roti);
        $('#phone').val(formData.phone);
        $('#named').val(formData.named);
        $('#regular').val(formData.regular);
        $('#payment').val(formData.payment);
        $('#start_date').val(formData.start_date);
        $('#end_date').val(formData.end_date);
        $('#route').val(formData.route);
        $('#position').val(formData.position);

        populateTiffinUI(formData.tiffins);

        form.action = delUrl + 'update/' + id + '/';


        // Open the modal
        var modal = new bootstrap.Modal(document.getElementById('addCustomerModal'));
        modal.show();
    });
    $('#customer-table').on('click', '.detail-btn', function () {
        // Get the ID from the data-id attribute of the delete button
        // Set the ID in the modal form action attribute

        $('#addCustomerModalLabel').text('Update Customer');
        var form = document.getElementById('addCustomerForm');
        form.reset();
        let data = $(this).data('row');
        var id = data.id;
        form.reset();
        $('#detail-name').text(data.name);
        $('#detail-phone').text(data.phone);
        $('#detail-package').text(data.package);
        $('#detail-regular').text(data.regular);
        $('#detail-named').text(data.named);
        $('#detail-roti').text(data.roti);
        $('#detail-gravy').text(data.gravy);
        $('#detail-dry').text(data.dry);
        $('#detail-note').text(data.note);
        $('#detail-address').text(data.address);
        $('#detail-start-date').text(data.start_date);
        $('#detail-end-date').text(data.end_date);
        

        form.action = delUrl + 'update/' + id + '/';


        // Open the modal
        var modal = new bootstrap.Modal(document.getElementById('customerDetailModal'));
        modal.show();
    });

    function populateTiffinUI(tiffinData) {
        var entries = [];
        let count = 0;
        tiffinData.forEach(function (tiffin) {
            var tiffinEntry = $(".tiffin-entry").first().clone();
            tiffinEntry.find("input[name='roti[]']").val(tiffin.roti);
            tiffinEntry.find("input[name='dry[]']").val(tiffin.dry);
            tiffinEntry.find("input[name='gravy[]']").val(tiffin.gravy);
            tiffinEntry.find("select[name='tiffin[]']").val(tiffin.type);
            tiffinEntry.find("select[name='rice[]']").val(tiffin.rice);
            entries.push(tiffinEntry);
            count++;
        });



        if (count) {
            $("#tiffinEntries").empty();
            entries.forEach(function (tiffin) {
                $("#tiffinEntries").append(tiffin);
                count++;
            });
            $("#tiffinEntries").show();
        }


        // Update remove buttons state
        updateRemoveButtons();
    }
    function updateRemoveButtons() {
        var entries = $(".tiffin-entry");
        if (entries.length === 1) {
            entries.find(".remove-tiffin-entry").prop("disabled", true);
        } else {
            entries.find(".remove-tiffin-entry").prop("disabled", false);
        }
    }
    function resetForm() {
        $("#tiffinEntries").hide();
        // Reset the form fields
        var form = document.getElementById('addCustomerForm');
        form.reset();
    }

    $('#add-button').click(function() {
        // Your code to execute when the button is clicked
        console.log('Button clicked');
        resetForm();
    });

});