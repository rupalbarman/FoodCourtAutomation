$(document).ready(function() {

    $('#registerButton').click(function() {
        resetHiddenFields();
        var data = {};
        data['username'] = $('#username').val();
        data['password'] = $('#password').val();

        $.ajax({
            type: 'POST',
            url: '/api/login',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            success: function(callback) {
                console.log(callback);
                if (callback.status == 'signup')
                    alert('Signed up ' + callback.username);
                else
                    alert('Logged in ' + callback.username);
            },
            error: function() {
                $('#messageDiv').html("error!");
            }
        });
    });

    function resetHiddenFields() {
        $('#selectedRestaurentId').val('');
    }

    $('#table1 tbody tr').on('click', '#viewMenuButton', function(e) {
        // clear old data first but not selected restaurent id
        $('#itemCounter').val('1');
        $("#selectedItem").val('');
        $('#selectedItemCount').val('');
        $('#selectedItemId').val('');
        $('#selectedItemPrice').val('');
        $("#spnMenuText").html('');

        var restaurent_id = $(e.target).closest('tr').find('td:first').text();

        if ($('#selectedRestaurentId').val() == '') {
            $('#selectedRestaurentId').val(restaurent_id);
        } else if ($('#selectedRestaurentId').val() != restaurent_id) {
            alert('Complete your order from restaurent ' + $('#selectedRestaurentId').val() + ' first');
            return;
        }

        $.ajax({
            type: 'GET',
            url: '/api/get_restaurents/' + restaurent_id,
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function(callback) {
                console.log(callback);
                populateMenuTable(callback);
            },
            error: function() {
                $('#messageDiv').html("error!");
            }
        });

        $('#menuItemModal').modal({show:true});
    });

    function populateMenuTable(result) {
        var tr = '';
        for (var i=0; i<result['menu'][0]['items'].length; i++) {
            tr = tr.concat('<tr><td>' + result['menu'][0]['items'][i]['id'] + '</td><td>'+ result['menu'][0]['items'][i]['name'] + '</td><td>' + result['menu'][0]['items'][i]['price'] + '</td></tr>')
        }
        $("#table2 tbody").html(tr);
    }

    $("#table2").on('click', 'tr:has(td)', function(e) {
        $("#table2 td").removeClass("highlight");
        var clickedCell = $(e.target).closest("tr");
        clickedCell.addClass("highlight");
        //save the value in hidden field
        $("#selectedItemId").val(clickedCell.find('td:first').text());
        $("#selectedItem").val(clickedCell.find('td').eq(1).text());
        $("#selectedItemPrice").val(clickedCell.find('td:last').text());
        $("#spnMenuText").html(
          'Selected: <b> ' + clickedCell.find('td:first').text() + ' ' + clickedCell.find('td').eq(1).text() + '</b>');
    });

    // add to cart button is this
    $('#proceedMenuItemButton').click(function(){
        // get count of last item added
        $('#selectedItemCount').val($('#itemCounter').val());
        if($("#selectedItemId").val().trim() == '') {
            // avoid empty addition to cart
            alert('Empty addition not allowed');
            return;
        }

        addToCartTable($('#selectedRestaurentId').val(), $("#selectedItemId").val(), $("#selectedItem").val(), $("#selectedItemPrice").val(), $('#selectedItemCount').val())

        $('#menuItemModal').modal('toggle');
    });

    function addToCartTable(restaurent_id, item_id, item, price, count) {
        var template = "<tr><td>" + restaurent_id + "</td><td>" + item_id + "</td><td>" + item + "</td><td>" + price + "</td><td>" + count + "</td></tr>";
        $('#cartTable tbody').append(template);
    }

    $('#showCartButton').click(function() {
        $('#cartModal').modal({show:true});
    });

    $('#checkoutButton').click(function() {
        if ($("#cartTable tbody").html().trim() == '') {
            alert("Cannot perform empty checkout");
            return;
        }
        var username = $('#welcomeTag').text().replace('Welcome', '').trim();
        var input = {};
        input['username'] = username;
        input['items'] = [];
        var table = $("#cartTable > tbody")[0];
        var i = 0;
        item_count = {};
        $("#cartTable > tbody > tr").each(function() {
            var restaurent_id = $(table.rows[i].cells[0]).text();
            var item_id = $(table.rows[i].cells[1]).text();
            var count = $(table.rows[i].cells[4]).text();
            var item = $(table.rows[i].cells[2]).text();
            var price = $(table.rows[i].cells[3]).text();

            if (item_count[item_id]) {
               item_count[item_id] += Number(count);
            } else {
               item_count[item_id] = Number(count);
            }

            i++;
        });
        Object.keys(item_count).forEach(function(key) {
            input['items'].push({ 'itemId' : key, 'count' : item_count[key] });
        });
        console.log('Before ordering ' + JSON.stringify(input));

        //reset all - ie, clear all hidden vals, cartTable
        clearCartAndHiddenVals();

        $.ajax({
            type: 'POST',
            url: '/api/checkout',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(input),
            success: function(callback) {
                console.log(callback);
            },
            error: function() {
                $('#messageDiv').html("error!");
            }
        });
        
        $('#cartModal').modal({show:false});
    });

    function clearCartAndHiddenVals() {
        $('#itemCounter').val('1');
        $("#selectedItem").val('');
        $('#selectedItemCount').val('');
        $('#selectedItemId').val('');
        $('#selectedItemPrice').val('');
        $("#spnMenuText").html('');
        $('#selectedRestaurentId').val('');
        $("#cartTable > tbody").html('');
    }

    $('#ordersTable').on('click', '#statusCheckButton', function(e) {
        var invoice = $(e.target).closest("tr").find('td:first').text();

        $.ajax({
            type: 'GET',
            url: '/api/check_order_status/' + invoice,
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function(callback) {
                console.log(callback);
                alert('Orders before yours is ' + callback.status);
            },
            error: function() {
                $('#messageDiv').html("error!");
            }
        });
    });

    $('#ordersTable').on('click', '#orderDetailButton', function(e) {
        var invoice = $(e.target).closest("tr").find('td:first').text();

        $.ajax({
            type: 'GET',
            url: '/api/get_order_details/' + invoice,
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function(callback) {
                console.log(callback);
                alert('Order details ' + callback.order);
            },
            error: function() {
                $('#messageDiv').html("error!");
            }
        });
    });
});