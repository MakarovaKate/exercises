import string
import operator

with open('C:\\Users\\User\\Desktop\\ex\\ex1\\names.txt', 'r') as inf:
	name_list = [[name, 0] for name in inf.read().replace('"', '').split(',')]

name_list.sort(key=operator.itemgetter(0)) #сортирую список имен
alpha = string.ascii_uppercase #создаю строку с алфавитом

#функция, которая будет складывать порядковые номера букв в имени
def sum_letter_name(name):
	sum_letter = 0
	for letter in name:
		sum_letter += (alpha.index(letter) + 1)
	return sum_letter

#заполняю таблицу с именами суммами
for name_line in name_list:
	name_line[1] = sum_letter_name(name_line[0])

#накапливаю произведения порядкового номера имени (т.к. имена уникальны использую порядковый номер строки) на сумму его букв
result = 0
for name_line in name_list:
	result += (name_list.index(name_line) + 1) * name_line[1]
print(result)
