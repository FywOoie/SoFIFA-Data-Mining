import sqlite3

con = sqlite3.connect('players.db')
cursorObj = con.cursor()
select_sql = 'select * from players'
results = cursorObj.execute(select_sql)

ca_pre = 0
pa_pre = 0
for index, info in enumerate(results.fetchall()):
    if info[1] == None:
        con.execute("update players set name='Player' where id=(index+1)")
    elif info[2] == None:
        con.execute("update players set club='Free' where id=(index+1)")
    elif info[3] == None:
        con.execute("update players set current_ability=%d where id=(index+1)",ca_pre)
    elif info[4] == None:
        con.execute("update players set potential_ability=%d where id=(index+1)",pa_pre)
    
    ca_pre = info[3]
    pa_pre = info[4]