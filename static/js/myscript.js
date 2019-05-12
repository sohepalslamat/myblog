function check(){
        var name = document.querySelector('input[name=name]');
        var email = document.querySelector('input[name=email]');
        var password = document.querySelector('input[name=password]');

        if ( name.value == '' || email.value == '' || password.value == ''){
        button = document.querySelector('button');
        button.disabled=true;
        button.classList.add('disable_button');
        }
        else if ( name.value != '' && email.value != '' && password.value != ''){
        button.disabled=false;
        button.classList.remove('disable_button');
        }
        }