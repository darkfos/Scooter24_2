import requests as req


request = req.get("https://avatars.mds.yandex.net/get-mpic/4525599/img_id7535979219198325086.jpeg/orig")
print(request.content)