import json

with open('~/Projects/my_remote/documentation/sample.json') as f:
  data = json.load(f)

for device in data['on_load']:
    print(device['device'])
    for code_entry in device['codes']:
      if "code" in code_entry:
        print("  code is: %s" % code_entry["code"])
      if "delay" in code_entry:
        print("  delay is: %s" % code_entry["delay"])
