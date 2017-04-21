"use strict";

 // https://forum.jquery.com/topic/using-the-submit-event-with-modal-form-dialog

$(function(){

  $("#company_add").on("click", function(evt){
    evt.preventDefault();

    $('#company_name').empty();

    // Loop inside the query object returned, create name list HTML
    var html_company = ("<input type='text' name='company_name'"
                        + " id='company-list'"
                        + " class='company-list'"
                        + "placeholder='Please input the new company name'>"
                        +"<button type='button' id='company-list'>back to list </button>"
                        );

    $('#company_name').append(html_company);
  })

  $("#company_list").on("click", function(evt){
    evt.preventDefault();

    $('#company_name').empty();

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
  });

  $("#department_add").on("click", function(evt){
    evt.preventDefault();

    $('#department_name').empty();

    // Loop inside the query object returned, create name list HTML
    var html_department = ("<input type='text' name='department_name'"
                        + " id='department-list'"
                        + " class='department-list'"
                        + "placeholder='Please input the new department name'>"
                        +"<button type='button' id='department-list'>back to list </button>"
                        );

    $('#department_name').append(html_department);
  })

  $("#title_add").on("click", function(evt){
    evt.preventDefault();

    $('#title_name').empty();

    // Loop inside the query object returned, create name list HTML
    var html_title = ("<input type='text' name='title_name'"
                        + " id='title-list'"
                        + " class='title-list'"
                        + "placeholder='Please input the new title name'>"
                        +"<button type='button' id='title-list'>back to list </button>"
                        );

    $('#title_name').append(html_title);
  })

  $("#office_add").on("click", function(evt){
    evt.preventDefault();

    $('#office_name').empty();

    // Loop inside the query object returned, create name list HTML
    var html_office = ("<input type='text' name='office_name'"
                        + " id='office-list'"
                        + " class='office-list'"
                        + "placeholder='Please input the new office name'>"
                        +"<button type='button' id='office-list'>back to list </button>"
                        );

    $('#office_name').append(html_office);
  })

})