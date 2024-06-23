# import requests
# import json

# url = "http://127.0.0.1:5000/todo?updated_after=2024-06-22"
# headers = {"Content-Type": "application/json"}
# # data = {
# #     "name": "Buy Laptop",
# #     "description": "Fix the Laptop"
# # }

# # # response = requests.post(url, headers=headers, data=json.dumps(data))

# response2 = requests.get(url, headers=headers)
# complete_response = response2.json()
# print(response2.status_code)
# print(complete_response)

# with open("todo.json", "w") as file:
#     json.dump(complete_response, file, indent=4)

# print(response.status_code)
# print(response.json())


import requests

url = 'http://127.0.0.1:5000/todo/01J12V4P6EBJ5W83MND7T867XF'
params = {
    # 'name': 'Osama',
    # 'description': 'hello',
    'is_Completed' : False
}

response = requests.put(url, params=params)

print(response.status_code)
print(response.json())  # If the server returns JSON response


# import requests

# url = 'http://127.0.0.1:5000/todo/01J11D4EN6BK5CQNCNZGT6KW9'

# response = requests.delete(url)

# print(response.status_code)
# print(response.text)  # Response content, if any
