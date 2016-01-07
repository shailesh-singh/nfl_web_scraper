#!/usr/bin/python

from BeautifulSoup import BeautifulSoup as bs
import urllib2
from optparse import OptionParser
import sys

parser = OptionParser()
parser.add_option("-y","--year",help="Year of Super Bowl", type="int")
parser.add_option("-w","--week",help="Game week of Super Bowl", type="int")
parser.add_option("-p","--position",help="POSITIONS: qb,rb,wr,te")


(options, args) = parser.parse_args()


#check if all args are met
isArgs = options.week is not None and options.year is not None and options.position is not None

if isArgs==False:
    print "args not met. Check help menu for usage" 
    sys.exit()
    
isPosition = options.position.lower() in ["qb","rb","wr","te"]

if not isPosition:
    print "position needs to be one of the following: qb, rb, wr, te"
    sys.exit()

game_year = options.year
start_week = options.week
max_week = options.week 

player_position = {
    "qb":{
        "position_code":1,
        "delimiter":"QB"
    },
    "rb":{
        "position_code":2,
        "delimiter":"RB"
    },
    "wr":{
        "position_code":3,
        "delimiter":"WR"
    },    
    "te":{
        "position_code":4,
        "delimiter":"TE"
    }, 
    "k":{
        "position_code":7,
        "delimiter":"K"
    },             
}



position = player_position[options.position]

#CSV Header
print "team,player,opposition,passing_yds,passing_td,passing_int,rushing_yds,rushing_td,receving_yds,receiving_td,misc_fumTD,misc_2pt,fum_lost,fantasy,week,game_year"


lines_per_page = 25
number_of_pages = 7 



max_columns =13
for x in range(start_week,max_week+1):
    for offset in map(lambda a: lines_per_page*a-24,range(1,number_of_pages +1)):    
        soup = bs(urllib2.urlopen("http://fantasy.nfl.com/research/scoringleaders?offset={}&position={}&sort=pts&statCategory=stats&statSeason={}&statType=weekStats&statWeek={}".format(offset,position["position_code"],
    game_year,x)))
        
        title = soup.find("table", {"class" : "tableType-player hasGroups"})
        
        if title != None:
            rows = []
            temp_line =[]
            p = []
            
            team=None
            for i in title.findAll('tr'):
                row_data = i.findAll('td')

                for j in row_data:
                    z= j.findAll('em') #Extract player team and position
                    team = None
                    if len(z) > 0:
                        str_position_team = z[0].text
                        if str_position_team.find("-") >0:
                            team = str_position_team.split("-")[1]
                            
                    player = None      
                    pn = j.findAll('a') #Extract player name
                    if len(pn)>0: 
                        player= pn[0].text    

                    temp_line.append(team.strip()+ "," + player if team and player else j.text)

                
            
        start = 0
        end = max_columns
        inc = max_columns
                        
        player_list = []
        for i in (range(1,(len(temp_line) +1)/max_columns+1)):                       
            if temp_line[start+1] !="Bye": #Exclude Players on Bye
                player_list.append(",".join(temp_line[start:end]+['{}'.format(x)]+['{}'.format(game_year)]))
                start = end
                end = end+inc
                        
                
        for i in player_list:
            i = i.replace("-","")
            i =  i.replace("@","")+",True" if i.find("@")>-1 else i+",False" 
            print i
                
    
