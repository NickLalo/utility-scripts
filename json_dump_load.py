import json  
      
test_dict ={
    "a": 1,
    "b": 2,
    "c": 3
}  

# dump json
with open("test_dict.json", "w", encoding='utf-8') as outfile:  
    json.dump(test_dict, outfile)

test_dict = {}

# load json
with open("test_dict.json", "r") as infile:
    test_dict = json.load(infile)

for key, value in test_dict.items():
    print(key, value)