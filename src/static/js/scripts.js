/*!
* Start Bootstrap - Blog Home v5.0.8 (https://startbootstrap.com/template/blog-home)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-home/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
//import { DatePicker } from '@syncfusion/ej2-calendars';
//import { loadCultureFiles } from '../common/culture-loader';

$(document).ready(function(){

    $('#button-search').click(function(){
        let value = $('#input-search').val()
        console.log(value)

        $.ajax({
            url: "/news/content_filter",
            type: 'GET',
            data: {
                str: value
            },
            success: function(data) {
                let htmlString = ''
                 $.each(data, function (i, v) {
                   
                    htmlString+=`

                    <div class="card mb-3">
                    <div class="row no-gutters">
                    <div class="col-md-4">
                        <a href="view_new/${v._id}">
                            <img src="${v.img}" class="card-img mx-3 mt-3" alt="Foto de la noticia ${v.title} " >
                        </a>
                        <a href="${v.url}">
                            <button type="button m-2" class="btn btn-secondary card-img mx-3 mb-1"> Ver más </button>
                        </a>
                    </div>
                    
                    <div class="col-md-8">
                        <div class="card-body">
                        <h5 class="card-title">${v.title}</h5>
                        <p class="line-clamp"> ${v.content} </p>
                        
    
                        <div class="row">
                            <div class="col-12 col-md-8">
                                <p class="card-text mt-3"><small class="text-muted">${v.date}</small></p>
                            </div>
                            <div class="col-6 col-md-4">
                                <p class="card-text mt-3"><small class="text-muted">${v.np}</small></p>
                            </div>
                          </div>
                        </div>
                    </div>
                    </div>
                </div>

                            
                `
                })


                $('#list_filter').html(htmlString);

                
            },
            error : function(xhr, status) {
                alert("Ha ocurrido un error: " + xhr.status + " " + xhr.statusText);
            },
        })
    });


    

    $('#deletebd').click(function(){
        let value = $('#deletebd').val()
        let confirmAction = confirm("Se borrarán todas las noticias que hay en la Base de Datos");
        if (confirmAction) {
            $(function () {
                $.ajax({
                    url: "/delete",
                    type: 'DELETE',
                    success: function() {
                        alert("Base de datos eliminada con éxito")
                    },
                    error : function(xhr, status) {
                        alert("Ha ocurrido un error: " + xhr.status + " " + xhr.statusText);
                    },
                })
            });
        }
    })

    $('#updatebd').click(function(){
        let value = $('#updatebd').val()
        let confirmAction = confirm("La Base de Datos se actualizará");
        if (confirmAction) {
            $(function () {
                $.ajax({
                    url: "/update",
                    type: 'PUT',
                    success: function() {
                        alert("Base de datos actualizada")
                    },
                    error : function(xhr, status) {
                        alert("Ha ocurrido un error: " + xhr.status + " " + xhr.statusText);
                    },
                })
            });
        }
    })

    
    $('#searchInput').change(function(){
        let date = $(this).val();
        console.log(date)
        
        $.ajax({
            url: "news_date",
            type: 'GET',
            data: {
                start: date
            },
            success: function(data) {

               alert("bien")
            },
            error : function(xhr, status) {
                alert("Ha ocurrido un error: " + xhr.status + " " + xhr.statusText);
            },
        })



    })
   

    $('#nuevaexpresion').change(function(){
        let value = $(this).val()
        console.log(value)
        
        $.ajax({
            url: "bow/addre",
            type: 'GET',
            data: {
                re: value
            },
            success: function(data) {
                alert("Expresión añadida correctamente");
                alert("Las noticias que se encuentre a partir de ahora, contendrán esta nueva palabra o expresión");
                window.location.href= "/bow_manage"
            },
            error : function(xhr, status) {
                alert("Ha ocurrido un error: " + xhr.status + " " + xhr.statusText);
            },
        })
    });

   
   

})


    function BorrarUsuario(value) {
        let confirmAction = confirm("Estás seguro de que deseas eliminar el usuario?");
        if (confirmAction) {
            $(function () {
                console.log(value)
                $.ajax({
                    url: "user_manage/deleteuser/"+value,
                    type: 'DELETE',
                    success: function() {
                        alert("Usuario eliminado")
                        $('#'+value).hide();
                    },
                    error : function(xhr, status) {
                        alert("Ha ocurrido un error: " + xhr.status + " " + xhr.statusText);
                    },
                })
            });
        }
    }

    function BorrarExpresion(value) {
        $(function () {
            console.log(value)
            let confirmAction = confirm("Estás seguro de que deseas eliminar la expresión "+value+"?");
            $.ajax({
                url: "bow/deletere",
                type: 'GET',
                data: {
                    re: value
                },
                success: function() {
                    alert("Expresión eliminada correctamente");
                    window.location.href= "/bow_manage"
                },
                error : function(xhr, status) {
                    alert("Ha ocurrido un error: " + xhr.status + " " + xhr.statusText);
                },
            })
        });
    }

    function AceptarSolicitud(){
        $(function (){
            alert("Se ha enviado su solicitud. Se enviarán sus datos al correo solicitado cuando se haya dado de alta su usuario. ¡GRACIAS! ");
        })
    }

    function ActualizacionNoticias(){
        let confirmAction = confirm("Estás seguro de que desea actualizar toda las noticias?. Este proceso puede tardar unos minutos.");

        if (confirmAction) {
            $(function () {
                $.ajax({
                    url: "db_manage/updateall/",
                    type: 'GET',
                    success: function() {
                        alert("Base de datos actualizada")
                    },
                    error : function(xhr, status) {
                        alert("Ha ocurrido un error: " + xhr.status + " " + xhr.statusText);
                    },
                })
            });
        }
        
    }


   
    function BusquedaDiaria(){
        let confirmAction = confirm("Desea realizar la búsqueda diaria?");

        if (confirmAction) {
            $(function () {
                $.ajax({
                    url: "news/dialy_update",
                    type: 'GET',
                    beforeSend: function(){$('#loading').show();},
                    success: function(data) {
                        alert("Búsqueda diaria realizada con éxito. Se han encontrado "+ data + " noticias publicadas desde la ultima actualización.")
                        window.location.href= "/db_manage"
                    },
                    error : function(xhr, status) {
                        alert("Ha ocurrido un error: " + xhr.status + " " + xhr.statusText);
                    },
                    complete: function(){
                        $('#loading').hide(); 
                    }
                   
                })
            });
           
        }
       
    }


    
    

   


    