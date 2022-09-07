# NAI-attg-exploration
 
 ## What is this for?
 
 This code is to allow people to do research on the bracketed stuff at the start of a NovelAI story. (attg and more) 
 
 It makes API calls, processes the responses and puts them into json files.
 Then goes through the responses, including the probabilities of alternative tokens (logprobs), and puts them together into one json, so you can gain insights from them. (this "gaining insights" part still needs work) 
 
 There is some stuff to just play around with the AI as well. You can do that in 'usageExample.py' if you set research to False, and in 'tkinter plus api.py'
 
 A major goal is to make it easily usable by people who don't know anything coding, but it's not there yet. 'tkinter plus api.py' does that, but what you can do there is very limited.
 
 
 ## What is NovelAI?
 NovelAI is a website where you can co-author stories with an Artifical Intelligence trained to write stories. Check it out at novelai.net
 
 ## Instructions (not non-Pythoner-friendly yet)
 - You can use 'tkinter plus api.py' to generate things very easily. just open it, write your prompt in the first window and press f5 to generate.
 - usageExample.py shows how you could use scripts.py and globalVariables.py to get outputs.
	- basically you set the prompt in prompt.txt, set research to 0 in usageExample.py, run it, and outputs will go to outputs.txt and previous outputs.txt
 - the outputs will be collected in outputs.txt in outFolder you designate in usageExample.py
 - if you don't set an authorization key in globalVariables.py, meaning, if you leave it as is, I *think* it will use up your free trial generations. I am not 100% sure. Mostly sure.
	- you can find your authorization key from the network tab if you inspect the NAI page when you generate something, in 'generate', under 'Request Headers'
 - instructions for doing permutations are in permutations explanation, but in summary: $$$<version 1 name>:<text>,,,<version 2 name>:<text>$$$

 ## partial to-do list
 ### priority (not urgent)
 - better processing of the 'contexts to distributions.json' file, so that the contexts that belong together are together, and the corresponding probability
 - make this stuff non-Pythoner-friendly
 ### rest
 - lots and lots of refactoring and rewriting
 - distributions are summed. (the code for summing them is already in place)
 - add an easy way find an authorization key. (either a tutorial or using the Login feature from the API, if possible)
 - include decoding for Krake tokens
 - refactor, improve readability
 - include decoding for Krake token
 - integrate everything into the tkinter app (tkinter plus api.py)
