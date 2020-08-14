import operator as op

with open('C:\\Users\\User\\Desktop\\ex\\ex2\\hits.txt', 'r') as inf:
	links_list = [line.strip().split('\t') for line in inf.readlines()]

#записываю ip в отдельный список
ip_list = [link[1] for link in links_list]

#использую словарь, чтобы записать количество повторений каждого ip
ip_dict = dict()
for ip in ip_list:
	if ip not in ip_dict:
		ip_dict[ip] = ip_list.count(ip)
	else:
		continue

#записываю результат подсчета ip в двумерный список
ip_table = [[key, value] for key, value in ip_dict.items()]
#сортирую двумерный список по убыванию количества упоминаний ip
ip_table.sort(key=op.itemgetter(1), reverse=True)
#вывожу первые пять ip
print(*[i[0] for i in ip_table][:5], sep = ', ')
