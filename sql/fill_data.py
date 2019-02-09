dump = open('insta485db-dump.txt').read()
dump = dump.split('\n')
f = open('data.sql', 'a')

table = ''
params = {}

for line in dump:
    if 'SELECT * FROM ' in line:
        table_idx = line.find('SELECT * FROM ') + len('SELECT * FROM ')
        table = line[table_idx:-1]
    if '=' in line:
        vals = line.split(' = ')
        if vals[0] != 'created':
        	params[vals[0]] = vals[1]
    if line == '':
        command = 'INSERT INTO ' + table + '('
        for key in params.keys():
            command += key + ','
        command = command[:-1]
        command += ') VALUES ('
        for val in params.values():
            command += ("\'" + val + "\',")
        command = command[:-1]
        command += ');'
        f.write(command + '\n')
        params = {}
