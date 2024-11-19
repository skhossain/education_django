$('#id_student_id').select2({
    ajax: {
      url: '/apiedu-studentinfo-api/',
      data: function (params) {
        var query = {
          student_name: params.term,
        }
        // Query parameters will be ?search=[term]&type=public
        return query;
      },
      processResults: function (data) {
        // Transforms the top-level key of the response object from 'items' to 'results'
        console.log(data)
        return {
            results: $.map(data, function (item) {
                return {
                    text: item.student_name,
                    value:item.student_roll,
                    id: item.student_roll
                }
            })
        };
        
      }
    }
  });
