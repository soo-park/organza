
function initMap() {

  var center = {lat: 39.50, lng: -98.35};
  var map = new google.maps.Map(document.getElementById('map'),{
              center: center,
              zoom: 4,
              draggable: false,
              // Map style from
              // https://snazzymaps.com/style/100182/new-artium
              styles: [
                      {
                          "featureType": "administrative",
                          "elementType": "labels.text.fill",
                          "stylers": [
                              {
                                  "color": "#444444"
                              }
                          ]
                      },
                      {
                          "featureType": "landscape",
                          "elementType": "all",
                          "stylers": [
                              {
                                  "color": "#f2f2f2"
                              }
                          ]
                      },
                      {
                          "featureType": "poi",
                          "elementType": "all",
                          "stylers": [
                              {
                                  "visibility": "off"
                              }
                          ]
                      },
                      {
                          "featureType": "road",
                          "elementType": "all",
                          "stylers": [
                              {
                                  "saturation": -100
                              },
                              {
                                  "lightness": 45
                              }
                          ]
                      },
                      {
                          "featureType": "road.highway",
                          "elementType": "all",
                          "stylers": [
                              {
                                  "visibility": "simplified"
                              }
                          ]
                      },
                      {
                          "featureType": "road.arterial",
                          "elementType": "labels.icon",
                          "stylers": [
                              {
                                  "visibility": "off"
                              }
                          ]
                      },
                      {
                          "featureType": "transit",
                          "elementType": "all",
                          "stylers": [
                              {
                                  "visibility": "off"
                              }
                          ]
                      },
                      {
                          "featureType": "water",
                          "elementType": "all",
                          "stylers": [
                              {
                                  "color": "#cdd2d4"
                              },
                              {
                                  "visibility": "on"
                              }
                          ]
                      },
                      {
                          "featureType": "water",
                          "elementType": "geometry.fill",
                          "stylers": [
                              {
                                  "color": "#dfdbd8"
                              }
                          ]
                      }
                  ]
            });

    $.get("/data/companies", function(data){
        for (var i = 0; i < data.data.length; i++) {
            (function(i) {
                $.get("https://maps.googleapis.com/maps/api/geocode/json?address="+data.data[i].address+","+data.data[i].city+","+data.data[i].state+"&key=AIzaSyBFGHze_U0BhQWbzg_nsH38nLzsfnEvxhQ", 
                function(data2){
                    var pos = data2.results[0].geometry.location;
                    var marker = new google.maps.Marker({
                        position: pos,
                        title: data.data[i].office_name,
                        map: map
                        });
                    $("#company-list").append("<li>"+ data.data[i].office_name +"</li>"
                                            + "<ul>"
                                              + "<li> Address: "+ data.data[i].address +"</li>"
                                              + "<li> City: "+ data.data[i].city +"</li>"
                                              + "<li> State: "+ data.data[i].state +"</li>"
                                              + "<li> Country: "+ data.data[i].country +"</li>"
                                              + "<li> Postal code: "+ data.data[i].postal_code +"</li>"
                                              + "<li> Phone: "+ data.data[i].phone +"</li>"
                                              + "<li> Fax: "+ data.data[i].fax +"</li>"
                                            + "</ul>")
                 });
            })(i)
        }
    })
}
