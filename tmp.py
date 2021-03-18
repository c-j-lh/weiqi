import re
content = open('data/data001.sgf', 'r').read().strip('(').strip(')')
moves = []
def number(chars):
    return tuple(ord(char)-ord('a')+1 for char in chars)
    
for i in re.findall( r'.{1,2}\[[^]]*\]', content):
    i = i.strip(';')
    index = i.find('[')
    tag = i[:index]
    data = i[index+1 : -1]
    print(tag,data)
    if tag in 'BW':
        moves.append(number(data))

f'INSERT INTO game VALUES (0,"B+7.5", "2020-10-05", NULL, "Le Heng2", "Le Heng3");'  
gameid = 0     
for moveno, (movex, movey) in enumerate(moves):
    print(f'INSERT INTO move VALUES ({gameid},{moveno}, {movex},{movey});')
    #print(moves)
'''for value in content:
    if value:
        print(value)'''
