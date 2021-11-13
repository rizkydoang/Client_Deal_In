var check_signup = function() {
    var password = document.getElementById('password').value
    var con_password = document.getElementById('confirm_password').value
    if(password != '' || con_password != ''){
        if(password.length > 4){
            if(password == con_password){
                document.getElementById('message').style.color = 'green';
                document.getElementById('message').innerHTML = 'Matching';
                document.getElementById('submit').disabled = false;
            }else{
                document.getElementById('message').style.color = 'red';
                document.getElementById('message').innerHTML = 'Not Matching';
                document.getElementById('submit').disabled = true;
            }
        }else{
            document.getElementById('message').style.color = 'red';
            document.getElementById('message').innerHTML = 'Password Must 5 Character';
            document.getElementById('submit').disabled = true;
        }
    }else{
        document.getElementById('message').style.color = 'red';
        document.getElementById('message').innerHTML = 'Please input your password';
        document.getElementById('submit').disabled = true;
    }
}
    
var check_login_user = function() {
    var username = document.getElementById('username').value
    if(username != ''){
        if(username.length > 4){
            document.getElementById('message_user').innerHTML = '';
            document.getElementById('submit').disabled = false;
        }else{
            document.getElementById('message_user').style.color = 'red';
            document.getElementById('message_user').innerHTML = 'username must 5 Character';
            document.getElementById('submit').disabled = true;
        }
    }else{
        document.getElementById('message_user').style.color = 'red';
        document.getElementById('message_user').innerHTML = 'please input username';
    }
    
}

var check_login_pass = function() {
    var password = document.getElementById('password').value
    if(password != ''){
        if (password.length > 4){
            document.getElementById('message_pass').innerHTML = '';
            document.getElementById('submit').disabled = false;
        }else{
            document.getElementById('message_pass').style.color = 'red';
            document.getElementById('message_pass').innerHTML = 'Password must 5 Character';
            document.getElementById('submit').disabled = true;
        }
    }else{
        document.getElementById('message_pass').style.color = 'red';
        document.getElementById('message_pass').innerHTML = 'please input password';
    }
}



// function removeById(id){
//     var elem = document.getElementById(id)
//     elem.removeChild.removeChild(elem)
// }

