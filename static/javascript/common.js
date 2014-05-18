$(document).ready(function(){

    $('.edit-meals').click(function(e){
        var meal_id = $(this).attr('data-val');
        $("#meal-"+meal_id).show();
    });

    $('.meal-submit').click(function(e){
         var url = $(this).parents('form').attr('action');
         var meals_form = $(this).parents('form').serialize();
         console.log('url is :', url, meals_form);
         //$.ajax({
             //url: url,
             //type: 'POST',
             //data: meals_form,
             //success: function(resp){
                 //console.log('submit result :',resp);
             //}
         //})
         $.getJSON(url, meals_form, function(resp){
             console.log('response received..');
         })
    });

});
