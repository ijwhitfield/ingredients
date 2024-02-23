# this script automates the backend data side of recipe collection

import csv

nodedict = dict()
edgedict = dict()
recdict = dict()
with open('nodes.csv', 'r', newline='') as nodescsv, open('edges.csv', 'r', newline='') as edgescsv, open('recipes.csv', 'r', newline='') as reccsv:
    reader = csv.reader(nodescsv)
    next(reader)
    for row in reader:
        nodedict[row[0]]=[row[1],int(row[2])]

    reader = csv.reader(edgescsv)
    next(reader)
    for row in reader:
        edgedict[(row[0],row[1])]=int(row[2])
    

    reader = csv.reader(reccsv)
    next(reader)
    for row in reader:
        if row[0] in recdict.keys():
            recdict[row[0]].append(row[1])
        else:
            recdict[row[0]]=[row[1]]
 
    print("You currently have "+str(len(nodedict.keys()))+" nodes, "+str(len(edgedict.keys()))+" edges, and "+str(len(recdict.keys()))+" recipes logged")
    while True: # add recipe loop
        while True: # pick a valid recipe name loop
            recipename = input("Enter a recipe name: ").lower().strip()
            if recipename in recdict.keys():
                print("You already added that recipe.")
            else:
                recdict[recipename]=[]
                break
        nexting=""
        while True: # add ingredient loop
            nexting = input("Enter an ingredient or 'done': ").lower().strip()
            if nexting == "done":
                break
            # don't allow repeat ingredients
            if nexting not in recdict[recipename]:
                recdict[recipename].append(nexting)
                if nexting not in nodedict.keys():
                    # if that ingredient is not yet listed in nodes.csv, add it with Group 'unknown' and count 1
                    nodedict[nexting]=['unknown',1]
                else:
                    # if that ingredient already is listed in nodes.csv, add 1 to its count
                    nodedict[nexting][1]+=1
        recdict[recipename] = sorted(recdict[recipename]) # the A ingredient will always be earlier alphabetically than the B ingredient
        for a_index in range(len(recdict[recipename])-1):
            a=recdict[recipename][a_index]
            for b in recdict[recipename][a_index+1:]:
                if (a,b) in edgedict.keys():
                    edgedict[(a,b)]+=1
                else:
                    edgedict[(a,b)]=1
        if input("Add another recipe? (y/n): ").strip()!='y':
            break

print("Starting the write process...")
with open('nodes.csv','w',newline='') as nodescsv, open('edges.csv','w',newline='') as edgescsv, open('recipes.csv','w',newline='') as reccsv:
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

    recwriter = csv.writer(reccsv)
    recwriter.writerow(['Recipe','Ingredient'])
    for rec in recdict.keys():
        #write a recipe-ingredient pair for every ingredient
        for ing in recdict[rec]:
            recwriter.writerow([rec]+[ing])
    print("Recipes Written")
