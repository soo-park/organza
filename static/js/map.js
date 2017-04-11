function initMap() {

//########## Blocker: multiple marker not working
    // var markerArray = [
    //                   { lat: 33.681735, lng: -117.852191 }  //LA OFFICE(HEADQUARTERS)
    //                 , { lat: 29.989029, lng: -95.491080}   //HOUSTON(TEXAS)
    //                 , { lat: 29.989029, lng: -95.491080}   //PANMERIDIAN TUBULAR-TEXAS
    //                 , { lat: 39.744950, lng: -104.987832}  //PANMERIDIAN TUBULAR-COLORADO
    //                 , { lat: 34.098870, lng: -117.395786}  //STATE PIPE & SUPPLY
    //                 ];

    // var markerTitleArray = [
    //                        'LA OFFICE(HEADQUARTERS)'
    //                       ,'HOUSTON(TEXAS)'
    //                       ,'PANMERIDIAN TUBULAR-TEXAS'
    //                       ,'PANMERIDIAN TUBULAR-COLORADO'
    //                       ,'STATE PIPE & SUPPLY'
    //                       ];

    // for (var i = 0; i < markerArray.length; i++) {

    //     var marker = new google.maps.Marker({
    //         position: markerArray[i],
    //         map: map,
    //         });
    //     marker.setMap(map);
    //     marker.setTitle(marketTitleArray[i]);
    // }

    var center = {lat: 35.514534, lng: -98.173220};
    var map = new google.maps.Map(document.getElementById('map'),{
                center: center,
                zoom: 2,
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
}




// google.maps.event.addDomListener(window, 'load', initMap);