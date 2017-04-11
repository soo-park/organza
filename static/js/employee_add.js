"use strict";

// ############## BLOCKER ###################
// is there a way to not name them one by one but accept the form name
$(function(){
  $('#add').on('submit', function(evt){
    evt.preventDefault();

    // receives data from user_add.html
    // Ajax goes to the server side and make request
    // attach the arg in the string as a parameter or have it as a second parameter
    $.get('/add_employee.json', { // dynamically generate this 
                              //$('#'+iterated_string_from_dic').key(): $('#'+iterated_string_from_dic').val(),

                              "birthday": $('#birthday').val(),
                              "personal_email": $('#personal_email').val(),
                              "first_name": $('#first_name').val(),
                              "mid_name": $('#mid_name').val(),
                              "last_name": $('#last_name').val(),
                              "nickname": $('#nickname').val(),
                              "k_name": $('#k_name').val(),
                              "kanji_name": $('#kanji_name').val(),
                              "phone": $('#phone').val(),
                              "mobile": $('#mobile').val(),
                              "address_line1": $('#address_line1').val(),
                              "address_line2": $('#address_line2').val(),
                              "city": $('#city').val(),
                              "state": $('#state').val(),
                              "country": $('#country').val(),
                              "postal_code": $('#postal_code').val(),
                              "emergency_name": $('#emergency_name').val(),
                              "emergency_phone": $('#emergency_phone').val(),
                              "admin": $('#admin').val()
                              }).done(handleAdd);

    // you will receive employee ids as the following format
    // employees = {'1': {'first_name': 'firsta', 'last_name' : 'lasta'}}
    function handleAdd(employee){
      var html_employee = '';
      // redirect to the same page with clean slate
      // and flash that the user is added to the list safely on the same page
    };
  })
});