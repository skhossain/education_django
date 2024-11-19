//Sidebar menu
$(function(){
    var current = location.pathname;
    $('#stacked-menu li a').each(function(){
        var $this = $(this);
        // if the current path is like this link, make it active
        if($this.attr('href').indexOf(current) !== -1){
            $this.addClass('has-active active-color');
            // this.parent().addClass('has-active');
            $this.parents('.has-child').addClass('has-open has-active')
        }
    })
    
})


let myPromise = new Promise(function(myResolve, myReject) {
// "Producing Code" (May take some time)

  myResolve(); // when successful
  myReject();  // when error
});

// "Consuming Code" (Must wait for a fulfilled Promise)
myPromise.then(
  function(value) { /* code if successful */ },
  function(error) { /* code if some error */ }
);
function print_div_data(divName) {
            var promise = new Promise(function (resolve,reject) {
            var divContents = document.getElementById(divName).innerHTML;
            var title = document.getElementById('print_title').value;
            var host="http://"+window.location.host+"/static/assets/stylesheets/custom.css" 
            var a = window.open('', '', 'height=3508, width=2480');
            a.document.write('<html><head>');
            a.document.write('<title>'+title+'</title>');
            a.document.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">');
            a.document.write('<link rel="stylesheet" href='+host+'>');
            a.document.write('</head><body>');
            a.document.write(divContents);
            a.document.write('</body></html>');
            a.document.close();
            if(a.document){
              resolve(a)
            }else{
              reject(("It is a failure lode print window."));
            }
          // setTimeout(() => {
            //   a.print();
            // }, 500);

            });
            return promise;
            
        }
function print_div(div){
  print_div_data(div).then(x=>{
    setTimeout(() => {
     x.print()
    }, 500);
    x.onafterprint = x.close;  
  }).catch(err=> {
  alert("Error: " + err);
})
}
      
function modal_close(c){
  $('#'+c).modal('hide')
}
function off_future_date(id){
    var dtToday = new Date();
    var month = dtToday.getMonth() + 1;
    var day = dtToday.getDate();
    var year = dtToday.getFullYear();
    if(month < 10)
        month = '0' + month.toString();
    if(day < 10)
        day = '0' + day.toString();

    var maxDate = year + '-' + month + '-' + day;    
    $('#'+id).attr('max', maxDate);
}
//Loder
function loder_Spinner(val){
  if(val){
      Swal.fire({
          imageUrl: '/static/assets/images/ajax/Spinner.gif',
          showConfirmButton: false,   
        })          
  }else{
      swal.close()
  }
}