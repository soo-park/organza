"use strict";

$(function(){
  $('#login').on('submit', function(evt){
    evt.preventDefault();

    // in the session, there lives the login authorization
    // the session has email/password on file
    // when comming to logged, this javascript will load correct page
    // with authorized menu for the user
    // there are three user classes 'user', 'employee', 'admin'
    $.get(session.email, session.password, {"email" : email,
                                     "password" : password,
                                    }).done(handleLoginResults);

    // do query for the employee date_employeed, date_departed
    // make admin=True column
    // if date_employeed & not date_departed:
    //     if admin:
    //         return redirect('/admin_logged')
    //     else:
    //         return redirect("/employee_logged")
    // elif not date_employeed & date_departed:
    //     flash('no date employeed found. Please contact the admin for further information.')
    //     return redirect("/") direct to user
    // else:
    //     # TODO: add a "status" into model, and assign default='user'

    function handleLoginResults(status){
      $('#logged_index').empty();
      var html_employees = '';
      for(var employee in employees){
        html_employees += ("<li><a href = '/employee/"
                            + employee
                            + "'>"
                            + employees[employee].first_name
                            + " "
                            + employees[employee].last_name
                            + "</a></li>");
      };
      $('#logged_index').append('<ul>'+ html_employees + '</ul>');
    };
  })
});