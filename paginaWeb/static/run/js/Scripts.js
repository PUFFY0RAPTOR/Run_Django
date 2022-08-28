//function fechacorrect(){
    //var v1 = (document.getElementById('f1').value);
    
    //alert (v1);
    //recorrer texto 
//}


function cookieSesion() {
    let v1 = document.getElementById("iniciarSesion1").value
    let v2 = document.getElementById("contrasena1").value

    primera = sessionStorage.getItem("nameSession").value;
    if (primera == "null" || primera == null){
        //alert("No has iniciado sesion, deberias de hacerlo")
        if (v1 == "mateo.220@hotmail.com" && v2 == "1234"){
            sessionStorage.setItem("nameSession", v1);//aqui en vez de definir las variables v1 y v2 puedo poner los  codigos directamente
            sessionStorage.setItem("passSession", v2);
            window.open('usuarios/indexUsuario.html', "_self");
        }
    }  
}

function interface(){

    primera = sessionStorage.getItem("nameSession").value;
    if (primera != "null"){ //esto esta malo
        console.log(primera);
        //alert("inicio de sesion exitoso")
        window.open('usuarios/indexUsuario.html', "_self");

    }
}

function closeSession(){

    sessionStorage.setItem("nameSession", "null");
    sessionStorage.setItem("passSession", "null");
    //alert("cierre de sesion exitoso")
    window.open('../index.html', "_self");
    
<<<<<<< HEAD
    //Soy Sebas probando Django
=======
    //Soy Sebas
    //soy mateo
>>>>>>> master
}