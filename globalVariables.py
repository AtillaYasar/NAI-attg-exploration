

defaultPayload ={"input": "[ Author:",
                 "model": "euterpe-v2", #euterpe-v2, #6B-v4, #krake-v2
                 "parameters":{
                     "use_string":True,
                     "prefix":"vanilla",
                     "temperature":1.33,
                     "max_length":400,
                     "min_length":1,
                     "top_p":0.88,
                     "top_a":0.085,
                     "typical_p":0.965,
                     "tail_free_sampling":0.937,
                     "repetition_penalty":1.05,
                     "repetition_penalty_range":560,
                     "repetition_penalty_frequency":0,
                     "repetition_penalty_presence":0,
                     "order":[3,4,5,2,0],
                     "num_logprobs":30
                     }
                 }

'''
headers = {'Content-Type': 'application/json',
           'authorization': 'Bearer secretauthorizationkey'
           }
'''

# you need to add an authorization key to the 'headers' dictionary below, as is shown above, except obviously using the correct key.
headers = {'Content-Type': 'application/json'}





















