function window_open(href, width, height){
    window.open(href,'','Toolbar=0,Location=0,Directories=0,Status=0,Menubar=1,Scrollbars=0,Resizable=0 width=' + width + ',height=' + height + ',left=' + ((window.innerWidth - width)/2) + ',top=' + ((window.innerHeight - height)/2))
}

function show(state, href){
    document.getElementById('window').style.display = state;
    document.getElementById('wrap').style.display = state;
    $('.content').load(href);
    //$('.content').append('<p>***</p>');
}


window.addEventListener("load", function(){
    document.getElementById("mTab").addEventListener("click", function(e){
        var elem = e.target || e.srcElement, field = document.createElement("input");
        // alert(elem.cellIndex);
        if (elem.cellIndex == "3") {
            field.type = "number"
            field.value = elem.innerHTML;
            temp = elem.innerHTML;
            elem.innerHTML = "";
            elem.appendChild(field);
            field.focus();
            //console.log('listeners');

            flag = false;

            field.addEventListener("focusout",function(event){
                if (flag == false) {
                    //elem.innerHTML = this.value;
                    elem.innerHTML = temp;
                    //this.parentNode.removeChild(this);
                    //console.log('Blur used');
                    //console.log(event);
                }
            });
            field.addEventListener("keydown",function(event){
                flag = true;
                if(event.which == 13){
                    //alert(elem.attributes.id.value);
                    //alert(this.value);
                    elem.innerHTML = this.value;
                    //console.log('Enter pressed');
                    //console.log(event);
                    //this.parentNode.removeChild(this);
                    a_url = "update_record/"
                    a_data = "id="+ elem.attributes.id.value + "&type=" + elem.attributes.class.value + "&amount="+this.value;

                    //console.log(a_data);
                    var time = performance.now();



                    $.ajax({ type: "GET",
                        url: a_url,
                        data: a_data,
                        success: function(data){
                            alert( "Прибыли данные: " + data );
                            elem.innerHTML = data;

                            //$('.ajax').html($('.ajax input').val());
                            //$('.ajax').removeClass('ajax');
                        },
                        error: function(data){
                            alert("ERROR. Response: "+data.value);
                        }

                    });
                    console.log(performance.now() - time);


                }
                flag = false;
            });


        }
    });
});



//определяем нажатие кнопки на клавиатуре
$('td.edit').keydown(function(event){
    arr = $(this).attr('class').split( " " );
    //проверяем какая была нажата клавиша и если была нажата клавиша Enter (код 13)
    alert(event.which)
    if(event.which == 13)
    {

        var table = $('table').attr('id');
        //выполняем ajax запрос методом POST
        $.ajax({ type: "POST",
            url:"update_cell.php",
            data: "value="+$('.ajax input').val()+"&id="+arr[2]+"&field="+arr[1]+"&table="+table,
            success: function(data){
                $('.ajax').html($('.ajax input').val());
                $('.ajax').removeClass('ajax');
            }});
    }});