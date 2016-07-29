window.onload = function () {

//Load list of locations (if the product were to be deployed these would be loaded from each City object in the database
    var locations = [
        ['Paris', 48.856614, 2.352222, 4],
        ['Munich', 48.135125, 11.581981, 5],
        ['Sao Paulo', -23.549887, -46.634340, 3],
        ['Glasgow', 55.867326, -4.253063, 2],
        ['London', 55.867326, -4.253063, 2],
        ['Budapest', 47.500615, 19.044466, 1]
    ];

//Adapted from http://stackoverflow.com/questions/3059044/google-maps-js-api-v3-simple-multiple-marker-example
//Create a new Google Maps object
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 3,
        center: new google.maps.LatLng(30, 0),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

// Create a popup for when users click on a map marker
    var infowindow = new google.maps.InfoWindow();

    var marker, i;

// Loop through each location in the list and place a marker there
    for (i = 0; i < locations.length; i++) {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[i][1], locations[i][2]),
            map: map
        });

        // Show a popup containing the city name and a link to the city page when a user clicks a map marker
        google.maps.event.addListener(marker, 'click', (function (marker, i) {
            return function () {
                var cityUrl = "/city/" + locations[i][0].toLowerCase().replace(" ", "-");
                infowindow.setContent("<h4>" + locations[i][0] + "</h4><a href='" + cityUrl + "'>Go to city page</a>");
                infowindow.open(map, marker);
            }
        })(marker, i));
    }

};