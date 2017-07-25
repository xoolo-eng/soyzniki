$('input[type=checkbox]').click(function(){
    var checkboxes = $('input[type=checkbox]').get()
    var submit = $('#form_user_add input[type=submit]').get(0)
    var disabled = true
    for (i=0; i<checkboxes.length; i++){
        if (checkboxes[i].checked == false) {
            disabled = true
        }
        else {
            disabled = false
            break
        }
    }
    if (disabled == false) {
        submit.disabled = 0;
    }
    else {
        submit.disabled = 1;
    }
});

