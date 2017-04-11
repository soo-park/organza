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
                'birthday': $('#birthday').val();
                'personal_email': $('#personal_email').val();
                'first_name': $('#first_name').val();
                'mid_name': $('#mid_name').val();
                'last_name': $('#last_name').val();
                'nickname': $('#nickname').val();
                'k_name': $('#k_name').val();
                'kanji_name': $('#kanji_name').val();
                'phone': $('#phone').val();
                'mobile': $('#mobile').val();
                'address_line1': $('#address_line1').val();
                'address_line2': $('#address_line2').val();
                'city': $('#city').val();
                'state': $('#state').val();
                'country': $('#country').val();
                'postal_code': $('#postal_code').val();
                'emergency_name': $('#emergency_name').val();
                'emergency_phone': $('#emergency_phone').val();
                'admin': $('#admin').val();
                'company_name': $('#company_name').val();
                'department_name': $('#department_name').val();
                'title': $('#title').val();
                'office_name': $('#office_name').val();
                'office_email': $('#office_email').val();
                'password': $('#password').val();
                'date_employeed': $('#date_employeed').val();
                'date_departed': $('#date_departed').val();
                'job_description': $('#job_description').val();
                'office_phone': $('#office_phone').val();
                'title_id': $('#title_id').val();
                'department_id': $('#department_id').val();
                'office_id': $('#office_id').val();
                'department_id': $('#department_id').val();
    }).done(handleAdd);

    // you will receive employee ids as the following format
    // employees = {'1': {'first_name': 'firsta', 'last_name' : 'lasta'}}
    function handleAdd(employee){
      var html_employee = '';
      // Employee added. Would you like to add another one?
      // if not redirect to the homepage
      // if yes redirect to the add_employee page
    };
  })
});