from scripts import*
from globalVariables import headers, defaultPayload


with open('prompt.txt', 'r') as f:
    contents = f.read()
        
alterations = {
    'input':contents,
    'model':'euterpe-v2'}

updateScriptsPayload(alterations) 

#the actual point of this repo.
if 1:
    iterations = 5

    folderName = 'example folder'
    if folderName not in os.listdir(os.getcwd()):
        os.mkdir(folderName)
           
    baseFolder = os.getcwd()
    outFolder = baseFolder + '\\' + folderName + "\\" + uniqueTime()
    pListToFolder( [alterations['input']]*iterations, outFolder)
    linkDistributions(outFolder)


#for just generating for fun. output will be in outputs.txt and previous outputs.txt
#write the prompt in prompt.txt in the folder ../attg exploration
# and set iterations to whatever you want.
if 0:
    iterations = 3

    justGenerate(iterations)















