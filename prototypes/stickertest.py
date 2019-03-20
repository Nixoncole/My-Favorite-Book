import requests, sys, hashlib
from PIL import Image
import io
import json

img = Image.open("qr3.png")
md5 = hashlib.md5()
with io.BytesIO() as memf:
    img.save(memf, 'PNG')
    data = memf.getvalue()
    md5.update(data)
hash = md5.hexdigest()
print(hash)


baseurl = "https://sandbox.pwinty.com/v3.0"
order_path = "/orders"
image_path = "/orders/{}/images"
productlist_path = '/catalogue/prodigi direct/destination/US'
order_status_path = "/orders/{}/SubmissionStatus"
order_submission_path = "/orders/{}/status"

sticker_sku = "M-STI-3X4"

headers = {'Content-type': 'application/json',
           'accept': 'application/json',
           'X-Pwinty-MerchantId': '77f02b2f-ad0e-4265-b7f6-7e7cbf1a5b2e',
           'X-Pwinty-REST-API-Key': 'test_abc09cba-3b68-4263-b04b-f1e195881f6e'
           }
order_data = {'countryCode': 'US',
              'recipientName': 'Cole Nixon',
              'address1': '23707 SW Mountain Creek Rd',
              'addressTownOrCity': 'Sherwood',
              'stateOrCounty': 'Oregon',
              'postalOrZipCode': '97140',
              'preferredShippingMethod': 'Budget'
              }
# Place order
resp = requests.post(baseurl+order_path, headers=headers, json=order_data)
order_id = json.loads(resp.text)['data']['id']


image_path = image_path.format(order_id)
image_data = {'orderId': order_id,
              'sku': sticker_sku,
              'copies': 1,
              'size': 'ShrinkToFit',
              'url': 'https://api.qrserver.com/v1/create-qr-code/?data=http://localhost:5000/book/3&size=600x600'
              }
# Upload image
r = requests.post(baseurl+image_path, headers=headers, json=image_data)
print(r)

# Verify order is good to go
order_status_path = order_status_path.format(order_id)
hep = requests.get(baseurl+order_status_path, headers=headers)
if json.loads(hep.text)['data']['isValid'] == True:
    print(hep)
    # finalize order
    order_submission_path = order_submission_path.format(order_id)
    wow = requests.post(baseurl+order_submission_path, headers=headers, json={'status': 'Submitted'})
    print(wow)

    # and just like that, we have a fully functioning order management












