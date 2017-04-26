The file nba_app.py sets up a web server that is allowed for access for all terminals that shares the same IP address.
To use it, first run the .py file on your local machine (or flask run -host 0.0.0.0) and it should say :

 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

Then you can open a browser on any other machine or cellphone using the same internet connection and replace 0.0.0.0 with your local IP address. Go to this webpage with port 5000 and the webpage will instruct you what to do next to input your request and get prediction results.