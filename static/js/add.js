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