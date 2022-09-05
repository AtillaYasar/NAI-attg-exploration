

defaultPayload ={"input": "some nonsense:",
                 "model": "6B-v4", #euterpe-v2, #6B-v4, #krake-v2
                 "parameters": {
                     "use_string": True,
                     "prefix":"vanilla",
                     "trim_whitespaces": False,
                     "temperature": 1,
                     "min_length": 10,
                     "max_length": 100,
                     "stop_sequences": [],# [ [60],[2361],[198],[59],[837],[11] ],
                     "num_logprobs": 30
                     }
                 }

'''
headers = {'Content-Type': 'application/json',
           'authorization': 'Bearer secretauthorizationkey'
           }
'''

# you need to add an authorization key to the 'headers' dictionary below, as is shown above, except obviously using the correct key.
headers = {'Content-Type': 'application/json'}





















