from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

year = 2020
url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
headers = headers[1:] 
rows = soup.findAll('tr')[1:] 
player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
stats = pd.DataFrame(player_stats, columns = headers)
stats = stats.dropna(how='all')
names_list = stats['Player']

'''
1. loop through every name in names_list 
2. for each name, compare last name to everyone's first name
	a. if last = first, add player to name_train, then loop thru
	   comparing new last to everyone's first name
	b. repeat until no match
'''

longest_train = ""
longest_count = 0

for name_main in names_list: #loop thru each name once
	name_train = ""
	full_name_main = name_main.split()
	first_name_main = full_name_main[0]
	last_name_main = full_name_main[1]
	name_train = name_train + first_name_main + " " + last_name_main
	not_finished = True
	train_count = 1
	while (not_finished): #loop until no match is found for name
		count = 0 
		for name_body in names_list: #compare names to see if there's a match
			full_name_body = name_body.split()
			first_name_body = full_name_body[0]
			last_name_body = full_name_body[1]
			if (last_name_main == first_name_body):
				name_train = name_train + " " + last_name_body
				first_name_main = first_name_body
				last_name_main = last_name_body
				train_count += 1
				break
			count += 1
		if (train_count > longest_count):
			longest_train = name_train
			longest_count = train_count
		if (count == len(names_list)): #to break out of while loop
			not_finished = False
	if (train_count != 1): #current iteration prints a line for train with 2+ players
		print(name_train) 
		
print("Longest train is \"%s\" with %s players" % (longest_train, longest_count))