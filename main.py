import time
import requests
import json


class WORKSOUT:
    def __init__(self):
        self.header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ko-KR,ko;q=0.9',
            'Content-Type': 'application/json',
            'Origin': 'https://www.worksout.co.kr',
            'Sec-Fetch-Dest': 'cors',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebkit/605.1.15 (KHTML, like Gecko)  Mobile/15E148 Kasina/2.0.6',
        }

    def url_customize(self, data):
        return int(data.split("/")[-1])


    def size(self, url):
        out_data = {}
        req = requests.post("https://api.worksout.co.kr/v1/products/sizes", headers=self.header, data=json.dumps({"productIds": [url]}))
        for i in req.json()["payload"]:
            out_data.update({i["sizeName"]:i["productSizeId"]})
        for i in out_data:
            print(i)
            print(out_data[i])
        return out_data

    def login(self, data):
        req = requests.post("https://api.worksout.co.kr/v1/users/login", data=json.dumps(data), headers=self.header)
        self.header["Cookie"] = req.headers["Set-Cookie"]
        self.header["Authorization"] = f'bearer {req.headers["Set-Cookie"].split("refresh-token=")[-1].split("; ")[0]}'

    def cart_clear(self):
        req = requests.get("https://api.worksout.co.kr/v1/carts", headers= self.header)
        cart_list = []
        for i in req.json()["payload"]["carts"]:
            cart_list.append(i["cartId"])
        for i in cart_list:
            requests.put(f'https://api.worksout.co.kr/v1/carts/{i.split(":")[0]}', data=json.dumps({"sizeId": int(i.split(":")[-1])}), headers =self.header)

    def get_check(self, product_code, size):
        for i in size:
            data = json.dumps({"count":1,"sizeId":int(size[i]),"answer":""})
            cnt = 0
            while True:
                req = requests.post(f"https://api.worksout.co.kr/v1/carts/{product_code}", data=data, headers=self.header)
                if "NOT_FOUND" in req.json()["code"]:
                    break
                elif "PRODUCT_EXCEED" in req.json()["code"]:
                    break
                cnt += 1
            size[i] = cnt

        self.cart_clear()
        return size

    def run(self, data):
        data["url"] = self.url_customize(data["url"])
        size_list = self.size(data["url"])
        print(json.dumps(size_list, ensure_ascii=False, indent=4))
        self.login(data)
        self.cart_clear()
        return self.get_check(data["url"], size_list)




data = {
    "email": "",
    "password": "",
    "url": "https://www.worksout.co.kr/product/166310"
}

print(json.dumps(WORKSOUT().run(data), ensure_ascii=False, indent=4))
