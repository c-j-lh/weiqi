import requests
import re
from bs4 import BeautifulSoup
from random import randrange, sample, choice
from datetime import timedelta, datetime
from itertools import product

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
moves = []
def number(chars):
    return tuple(ord(char)-ord('a')+1 for char in chars)
    
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
    games[gameid] = [result, date, names, None]
    moves.append([])
    
    try:
        content = open(f'data/{gameid:04d}.sgf', 'r').read()
    except:
        r = requests.get(url, allow_redirects=True)
        open(f'data/{gameid:04d}.sgf', 'w').write(str(r.content))
        content = r.content
        raise Exception
        
    event = None   
    for i in re.findall( r'.{1,2}\[[^]]*\]', str(content)):
        i = i.strip(';')
        index = i.find('[')
        tag = i[:index]
        data = i[index+1 : -1]
        #print(tag,data)
        if tag in 'BW':
            moves[-1].append(number(data))
        elif tag=='EV':
            #print(data)
            games[gameid][3] = data
    
    #gameid = 0
    if moves[-1]:    
        s += 'INSERT INTO move VALUES\n'
        s += ',\n'.join(f'\t({gameid},{moveno}, {movex},{movey})'
                        for moveno, (movex, movey) in enumerate(moves[-1])) + ';\n'
    #for moveno, (movex, movey) in enumerate(moves[-1]):
    #    s += f'\t({gameid},{moveno}, {movex},{movey});\n'
    #s += '\n'

print(open('weiqi.sql', 'r').read() + '\n\n')
print('''
INSERT INTO country VALUES ("China","China.jpg");
INSERT INTO country VALUES ("Japan","China.jpg");
INSERT INTO country VALUES ("Korea","China.jpg");

insert into competition values ("World Amateur Champion Special Competition");
insert into competition values ("Chinese Agon Cup");
insert into event values ("Chinese Agon Cup", 8);
insert into event values ("Chinese Agon Cup", 9);
insert into event values ("Chinese Agon Cup", 10);
insert into event values ("World Amateur Champion Special Competition", 0);
insert into hosts values ("Chinese Agon Cup", "China");
''')
    
    
for name, (country, ranking) in players.items():
    dob = random_date(start, end).date()
    print(f'INSERT INTO player VALUES ("{name}", {country}, "{ranking}", "{dob}", false, null, null, null);')
print()
    
ll = list(games.items())
for gameid, (result, date, names,_ignore) in ll[:-5]:
    print(f'INSERT INTO game VALUES ({gameid}, "{result}", "{date}", "Chinese Agon Cup", {choice([8,9,10])}, "{names[0]}", "{names[1]}");')
for gameid, (result, date, names,_ignore) in ll[-5:]:
    print(f'INSERT INTO game VALUES ({gameid}, "{result}", "{date}", "World Amateur Champion Special Competition", 0, "{names[0]}", "{names[1]}");')
print()

print(s)

players = list(players.keys())
gamesC = sample(range(len(games)), 10)

cid = 0
for gameid in gamesC: 
    if len(moves[gameid])<2:
        continue
    movesC = sample(range(len(moves[gameid])), 2)
    playersC = sample(players, 2)
    for moveid, player in product(movesC, playersC):
        print(f'insert into comment values ({cid}, "Good move", 0, {player!r}, {gameid}, {moveid});')
        #print(gameid, moveid, player, "gg")
        cid += 1
print()

cidC = cid
for cid in sample(range(cidC), 5):
    for player in sample(players, 5):
        print(f'insert into Votes values ({player!r}, {cid}, {choice([False]*2+[True]*5)});')
print()        


for cid in sample(range(cidC), 5):
    for player in sample(players, 5):
        print(f'insert into Tags values ({player!r}, {cid});')   
print()

'''url = 'http://gokifu.com/f/39i9-gokifu-20210225-Shin_Jinseo-Ke_Jie.sgf'
r = requests.get(url, allow_redirects=True)

open('data/001.sgf', 'wb').write(r.content)'''