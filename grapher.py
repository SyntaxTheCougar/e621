from e6g_connection import DataRetriever
import plotly.plotly as py
from sets import Set
import numpy as np

import pprint
import networkx as nx
from plotly.graph_objs import *
import matplotlib.pyplot as plt


dr = DataRetriever()
#posts = dr.getFirstPage()
posts = dr.getFirstN(5)


py.sign_in('humun', '9aq7qo7ayd')

#[post,{tags}]
#[tag,{posts}]]

tagToPosts = {}
postToTags = {}

def scatter_nodes(pos, labels=None, color=None, size=20, opacity=1):
    # pos is the dict of node positions
    # labels is a list  of labels of len(pos), to be displayed when hovering the mouse over the nodes
    # color is the color for nodes. When it is set as None the Plotly default color is used
    # size is the size of the dots representing the nodes
    #opacity is a value between [0,1] defining the node color opacity
    L=len(pos)
    trace = Scatter(x=[], y=[],  mode='markers', marker=Marker(size=[]))
    for k in range(L):
        trace['x'].append(pos[k][0])
        trace['y'].append(pos[k][1])
    attrib=dict(name='', text=labels , hoverinfo='text', opacity=opacity) # a dict of Plotly node attributes
    trace=dict(trace, **attrib)# concatenate the dict trace and attrib
    trace['marker']['size']=size
    return trace     
	
	
def scatter_edges(G, pos, line_color=None, line_width=1):
	trace = Scatter(x=[], y=[], mode='lines')
	for edge in G.edges():
		trace['x'] += [pos[edge[0]][0],pos[edge[1]][0], None]
		trace['y'] += [pos[edge[0]][1],pos[edge[1]][1], None]  
		trace['hoverinfo']='none'
		trace['line']['width']=line_width
		if line_color is not None: # when it is None a default Plotly color is used
			trace['line']['color']=line_color
	return trace        

#fill dictionaries 
for post in posts:
	tags = post["tags"].split()
	id = post["id"]
	
	print "========="
	print "ID: " + str(id) 
	print "Tags: " + str(tags)
	print "========="
	print " "
	
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
G=nx.MultiDiGraph()
G.add_nodes_from(i[0] for i in tuples)

for k1, v1 in tuples: 
	for k2, v2 in tuples:
		if k1 == k2: 
			break
		
		commons = v1.intersection(v2)
		a = tuples.index((k1,v1))
		b = tuples.index((k2,v2))
		
		#print k1 + ":" + str(a) + " U " + k2 + ":" + str(b) + " = " + str(commons)
		print k1 + " , " + k2 + " : " + str(len(commons))
		#matrix[a][b] = commons 
		if len(commons) >= 1:
			Edges.append((k1,k2, len(commons)))
			#G.add_edge(k1,k2,weight=commons)

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

#nx.draw_networkx_nodes(G, pos)
#nx.draw_networkx_edges(G, pos, edge_color=edgewidth)
nx.draw(G, node_color='c', node_size=nodesize , edge_width=edgewidth, with_labels=True)
plt.show()

raw_input ("Press <enter> to terminate program") 
