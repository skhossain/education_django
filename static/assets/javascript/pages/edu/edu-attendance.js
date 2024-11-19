function change_present(id){
    var check=$('#' + id).is(":checked")
    let present=1
    if(check){
        present=1
    }else{
        present=0
    }
    let student_roll=id.slice(1, -2);
    let day=id.slice(-2);
    let sheet_id=$('#sheet_id').val()
    $.ajax({
        url: '/edu-attendance-change/' + sheet_id,
        type: 'post',
        data:{'student_roll':student_roll,'day':day,'present':present},
        dataType: 'json',
        success: function (data) {
            console.log(data)
        }
    })
}
function change_present_all(id){
    var check=$('#' + id).is(":checked")
    let present=1
    if(check){
        present=1
    }else{
        present=0
    }
    let student_roll=null
    let day=id.slice(1,);
    let sheet_id=$('#sheet_id').val()
    $.ajax({
        url: '/edu-attendance-change/' + sheet_id,
        type: 'post',
        data:{'student_roll':student_roll,'day':day,'present':present},
        dataType: 'json',
        success: function (data) {
            if(data.success){
                location.reload()
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'All student status change in this column! Wait few second.',
                    showConfirmButton: false,
                    timer: 5000
                  })
            }
        }
    })
}
$(document).ready(function(){
    var today = new Date();
    var currentDay = today.getDate();
    var y=new Date().getFullYear(); // generate the year of specific DATE
    var m=new Date().getMonth(); // generate the month of specific DATE
    var ac_y= parseInt($('#ac_year').text())
    var ac_m = parseInt($('#ac_month').attr('data-value'))

    if (ac_y == y && ac_m == m+1){
       
    if(currentDay<10){
        currentDay='0'+String(currentDay)
    }else{
        currentDay=String(currentDay)
    }
   var student_list=document.querySelectorAll('.student')
   var days=$('#h_days').val()
   
   student_list.forEach(e => {
        element=$(e).attr('data-id')
       for (let index = 1; index < Number(days.slice(8,-1)); index++) {
           let day=index
            if(day<10){
                day='0'+String(day)
            }else{
                day=String(day)
            }
            if(currentDay === day){
                $('#p'+element+day).removeAttr('disabled')
                $('#a'+element+day).removeAttr('disabled')
                $('#d'+String(index)).removeAttr('disabled')
            }
            if(document.getElementById('a'+element+day)){
                var check=$('#d'+String(index)).is(":checked")
                if(check){
                $('#d'+String(index)).removeAttr('checked')
                }
            }
       }
   });
}
});