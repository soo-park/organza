"use strict";

 // https://forum.jquery.com/topic/using-the-submit-event-with-modal-form-dialog

$(function(){

  $("#company_add").on("click", function(evt){
    evt.preventDefault();

    $('#company_name').empty();

    // Loop inside the query object returned, create name list HTML
    var html_company = ("<input type='text' name='company_name'"
                        + " id='company_list'"
                        + "placeholder='Please input the new company name'>"
                        +"<button type='button' id='company_list'>back to list </button>"
                        );

    $('#company_name').append(html_company);
  })

  $("#company_list").on("click", function(evt){
    evt.preventDefault();

    $('#company_list').empty();

    var html_list = ("<select name='company_name'>"
                       + " <option></option>"
                       + "{% for company in companies %}"
                       + "<option value='{{ company.company_name }}'>"
                       + "{{ company.company_name }}"
                       + "</option>"
                       + "{% endfor %}"
                       + "</select>"
                       + "<button type='button' id='company_add'>add company </button>"
                       );
        
    $('#company_name').append(html_list);
  })

  $("#dialog-div").bind( "submit", function() {
    allFields.removeClass('ui-state-error');
    var bValid = checkLength(username,"username", 3, 50);
    bValid = bValid && checkLength(password,"password",5,16);
    bValid = bValid && checkLength(first_name,"first_name", 6, 80);
    bValid = bValid && checkRegexp(/^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter.");
    bValid = bValid && checkRegexp(/^[a-z]([0-9a-z_])+$/i, "First Name may consist of a-z, 0-9, underscores, begin with a letter.");
    bValid = bValid && checkRegexp(password,/^([0-9a-zA-Z])+$/,"Password field only allow : a-z 0-9");
    if (bValid) {
     $('#users tbody').append('<tr>' +
      '<td>' + username.val() + '</td>' + 
      '<td>' + first_name.val() + '</td>' + 
      '<td>' + password.val() + '</td>' +
      '</tr>'); 
     $(this).dialog('close');
    }
  })