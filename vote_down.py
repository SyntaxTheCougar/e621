

username=Polybius
password=700mbm
post_list=[]

UP = 1
DOWN = -1

def vote()
	for post in post_list:
		id_n = post['id']
		params={'id': id_n, 'score' , 'name': username, 'password': password }



