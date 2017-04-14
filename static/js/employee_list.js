"use strict";

// anonimous function of AJAX to avoid a dirty name space 
$(function(){
  // AJAX event handler to attach action onto a ID
  $('#search').on('submit', function(evt){
    // to stop going to the server side
    console.log('Made it to list function');
    evt.preventDefault();

    // JQuery gets the submitted value by the id
    // figure out what the user typed in
    // not like regular JS the value is not value() but is val() in JQuery
    var companySearch = $('#company').val();
    var departmentSearch = $('#department').val();
    var firstNameSearch = $('#first-name').val();
    var lastNameSearch = $('#last-name').val();

    // // Ajax goes to the server side and make request
    // // attach the arg in the string as a parameter or have it as a second parameter

    // // Example on attatching the parameter in the string
    // $.get('/search_employees.json?first_name='+firstNameSearch, handleSearchResults);

    // Example on using the arguments as a second parameter
    // multiple values can be passed to the server side as a dictionary
    // style guide: make the route name to be .json to know you are getting JSON
    $.get('/search_employees.json', {"company_name" : companySearch,
                                     "department_name" : departmentSearch,
                                     "first_name" : firstNameSearch,
                                     "last_name" : lastNameSearch
                                    }).done(handleSearchResults);

    // The callback function definition
    // you will receive employee ids as the following format
    // employees = {'1': {'first_name': 'firsta', 'last_name' : 'lasta'}}
    function handleSearchResults(employees){
      // delete the enteire tinng (find the sytax)
      $('#active_search_result').empty();

      // Loop inside the query object returned, create name list HTML
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
      $('#active_search_result').append('<ul>'+ html_employees + '</ul>');
    };
  })

  $(document).ready(function(){
   $(window).scroll(lazyload);
   lazyload();
  });

  var options = $$('#select');
  var len = options.length;
  for (var i = 0; i < len; i++) {
    options[i].selected = false;
  }