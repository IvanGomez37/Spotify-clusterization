data = set()

f = open('10 mil id.txt', 'r')

for x in f :
    data.add(x)

with open('uniqueids.txt', 'w') as output:
    for dat in data:
        output.write(dat)