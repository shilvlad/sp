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
        //alert(elem.cellIndex);
        if (elem.cellIndex == "3" && elem.tagName == "TD") {

            field.type = "number"
            field.style.width = "100"
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
                    elem.innerHTML = this.value;
                    a_url = "update_record/"
                    a_data = "id="+ elem.attributes.id.value + "&type=" + elem.attributes.class.value + "&amount="+this.value;

                    var time = performance.now();



                    $.ajax({ type: "GET",
                        url: a_url,
                        data: a_data,
                        success: function(data){
                            var xmlDoc = $.parseXML( data );
                            elem.innerHTML = $(xmlDoc).find( "field" ).text();

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
        if (elem.cellIndex == "2" && elem.tagName == "TD") {

            field.type = "text"
            field.style.width = "300"
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
                    elem.innerHTML = this.value;

                    a_url = "update_comment/"
                    a_data = "id="+ elem.attributes.id.value + "&type=" + elem.attributes.class.value + "&comment=" + this.value;

                    var time = performance.now();



                    $.ajax({ type: "GET",
                        url: a_url,
                        data: a_data,
                        success: function(data){
                            var xmlDoc = $.parseXML( data );
                            elem.innerHTML = $(xmlDoc).find( "field" ).text();

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



