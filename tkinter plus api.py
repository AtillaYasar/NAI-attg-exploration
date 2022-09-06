# contains a request header with my authorization key
from globalVariables import headers, defaultPayload

import json, requests, threading, ast
from tkinter import*


def readTxt(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        contents = f.read()
    return contents

# making calls with the NovelAI API, it generates text using an AI
def apiCall(context):

    # settings for the generation
    payload = defaultPayload
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
    return textWidget.get(1.0, 'end')[:-1]

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



root = Tk()

# style
textSettings = {'bg':'black', 'insertbackground':'red', 'fg':'light blue', 'height':'10', 'font':('comic sans', '15')}
labelSettings = {'font':('comic sans', '10')}

# make widgets
label = Label(root, text='press f5 to generate', **labelSettings)
promptText = Text(root, **textSettings)
text = Text(root, **textSettings)

# putting the API call on a different thread, so that it doesn't freeze the app during generation
root.bind('<KeyPress-F5>', lambda *args:threading.Thread(target=newGeneration).start())

# place widgets
for w in label, promptText, text:
    w.pack()

promptText.insert(1.0, readTxt('prompt.txt'))




root.mainloop()




















