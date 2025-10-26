import requests

BASE = "http://127.0.0.1:5000/"

response1 = requests.get(BASE + "helloworld/hilanco")
response2 = requests.put(BASE + "video/42",{"likes":10})
response3 = requests.put(BASE + "video/42",{"name": "video", "views":5, "likes":10})
response4 = requests.get(BASE + "video/4")

print(response1.json())
print(response2.json())
print(response3.json())
print(response4.json())

print('\n')

data = [{"name": "video1", "views":5, "likes":10},
		{"name": "video2", "views":10, "likes":20},
		{"name": "video3", "views":15, "likes":30},
		{"name": "video4", "views":20, "likes":40}]

for i in range(len(data)):
	response = requests.put(BASE + "video/" + str(i), data[i])
	print(response.json())

response5 = requests.delete(BASE + "video/0")
print(response5)

for i in range(len(data)):
	response = requests.get(BASE + "video/" + str(i))
	print(response.json())

print('\n')

data = [{"name": "video1", "views":5, "likes":10},
		{"name": "video2", "views":10, "likes":20},
		{"name": "video3", "views":15, "likes":30},
		{"name": "video4", "views":20, "likes":40}]

for i in range(len(data)):
	response = requests.put(BASE + "video_db/" + str(i), data[i])
	print(response.json())

response6 = requests.delete(BASE + "video_db/0")
print(response6)

for i in range(len(data)):
	response = requests.get(BASE + "video_db/" + str(i))
	print(response.json())

response7 = requests.get(BASE + "video_db/500")
print(response7.json())

print('\n')

response8 = requests.patch(BASE + "video_db/1", {"name": "new_name"})
print(response8.json())