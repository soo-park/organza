$(".login_menu").on("click", function(evt){

  console.log("made it");
  if(sessionScope.permission === 'admin'){
    
    let adminMenu = 
                    "<li class='page-scroll'>"
                    + "<a href='/map'>Locations</a>"
                    + "</li>"
                    + "<li class='page-scroll'>"
                    + "<a href='/employee/all'>Search</a>"
                    + "</li>"
                    + "<li class='page-scroll'>"
                    + "<a href='/employee/add'>Add</a>"
                    + "</li>"
                    + "<li class='page-scroll'>"
                    + "<a href='/company/all'>Stats</a>"
                    + "</li>"
                    + "<li class='page-scroll'>"
                    + "<a href='/statistics'>Org Chart</a>"
                    + "</li>"
                    + "<li class='page-scroll'>"
                    + "<a href='/contacts'>Contact Us</a>"
                    + "</li>";

    $(".nav navbar-nav navbar-right").append(adminMenu);

  } else if (sessionScope.permission === 'employee'){
    
    let employeeMenu = 
                    "<li class='page-scroll'>"
                    + "<a href='/map'>Locations</a>"
                    + "</li>"
                    + "<li class='page-scroll'>"
                    + "<a href='/employee/all'>Search</a>"
                    + "</li>"
                    + "<li class='page-scroll'>"
                    + "<a href='/company/all'>Stats</a>"
                    + "</li>";

    $(".nav navbar-nav navbar-right").append(employeeMenu);
  
  } else {
  
    let userMenu = 
                    "<li class='page-scroll'>"
                    + "<a href='/map'>Locations</a>"
                    + "</li>"
                    + "<li class='page-scroll'>"
                    + "<a href='/statistics'>Org Chart</a>"
                    + "</li>"
                    + "<li class='page-scroll'>"
                    + "<a href='/contacts'>Contact Us</a>"
                    + "</li>";
    $(".nav navbar-nav navbar-right").append(userMenu);
  }
})


$("#logout-button").on("click", function(){
  
  alert("You have been logged out.");

})