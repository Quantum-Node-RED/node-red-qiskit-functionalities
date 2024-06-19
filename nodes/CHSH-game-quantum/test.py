import sys
import json

input = sys.argv[1]
parse_input = json.loads(input)

x = parse_input["x"]
y = parse_input["y"]

result = {"a": x, "b": y}

if x == 0 or y == 0:
  result["result"] = "win"
else:
  result["result"] = "lose"

print(json.dumps(result))
