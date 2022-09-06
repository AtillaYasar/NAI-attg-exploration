from scripts import*
from globalVariables import headers, defaultPayload


with open('prompt.txt', 'r') as f:
    contents = f.read()
        
alterations = {
    'input':contents,
    'model':'6B-v4'}

updateScriptsPayload(alterations) 

#the actual point of this repo.
research = False
if research:
    iterations = 5

    folderName = 'example folder'
    if folderName not in os.listdir(os.getcwd()):
        os.mkdir(folderName)
           
    baseFolder = r'C:\Users\Gebruiker\Desktop\attg exploration'
    outFolder = baseFolder + '\\' + folderName + "\\" + uniqueTime()
    pListToFolder( [alterations['input']]*iterations, outFolder)
    linkDistributions(outFolder)


#for just generating for fun. output will be in outputs.txt. write the prompt in prompt.txt in the folder ../attg exploration
# and set iterations to whatever you want.
if not research:
    iterations = 4

    generateForFun(iterations)
















