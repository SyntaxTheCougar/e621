from e6g_connection import DataRetriever
from sets import Set
import numpy as np

import pprint
import networkx as nx
from plotly.graph_objs import *
import matplotlib.pyplot as plt
from operator import itemgetter


dr = DataRetriever()
#posts = dr.getFirstPage()
posts = dr.getFirstN(500)

#[post,{tags}]
#[tag,{posts}]]

tagToPosts = {}
postToTags = {}

#fill dictionaries 
for post in posts:
	tags = post["tags"].split()
	id = post["id"]
	
	# print "========="
	# print "ID: " + str(id) 
	# print "Tags: " + str(tags)
	# print "========="
	# print " "
	
	if id in postToTags:
		postToTags[id].add(tags)
	else:
		postToTags[id] = Set(tags)
		
	
	for tag in tags: 
		if tag in tagToPosts:
			tagToPosts[tag].add(id)
		else:
			tagToPosts[tag] = Set([id])
			
		
#remove tags with only one post 
for key in tagToPosts.keys(): 
	if len(tagToPosts[key]) == 1:
		del tagToPosts[key]
	
#make adjancecy matrix
matrix = np.zeros((len(tagToPosts),len(tagToPosts)), dtype=np.int)

tuples = tagToPosts.items()

Edges = []
G=nx.MultiGraph()
G.add_nodes_from(i[0] for i in tuples)


for k1, v1 in tuples: 
	for k2, v2 in tuples:
		if k1 == k2: 
			break
		
		commons = v1.intersection(v2)
		
		if len(commons) >= 1 :
			Edges.append((k1,k2, len(commons)))
			#print k1 + " , " + k2 + " : " + str(len(commons))

print "Posts: " + str(len(posts))
print "Tags: " + str(len(tagToPosts))
pp = pprint.PrettyPrinter(indent=4)

#print 
#pp.pprint(tagToPosts)
#print
#pp.pprint(tuples)
#print
#pp.pprint(Edges)

G.add_weighted_edges_from(Edges)

edgewidth = [ d['weight'] for (u,v,d) in G.edges(data=True)]
nodesize = [len(v)*20 for k, v in tagToPosts.iteritems() ]

#pp.pprint(nodesize)


# find node with largest degree
largest_hub=G.nodes()[10]
print str(largest_hub)
#(largest_hub,degree)=sorted(node_and_degree,key=itemgetter(1))[-1]
# Create ego graph of main hub
G=nx.generators.barabasi_albert_graph(1000,2)
hub_ego=nx.ego_graph(G,largest_hub)
# Draw graph
pos=nx.spring_layout(hub_ego)
nx.draw(hub_ego,pos,node_color='b',node_size=50,with_labels=True)
# Draw ego as large and red
nx.draw_networkx_nodes(hub_ego,pos,nodelist=[largest_hub],node_size=300,node_color='r', with_labels=True)
#plt.savefig('ego_graph.png')


#nx.draw_networkx_nodes(G, pos)
#nx.draw_networkx_edges(G, pos, edge_color=edgewidth)
#nx.draw(G, node_color='c', node_size=nodesize , edge_width=edgewidth, with_labels=True)
plt.show()

raw_input ("Press <enter> to terminate program") 
