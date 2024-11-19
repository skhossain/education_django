$('#id_class_id').select2({placeholder: " Select a Class "})
$('#id_academic_year_id').select2({placeholder: " Select a Year "})

// exam_term
function show_marge_term_result(){
    let class_id = $('#id_class_id').val()
    let academic_year_id = $('#id_academic_year_id').val()
    let header_title = $('#id_title').val()
    let exam_terms = document.querySelectorAll(".exam_term");
    let terms=[]
    exam_terms.forEach(term => {
        if(term.checked){
            terms.push(term.value)
        }
    });
    window.open('/edu-published-result-marge-view?academic_year='+academic_year_id+'&class_id='+class_id+'&terms='+terms+'&header_title='+header_title+'','_blank');
}