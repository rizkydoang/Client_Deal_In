function Update_Item(id_item) {
    document.getElementById('id').value = document.getElementById(id_item + '_updt_id_item').value
    document.getElementById('item').value = document.getElementById(id_item + '_updt_name').value
    document.getElementById('qty').value = document.getElementById(id_item + '_updt_quantity').value
    document.getElementById('category').value = document.getElementById(id_item + '_updt_id_category').value
    document.getElementById('desc').value = document.getElementById(id_item + '_updt_description').value
    document.getElementById('price').value = document.getElementById(id_item + '_updt_price').value

    document.getElementById('type_button').value = 'Edit'
    document.getElementById('action').value = 'update'
    document.getElementById('label').innerHTML = 'Edit Barang'
}

function Clear_Update_Item() {
    document.getElementById('id').value = ''
    document.getElementById('item').value = ''
    document.getElementById('qty').value = ''
    document.getElementById('category').value = ''
    document.getElementById('desc').value = ''
    document.getElementById('price').value = ''

    document.getElementById('type_button').value = 'Tambah'
    document.getElementById('action').value = 'post'
    document.getElementById('label').innerHTML = 'Tambah Barang'
}

(function($) {
    $.fn.inputFilter = function(inputFilter) {
        return this.on("input keydown keyup mousedown mouseup select contextmenu drop", function() {
            if (inputFilter(this.value)) {
                this.oldValue = this.value;
                this.oldSelectionStart = this.selectionStart;
                this.oldSelectionEnd = this.selectionEnd;
            } else if (this.hasOwnProperty("oldValue")) {
                this.value = this.oldValue;
                this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
            } else {
                this.value = "";
            }
        });
    };
}(jQuery));


$("#cart_qty").inputFilter(function(value) {
    return /^\d*$/.test(value); });

// function getCookie(cname) {
//     let name = cname + "=";
//     let decodedCookie = decodeURIComponent(document.cookie);
//     let ca = decodedCookie.split(';');
//     for (let i = 0; i < ca.length; i++) {
//         let c = ca[i];
//         while (c.charAt(0) == ' ') {
//             c = c.substring(1);
//         }
//         if (c.indexOf(name) == 0) {
//             return c.substring(name.length, c.length);
//         }
//     }
//     return "";
// }


// const CartItem = async (id) => {
//     const response = await fetch('http://127.0.0.1:8000/api/store/index/', {
//         method: 'GET',
//         crossorigin: true,
//         headers: {
//             "Access-Control-Allow-Origin": "*",
//             'Content-Type': 'text/plain'
//         },
//     });
//     const myJson = await response.json(); //extract JSON from the http response
//     console.log(myJson);
// }

// function CartItem(id) {
//     $.ajax({
//         url: 'http://127.0.0.1:8000/api/store/item/'+id+'/',
//         type: 'GET',
//         // crossDomain: true,
//         dataType: 'json',
//         mode: 'no-cors',
//         // crossOrigin: true,
//         // async: true,
//         // contentType: 'application/json',
//         headers: {
//             "Authorization": getCookie("token_access"),
//         //     'Access-Control-Allow-Methods': '*',
//         //     "Access-Control-Allow-Credentials": true,
//         //     "Access-Control-Allow-Headers" : "Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization",
//         //     "Access-Control-Allow-Origin": "*",
//         //     "Control-Allow-Origin": "*",
//         },
//         success: function (data) {
//             console.log(data.data);

//             // var html = '';
//             // html += 
//             // '<tr class="list_item">'+
//             //     '<td><img src="'+data.data[0].photo_item+'" alt="Girl in a jacket" width="50" height="50"></td>'+
//             //     '<td>'+data.data[0].name+'</td>'+
//             //     '<td>'+data.data[0].quantity+'</td>'+
//             //     '<td>'+data.data[0].price+'</td>'+
//             //     '<td><input type="number" class="form-control" style="width: 75px;" id="qty" name="qty" min="1" value="1" placeholder="Qty"></td>'+
//             //     '<td><textarea class="form-control" style="width: 250px;" id="description" name="description" placeholder="Deskripsi"></textarea></td>'+
//             //     '<td><input type="hidden" id="id_item" name="id_item" value="'+data.data[0].id+'"></td>'+
//             //     '<td><input type="hidden" id="price" name="price" value="'+data.data[0].price+'"></td>'+
//             // '</tr>';
//             // $('#table_cart_list').html(html);
//         },
//         error: function (jqXHR, textStatus, errorThrown) {
//             console.log(textStatus, errorThrown);
//         }
//     });
// }