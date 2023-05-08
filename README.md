# instaMapsReactFlask
Instagram Pictures on Maps

## Features
- Scrap Instagram Pictures and Metadata of Target User on Flask Api
- Load Instagram data on React and display them on Maps

## Installed packages on React:
leaflet
react-leaflet

## instruction
Replace urls on MarkerList.jsx and App.js based on your environment.
Run with the following commands
- in server, run "python3 app.py"
- in client, run "npm start"

Type your instagram username and password, and target username to display their data on maps.
From second time, you can use only target field to call their data (as its already downloaded on server).

## limitation
Don't use your real instagram account, as it can be banned.
Only Images are supported atm (not video). 
Scrapper may not be able to run on headless server. 

## TODO
Styling on Popup Windows