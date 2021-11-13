function Update_Item(id_item) {
    document.getElementById('id').value = document.getElementById(id_item + '_updt_id_item').value
    document.getElementById('item').value = document.getElementById(id_item + '_updt_name').value
    document.getElementById('qty').value = document.getElementById(id_item + '_updt_quantity').value
    document.getElementById('category').value = document.getElementById(id_item + '_updt_id_category').value
    document.getElementById('desc').value = document.getElementById(id_item + '_updt_description').value
    document.getElementById('price').value = document.getElementById(id_item + '_updt_price').value
}

function Clear_Update_Item() {
    document.getElementById('id').value = ''
    document.getElementById('item').value = ''
    document.getElementById('qty').value = ''
    document.getElementById('category').value = ''
    document.getElementById('desc').value = ''
    document.getElementById('price').value = ''
}


function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}


function CartItem(id) {
    $.ajax({
        url: 'http://127.0.0.1:8000/api/store/item/'+id+'/',
        headers: {
            "Authorization": getCookie("token_access")
        },
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data.data[0]);

            var html = '';
            html += 
            '<tr class="list_item">'+
                '<td><img src="'+data.data[0].photo_item+'" alt="Girl in a jacket" width="50" height="50"></td>'+
                '<td>'+data.data[0].name+'</td>'+
                '<td>'+data.data[0].quantity+'</td>'+
                '<td>'+data.data[0].price+'</td>'+
                '<td><input type="number" class="form-control" style="width: 75px;" id="qty" name="qty" min="1" value="1" placeholder="Qty"></td>'+
                '<td><textarea class="form-control" style="width: 250px;" id="description" name="description" placeholder="Deskripsi"></textarea></td>'+
                '<td><input type="hidden" id="id_item" name="id_item" value="'+data.data[0].id+'"></td>'+
                '<td><input type="hidden" id="price" name="price" value="'+data.data[0].price+'"></td>'+
            '</tr>';
            $('#table_cart_list').html(html);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            swal.fire('Error Get Data', 'Please try again', 'error');
        }
    });
}