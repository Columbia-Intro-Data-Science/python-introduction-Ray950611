from flask import Flask

import numpy
from bs4 import BeautifulSoup
import requests
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from Tkinter import *

app = Flask(__name__)

@app.route("/")
######
def nba():
    ###########2 prediction module functions: season/game
    def season_predict(season_input,team_name):
        TeamFull = ['San Antonio Spurs', 'Golden State Warriors', 'Oklahoma City Thunder', 'Cleveland Cavaliers', 'Toronto Raptors', 'Los Angeles Clippers', 'Atlanta Hawks', 'Boston Celtics', 'Charlotte Hornets', 'Utah Jazz', 'Indiana Pacers', 'Miami Heat', 'Portland Trail Blazers', 'Detroit Pistons', 'Houston Rockets', 'Dallas Mavericks', 'Washington Wizards', 'Chicago Bulls', 'Orlando Magic', 'Memphis Grizzlies', 'Sacramento Kings', 'Denver Nuggets', 'New York Knicks', 'New Orleans Pelicans', 'Minnesota Timberwolves', 'Milwaukee Bucks', 'Phoenix Suns', 'Brooklyn Nets', 'Los Angeles Lakers', 'Philadelphia 76ers']
        Teams = ['SAS','GSW','OKC','CLE','TOR','LAC','ATL','BOS','CHO','UTA','IND','MIA','POR','DET','HOU','DAL','WAS','CHI','ORL','MEM','SAC','DEN','NYK','NOP','MIN','MIL','PHO','BRK','LAL','PHI']
        #check input
        if season_input=='':
            return "Null season input!"
        season_input = int(season_input)
        if season_input <2016 or season_input>2017:
            return "Error season input!Not valid for app use."
        if team_name not in Teams:
            return "Error input team name!"
        #database
        season_train = season_input - 1
       
        advanced_train = 'http://www.basketball-reference.com/leagues/NBA_'+str(season_train)+'_advanced.html'
        
        req = requests.get(advanced_train) 
        
        text = BeautifulSoup(req.text, 'html.parser')
        stats = text.find('div',{'id': 'all_advanced_stats'}) 
        cols = [i.get_text() for i in stats.thead.find_all('th')] 
        
        # convert from unicode to string 
        cols = [x.encode('UTF8') for x in cols] 
        #print cols
        # get rows 
        rows=[]
        for i in stats.tbody.find_all('tr'):
            cols = [j.get_text() for j in i.find_all('td')] 
            
            row_i = [x.encode('UTF8') for x in cols]
            
            rows.append(row_i)
        
        
        PERAvg_train = np.zeros(30)
        GP_train = np.zeros(30)
        Min_train = np.zeros(30)
        
        for row in rows:
            if len(row)==0:
                continue
            if row[3]!='TOT':
                team = row[3]
                mins = row[5]
                gp = row[4]
                index = Teams.index(team)
                if float(mins)/float(gp) > 8.0:
                    GP_train[index] += int(gp)
                    Min_train[index] += int(mins)
                    PERAvg_train[index] += float(row[6]) * int(mins)
        PERAvg_train /= Min_train
        #y data
        team_train = 'http://www.basketball-reference.com/leagues/NBA_'+str(season_train)+'_ratings.html'
        req = requests.get(team_train) 
        
        text = BeautifulSoup(req.text, 'html.parser')
        stats = text.find('div',{'id': 'all_ratings'}) 
        cols = [i.get_text() for i in stats.thead.find_all('th')] 
        
        # convert from unicode to string 
        cols = [x.encode('UTF8') for x in cols] 
        #print cols
        # get rows 
        teams=[]
        for i in stats.tbody.find_all('tr'):
            cols = [j.get_text() for j in i.find_all('td')] 
            
            row_i = [x.encode('UTF8') for x in cols]
            
            teams.append(row_i)
        Wins_train = np.zeros(30)
        Conf = np.zeros(30)
        for team in teams:
            
            index = TeamFull.index(team[0])
            Wins_train[index] = float(team[5])
            Conf[index] = int(team[1] == 'W')    
        PERAvg_train = np.array(PERAvg_train).reshape((30,1))
        Wins_train = np.array(Wins_train).reshape((30,1))
        #new inquiry
        #regular season data wrapping
        advanced_test = 'http://www.basketball-reference.com/leagues/NBA_'+str(season_input)+'_advanced.html'
        
        req = requests.get(advanced_test) 
        
        text = BeautifulSoup(req.text, 'html.parser')
        stats = text.find('div',{'id': 'all_advanced_stats'}) 
        cols = [i.get_text() for i in stats.thead.find_all('th')] 
        
        # convert from unicode to string 
        cols = [x.encode('UTF8') for x in cols] 
        #print cols
        # get rows 
        rows=[]
        for i in stats.tbody.find_all('tr'):
            cols = [j.get_text() for j in i.find_all('td')] 
            
            row_i = [x.encode('UTF8') for x in cols]
            
            rows.append(row_i)
        
        
        # find the schema 
        team_test = 'http://www.basketball-reference.com/leagues/NBA_'+str(season_input)+'_ratings.html'
        req = requests.get(team_test) 
        
        text = BeautifulSoup(req.text, 'html.parser')
        stats = text.find('div',{'id': 'all_ratings'}) 
        cols = [i.get_text() for i in stats.thead.find_all('th')] 
        
        # convert from unicode to string 
        cols = [x.encode('UTF8') for x in cols] 
        #print cols
        # get rows 
        teams=[]
        for i in stats.tbody.find_all('tr'):
            cols = [j.get_text() for j in i.find_all('td')] 
            
            row_i = [x.encode('UTF8') for x in cols]
            
            teams.append(row_i)
        Wins = np.zeros(30)
        Conf = np.zeros(30)
        for team in teams:
            
            index = TeamFull.index(team[0])
            Wins[index] = float(team[5])
            Conf[index] = int(team[1] == 'W')    
        PERAvg = np.zeros(30)
        GP = np.zeros(30)
        Min = np.zeros(30)
        
        for row in rows:
            if len(row)==0:
                continue
            if row[3]!='TOT':
                team = row[3]
                mins = row[5]
                gp = row[4]
                index = Teams.index(team)
                if float(mins)/float(gp) > 8.0:
                    GP[index] += int(gp)
                    Min[index] += int(mins)
                    PERAvg[index] += float(row[6]) * int(mins)
        PERAvg /= Min
        PERAvg = np.array(PERAvg).reshape((30,1))
        Wins = np.array(Wins).reshape((30,1))
        ####
        
        regr = LinearRegression()
        regr.fit(PERAvg_train, Wins_train)
        ##############predict
        per = PERAvg[Teams.index(team_name)].reshape(1,-1)
        predicted = regr.predict(per)[0][0]
        Result= "Predicted winning ratio for "+team_name+":"+str(predicted)

        return Result
    def game_predict(season_input,home_team,guest_team):
        #check input
        if season_input=='':
            return "Null season input!"
        season_input = int(season_input)
        if season_input <2016 or season_input>2017:
            return "Error season input!Not valid for app use."
        
        ###initialization
        TeamFull = ['San Antonio Spurs', 'Golden State Warriors', 'Oklahoma City Thunder', 'Cleveland Cavaliers', 'Toronto Raptors', 'Los Angeles Clippers', 'Atlanta Hawks', 'Boston Celtics', 'Charlotte Hornets', 'Utah Jazz', 'Indiana Pacers', 'Miami Heat', 'Portland Trail Blazers', 'Detroit Pistons', 'Houston Rockets', 'Dallas Mavericks', 'Washington Wizards', 'Chicago Bulls', 'Orlando Magic', 'Memphis Grizzlies', 'Sacramento Kings', 'Denver Nuggets', 'New York Knicks', 'New Orleans Pelicans', 'Minnesota Timberwolves', 'Milwaukee Bucks', 'Phoenix Suns', 'Brooklyn Nets', 'Los Angeles Lakers', 'Philadelphia 76ers']
        Teams = ['SAS','GSW','OKC','CLE','TOR','LAC','ATL','BOS','CHO','UTA','IND','MIA','POR','DET','HOU','DAL','WAS','CHI','ORL','MEM','SAC','DEN','NYK','NOP','MIN','MIL','PHO','BRK','LAL','PHI']
        #regular season data wrapping
        if guest_team not in Teams or home_team not in Teams:
            return "Error input team name!"
        season_train = season_input - 1
        #database
        advanced_train = 'http://www.basketball-reference.com/leagues/NBA_'+str(season_train)+'_advanced.html'
        
        req = requests.get(advanced_train) 
        
        text = BeautifulSoup(req.text, 'html.parser')
        stats = text.find('div',{'id': 'all_advanced_stats'}) 
        cols = [i.get_text() for i in stats.thead.find_all('th')] 
        
        # convert from unicode to string 
        cols = [x.encode('UTF8') for x in cols] 
        #print cols
        # get rows 
        rows=[]
        for i in stats.tbody.find_all('tr'):
            cols = [j.get_text() for j in i.find_all('td')] 
            
            row_i = [x.encode('UTF8') for x in cols]
            
            rows.append(row_i)
        
        
        PERAvg = np.zeros(30)
        GP = np.zeros(30)
        Min = np.zeros(30)
        
        for row in rows:
            if len(row)==0:
                continue
            if row[3]!='TOT':
                team = row[3]
                mins = row[5]
                gp = row[4]
                index = Teams.index(team)
                if float(mins)/float(gp) > 8.0:
                    GP[index] += int(gp)
                    Min[index] += int(mins)
                    PERAvg[index] += float(row[6]) * int(mins)
        PERAvg /= Min
        ############
        Boxscore = []
        X_team = []#guestteam,hometeam
        X=[]
        y=[]#home margin
        z = []#hometeam win = 1
        for month in ["october","november","december","january","february","march","april"]:
            boxscore = "http://www.basketball-reference.com/leagues/NBA_"+str(season_train)+"_games-"+str(month)+".html"
            req = requests.get(boxscore) 
        
            text = BeautifulSoup(req.text, 'html.parser')
            stats = text.find('div',{'id': 'all_schedule'}) 
            cols = [i.get_text() for i in stats.thead.find_all('th')] 
        
            # convert from unicode to string 
            cols = [x.encode('UTF8') for x in cols] 
            #print cols
            # get rows 
        
            for i in stats.tbody.find_all('tr'):
                cols = [j.get_text() for j in i.find_all('td')] 
        
                row_i = [x.encode('UTF8') for x in cols]
                if row_i:
                    if row_i[2]:
                        Boxscore.append([int(row_i[2]),int(row_i[4])])
                        X_team.append([row_i[1],row_i[3]])
                        index_0 = TeamFull.index(row_i[1])
                        index_1 = TeamFull.index(row_i[3])
                        X.append([PERAvg[index_0],PERAvg[index_1]])
                        y.append(int(row_i[4])-int(row_i[2]))
                        z.append(int(int(row_i[4])>int(row_i[2])))#hometeam win
        X = np.array(X).reshape((len(X),2))
        y = np.array(y).reshape((len(X),1))
        z = np.array(z).reshape((len(X),1))
        #######
        #new inquiry
        advanced_test = 'http://www.basketball-reference.com/leagues/NBA_'+str(season_input)+'_advanced.html'
        
        req = requests.get(advanced_test) 
        
        text = BeautifulSoup(req.text, 'html.parser')
        stats = text.find('div',{'id': 'all_advanced_stats'}) 
        cols = [i.get_text() for i in stats.thead.find_all('th')] 
        
        # convert from unicode to string 
        cols = [x.encode('UTF8') for x in cols] 
        #print cols
        # get rows 
        rows=[]
        for i in stats.tbody.find_all('tr'):
            cols = [j.get_text() for j in i.find_all('td')] 
            
            row_i = [x.encode('UTF8') for x in cols]
            
            rows.append(row_i)
        
        
        PERAvg_test = np.zeros(30)
        GP = np.zeros(30)
        Min = np.zeros(30)
        
        for row in rows:
            if len(row)==0:
                continue
            if row[3]!='TOT':
                team = row[3]
                mins = row[5]
                gp = row[4]
                index = Teams.index(team)
                if float(mins)/float(gp) > 8.0:
                    GP[index] += int(gp)
                    Min[index] += int(mins)
                    PERAvg_test[index] += float(row[6]) * int(mins)
        PERAvg_test /= Min
    ############
        x_team = [guest_team,home_team]
        Result=[2]
        regr = LinearRegression()
        regr.fit(X, y)
    
        index_0 = Teams.index(x_team[0])
        index_1 = Teams.index(x_team[1])
        x = np.array([PERAvg_test[index_0],PERAvg_test[index_1]]).reshape(1,-1)
        Result="Hometeam game margin:"+str(regr.predict(x)[0][0])+"\n"
        ##
        regr = LogisticRegression()
        regr.fit(X, z)
        
        coef = regr.coef_[0]
        intercept = regr.intercept_[0]
        def model(x):
            return 1 / (1 + np.exp(-x))
        index_0 = Teams.index(x_team[0])
        index_1 = Teams.index(x_team[1])
        x = np.array([PERAvg_test[index_0],PERAvg_test[index_1]])
        prob = model(x[0] * coef[0] + x[1]*coef[1]+intercept)
        Result+= "Homwteam win prob:"+str(prob)
        return Result
###########tkinter button functions
    def show_game():
        season_input = year_g.get()
        home_team = t1.get()
        guest_team = t2.get()
        result = game_predict(season_input,home_team,guest_team)
        Label(main, text = "Result:").grid(row=7,column=0)
        T = Text(main,height=2,width=50)
        T.insert(END, result)
        T.grid(row=7,column=1)
    def show_season():
        season_input = year_s.get()
        team = t.get()
        result = season_predict(season_input,team)
        Label(main, text = "Result:").grid(row=2,column=0)
        T = Text(main,height=2,width=50)
        T.insert(END, result)
        T.grid(row=2,column=1)
               
    main = Tk()
    main.title("My NBA Predictor")
    #entry boxes and text boxes
    Label(main, text = "Game Prediction: Enter season(yyyy>2015,<current season):").grid(row=4)
    Label(main, text = "Enter Home Team Official Initial(all cap):").grid(row=5)
    Label(main, text = "Enter Guest Team Official Initial(all cap):").grid(row=6)
    Label(main, text = "Seasonal Prediction: Enter season(yyyy>2015,<current season):").grid(row=0)
    Label(main, text = "Enter Team Official Initial(all cap):").grid(row=1)
    t = Entry(main)
    year_s = Entry(main)
    t1 = Entry(main)
    t2 = Entry(main)
    year_g = Entry(main)
    t.grid(row=1,column=1)
    year_s.grid(row=0, column=1)
    t1.grid(row=5, column=1)
    t2.grid(row=6, column=1)
    year_g.grid(row=4, column=1)
    #buttons
    Label(main, text = "Predict(may take a minute):").grid(row=3,column=0)
    Label(main, text = "Predict(may take a minute):").grid(row=8,column=0)
    Button(main, text='Season', command=show_season).grid(row=3, column=1, sticky=W, pady=4)
    Button(main, text='Game', command=show_game).grid(row=8, column=1, sticky=W, pady=4)
    mainloop()
    #after quitting tk window
    return "Thanks For Using"


if __name__ == "__main__":
    app.run()