# Alsonic AI Music Generator

### Distinctiveness and Complexity
I believe my project is distinctive enough because it is a web application that generates music using AI. I have not seen any other web application that does this. This project is in my opinion not similar in any way to a social media site, e-commerce site or the CS50W Pizza Project. 

In this project I have made use of an AI model to generate music tracks. On the website you are able to prompt the AI to generate a song based upon the keywords that you have provided. Initially I started making a design in Figma. I then exported the design and made it responsive. Finally I set up the API routes so that the Javascript can easily fetch the data from the server. In conclusion I think that my project is complicated and distinctive enough to be considered as a final project.


### Files and directories
- `Django/alsonic/` - Main application directory.
    - `alsonic/` - Projects admin directory.
    - `media/` - Directory for storing temporary media files.
    - `tracks/` - Directory for storing generated media.
    - `website/` - Projects 'website' web-app directory.
        - `static/website/` - Directory for storing static files.
            - `css/` - Directory for storing css files.
                - `min/` - Minified css files.
                - `style.css` - CSS file for the website.
            - `js/` - Directory for storing Javascript files.
                - `min/` - Minified Javascript files.
                - `generate_track.js` - Javascript file with a function that generates a track component.
                - `smoothscroll.js` - Javascript file that redefines how the default scroll on a webpage works.
            - `icons/` - Directory for storing icons.
        - `templates/website/` - Directory that stores the HTML files.
            - `index.html` - Django HTML Template file for the index. Also includes some JavaScript code.
            - `layout.html` - Django HTML Template file for the default layout. Also includes some JavaScript code.
            - `login.html` - Django HTML Template file for the login view. Also includes some JavaScript code.
            - `recent_tracks.html` - Django HTML Template file for the view of the recent tracks. Also includes some JavaScript code.
            - `register.html` - Django HTML Template file for the register view. Also includes some JavaScript code.
            - `search.html` - Django HTML Template file for the search view. Also includes some JavaScript code.
        - `admin.py` - Django admin file.
        - `apps.py` - Django app file.
        - `models.py` - Python file in which the database models are defined. This includes the Track model in which tracks are stored.
        - `tests.py` - Python file in which the tests are defined (Although none are).
        - `urls.py` - Python file in which the urls of the web-app are defined.       
        - `views.py` - Python file in which the functions of the views of the web-app are defined.      

### Running the application
- Since the application uses AI to generate music, it is required to set up `PyTorch`. This can be done by following the instructions in [this video](https://www.youtube.com/watch?v=r7Am-ZGMef8). I'm quite sure that the server can still be ran without setting up PyTorch, however I have not been able to test this out myself.
- Install project dependencies by running `pip install -r requirements.txt`.
- Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate`.
- Run the server by running `python manage.py runserver`.
- Open the website and register an account to start generating music.
- Enjoy!

### Additional Information
This project will come with a couple pregenerated tracks, in case the setup of PyTorch was not successful. These tracks are generated using the AI model that is used in the application, which is Facebook's open-source AI model called Audiocraft Musicgen.

Of course I have demonstrated this project in a video, which you can find [here](https://youtu.be/dImi9UcS2Rg).