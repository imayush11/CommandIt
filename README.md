# Introduction: 
CommandIt is a Python based tool based on NLP & Google APIs. In simpler just provide voice commands to do stuff like schedule a meet in calendar 
or read a mail 
NLP helps to extract major keywords from the commands inputted & is further carried on by the code which requests the Google API for 
implementing the changes 

# Tech stack:
React Native for building a native version for all Android & IOS users
Python for backend 

# Folder structure:
1) Backend: Python backend code for speech recognition, NLP based actions & linking to Googles API for Calendar & gmail
2) mobile-app: React Native based frontend for Android & IOS
3) web-app: Python(Django & Flask) based web application for any browser

# Features:
1) Schedule meetings in calendar with just saying "Schedule a meet" or "Create a meet"
2) Reading & listing email by saying "Show unread emails" or "Read emails from bla@gmail.com"
3) Many more to add

# To run the web-app:
> pip install requirements.txt 
If you face any issues with pyaudio:
First install homebrew then install portaudio with brew:
> brew install portaudio
Then find the path to where your portaudio has been installed and replace the below two paths with your path:
! make sure to replace the path else it might not work
> pip3 install --global-option='build_ext' --global-option='-I/opt/homebrew/Cellar portaudio/19.7.0/include' --global-option='-L/opt/homebrew/Cellar/portaudio/19.7.0/lib' pyaudio
Once installations are complete:
> cd web-app
Then run the Django app:
> django-admin startproject index 

# To run the mobile-app
For android:
> npm run android 
For IOS:
> npn run ios

