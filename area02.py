import requests
from os import system
import os
import base64
import random,string
from colorama import Fore, init
from datetime import datetime
print(" 初始化中.......\n")
Card_list = []
f = open('TEST.txt')
for line in f.readlines():
    Card_list.append(line.split('\n')[0])
f.close

fist = "AREA 02｜User : "
system("title " + fist)
appVersion = '906'
init()
def log(taskName, tag, str):
    time = datetime.now()
    time = time.strftime('%H:%M:%S:%f')
    status = ''
    color = ''
    colorWHITE = Fore.WHITE
    if tag == 'i':
        status = 'INFO'
        color = Fore.YELLOW
    elif tag == 'e':
        status = 'ERROR'
        color = Fore.RED
    elif tag == 's':
        status = 'SUCCESS'
        color = Fore.GREEN
    elif tag == 'g':
        status = 'GET IT'
        color = Fore.BLUE
    elif tag == 'd':
        status = 'DONE'
        color = Fore.CYAN
    else:
        return
    print(colorWHITE + f'[{time}]' + color + f"[{taskName}] [{status}] {str}"+ colorWHITE)

try:
    # 登入
    email = input('Email : ')
    PW = input('Password : ')

    print('\n')
    log('MAIN', 'i', '登入中...')
    headers = {
        "accept": "*/*",
        "accept-language": "zh-TW,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "origin": "https://www.area02.com",
        "referer": "https://www.area02.com/login",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    data = {
        "query": "\n        mutation($emailOrPhone: String!, $password: String!) {\n          login(emailOrPhone: $emailOrPhone, password: $password) {\n            errors {\n              field\n              message\n            }\n            user {\n              id\n            }\n          }\n        }\n      ",
        "variables": {"emailOrPhone": email, "password": PW}}

    S = requests.session()
    r = S.post('https://www.area02.com/api/graphql', headers=headers, json=data)
    #print(r.text)
    try:
        id = (r.json()['data']['login']['user']['id'])
        log('MAIN', 's', '登入成功!')
    except:
        log('MAIN', 'e', '登入失敗...!')
        error()

    data = {
        "query": "\n      query {\n        me {\n          id\n          name\n          email\n          phone_verified\n          phone\n          user_phone\n          country_code\n          status\n          isSeller\n          applySeller {\n            id\n            apply_status\n            createdAt\n            identified_id\n            apply_type\n            seller_email\n            bank_account_name\n            bank_number_value\n            bank_account_number\n            branch_name_value\n            seller_fee_percentage\n            company_id_value\n            company_account_value\n          }\n          profile {\n            id\n            gender\n            nickname\n            realname\n            sizeId\n            size_us\n            city\n            district\n            zipcode\n            addresstw\n            birthday\n          }\n        }\n      }\n    "}
    r = S.post('https://www.area02.com/api/graphql', headers=headers, json=data)
    # print(r)
    # print(r.text)
    name = r.json()['data']['me']['profile']['realname']

    fist = fist + "{}#{}｜".format(name, id)
    system("title " + fist)
    log('MAIN', 'i', '讀取已上架商品中...')
    #讀取已上架商品
    data = {"query":"\n      query {\n        sellerProduct {\n          products {\n            id\n            status\n            createdAt\n            node {\n              id\n              title\n              sku_value\n              sex_value\n              brand {\n                id\n                parentBrand {\n                  id\n                  name\n                }\n              }\n              nodeImage {\n                uri\n              }\n            }\n            size {\n              id\n              us\n            }\n            price\n            stock_amount\n          }\n        }\n      }\n    "}
    r = S.post('https://www.area02.com/api/graphql', headers=headers, json=data)
    #print(r)
    #print(r.text)
    #input('')

    list = r.json()['data']['sellerProduct']['products']
    old_list = []
    up_list = {}
    nb_list = {}

    #處理錯誤的資料
    f = open('ERROR.txt', 'a')
    ### 處理不在 EXCEL 清單的資料
    EXCELSKU_list = []
    # 讀取EXCEL 清單
    for i in range(len(Card_list)):
        sku = Card_list[i].split('\t')[0]
        if sku not in EXCELSKU_list:
            EXCELSKU_list.append(sku)
    ###
    log('MAIN', 'i', '讀取不在 EXCEL 清單商品中...')
    for i in range(len(list)):
        sku_value = (list[i]['node']['sku_value'])
        #print(sku_value)
        size = (list[i]['size']['us'])
        idd = (list[i]['id'])
        price = (list[i]['price'])
        stock_amount = (list[i]['stock_amount'])

        # 下架不在 EXCEL 的 商品
        if sku_value not in EXCELSKU_list:
            data = {
                "query": "\n        mutation($id: Float!) {\n          sellerRemoveProduct(id: $id) {\n            errors {\n              field\n              message\n            }\n            success\n          }\n        }\n      ",
                "variables": {"id": int(idd)}}
            r = S.post('https://www.area02.com/api/graphql', headers=headers, json=data)
            # print(r.text)

            log('MAIN', 'd', '更新 {} {} {}  已下架'.format(sku_value, size, r))
            # 剩下的 保存
        else:
            old_list.append('{}:{}'.format(sku_value,size))
            up_list[('{}:{}'.format(sku_value,size))]=('{}:{}'.format(idd,price))
            nb_list[('{}:{}'.format(sku_value,size))]=(stock_amount)





    #print(old_list)
    #print(up_list)

    #print((up_list)['DD1877-002:5.5'].split(':')[0])
    #print((up_list)['DD1877-002:5.5'].split(':')[1])


    #input('asdasasd')




    ###########
    success_list = 0
    error_list = 0
    for i in range(len(Card_list)):

        try:
            sku = Card_list[i].split('\t')[0]
            size = Card_list[i].split('\t')[2]
            price = Card_list[i].split('\t')[1]
            UN = Card_list[i].split('\t')[3]
            if int(UN) < 0:
                error()
            data = {
                "query": "\nquery ($keyword: String, $parentBrandIds: [Int!], $brandIds: [Int!]) {\nnode(\nlimit: 200\ntitleOrSku: $keyword\nparentBrandIds: $parentBrandIds\nbrandIds:$brandIds\nproductChecked: false\n){\nnodes{\nid\ntitle\nsku_value\nsex_value\nnodeImage{\nuri\n}\nbrand{\nid\nname\nparentBrand{\nid\nname\n}\n}\n}\n}\n}\n",
                "variables": {"keyword": sku}}
            r = S.post('https://www.area02.com/api/graphql', headers=headers, json=data)
            id = (r.json()['data']['node']['nodes'][0]['id'])
            title = (r.json()['data']['node']['nodes'][0]['title'])
            sku_value = (r.json()['data']['node']['nodes'][0]['sku_value'])
            SEX = (r.json()['data']['node']['nodes'][0]['sex_value'])
            A = {'data': {
                'size': [{'id': 1, 'us': '3', 'group_name': 'male'}, {'id': 2, 'us': '3.5', 'group_name': 'male'},
                         {'id': 3, 'us': '4', 'group_name': 'male'}, {'id': 4, 'us': '4.5', 'group_name': 'male'},
                         {'id': 5, 'us': '5', 'group_name': 'male'}, {'id': 6, 'us': '5.5', 'group_name': 'male'},
                         {'id': 7, 'us': '6', 'group_name': 'male'}, {'id': 8, 'us': '6.5', 'group_name': 'male'},
                         {'id': 9, 'us': '7', 'group_name': 'male'},
                         {'id': 10, 'us': '7.5', 'group_name': 'male'},
                         {'id': 11, 'us': '8', 'group_name': 'male'},
                         {'id': 12, 'us': '8.5', 'group_name': 'male'},
                         {'id': 13, 'us': '9', 'group_name': 'male'},
                         {'id': 14, 'us': '9.5', 'group_name': 'male'},
                         {'id': 15, 'us': '10', 'group_name': 'male'},
                         {'id': 16, 'us': '10.5', 'group_name': 'male'},
                         {'id': 17, 'us': '11', 'group_name': 'male'},
                         {'id': 18, 'us': '11.5', 'group_name': 'male'},
                         {'id': 19, 'us': '12', 'group_name': 'male'},
                         {'id': 20, 'us': '12.5', 'group_name': 'male'},
                         {'id': 21, 'us': '13', 'group_name': 'male'},
                         {'id': 22, 'us': '13.5', 'group_name': 'male'},
                         {'id': 23, 'us': '14', 'group_name': 'male'},
                         {'id': 24, 'us': '14.5', 'group_name': 'male'},
                         {'id': 25, 'us': 'W3.5', 'group_name': 'female'},
                         {'id': 26, 'us': 'W4', 'group_name': 'female'},
                         {'id': 27, 'us': 'W4.5', 'group_name': 'female'},
                         {'id': 28, 'us': 'W5', 'group_name': 'female'},
                         {'id': 29, 'us': 'W5.5', 'group_name': 'female'},
                         {'id': 30, 'us': 'W6', 'group_name': 'female'},
                         {'id': 31, 'us': 'W6.5', 'group_name': 'female'},
                         {'id': 32, 'us': 'W7', 'group_name': 'female'},
                         {'id': 33, 'us': 'W7.5', 'group_name': 'female'},
                         {'id': 34, 'us': 'W8', 'group_name': 'female'},
                         {'id': 35, 'us': 'W8.5', 'group_name': 'female'},
                         {'id': 36, 'us': 'W9', 'group_name': 'female'},
                         {'id': 37, 'us': 'W9.5', 'group_name': 'female'},
                         {'id': 38, 'us': 'W10', 'group_name': 'female'},
                         {'id': 39, 'us': 'W10.5', 'group_name': 'female'},
                         {'id': 40, 'us': 'W11', 'group_name': 'female'},
                         {'id': 41, 'us': 'W11.5', 'group_name': 'female'},
                         {'id': 42, 'us': 'W12', 'group_name': 'female'},
                         {'id': 43, 'us': 'W12.5', 'group_name': 'female'},
                         {'id': 44, 'us': 'W13', 'group_name': 'female'},
                         {'id': 45, 'us': 'W14', 'group_name': 'female'},
                         {'id': 46, 'us': '2c', 'group_name': 'kid'},
                         {'id': 47, 'us': '2.5c', 'group_name': 'kid'},
                         {'id': 48, 'us': '3c', 'group_name': 'kid'},
                         {'id': 49, 'us': '3.5c', 'group_name': 'kid'},
                         {'id': 50, 'us': '4c', 'group_name': 'kid'},
                         {'id': 51, 'us': '4.5c', 'group_name': 'kid'},
                         {'id': 52, 'us': '5c', 'group_name': 'kid'},
                         {'id': 53, 'us': '5.5c', 'group_name': 'kid'},
                         {'id': 54, 'us': '6c', 'group_name': 'kid'},
                         {'id': 55, 'us': '6.5c', 'group_name': 'kid'},
                         {'id': 56, 'us': '7c', 'group_name': 'kid'},
                         {'id': 57, 'us': '7.5c', 'group_name': 'kid'},
                         {'id': 58, 'us': '8c', 'group_name': 'kid'},
                         {'id': 59, 'us': '8.5c', 'group_name': 'kid'},
                         {'id': 60, 'us': '9c', 'group_name': 'kid'},
                         {'id': 61, 'us': '9.5c', 'group_name': 'kid'},
                         {'id': 62, 'us': '10c', 'group_name': 'kid'},
                         {'id': 63, 'us': '10.5c', 'group_name': 'kid'},
                         {'id': 64, 'us': '11c', 'group_name': 'kid'},
                         {'id': 65, 'us': '11.5c', 'group_name': 'kid'},
                         {'id': 66, 'us': '12c', 'group_name': 'kid'},
                         {'id': 67, 'us': '12.5c', 'group_name': 'kid'},
                         {'id': 68, 'us': '13c', 'group_name': 'kid'},
                         {'id': 69, 'us': '13.5c', 'group_name': 'kid'},
                         {'id': 70, 'us': '1y', 'group_name': 'kid'},
                         {'id': 71, 'us': '1.5y', 'group_name': 'kid'},
                         {'id': 72, 'us': '2y', 'group_name': 'kid'},
                         {'id': 73, 'us': '2.5y', 'group_name': 'kid'},
                         {'id': 74, 'us': '3y', 'group_name': 'kid'},
                         {'id': 75, 'us': '3.5y', 'group_name': 'kid'},
                         {'id': 76, 'us': '4y', 'group_name': 'kid'},
                         {'id': 77, 'us': '4.5y', 'group_name': 'kid'},
                         {'id': 78, 'us': '5y', 'group_name': 'kid'},
                         {'id': 79, 'us': '5.5y', 'group_name': 'kid'},
                         {'id': 80, 'us': '6y', 'group_name': 'kid'},
                         {'id': 81, 'us': '6.5y', 'group_name': 'kid'},
                         {'id': 82, 'us': '7y', 'group_name': 'kid'},
                         {'id': 83, 'us': '2c', 'group_name': 'toddler'},
                         {'id': 84, 'us': '2.5c', 'group_name': 'toddler'},
                         {'id': 85, 'us': '3c', 'group_name': 'toddler'},
                         {'id': 86, 'us': '3.5c', 'group_name': 'toddler'},
                         {'id': 87, 'us': '4c', 'group_name': 'toddler'},
                         {'id': 88, 'us': '4.5c', 'group_name': 'toddler'},
                         {'id': 89, 'us': '5c', 'group_name': 'toddler'},
                         {'id': 90, 'us': '5.5c', 'group_name': 'toddler'},
                         {'id': 91, 'us': '6c', 'group_name': 'toddler'},
                         {'id': 92, 'us': '6.5c', 'group_name': 'toddler'},
                         {'id': 93, 'us': '7c', 'group_name': 'toddler'},
                         {'id': 94, 'us': '7.5c', 'group_name': 'toddler'},
                         {'id': 95, 'us': '8c', 'group_name': 'toddler'},
                         {'id': 96, 'us': '8.5c', 'group_name': 'toddler'},
                         {'id': 97, 'us': '9c', 'group_name': 'toddler'},
                         {'id': 98, 'us': '9.5c', 'group_name': 'toddler'},
                         {'id': 99, 'us': '10c', 'group_name': 'toddler'},
                         {'id': 100, 'us': 'XS', 'group_name': 'male'},
                         {'id': 101, 'us': 'S', 'group_name': 'male'},
                         {'id': 102, 'us': 'M', 'group_name': 'male'},
                         {'id': 103, 'us': 'L', 'group_name': 'male'},
                         {'id': 104, 'us': 'XL', 'group_name': 'male'},
                         {'id': 105, 'us': 'XXL', 'group_name': 'male'},
                         {'id': 106, 'us': 'XXXL', 'group_name': 'male'},
                         {'id': 107, 'us': 'XXS', 'group_name': 'female'},
                         {'id': 108, 'us': 'XS', 'group_name': 'female'},
                         {'id': 109, 'us': 'S', 'group_name': 'female'},
                         {'id': 110, 'us': 'M', 'group_name': 'female'},
                         {'id': 111, 'us': 'L', 'group_name': 'female'},
                         {'id': 112, 'us': 'XL', 'group_name': 'female'},
                         {'id': 113, 'us': 'XS', 'group_name': 'kid'},
                         {'id': 114, 'us': 'S', 'group_name': 'kid'},
                         {'id': 115, 'us': 'M', 'group_name': 'kid'}, {'id': 116, 'us': 'L', 'group_name': 'kid'},
                         {'id': 117, 'us': 'XL', 'group_name': 'kid'},
                         {'id': 118, 'us': 'N/S', 'group_name': 'male'},
                         {'id': 119, 'us': 'N/S', 'group_name': 'female'}]}}
            male_list = {}
            female_list = {}
            kid_list = {}
            toddler_list = {}
            for i in range(len(A['data']['size'])):
                if 'male' == A['data']['size'][i]['group_name']:
                    male_list[A['data']['size'][i]['us']] = A['data']['size'][i]['id']
                elif 'female' == A['data']['size'][i]['group_name']:
                    female_list[A['data']['size'][i]['us']] = A['data']['size'][i]['id']
                elif 'kid' == A['data']['size'][i]['group_name']:
                    kid_list[A['data']['size'][i]['us']] = A['data']['size'][i]['id']
                elif 'toddler' == A['data']['size'][i]['group_name']:
                    toddler_list[A['data']['size'][i]['us']] = A['data']['size'][i]['id']
            if SEX == 'male':
                size_id = male_list[size]
            elif SEX == 'female':
                size = 'W%s' % size
                if size == 'W13.5':
                    size_id = 0
                else:
                    size_id = female_list[size]
            elif SEX == 'kid':
                size = '%sy' % size
                size_id = kid_list[size]
            elif SEX == 'toddler':
                size_id = toddler_list[size]
            # 上架商品
            data = {
                "query": "\n        mutation($applys: [ApplyProductInput!]!) {\n          createApplyProduct(applyProducts: $applys) {\n            success\n            errors {\n              field\n              message\n            }\n          }\n        }\n      ",
                "variables": {"applys": [{"nodeId": id, "sizeId": size_id, "price": int(price), "amount": int(UN)}]}}
            if "{}:{}".format(sku,size) in old_list:
                idd = ((up_list)["{}:{}".format(sku,size)].split(':')[0])
                oldNB = ((nb_list)["{}:{}".format(sku,size)])
                #print(idd)
                data={"query":"\n        mutation(\n          $id: Float!\n          $sizeId: Float!\n          $price: Float!\n          $amount: Float!\n        ) {\n          sellerUpdateProduct(\n            id: $id\n            sizeId: $sizeId\n            price: $price\n            stockAmount: $amount\n          ) {\n            errors {\n              field\n              message\n            }\n            success\n          }\n        }\n      ",
                      "variables":{"id":int(idd),"sizeId":size_id,"price":int(price),"amount":int(UN)}}
                if int(UN) == 0:
                    data ={"query":"\n        mutation($id: Float!) {\n          sellerRemoveProduct(id: $id) {\n            errors {\n              field\n              message\n            }\n            success\n          }\n        }\n      ",
                           "variables":{"id":int(idd)}}
                r = S.post('https://www.area02.com/api/graphql', headers=headers, json=data)
                #print(r.text)
                if int(UN) == 0:
                    log('MAIN', 'd', '更新 {} {} {} {} 庫存:{}->{} 已下架'.format(title, sku_value, size, r,oldNB,UN))
                else:
                    log('MAIN', 'd', '更新 {} {} {} {} 庫存:{}->{}'.format(title, sku_value, size, r,oldNB,UN))
                success_list = success_list + 1
            else:
                if int(UN) != 0:
                    r = S.post('https://www.area02.com/api/graphql', headers=headers, json=data)
                    log('MAIN', 's', '{} {} {} {}'.format(title, sku_value, size, r))
                else:
                    log('MAIN', 'g', '{} {} {} 庫存:0'.format(title, sku_value, size))
                success_list = success_list + 1
        except Exception as e:
            print(e)
            log('MAIN', 'e', '{} {} {}'.format(sku, size, 'ERROR'))
            error_list = error_list + 1
            f.write('{} {} {}'.format(sku, size, 'ERROR') + '\n')
        system("title " + fist + "TOTAL : {}   SUCCESS : {}   ERROR : {}".format(len(Card_list),(success_list), (error_list)))
    f.close()
except:
    pass
input("\n 全數完成 ! 任意鍵退出......")