import json
import requests
import operator

startup = {}
startupscale = 1
maxval = 0.
with open('input.txt') as f:
    for line in f:
        (key, val) = line.split('%')
        startup[key] = float(val)
        if float(val) > maxval:
            maxval = float(val)

alls = {}
root = {}

for j in startup:
    minmatch = 0.3
    with open("./lastfm/.api_key") as apikeyfile:
        apikey = (apikeyfile.readlines())[0]
    file = ("http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar"
            + "&artist=" + j + "&api_key=" + apikey + "&format=json")

    response = requests.get(file)
    json_data = json.loads(response.content)

    for i in json_data['similarartists']['artist']:
        key = i['name']
        match = i['match']
        if float(match) < minmatch:
            continue
        wgt = float(match) * startup[j] / maxval
        if key in alls:
            alls[key] += wgt
            root[key] += (',' + j + '(' + str(wgt)
                          + ')(match' + str(match) + ')')
        else:
            alls[key] = wgt
            root[key] = j + '(' + str(wgt) + ')(match' + str(match) + ')'

outfile = open('output.txt', 'w')
sortedall = sorted(alls.items(),
                   key=operator.itemgetter(1), reverse=True)
for item in sortedall:
    print(item, file=outfile)

outrootfile = open('outroot.txt', 'w')
for item in sorted(root.items(),
                   key=operator.itemgetter(0), reverse=False):
    print(item, file=outrootfile)
