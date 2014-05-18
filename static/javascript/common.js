$(document).ready(function(){

    $('.edit-meals').click(function(e){
        var meal_id = $(this).attr('data-val');
        $("#meal-"+meal_id).show();
    });

    $('.meal-submit').click(function(e){
         var url = $(this).parents('form').attr('action');
         console.log('url is :', url);
         var meals_form = $(this).parents('form').serialize();
         $.ajax({
             url: url,
             type: 'POST',
             data: meals_form,
             success: function(resp){
                 console.log('submit result :',resp);
             }
         })
    });

});
