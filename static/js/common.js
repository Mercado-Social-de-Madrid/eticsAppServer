$(function(){
    $('[data-toggle="tooltip"]').tooltip();

    $('.gallery-form').on('submit', function(event ){
        var order = 0;

        $('.gallery-form-photo').each(function(){
            var $question = $(this);
            $question.find('input[id$="order"]').val(order);
            order++;
        });
    });

     $(".gallery-form").on('change', '.form-photo > input', function(){
        console.log("AAAAAA");
        var input = this;
        var target = $(input).siblings('img');
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                    $(target).attr('src', e.target.result);
  
            }
            reader.readAsDataURL(input.files[0]);
        }
    });

});
