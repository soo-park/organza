function initMap() {

    var center = {lat: 30.514534, lng: -106.173220};
    var map = new google.maps.Map(document.getElementById('map'),{
                center: center,
                zoom: 4,
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

    var locations = [
            { 
                name: 'LA OFFICE(HEADQUARTERS)',
                latlng: { 
                    lat: 33.681735, lng: -117.852191 
                }
            },
            { 
                name: 'HOUSTON(TEXAS)',
                latlng: { 
                    lat: 29.989029, lng: -95.491080
                }
            },
            { 
                name: 'PANMERIDIAN TUBULAR-TEXAS',
                latlng: { 
                    lat: 29.989029, lng: -95.491080
                }
            },
            { 
                name: 'PANMERIDIAN TUBULAR-COLORADO',
                latlng: { 
                    lat: 39.744950, lng: -104.987832
                }
            },
            { 
                name: 'STATE PIPE & SUPPLY',
                latlng: { 
                    lat: 34.098870, lng: -117.395786
                }
            }
        ]

    for (var i = 0; i < locations.length; i++) {
        var marker = new google.maps.Marker({
            position: locations[i].latlng,
            title: locations[i].name,
            map: map
            });
    }
}
