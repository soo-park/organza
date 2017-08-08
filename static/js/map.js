function initMap() {

  var center = {lat: 39.50, lng: -98.35};
  var map = new google.maps.Map(document.getElementById('map'),{
    center: center,
    zoom: 4,
    zoomControl: true,
    scaleControl: false,
    scrollwheel: false,
    disableAutoPan: true,
    disableDoubleClickZoom: true,
    draggable: true,
    streetViewControl: false,

    // Map style from snazzymaps.com
    styles: [
      {
        "featureType": "all",
        "elementType": "labels.text.fill",
        "stylers": [
          {
              "color": "#ffffff"
          },
          {
              "weight": "0.20"
          },
          {
              "lightness": "28"
          },
          {
              "saturation": "23"
          },
          {
              "visibility": "off"
          }
        ]
      },
      {
        "featureType": "all",
        "elementType": "labels.text.stroke",
        "stylers": [
          {
              "color": "#494949"
          },
          {
              "lightness": 13
          },
          {
              "visibility": "off"
          }
        ]
      },
      {
        "featureType": "all",
        "elementType": "labels.icon",
        "stylers": [
          {
              "visibility": "off"
          }
        ]
      },
      {
        "featureType": "administrative",
        "elementType": "geometry.fill",
        "stylers": [
          {
              "color": "#000000"
          }
        ]
      },
      {
        "featureType": "administrative",
        "elementType": "geometry.stroke",
        "stylers": [
          {
            "color": "#144b53"
          },
          {
            "lightness": 14
          },
          {
            "weight": 1.4
          }
        ]
      },
      {
        "featureType": "landscape",
        "elementType": "all",
        "stylers": [
          {
            "color": "#08304b"
          }
        ]
      },
      {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [
          {
            "color": "#0c4152"
          },
          {
            "lightness": 5
          }
        ]
      },
      {
        "featureType": "road.highway",
        "elementType": "geometry.fill",
        "stylers": [
          {
            "color": "#000000"
          }
        ]
      },
      {
        "featureType": "road.highway",
        "elementType": "geometry.stroke",
        "stylers": [
          {
            "color": "#0b434f"
          },
          {
            "lightness": 25
          }
        ]
      },
      {
        "featureType": "road.arterial",
        "elementType": "geometry.fill",
        "stylers": [
          {
            "color": "#000000"
          }
        ]
      },
      {
        "featureType": "road.arterial",
        "elementType": "geometry.stroke",
        "stylers": [
          {
            "color": "#0b3d51"
          },
          {
            "lightness": 16
          }
        ]
      },
      {
        "featureType": "road.local",
        "elementType": "geometry",
        "stylers": [
          {
            "color": "#000000"
          }
        ]
      },
      {
        "featureType": "transit",
        "elementType": "all",
        "stylers": [
          {
            "color": "#146474"
          }
        ]
      },
      {
        "featureType": "water",
        "elementType": "all",
        "stylers": [
          {
            "color": "#021019"
          }
        ]
      }
    ]
  });

  google.maps.event.addDomListener(window, "resize", function() {
    var center = map.getCenter(); 
    google.maps.event.trigger(map, "resize");
    map.setCenter(center);
  });


  
  $.get("/data/companies", function(data){
    for (var i = 0; i < data.data.length; i++) {
      (function(i) {
        $.get("https://maps.googleapis.com/maps/api/geocode/json?address="+data.data[i].address+","+data.data[i].city+","+data.data[i].state+"&key=AIzaSyBFGHze_U0BhQWbzg_nsH38nLzsfnEvxhQ", 
        function(data2){
          var pos = data2.results[0].geometry.location;
          if (data.data[i].office_name !== ""){
            var contentString = 
              "<div class='col-sm-6 col-md-4 portfolio-item'>"
                + "<li class='company'>"+ data.data[i].office_name +"</li>"
                  + "<ul class='company'>"
                    + "<li> Address: "+ data.data[i].address +"</li>"
                    + "<li> City: "+ data.data[i].city +"</li>"
                    + "<li> State: "+ data.data[i].state +"</li>"
                    + "<li> Country: "+ data.data[i].country +"</li>"
                    + "<li> Postal code: "+ data.data[i].postal_code +"</li>"
                    + "<li> Phone: "+ data.data[i].phone +"</li>"
                    + "<li> Fax: "+ data.data[i].fax +"</li>"
                + "</ul>"
              +"</div>";
            var infowindow = new google.maps.InfoWindow({
                content: contentString
              });
            var marker = new google.maps.Marker({
                position: pos,
                title: data.data[i].office_name,
                map: map
                });

            marker.addListener('mouseover', function(){
              infowindow.open(map, this);
            });

            marker.addListener('mouseout', function() {
              infowindow.close();
            });

            $("#company-list").append(contentString)
          }
         });
      })(i)
    }
  })
}
