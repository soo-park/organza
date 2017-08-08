var sessionScope;

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
  + "<a href='/company/all'>Org Chart</a>"
  + "</li>"
  + "<li class='page-scroll'>"
  + "<a href='/statistics'>Statistics</a>"
  + "</li>"
  + "<li class='page-scroll'>"
  + "<a href='/contacts'>Contact Us</a>"
  + "</li>";

$("#menu-item").replaceWith(adminMenu);

} else if (sessionScope.permission === 'employee'){

let employeeMenu = 
  "<li class='page-scroll'>"
  + "<a href='/map'>Locations</a>"
  + "</li>"
  + "<li class='page-scroll'>"
  + "<a href='/employee/all'>Search</a>"
  + "</li>"
  + "<li class='page-scroll'>"
  + "<a href='/company/all'>Org Chart</a>"
  + "</li>";

$("#menu-item").replaceWith(employeeMenu);

} else {

let userMenu = 
  "<li class='page-scroll'>"
  + "<a href='/map'>Locations</a>"
  + "</li>"
  + "<li class='page-scroll'>"
  + "<a href='/company/all'>Org Chart</a>"
  + "</li>";
  + "<li class='page-scroll'>"
  + "<a href='/contacts'>Contact Us</a>"
  + "</li>";
$("#menu-item").replaceWith(userMenu);
}

$("#logout-button").on("click", function(){
  
  alert("You have been logged out.");

})
