$(document).ready(function(){

    $(".active_0").hide();
    $(".toggle_menu").click(function(){
        $(".menu_item").hide();
        active_value = $(this).val();
        $(".active_"+active_value).show();
        if (active_value == "1"){
            $(".active_text").text("active");
        }
        else{
            $(".active_text").text("inactive");
        }
    });

    $('.edit-meals').click(function(e){
        var meal_id = $(this).attr('data-val');
        $("#meal-"+meal_id).show();
    });

    $('.meal-submit').click(function(e){
         var url = $(this).parents('form').attr('action');
         var meals_form = $(this).parents('form').eq(0);

         var title  = $(meals_form).find('input[name=title]').eq(0).val();
         var description = $(meals_form).find('textarea[name=description]').eq(0).text();
         var price = $(meals_form).find("input[name=price]").eq(0).val();
         var active = $(meals_form).find('input[name=active]').eq(0).val();
         var d = {'title':title, 'description':description, 'price':price, 'active':active};

         $.ajax({
             url: url,
             type: 'POST',
             //data: meals_form.serialize(),
             data: JSON.stringify(d),
             success: function(resp){
                 console.log('submit result :',resp);
             }
         });

    });

    $("#id_submit").click(function(){
        title = $("#id_title").val();
        description = $("#id_description").val();
        price = $("#id_price").val();
        active= $("#id_active").is(':checked')

        if (!title){
            $("#title_error").show();
            return false;
        }
        else{
            $("#title_error").hide();
        }
        if (!description){
            $("#description_error").show();
            return false;
        }
        else{
            $("#description_error").hide();
        }
        return true;
    });


});
