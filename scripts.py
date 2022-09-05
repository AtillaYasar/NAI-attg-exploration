import json, requests, time, os, ast, math
from globalVariables import headers, defaultPayload

# I included stuff about dependencies in front of every function, which currently has no use.
# I'll later add some stuff that makes sense of that.

# takes a default dictionary and one containing only the changes to be made, returns the changed dictionary
# for example: default = {a:0, b:1, ..., z:25}, changes = {b:420}, it will return default, except with b changed to 420.
def alterDefault(changes, default):
    #no dependencies
    
    changesKeys = changes.keys()
    defaultKeys = default.keys()
    
    res = {}
    for option in defaultKeys:
        if option in changesKeys:
            res[option] = changes[option]
        else:
            res[option] = default[option]
            
    return res

def setPayload(newPayload):
    #dependencies
    #setPayload: payload
    
    global payload
    payload = newPayload

def updateScriptsPayload(changes):
    setPayload(alterDefault(changes, defaultPayload))

def makeJson(dic, filename):
    #dependencies
    #openJson: json
    
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(dic, f, indent=2)
        f.close()

def openJson(filename):
    #dependencies
    #openJson: json
    
    with open(filename, 'r', encoding="utf-8") as f:
        contents = json.load(f)
        f.close()
    return contents

generationCount = 0
#generates text using the NovelAI API
#also prints the count each time it generated something.
def generateText():
    #dependencies
    #generateText: ast, json, requests, generationCount
    
    global generationCount

    url = "https://api.novelai.net/ai/generate"
    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
    content = response.content
    
    decodedContent = content.decode()
    decodedContent = decodedContent.replace("null", "0.0000")
    stringified = ast.literal_eval(decodedContent)
    
    output = stringified["output"]
    logprobs = stringified["logprobs"]
    
    generationCount += 1
    print(generationCount)
    
    return {"payload":payload, "output":output, "logprobs":logprobs}

def justGenerate(iterations):
    #dependencies
    #justGenerate: generateText, makeJson, payload, uniqueTime, os

    #write prompt
    prompt = payload['input']
    if 'outputs.txt' in os.listdir(os.getcwd()):
        with open('previous outputs.txt', 'w') as f2:
            with open('outputs.txt', 'r') as f:
                f2.write(f.read())
        
    with open('outputs.txt', 'w') as f:
        f.write(''.join(['====== prompt: ======\n', prompt, '\n====== outputs ======\n', '------------------------------', '\n']))
        print(''.join(['====== prompt: ======\n', prompt, '\n====== outputs ======\n', '------------------------------', '\n']))

    #write each iteration as it comes out
    for i in range(iterations):
        response = generateText()
        output = response['output']
        
        with open('outputs.txt', 'a') as f:
            f.write(''.join([output, '\n', '------------------------------', '\n']))
            print(''.join([output, '\n', '------------------------------', '\n']))

def splitDictionary(dict_arg, names, contents, ID, extension, folder):
    #dependencies
    #splitDictionary: makeJson
    
    if len(names) != len(contents):
        exit('names and contents lists must have equal length')
        
    def makeName(name):
        return "".join(['(', name, ') ', ID, extension])
    
    manyDicts = []
    for lst in contents:
        subset = {'ID':ID}
        for k in lst:
            subset[k] = dict_arg[k]
        manyDicts.append(subset)
    for n, name in enumerate(names):
        name = makeName(name)
        
        filePath = folder + "/" + name
        makeJson(manyDicts[n], filePath)

def uniqueTime():
    #dependencies
    #uniqueTime: time
    
    return str(time.time()).replace('.', 'd')


def openListFile(filename):
    with open(filename, "r", encoding='utf-8') as f:
        lst = json.load(f)
    return lst

def listToFile(list_arg, filename, overwrite = 0):
    #no dependencies
    
    if overwrite:
        mode = "w"
    else:
        mode = "x"
    with open(filename, mode) as f:
        json.dump(list_arg, f, indent=2)
    return 0

#puts a set of logprobs into a more readable form
def processLogprobs(logprobs):
    #no dependencies
    
    allProcessed = []
    for generation in logprobs:
        chosenList = generation["chosen"]
        beforeList = generation["before"]

        chosenId = chosenList[0][0][0]
        chosenProb = chosenList[0][1][0]

        beforeProcessed = {"ids":[], "probs":[]}
        for token in beforeList:
            tokenId = token[0][0]
            tokenProb = token[1][0]
            beforeProcessed["ids"].append(tokenId)
            beforeProcessed["probs"].append(tokenProb)
        
        stringify = lambda iterable:",".join(map(str,iterable))
        beforeProcessed["ids"] = stringify(beforeProcessed["ids"])
        beforeProcessed["probs"] = stringify(beforeProcessed["probs"])

        beforeProcessed = [beforeProcessed["ids"], beforeProcessed["probs"]]
        
        generationProcessed = {"chosen":[chosenId, chosenProb], "alternatives":beforeProcessed}
        allProcessed.append(generationProcessed)
    return allProcessed

def processResponse(context, response):
    #dependencies:
    # processResponse: processLogprobs, dissectAttg
    
    logprobs = processLogprobs(response["logprobs"])
    output = response['output']
    tags = dissectAttg(context + output)
    return {'logprobs':logprobs, 'tags':tags, 'output':output}

#uses promptList to generate.. puts output files in outputFolder.
def firstStageGeneration(promptList, outputFolder):
    #dependencies:
    # firstStageGeneration: generateText, processResponse, uniqueTime
    def promptToFiles(prompt, splittingArguments, extraStuff={}):

        response = generateText()
        
        outputsName = outputFolder + "\\outputs.txt"
        with open(outputsName, "a") as f:
            f.write(''.join([response['output'], '\n', '------------------------------', '\n']))
            
        processed = processResponse(prompt, response)

        fullDict = extraStuff
        for k, v in processed.items():
            fullDict[k] = v
        fullDict['raw response'] = response
        
        splitDictionary(dict_arg = fullDict, ID = uniqueTime(), **splittingArguments)

    #defining how to split this dictionary into files. promptToFiles() will create several json files the API response.
    splittingArguments = {'names':['first stage normal', 'first stage logprobs', 'first stage raw'],
                          'contents':[['context','tags','output'],
                                      ['logprobs'],
                                      ['raw response']],
                          'extension':'.json',
                          'folder': outputFolder }

    for prompt in promptList:
        setPayload(alterDefault({'input':prompt}, payload))
        promptToFiles(prompt, splittingArguments, {'context':prompt})

def cleanEdges(string):
    #no dependencies
    
    if len(string) == 0:
        return string
    dirty = [" ","\t","\n"]
    while True:
        if string[0] in dirty:
            string = string[1:]
        else:
            break
    while True:
        if string[-1] in dirty:
            string = string[:-1]
        else:
            break
    return string

dictCrawlerResult = {}
def updateOriginals(context):
    #note: uses dictCrawlerResult and 2 global variables. danger danger.
    #dependencies
    #updateOriginals: cleanEdges
    
    global originalCat, originalEntry
    def getOriginal():
        originalCat, _, originalEntry = map(cleanEdges, cleanEdges(context).partition('[ ')[2].partition(';')[0].partition(':'))
        return originalCat, originalEntry
    originalCat, originalEntry = getOriginal()
    if originalCat not in dictCrawlerResult.keys():
        dictCrawlerResult[originalCat] = {}
    if originalEntry not in dictCrawlerResult[originalCat].keys():
        dictCrawlerResult[originalCat][originalEntry] = {}

#dictionary crawler, adjusted to collect tag stuff."
def dictCrawler(arg):
    #dependencies
    #dictCrawler: updateOriginals
    
    def ifList(listArg):
        for item in listArg:
            dictCrawler(item)

    def ifDict(dictArg):
        if 'tags' in dictArg.keys():
            updateOriginals(dictArg['context'])
            tags = dictArg['tags']
            for cat, entry in dictArg['tags'].items():
                if cat not in dictCrawlerResult[originalCat][originalEntry].keys():
                    dictCrawlerResult[originalCat][originalEntry][cat] = []
                dictCrawlerResult[originalCat][originalEntry][cat].append(entry)
                
        for value in dictArg.values():
            dictCrawler(value)

    def ifElse(value):
        pass
    
    t = type(arg)
    if t == list:
        ifList(arg)
    elif t == dict:
        ifDict(arg)
    else:
        ifElse(arg)

def pListToFolder(pList, outFolder):
    #dependencies:
    #pListtoFolder: time, firstStageGeneration, openListFile, dictCrawler, makeJson, os
    
    os.mkdir(outFolder)

    firstStageGeneration(pList, outFolder)
    firstStageCollection(outFolder)

    allTags = openListFile(outFolder + "/" + 'first stage collection')
    dictCrawler(allTags)
    makeJson(dictCrawlerResult, outFolder + "/" + 'dcr.json')


    overview = {'list of prompts':pList,
                'payload':payload,
                'amount of requests':len([name for name in os.listdir(outFolder) if 'first stage raw' in name])}
    makeJson(overview, outFolder+'\\overview of this folder.json')
    
    #os.rename(outFolder, outFolder.replace(' (b)', ''))

def decode(ids):
    #dependencies
    #decode: tokenList

    # tokenList = openListFile('gpt2 tokens')
    if type(ids) == int:
        return tokenList[ids]
    return list(map(lambda ID:tokenList[int(ID)], ids))

def contToDistr(prompt, logprobs):
    #dependencies
    #contToDistr: decode, math
    
    chosenTokens = []
    distributions = {}

    for d in logprobs:
        context = prompt + ''.join(decode(chosenTokens))
        #print('c:',context)
        alternatives, probs = d['alternatives']
        alternatives = decode(alternatives.split(','))
        probs = list(map(lambda s:round( math.exp(float(s)), 3), probs.split(',')))
        #print('alt:',alternatives,'\n')
        
        distributions[context] = {}
        for i in range(min(len(alternatives), len(probs))):
            distributions[context][str(alternatives[i])] = probs[i]
        
        chosenTokens.append(d['chosen'][0])
    return distributions

def linkDistributions(inFolder):
    #dependencies:
    #listDistributions: contToDistr, decode, processLogprobs, listToFile, openListFile

    global tokenList
    tokenList = openListFile('gpt2 tokens')
    
    relevantPaths = [f"{inFolder}\\{name}" for name in os.listdir(inFolder) if 'first stage raw' in name]
    contextsToDistribution = []
    for path in relevantPaths:
        file = openListFile(path)
        ID = file['ID']
        logprobs = processLogprobs(file['raw response']['logprobs'])
        prompt = file['raw response']['payload']['input']
        
        contextsToDistribution.append({'ID':ID,
                                       'prompt':prompt,
                                       'distributions':contToDistr(prompt, logprobs)})
        
    listToFile(contextsToDistribution, f'{inFolder}\\contexts to distributions.json', 1)
    return 0

def addDistr(d, distr):
    dCopy = d
    for token, number in distr.items():
        if token not in dCopy:
            dCopy[token] = 0
        dCopy[token] += number
    return dCopy

def firstMatch(string, matches):
    for match in matches:
        if match in string:
            return match
    return None

def endsWith(string, end):
    #checks if 'string' ends with 'end'. returns Boolean
    l = len(end)
    if string[-l:] == end:
        return True
    else:
        return False

def sortByValues(d):
    #no dependencies
    
    l = {}
    for k,v in d.items():
        if v not in l:
            l[v] = []
        l[v].append(k)
    l = {k:l[k] for k in sorted(l.keys(), reverse=True)}
    
    dSorted = {}
    for number, keys in l.items():
        for key in keys:
            dSorted[key] = number

    return dSorted

def sortAndSumDistributions(inFolder):
    #dependencies
    #sortAndSumDistributions: os, linkDistributions, openListFile, firstMatch, addDistr, listToFile, sortByValues

    if inFolder + "\\contexts to distributions.json" not in os.listdir(inFolder):
        linkDistributions(inFolder)
    linkedContexts = openListFile(inFolder + "\\contexts to distributions.json")

    authors = openListFile('top authors.json').keys()

    #for contexts that ends with a colon, it checks which author is in context"
    #and sums the contexts for that author's dictionary"
    firstEntries = {}
    for d in linkedContexts:
        for context, distr in d['distributions'].items():

            if endsWith(context, ':'):
                author = firstMatch(context, authors)
                
                if author not in firstEntries:
                    firstEntries[author] = {}
                if context not in firstEntries[author]:
                    firstEntries[author][context] = {}
                    
                firstEntries[author][context] = addDistr(firstEntries[author][context], distr)

    #sorts each distribution by values"
    firstEntriesV2 = {}
    for author, contexts in firstEntries.items():
        if author not in firstEntriesV2:
            firstEntriesV2[author] = {}
        for context, distribution in contexts.items():
            if context not in firstEntriesV2[author]:
                firstEntriesV2[author][context] = {}
            firstEntriesV2[author][context] = sortByValues(distribution)

    listToFile(firstEntriesV2, inFolder + "\\summed and sorted distributions.json", 1)


#takes a string containing attg stuff, returns a dictionary of category:entry pairs.
def dissectAttg(attg):
    #dependencies:
    #dissectAttg: cleanEdges
    res = cleanEdges(cleanEdges(attg).partition("[")[2].partition("]")[0]).split("; ")
    def f(l):
        res = {}
        for item in l:
            k,_,v = item.partition(":")
            if len(v) == 0:
                continue
            if v[0] == " ":
                v = v[1:]
            while True:
                if k in res.keys():
                    k += '+'
                else:
                    break
            res[k] = v
        return res
    res = f(res)
    return res

def firstStageCollection(outputFolder):
    #dependencies:
    #firstStageCollection: os, openJson, listToFile
    relevantFiles = [name for name in os.listdir(outputFolder) if 'first stage normal' in name]
    gatheredTags = []
    for name in relevantFiles:
        file = openJson(outputFolder + '/' + name)
        gatheredTags.append({k:v for k, v in file.items() if k in ['ID', 'context', 'tags']})
    listToFile(gatheredTags, outputFolder + '/first stage collection')














