# System rate test

import requests
import json
import time
import random
from datetime import datetime
import time
import random


url = 'http://172.18.83.153:9102/' # Production ESS-SWAGGER IP:PORT
queryStock_url = url + 'imhs-api/customer/QUERY_STOCK'
queryOutbound_url =  url + 'imhs-api/samsung/createOrderOutbound'

headers = {'Content-Type': 'application/json', 'accept': 'application/json'}


def getStockInformation():
    
    empty_set = []
    payload = {"queryMode": "TOTAL"}
    response = requests.post(queryStock_url,data=json.dumps(payload),headers=headers)
    result = response.json()
    skuCodes = result.get('data')
    for sku in skuCodes:
        skuCode = sku.get('skuCode')
        empty_set.append(skuCode)
    return empty_set

def getRandomWesOrders(NumOrder, getSku):

    
    for sku in range(NumOrder):
        skuId = random.choice(getSku)
        payload = {
            "orderNo": f"task-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "orderRuleTypeCode": "OUTBOUND",
            "detailList": [
                {
                    "skuCode": skuId,
                    "qty": 1
                    }
                ]
            }
        #print(payload)
        response = requests.post(queryOutbound_url,data=json.dumps(payload),headers=headers)
        result = response.json()
        time.sleep(1)
        #print(result)
        #print(payload)

def getSkuBatch(NumOrder, getSku):
    
    newdata=[]
    for sku in range(NumOrder):
        skuId = random.choice(getSku)
        if(sku == NumOrder-1):
            data = {"skuCode": skuId, "qty": 1}
            newdata.append(data)
        else:
            data = {"skuCode": skuId, "qty": 1},
            newdata.append(data)

        res = " ".join([str(item) for item in newdata])
    #print(res)
    check = res.replace('(', '')
    skubatch = check.replace(')', '')
    #print(skubatch)
    

    payload= {
        "orderNo": f"task-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "orderRuleTypeCode": "OUTBOUND",
        "detailList": [str(skubatch)]
        }
    
    print(payload)
    #response = requests.post(queryOutbound_url,data=json.dumps(payload),headers=headers)
    #result = response.json()
    #print(result)
        
    
    
    
        
        






if __name__ == '__main__':
    maxOrder = 100
    getSku = getStockInformation()
    #getRandomWesOrders(maxOrder,getSku)
    getSkuBatch(maxOrder,getSku)
