import requests
import re
from bs4 import BeautifulSoup
from random import randrange
from datetime import timedelta, datetime

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
# https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
start = datetime.strptime('1/1/1940', '%m/%d/%Y')
end = datetime.strptime('1/1/2000', '%m/%d/%Y')
#print(random_date(d1, d2))

#vgm_url = 'https://www.vgmusic.com/music/console/nintendo/nes/'
#html_text = requests.get(vgm_url).text

url_pattern = '[^"]*.sgf' # '"[^"]*.sgf"'

html_text = open("GoKifu Share SGF Go_Baduk_Weiqi games with friends..html", 'r').read()
soup = BeautifulSoup(html_text, 'html.parser')
players = dict()
games = dict()

countrycodes = {'xx':'null', 'kr':'"Korea"', 'ja':'"Japan"', 'cn':'"China"'}
s = ''
for gameid, game in enumerate(soup.find_all('div', {"class": "player_block cblock_3"})):
    #if gameclass='player_block cblock_3')
    players2 = game.find_all('div', {"class": 'player_name'})
    url = re.findall(url_pattern, str(game))[0]
    
    names = [0, 0]
    for i, player in enumerate(players2):
        country = player.img['src'].split('/')[-1][:-4]
        country = countrycodes[country]
        name = names[i] = player.a.string
        ranking = re.findall('\(.*\)', str(player))[0]
        ranking = ranking.strip('(').strip(')')
        players[name] = (country, ranking)
        #print(country, name, ranking)
    #print(url,'\n')
    #break
    result = game.find('div', {'class': 'game_result'}).string
    date = game.find('div', {'class': 'game_date'}).string
    games[gameid] = (result, date, names)
    
    r = requests.get(url, allow_redirects=True)
    #open(f'data/{gameid:04d}.sgf', 'wb').write(r.content)
    moves = []
    def number(chars):
        return tuple(ord(char)-ord('a')+1 for char in chars)
        
    for i in re.findall( r'.{1,2}\[[^]]*\]', str(r.content)):
        i = i.strip(';')
        index = i.find('[')
        tag = i[:index]
        data = i[index+1 : -1]
        #print(tag,data)
        if tag in 'BW':
            moves.append(number(data))

    #gameid = 0      
    '''for moveno, (movex, movey) in enumerate(moves):
        s += f'INSERT INTO move VALUES ({gameid},{moveno}, {movex},{movey});\n'
    s += '\n''''
    
for name, (country, ranking) in players.items():
    dob = random_date(start, end).date()
    print(f'INSERT INTO player VALUES ("{name}", {country}, "{ranking}", "{dob}", false, null, null, null);')
print()
    
for gameid, (result, date, names) in games.items():
    print(f'INSERT INTO game VALUES ({gameid}, "{result}", "{date}", NULL, "{names[0]}", "{names[1]}");')
print()
    
print(s)


'''url = 'http://gokifu.com/f/39i9-gokifu-20210225-Shin_Jinseo-Ke_Jie.sgf'
r = requests.get(url, allow_redirects=True)

open('data/001.sgf', 'wb').write(r.content)'''