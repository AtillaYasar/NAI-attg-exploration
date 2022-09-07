# contains a request header with my authorization key
from globalVariables import headers, defaultPayload

import json, requests, threading, ast
import tkinter as tk
from tkinter import ttk


def readTxt(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        contents = f.read()
    return contents

# making calls with the NovelAI API, it generates text using an AI
def apiCall(context):

    # settings for the generation
    payload = json.loads(getFromText(parametersText))
    payload['input'] = getFromText(promptText)
    del payload['parameters']['num_logprobs']

    url = "https://api.novelai.net/ai/generate"
    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
    
    content = response.content
    
    decodedContent = content.decode()
    decodedContent = decodedContent.replace("null", "0.0000")
    stringified = ast.literal_eval(decodedContent)
    
    output = stringified["output"]

    # just for making sure everything is working as expected
    print('\n\n', {'payload':payload['input']}, '\n\n', {'content':content})

    return output

def getFromText(textWidget):
    text = textWidget.get(1.0, 'end')[:-1]
    return text

# button function
def newGeneration():
    context = getFromText(promptText)
    apiResponse = apiCall(context)

    # clear text widget and put response in
    text.delete(1.0, 'end')
    text.insert(1.0, apiResponse)

# not in use yet.
def continueGeneration():
    context = getFromText(promptText) + getFromText(text)
    apiResponse = apiCall(context)



root = tk.Tk()

# style
textSettings = {'bg':'black', 'insertbackground':'red', 'fg':'light blue', 'height':'20', 'width':'100', 'font':('comic sans', '15')}
labelSettings = {'font':('comic sans', '10')}

# make widgets
tabContainer = tk.ttk.Notebook(root)
tabContainer.enable_traversal()

parametersTab = tk.Frame(root)
promptTab = tk.Frame(root)
displayTab = tk.Frame(root)

tabContainer.add(parametersTab, text='parameters')
tabContainer.add(promptTab, text='prompt')
tabContainer.add(displayTab, text='results')

parametersText = tk.Text(parametersTab, **textSettings)
label = tk.Label(displayTab, text='press f5 to generate', **labelSettings)
promptText = tk.Text(promptTab, **textSettings)
text = tk.Text(displayTab, **textSettings)


# putting the API call on a different thread, so that it doesn't freeze the app during generation
root.bind('<KeyPress-F5>', lambda *args:threading.Thread(target=newGeneration).start())

# place widgets
for w in tabContainer, promptText, text, parametersText:
    w.pack()

promptText.insert(1.0, readTxt('prompt.txt'))
parametersText.insert(1.0, str(json.dumps({k:v for k,v in defaultPayload.items() if k != 'input'}, indent=2)))


root.mainloop()




















