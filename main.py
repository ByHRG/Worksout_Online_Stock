import requests
import json


class WORKSOUT:
    def __init__(self):
        self.url = "https://worksout.co.kr/product/"

    def url_setting(self, url):
        return url.split("/")[-1]

    def run(self, product_code):
        if "worksout" in product_code:
            product_code = self.url_setting(product_code)
        try:
            req = requests.get(self.url + product_code)
            data = json.loads(
                req.text.split('<script id="__NEXT_DATA__" type="application/json">')[
                    -1
                ].split("</script>")[0]
            )
        except:
            req = requests.get(self.url + product_code + "?reloaded")
            data = json.loads(
                req.text.split('<script id="__NEXT_DATA__" type="application/json">')[
                    -1
                ].split("</script>")[0]
            )

        output = {
            "Name": data["props"]["pageProps"]["productDetail"]["productName"],
            "Model": data["props"]["pageProps"]["productDetail"]["productCode"],
            "Image": data["props"]["pageProps"]["productDetail"]["productImageUrls"][0],
            "Price": str(data["props"]["pageProps"]["productDetail"]["currentPrice"]),
            "Url": self.url + product_code,
            "Stock": {},
        }
        for i in data["props"]["pageProps"]["productDetail"]["productSizes"]:
            data = {str(i["sizeName"]): str(i["currentStock"])}
            output["Stock"].update(data)
        return output


print(WORKSOUT().run('https://worksout.co.kr/product/153437'))
