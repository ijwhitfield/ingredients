# run this script to completely recompute all edges and nodes based on the data in recipes (you probably made a mistake)

import csv
#TODO save group data by making a nodedict first, and adding group data to the new nodes
if input("Are you sure you want to recompute all edges and nodes? (y/n): ")=='y':
    #save group data (groupdict)
    groupdict = dict()
    with open('nodes.csv','r',newline='') as nodescsv:
        reader = csv.reader(nodescsv)
        next(reader)
        for row in reader:
            groupdict[row[0]]=row[1]

    with open('recipes.csv','r',newline='') as reccsv, open('nodes.csv','w',newline='') as nodescsv, open('edges.csv','w',newline='') as edgescsv:
        recreader = csv.reader(reccsv)
        next(recreader)
        recdict = dict()
        nodedict = dict()
        edgedict = dict()
        for row in recreader: #each row is an ingredient
            # add to recipe so we can do edges later
            if row[0] in recdict.keys():
                recdict[row[0]].append(row[1])
            else:
                recdict[row[0]]=[row[1]]
            # add to node, recipe independent
            if row[1] not in nodedict.keys():
                if row[1] in groupdict.keys():
                    nodedict[row[1]]=[groupdict[row[1]],1]
                else:
                    nodedict[row[1]]=['unknown',1]
            else:
                nodedict[row[1]][1]+=1
        for recipe in recdict.keys():
            recdict[recipe] = sorted(recdict[recipe]) # the A ingredient will always be earlier alphabetically than the B ingredient
            for a_index in range(len(recdict[recipe])-1):
                a=recdict[recipe][a_index]
                for b in recdict[recipe][a_index+1:]:
                    if (a,b) in edgedict.keys():
                        edgedict[(a,b)]+=1
                    else:
                        edgedict[(a,b)]=1
        nodewriter = csv.writer(nodescsv)
        nodewriter.writerow(['ID','Group','Size'])
        for node in nodedict.keys():
            nodewriter.writerow([node]+nodedict[node])
        print("Nodes written")

        edgewriter = csv.writer(edgescsv)
        edgewriter.writerow(['A','B','Weight'])
        for edge in edgedict.keys():
            edgewriter.writerow(list(edge)+[edgedict[edge]])
        print("Edges written")  