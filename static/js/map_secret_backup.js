function initMap() {
  var mapCenter = new google.maps.LatLng(90, -102); // center coordinate picked
  var map = new google.maps.Map(document.getElementById('map'),{
                            zoom: 4,
                            center:mapCenter
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

  var markerArray = [
                      new google.maps.LatLng(33.681735, -117.852191)  //LA OFFICE(HEADQUARTERS)
                    , new google.maps.LatLng(29.989029, -95.491080)   //HOUSTON(TEXAS)
                    , new google.maps.LatLng(29.989029, -95.491080)   //PANMERIDIAN TUBULAR-TEXAS
                    , new google.maps.LatLng(39.744950, -104.987832)  //PANMERIDIAN TUBULAR-COLORADO
                    , new google.maps.LatLng(34.098870, -117.395786)  //STATE PIPE & SUPPLY
                    ];


  var markerArray = [
                      { lat: 33.681735, lng: -117.852191 }  //LA OFFICE(HEADQUARTERS)
                    , { lat: 29.989029, lng: -95.491080}   //HOUSTON(TEXAS)
                    , { lat: 29.989029, lng: -95.491080}   //PANMERIDIAN TUBULAR-TEXAS
                    , { lat: 39.744950, lng: -104.987832}  //PANMERIDIAN TUBULAR-COLORADO
                    , { lat: 34.098870, lng: -117.395786}  //STATE PIPE & SUPPLY
                    ];



  for (var i = 0; i < markerArray.length; i++) {
    var marker = new google.maps.Marker({
      map:map,
      position: markerArray[i]
    });
    marker.setMap(map);
    marker.setTitle(marketTitleArray[i]);

google.maps.event.addDomListener(window, 'load', initMap);






// This script links to trip_detail.html and updates/loads maps, markers, routes
// The interactive tables are inputed here

// *****************************************************************************
// JS for Google Maps
// The function initializes the map with origin on San Francisco

var map;
var uniqueId = 0;
var markers = [];
var timeout;
var chart;
var elSvc;
// var path = new Array();
var my_location = {lat: 37.7572439, lng: -122.4388962};

var endpoints = [];

function initMap() {
  
  var directionsService = new google.maps.DirectionsService;
  var directionsDisplay = new google.maps.DirectionsRenderer;
  // var geocoder = new google.maps.Geocoder();
  map = new google.maps.Map(document.getElementById('map'), {
    center: my_location,
    zoom: 15,
    mapTypeId: 'roadmap'
  });
  directionsDisplay.setMap(map);
  document.getElementById('submit').addEventListener('click', function() {

    endpoints = [];
    clearMarkers();
    markers = [];
    calculateAndDisplayRoute(directionsService, directionsDisplay);
  });
  
}

function clearMarkers() {
        for (var i = 0; i < markers.length; i++ ){
            markers[i].setMap(null);
        }
      }


function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    directionsService.route({
      origin: document.getElementById('start').value,
      destination: document.getElementById('end').value,
      travelMode: 'WALKING'
    }, function(response, status) {
      if (status === 'OK') {
        directionsDisplay.setDirections(response);
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    });
    console.log(endpoints);
    codeAddress('start');
    codeAddress('end');

}

function codeAddress(loc) {
    var geocoder = new google.maps.Geocoder();
    address = document.getElementById(loc).value;
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == 'OK') {
        // map.setCenter(results[0].geometry.location);
        // var marker = new google.maps.Marker({
        //     map: map,
        //     position: results[0].geometry.location
        // });
        var lat = results[0].geometry.location.lat();
        var lng = results[0].geometry.location.lng();
        var my_latlon = {'lat': lat, 'lng': lng};
        endpoints.push(my_latlon);
        pushEndpoints();
      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
    });
  }

function pushEndpoints() {
    if(endpoints.length===2) {
    console.log(endpoints);
    var dataInput = {'first': JSON.stringify(endpoints[0]),
                     'second': JSON.stringify(endpoints[1])};
    console.log(dataInput);
    // post data to route, returns data with show markers
    $.post('/markers.json', dataInput, showMarkers);
    $.post('/green-markers.json', dataInput, showgreenMarkers);
    }
}

function showMarkers(data) {
    var image = {
          url: '/static/img/danger.gif',
          // This marker is 20 pixels wide by 32 pixels high.
          size: new google.maps.Size(20, 32),
          // The origin for this image is (0, 0).
          origin: new google.maps.Point(0, 0),
          // The anchor for this image is the base of the flagpole at (0, 32).
          anchor: new google.maps.Point(0, 32)
        };

    if (data) {
        data = JSON.parse(data);
        // console.log(data);
        for (var geo in data) {

            var myLatLng = {lat: data[geo].lat, lng: data[geo].lng};
            var marker = new google.maps.Marker({
              position: myLatLng,
              map: map,
              icon: image,
              dragable: true});
        
            markers.push(marker);
                }
            }
    }


function showgreenMarkers(data) {
    var marker;

          var policeMarker = {
          url: '/static/img/police.gif',
          // This marker is 20 pixels wide by 32 pixels high.
          size: new google.maps.Size(20, 32),
          // The origin for this image is (0, 0).
          origin: new google.maps.Point(0, 0),
          // The anchor for this image is the base of the flagpole at (0, 32).
          anchor: new google.maps.Point(0, 32)
        };

        var greenMarker = {
          url: '/static/img/safe.png',
          // This marker is 20 pixels wide by 32 pixels high.
          size: new google.maps.Size(20, 32),
          // The origin for this image is (0, 0).
          origin: new google.maps.Point(0, 0),
          // The anchor for this image is the base of the flagpole at (0, 32).
          anchor: new google.maps.Point(0, 32)
        };

    if (data) {
        // data = JSON.parse(data);
        // console.log(data);
        for (var geo in data) {
            console.log(data[geo].lat);
            var myLatLng = {lat: data[geo].lat, lng: data[geo].lng};
            var description = data[geo].category;
            if (description === 'police department') {
                marker = new google.maps.Marker({
                position: myLatLng,
                map: map,
                icon: policeMarker,
                dragable: true});
        

            } else {
              marker = new google.maps.Marker({
              position: myLatLng,
              map: map,
              icon: greenMarker,
              dragable: true});
            }
        
            markers.push(marker);
                }
            }
    }


//Sets the map on all markers in the array.
function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    console.log(markers[i]);
    markers[i].setMap(map);
  }
}

