# CS50FinalProject
For my CS50 final projects, my two groupmates and I created a website, called Horizons, that will show the user the top ten songs, books, and films from their chosen country.

To compile, first download the source files contained in an overall folder “final”. Enter “cd final” and then “cd stuff” into the terminal window to open up the folders’ contents. To run the program, enter “flask run” into the terminal window to open up the webpage. (The APIs we used to create our search function are GoogleBooks, LastFM, and MovieAPI. Since we hardcoded the API keys into the program, you will not need to acquire API keys in order to compile use our project.)

Upon opening the website, you will be directed to the homepage that explains the purpose of the website as well as a basic rundown as to the website’s features are. You can learn more about us and our idea on the “about us” page, which can be accessed on the navigation menu. However, to access all the search features, you will need to create and account by clicking on “register” on the navigation menu. On the “register” page, enter a username, password, and password confirmation to create an account. Once you register for an account, log in by clicking “log in” on the navigation menu. On the “log in” page, enter your registered username and password, and then you will have access to the “search books”, “search movies”, “search songs”, and “library” tabs on the navigation menu.

To search relevant books about a country, first click on the “search books” tab on the navigation menu. You will be directed to the “search books” page. Then, click on the dropdown menu to select an interested country and after, press the “Search Books” function. The program will then output five relevant books of that country that you can use to learn more about the selected country.

To search relevant movies about a country, first click on the “search movies” tab on the navigation menu. You will be directed to the “search movies” page. Then, click on the dropdown menu to select an interested country and after, press the “Search Movies” function. The program will then output five relevant movies of that country that you can use to learn more about the selected country.

To search popular songs of a country, first click on the “search songs” tab on the navigation menu. You will be directed to the “search songs” page. Then, click on the dropdown menu to select an interested country and after, press the “Search Songs” function. The program will then output the top five most popular songs in that country (from last week) that you can use to learn more about the selected country.

Lastly, the library tab on the navigation menu will have a list of all previous searches you have conducted. To see a history of your searches, click on “library” on the navigation menu.

To log out, click “log out” on the navigation menu.
