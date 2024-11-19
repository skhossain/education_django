function question_enable(button,id){
    
    $.ajax({
        url: 'edu-submitted-questionLive/'+id,
        type: 'get',
        success: function (data) {
            console.log(data)
            $(button). attr("disabled", true);
            var b =$(button).parent().parent().children('.publish_status')
            b.text('Live')
        }            
    });
}

