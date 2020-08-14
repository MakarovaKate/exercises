import sqlite3
from datetime import datetime
from datetime import timedelta

conn = sqlite3.connect('tech_quality.db')
c = conn.cursor()

c.execute('''CREATE TABLE users
             (id TEXT PRIMARY KEY, role TEXT) ''')

c.execute('''CREATE TABLE lessons
             (id TEXT PRIMARY KEY, event_id INTEGER, subject TEXT, day TEXT,
             FOREIGN KEY (event_id) REFERENCES participants (event_id)) ''') 

c.execute('''CREATE TABLE participants  
	         (user_id TEXT, event_id INTEGER,
	         PRIMARY KEY (user_id, event_id),
	         FOREIGN KEY (user_id) REFERENCES users (id),
	         FOREIGN KEY (event_id) REFERENCES lessons (event_id))''')

c.execute('''CREATE TABLE quality 
	         (lesson_id TEXT, tech_quality INTEGER,
	         FOREIGN KEY (lesson_id) REFERENCES lessons (id))''')

#for users
users = list()

with open('C:\\Users\\User\\Desktop\\ex\\ex3\\tech_quality\\users.txt', 'r') as inf:
	for line in inf.readlines():
		users.append([element.strip() for element in line.split(' | ')])

#использую словарь, чтобы отследить уникальность user_id
uniq_users = dict()
for user in users[2:len(users) - 2]:
	if user[0] not in uniq_users:
		uniq_users[user[0]] = user[1]
	else:
		continue

insert_for_users = 'INSERT INTO users ({}, {}) VALUES (?, ?)'.format(users[0][0], users[0][1])
c.executemany(insert_for_users, uniq_users.items())

#for lessons
lessons = list()

with open('C:\\Users\\User\\Desktop\\ex\\ex3\\tech_quality\\lessons.txt', 'r') as inf:
	for line in inf.readlines():
		lessons.append([element.strip() for element in line.split(' | ')])

#вычисляю московское время и получаю дату
for lesson in lessons[2:len(lessons) - 2]:
	if lesson[-1].find('.') != -1:
		lesson[-1] = (datetime.strptime(lesson[-1], "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours=3)).strftime("%Y-%m-%d")
	else:
		lesson[-1] = (datetime.strptime(lesson[-1], "%Y-%m-%d %H:%M:%S") + timedelta(hours=3)).strftime("%Y-%m-%d")


insert_for_lessons = 'INSERT INTO lessons ({}, {}, {}, day) VALUES (?, ?, ?, ?)'.format(lessons[0][0], lessons[0][1], lessons[0][2])
c.executemany(insert_for_lessons, lessons[2:len(lessons) - 2])

#for participants
participants = list()

with open('C:\\Users\\User\\Desktop\\ex\\ex3\\tech_quality\\participants.txt', 'r') as inf:
	for line in inf.readlines():
		participants.append([element.strip() for element in line.split(' | ')])

#отслеживаю дубли по сочетанию event_id и user_id
uniq_participants = list()
for participant in participants[2:len(participants) - 2]:
	if participant not in uniq_participants:
		uniq_participants.append(participant)
	else:
		continue

insert_for_participants = 'INSERT INTO participants ({}, {}) VALUES (?, ?)'.format(participants[0][0], participants[0][1])
c.executemany(insert_for_participants, uniq_participants)

#for quality
quality = list()

with open('C:\\Users\\User\\Desktop\\ex\\ex3\\tech_quality\\quality.txt', 'r') as inf:
	for line in inf.readlines():
		quality.append([element.strip() for element in line.split(' | ')])		

insert_for_quality = 'INSERT INTO quality ({}, {}) VALUES (?, ?)'.format(quality[0][0], quality[0][1])
c.executemany(insert_for_quality, quality[2:len(quality) - 2])
c.execute('''UPDATE quality SET tech_quality = NULLIF(tech_quality,''); ''')  #пустоту заменяю на значения None

conn.commit()

c.execute('''SELECT day, user_id, AVG(tech_quality) AS average_score FROM 
	((SELECT lessons.id as lesson_id, event_id, day, tech_quality FROM 
	 lessons INNER JOIN quality 
	 ON lessons.id = quality.lesson_id 
	 WHERE subject = "phys" AND tech_quality IS NOT NULL) phys_table 
	 INNER JOIN (SELECT event_id, participants.user_id as user_id FROM 
                 users INNER JOIN participants
                 ON users.id = participants.user_id
                 WHERE role = "tutor") tutor_table
     ON phys_table.event_id = tutor_table.event_id) origin_table
     GROUP BY day, user_id
     ORDER BY day, average_score;''') 

#phys_table - таблица со всеми уроками физики, за которые есть оценки
#tutor_table - таблица со всеми ивентами и учителями, которые их вели
#итоговую таблицу сортирую по дате и средней оценке учителей, так каждая первая строка с новой датой будет содержать минимальную среднюю оценку за день

#записываю минимальные оценки
with open('C:\\Users\\User\\Desktop\\ex\\ex3\\table_for_result.txt', 'w') as ouf:
	ouf.write('day\tuser_id\taverage_score\n')
	writed_days = list()
	for row in c.fetchall():
		if row[0] not in writed_days:
			writed_days.append(row[0])
			ouf.write('{}\t{}\t{}'.format(row[0], row[1], round(row[2], 2)))
			ouf.write('\n')
		else:
			continue

c.close()
conn.close()
