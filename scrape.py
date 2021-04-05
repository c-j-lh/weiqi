import requests
import re
from bs4 import BeautifulSoup
from random import randrange, sample, choice, seed
from datetime import timedelta, datetime
from itertools import product


# https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
start = datetime.strptime('1/1/1940', '%m/%d/%Y')
end = datetime.strptime('1/1/2000', '%m/%d/%Y')

url_pattern = '[^"]*.sgf' # '"[^"]*.sgf"'

html_text = open("GoKifu Share SGF Go_Baduk_Weiqi games with friends..html", 'r').read()
soup = BeautifulSoup(html_text, 'html.parser')
players = dict()
games = dict()

countrycodes = {'xx':'null', 'kr':'"Korea"', 'ja':'"Japan"', 'cn':'"China"'}
s = ''
moves = []
def number(chars):
    return tuple(reversed([ord(char)-ord('a')+1 for char in chars]))
    
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
        content = r.content.decode("utf-8")
        open(f'data/{gameid:04d}.sgf', 'w').write(str(content))
        
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
        s += ', '.join(f'({gameid},{moveno}, {movex},{movey})'
                        for moveno, (movex, movey) in enumerate(moves[-1])) + ';\n'
    #for moveno, (movex, movey) in enumerate(moves[-1]):
    #    s += f'\t({gameid},{moveno}, {movex},{movey});\n'
    #s += '\n'

print(open('weiqi.sql', 'r').read() + '\n\n')
print('''
INSERT INTO country VALUES ("China","images/cn.png", "The earliest written reference to the game is generally recognized as the historical annal Zuo Zhuan (c. 4th century BCE), referring to a historical event of 548 BCE. It is also mentioned in Book XVII of the Analects of Confucius and in two books written by Mencius (c. 3rd century BCE). In all of these works, the game is referred to as yì (弈). Today, in China, it is known as weiqi (simplified Chinese: 围棋; traditional Chinese: 圍棋; pinyin: wéiqí; Wade–Giles: wei ch'i), lit. 'encirclement board game'.


A 19×19 Go board model from a Sui dynasty (581–618 CE) tomb.
Go was originally played on a 17×17 line grid, but a 19×19 grid became standard by the time of the Tang Dynasty (618–907).");

INSERT INTO country VALUES ("Japan","images/jp.png", "The game reached Japan in the 7th century CE—where it is called go (碁) or igo (囲碁). It became popular at the Japanese imperial court in the 8th century, and among the general public by the 13th century. The game was further formalized in the 15th century. In 1603, Tokugawa Ieyasu re-established Japan's unified national government. In the same year, he assigned the then-best player in Japan, a Buddhist monk named Nikkai (né Kanō Yosaburo, 1559), to the post of Godokoro (Minister of Go).");
INSERT INTO country VALUES ("Korea","images/kr.png", "In Korea, the game is called baduk (hangul: 바둑), and a variant of the game called Sunjang baduk was developed by the 16th century. Sunjang baduk became the main variant played in Korea until the end of the 19th century, when the current version was reintroduced from Japan.
");

insert into competition values ("World Amateur Champion Special Competition", 4, 10, "The World Amateur Go Championship (WAGC) is an event in which amateur players from around the world compete for the official world amateur title. The event is held every year, under the supervision of the International Go Federation. The first WAGC was held in 1979 with 30 participants from 14 countries.");
insert into competition values ("Chinese Agon Cup", 5, 5, "The China-Japan Agon Cup is a tournament where the current Agon Cup/Ahan Tongshan Cup title holders from China and Japan play each other.");
insert into event values ("Chinese Agon Cup", 8, "start of Liu Xing's 2-year reign", "");
insert into event values ("Chinese Agon Cup", 9, "same winner and runner-up as last year.");
insert into event values ("Chinese Agon Cup", 10, "Cho U a consistent runner-up");
insert into event values ("World Amateur Champion Special Competition", 0, "This year, it remains more international than many of the other competitions.");
insert into hosts values ("Chinese Agon Cup", "China");
''')
    
seed(0)
for name, (country, ranking) in players.items():
    dob = random_date(start, end).date()
    print(f'INSERT INTO player VALUES ("{name}", {country}, "{ranking}", "{dob}", false, null, null, null);')
print()

seed(0)
ll = list(games.items())
for gameid, (result, date, names,_ignore) in ll[:-5]:
    print(f'INSERT INTO game VALUES ({gameid}, "{result}", "{date}", "Chinese Agon Cup", {choice([8,9,10])}, "{names[0]}", "{names[1]}");')
for gameid, (result, date, names,_ignore) in ll[-5:]:
    print(f'INSERT INTO game VALUES ({gameid}, "{result}", "{date}", "World Amateur Champion Special Competition", 0, "{names[0]}", "{names[1]}");')
print()

print(s)

seed(0)
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


seed(0)
cidC = cid
for cid in sample(range(cidC), 5):
    for player in sample(players, 5):
        print(f'insert into Votes values ({player!r}, {cid}, {choice([False]*2+[True]*5)});')
print()        


seed(0)
for cid in sample(range(cidC), 5):
    for player in sample(players, 5):
        print(f'insert into Tags values ({player!r}, {cid});')   
print()

print('''update comment
set voteCount = (select count(*) from votes where commentID=id);
-- select * from comment;

create trigger addVote
after insert on votes
for each row
update comment
set voteCount = voteCount + if(new.downUp, 1, -1)
where new.commentID=id;

create trigger subVote
after delete on votes
for each row
update comment
set voteCount = voteCount - if(old.downUp, 1, -1)
where old.commentID=id;

DELIMITER //
create trigger changeVote
after update on votes
for each row
BEGIN
	update comment
	set voteCount = voteCount - if(old.downUp, 1, -1)
	where old.commentID=id;
    
	update comment
	set voteCount = voteCount + if(new.downUp, 1, -1)
	where new.commentID=id;
END;//
delimiter ;''')
'''url = 'http://gokifu.com/f/39i9-gokifu-20210225-Shin_Jinseo-Ke_Jie.sgf'
r = requests.get(url, allow_redirects=True)

open('data/001.sgf', 'wb').write(r.content)'''