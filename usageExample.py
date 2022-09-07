from scripts import*
from globalVariables import headers, defaultPayload



'''instructions:
1) write your prompt in prompt.txt or in coded prompt.txt
2) set parameters below
3) run this file
4) results will appear in:
    if useCoded is True:
        coded outputs.txt' in this folder
        
    if research is True:
        in the 'example folder' folder, in a subfolder there

    if research is False and useCoded is False:
        'outputs.txt' and 'previous outputs.txt' in this folder and in the 'non research stuff' folder
'''

"set parameters here"
useCoded = False
research = True
iterations = 5


"dont go below"

if useCoded:
    prompt = readTxt('coded prompt.txt')
else:
    prompt = readTxt('prompt.txt')

alterations = {
    'input':prompt,
    'model':'6B-v4'}

updateScriptsPayload(alterations)



#the actual point of this repo.
if research:
    folderName = 'example folder'
    if folderName not in os.listdir(os.getcwd()):
        os.mkdir(folderName)
           
    baseFolder = os.getcwd()
    outFolder = baseFolder + '\\' + folderName + "\\" + uniqueTime()
    pListToFolder( [alterations['input']]*iterations, outFolder)
    linkDistributions(outFolder)


#for just generating for fun. output will be in outputs.txt. write the prompt in prompt.txt in the folder ../attg exploration
# and set iterations to whatever you want.
if not research:
    generateForFun(iterations)
















