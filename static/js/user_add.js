"use strict";

// ############## BLOCKER ###################
// is there a way to not name them one by one but accept the form name
$(function(){
  $('#add').on('submit', function(evt){
    evt.preventDefault();
    // receives data from user_add.html
    var birthday = $('#birthday').val();
    var personal_email = $('#personal_email').val();
    var first_name = $('#first_name').val();
    var mid_name = $('#mid_name').val();
    var last_name = $('#last_name').val();
    var nickname = $('#nickname').val();
    var k_name = $('#k_name').val();
    var kanji_name = $('#kanji_name').val();
    var phone = $('#phone').val();
    var mobile = $('#mobile').val();
    var address_line1 = $('#address_line1').val();
    var address_line2 = $('#address_line2').val();
    var city = $('#city').val();
    var state = $('#state').val();
    var country = $('#country').val();
    var postal_code = $('#postal_code').val();
    var emergency_name = $('#emergency_name').val();
    var emergency_phone = $('#emergency_phone').val();
    var admin = $('#admin').val();

    // // Ajax goes to the server side and make request
    // // attach the arg in the string as a parameter or have it as a second parameter
    $.get('/add_user.json', { "birthday": birthday,
                              "personal_email": personal_email,
                              "first_name": first_name,
                              "mid_name": mid_name,
                              "last_name": last_name,
                              "nickname": nickname,
                              "k_name": k_name,
                              "kanji_name": kanji_name,
                              "phone": phone,
                              "mobile": mobile,
                              "address_line1": address_line1,
                              "address_line2": address_line2,
                              "city": city,
                              "state": state,
                              "country": country,
                              "postal_code": postal_code,
                              "emergency_name": emergency_name,
                              "emergency_phone": emergency_phone,
                              "admin": admin
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