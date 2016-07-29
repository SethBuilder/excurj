var currentRating = 0;

function showStars(starNumber) {

    //Save the current star selection
    currentRating = starNumber;

    //Load each star from the DOM
    var starArray = [$("#reviewStar0"), $("#reviewStar1"), $("#reviewStar2"), $("#reviewStar3"), $("#reviewStar4")];

    //If the star number is lower than the one that is being hovered over then set it to selected
    for (var i = 0; i <= starNumber; i++) {
        starArray[i].removeClass("glyphicon-star-empty");
        starArray[i].addClass("glyphicon-star");
    }

    //Otherwise set it to unselected
    for (var j = starNumber + 1; j <= 4; j++) {
        starArray[j].removeClass("glyphicon-star");
        starArray[j].addClass("glyphicon-star-empty");
    }

}

//Save a review to the database using AJAX and display the new review on screen
function saveReview(rated_username, rating_username) {

    //Get the review comment inputted by the user
    var reviewComment = $("#reviewText").val();

    //Get the table of previous reviews
    var reviewsTable = $("#reviewsTable");

    //Post the new review to the database using AJAX
    $.get('/submitreview/', {
        rating_user: rating_username.toString(),
        rated_user: rated_username,
        comment: reviewComment,
        rating: currentRating.toString()
    }, function (data) {

        //Check if the rating has been successfully posted
        if (data == "Rating confirmed") {

            //Get the HTML from the current list of reviews for later adaptation
            var newHtml = reviewsTable.html();

            //Set URL - this URL will be changed to template version on next page refresh so this is temporary
            var newUrl = "/user/" + rating_username;

            //Display the username of the person rating (the person currently logged in)
            newHtml += "<tr><td><h4><a href='" + newUrl + "'>" + rating_username + " </a>";

            //Display the correct amount of stars they have given
            for (var i = 0; i <= currentRating; i++)
                newHtml += "<span class='glyphicon glyphicon-star' aria-hidden='true'></span>";

            //Display the comment
            newHtml += "</h4><p>" + reviewComment + "</p></td></tr>";

            //Update the ratings table to show the new review
            reviewsTable.html(newHtml);

            //Delete the text entered into the review input box
            $("#reviewText").val("");

        }
        else{
            $("#reviewText").val("Please log in and create a profile before reviewing other users");
        }

    });

}
