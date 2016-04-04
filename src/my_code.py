import json as sj
import sys
import datetime as dt
from dateutil import parser
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt

# reads the input tweet file
input_file = open(sys.argv[1])
output_file = open(sys.argv[2],'a')
lines = input_file.readlines()
leng = len(lines)
#print leng
time_list = []
total_hashtags=[]
# Loops through the input tweet file, till it reaches a tweet posted 60 seconds ago..
for count in range(leng):
	json = sj.loads(lines[count].strip())
	date_of_tweet = parser.parse(json['created_at'])
	#print 'Twitted Date: ',date_of_tweet
	time_list.append(date_of_tweet)
	max_date_tweet = max(dt for dt in time_list)
	if (abs(max_date_tweet - date_of_tweet).seconds <= 60) :
		try:
			hash_tags = []
			hash_text = json['entities']['hashtags']
			# if there is any hash tag in the tweet, extract only the ascii content hash tags from the tweet
			if len(hash_text) > 0:
				hash_tags = ['#'+i['text'].encode('ascii','ignore').lower() for i in hash_text if len(i['text'].encode('ascii','ignore')) > 0]
				#print hash_tags
        	# if the hash tags are more than one, then they are used to build edge-list and to calculate degree
			if len(hash_tags) > 1:
				time_list.append(date_of_tweet)
				total_hashtags.append(hash_tags)
			indices_to_delete = [i for i, j in enumerate(time_list) if abs(j-max_date_tweet).seconds > 60]
			time_list = [x for i,x in enumerate(time_list) if i not in indices_to_delete]
			total_hashtags = [x for i,x in enumerate(total_hashtags) if i not in indices_to_delete]
		except KeyError:
			print "Error in hashtags"

	# Creating all the combinations of hash tags and sorted so as to avoid duplicated edge list
	edge_list=[]
	for i in total_hashtags:
		edge_list.append(list(combinations(sorted(i),2)))
		#print edge_list
	set_list = {j for i in edge_list for j in i} # duplicate edge list is avoided by Set item

	# Created Graph using Networkx module, plotted graph and extracted degree and number of nodes
	G=nx.Graph()
	G.add_edges_from(set_list)
	try:
		avg_deg = round(sum(G.degree().values())*1.0/len(G.nodes()),2)
		#print len(G.nodes()),avg_deg
		output_file.write('%s\n'%(avg_deg))
	except ZeroDivisionError:
		print "No hashtags found in the last 60 seconds to create hash graph"

	nx.draw(G,nx.spring_layout(G, scale=2),node_size=500,with_labels=True)
	# nx.draw_networkx_labels(G,nx.spring_layout(G),labels=cities)
	# plt.savefig('circular_tree.png')
	plt.show()
