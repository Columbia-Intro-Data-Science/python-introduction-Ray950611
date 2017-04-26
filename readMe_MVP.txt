The Minimal Viable Product nba_module.py is an app that sets upa flask server on the local host http://127.0.0.1:5000/ 
To use it, run from terminal:

export FLASK_APP=nba_modul.py
flask run

And as soon as you see :
 
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

go to your browser and load the host: http://127.0.0.1:5000/ 
You should see a pop up GUI window called My NBA Predictor.
This is the app that you can play with, just type in the season and team input as specified. Here is a complete listing of teams and their official initials:

['San Antonio Spurs', 'Golden State Warriors', 'Oklahoma City Thunder', 'Cleveland Cavaliers', 'Toronto Raptors', 'Los Angeles Clippers', 'Atlanta Hawks', 'Boston Celtics', 'Charlotte Hornets', 'Utah Jazz', 'Indiana Pacers', 'Miami Heat', 'Portland Trail Blazers', 'Detroit Pistons', 'Houston Rockets', 'Dallas Mavericks', 'Washington Wizards', 'Chicago Bulls', 'Orlando Magic', 'Memphis Grizzlies', 'Sacramento Kings', 'Denver Nuggets', 'New York Knicks', 'New Orleans Pelicans', 'Minnesota Timberwolves', 'Milwaukee Bucks', 'Phoenix Suns', 'Brooklyn Nets', 'Los Angeles Lakers', 'Philadelphia 76ers']
        ['SAS','GSW','OKC','CLE','TOR','LAC','ATL','BOS','CHO','UTA','IND','MIA','POR','DET','HOU','DAL','WAS','CHI','ORL','MEM','SAC','DEN','NYK','NOP','MIN','MIL','PHO','BRK','LAL','PHI']

There are two prediction options season/game, you can run one of them using the respective button. This may take a few seconds so please wait patiently while the app fetches data from online intime. 
The results will be shown in a text box. You can predict as many times as you want to using the two buttons, and when you are done, simply close the GUI window and the website will show the sentence:

Thanks For Using

Reload the webpage if you want to restart the GUI window and use the app again.
