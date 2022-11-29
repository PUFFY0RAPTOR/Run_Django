//function fechacorrect(){
    //var v1 = (document.getElementById('f1').value);
    
    //alert (v1);
    //recorrer texto 
//}
function confirmarEliminar(url){
    if (confirm("¿Estás seguro?")){
        location.href = url;
    }
}

function contador(url, contador){
    const valorFuncion = async () =>{
        try{
            const response = await fetch(url);
            const data = await response.json();
            if(data.message==="success"){
                alert("Agregado correctamente")
                let carrito = document.getElementById('contador_carrito').innerHTML
                carrito = parseInt(carrito) + 1
                document.getElementById('contador_carrito').innerHTML = carrito
            }else{
                alert("Hubo un error")
            }
        }catch (error) {
            console.log(error)
        }
    }
    valorFuncion();
    //aqui se agrega el producto al carrito sin recargar la pagina, y luego se agrega el nuevo valor
    //al contador del carrito, el cual funciona al recargar la pagina, pero si se esto no ocurriera y pudiera
    //modificar ese contador con ajax entonces, y solo entonces, obtendria luego el valor de este y lo cambiaria y luego
    //lo corrijo
    //let contador1 = document.getElementById('contador_carrito').innerHTML
    //let newContador = parseInt(contador1)
    //console.log("Este es el contador: ", newContador+100)
    //document.getElementById('contador_carrito').innerHTML = newContador;
    //location.href = url;
    //console.log(contador)
    //dato = $('#dato').val();
    //resultado = $('#respuesta');
    //token = $('input[name="csrfmiddlewaretoken"]').val();
    //console.log("Token:" + token);

    //$.ajax({
    //    url: url,
    //    type: 'get',
        //data: { "dato": dato, "csrfmiddlewaretoken": token},
        //dataType: 'json',
   //     success: function(respuesta){
            //console.log(respuesta);
   //     },
    //    error: function(error){
           // console.log("Error" + error);
     //   }



}
// function cookieSesion() {
//     let v1 = document.getElementById("iniciarSesion1").value
//     let v2 = document.getElementById("contrasena1").value

//     primera = sessionStorage.getItem("nameSession").value;
//     if (primera == "null" || primera == null){
//         //alert("No has iniciado sesion, deberias de hacerlo")
//         if (v1 == "mateo.220@hotmail.com" && v2 == "1234"){
//             sessionStorage.setItem("nameSession", v1);//aqui en vez de definir las variables v1 y v2 puedo poner los  codigos directamente
//             sessionStorage.setItem("passSession", v2);
//             window.open('usuarios/indexUsuario.html', "_self");
//         }
//     }  
// }

// function interface(){

//     primera = sessionStorage.getItem("nameSession").value;
//     if (primera != "null"){ //esto esta malo
//         console.log(primera);
//         //alert("inicio de sesion exitoso")
//         window.open('usuarios/indexUsuario.html', "_self");

//     }
// }


// function closeSession(){

//     sessionStorage.setItem("nameSession", "null");
//     sessionStorage.setItem("passSession", "null");
//     //alert("cierre de sesion exitoso")
//     window.open('../index.html', "_self");
    

//     //uno mas
// }