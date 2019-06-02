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

async function delay(delayInms) {
      return new Promise(resolve  => {
        setTimeout(() => {
          resolve(2);
        }, delayInms);
      });
    }

async function sample() {
        x=document.getElementById('load');
        for (var i=0; i<45 ; i++){
        x.innerText += " *";
        await delay(100);}
        location.href='/';
    }

async function flash(){
        y= document.getElementsByTagName('h1')[1];
        for (var i=0; i<50 ; i=i+1){
        y.classList.remove('name')
        y.classList.add('flash');
        await delay(300);
        y.classList.remove('flash');
        y.classList.add('name')
        await delay(150);
        }
    }

