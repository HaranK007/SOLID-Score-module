import requests

import matplotlib.pyplot as plt
import matplotlib

RAINFI_PATH = "https://api-v2.rain.fi"

def nft_loans(pubkey):
    lending_lst = []
    borrowing_lst = []
    api_route = "/loans/activity-by-user?pubkey="
    api_url = RAINFI_PATH + api_route+ pubkey
    headers = {"Content-Type": "application/json"}
    payload = {}
    response = requests.request("GET", api_url, headers=headers , data = payload)
    res = response.json()
    stats = res["loans"]
    for i in stats:
        if i["lender"] != pubkey:
            borrowing_lst.append(i)
        else:
            lending_lst.append(i)

    return lending_lst, borrowing_lst

def lend_plot(lend):
    #lender nft plot
    total = 0
    repaid = 0
    ongoing = 0
    default = 0
    for i in lend:
        if i["isFrozen"] == False:
            continue
        else:
            total+=1
            if i["status"] == "Repaid":
                repaid += 1
            elif i["status"] == "Ongoing":
                ongoing += 1
            else:
                default+=1

    categories = ['Total', 'Repaid', 'Ongoing', 'Defaulted']
    values = [total,repaid,ongoing,default]

    colors = ['blue', 'green', 'orange', 'red']

    plt.bar(categories, values, color=colors, width = 0.4)

    plt.title('NFT LENDER STATS')
    plt.xlabel('stats')
    plt.ylabel('count')

    plt.ylim(0,total+10 -(total%10))
    plt.xlim(-1, len(categories))
    plt.show()

def borrow_plot(borrow):
    total = 0
    repaid = 0
    ongoing = 0
    default = 0
    for i in borrow:
        if i["isFrozen"] == False:
            continue
        else:
            total+=1
            if i["status"] == "Repaid":
                repaid += 1
            elif i["status"] == "Ongoing":
                ongoing += 1
            else:
                default+=1

    categories = ['Total', 'Repaid', 'Ongoing', 'Defaulted']
    values = [total,repaid,ongoing,default]

    colors = ['blue', 'green', 'orange', 'red']

    plt.bar(categories, values, color=colors, width = 0.4)

    plt.title('NFT BORROWER STATS')
    plt.xlabel('stats')
    plt.ylabel('count')

    plt.ylim(0,total+10 -(total%10))
    plt.xlim(-1, len(categories))
    plt.show()






lend,borrow = nft_loans("9is85us6rMpZVv63peUFbqq113YnQSNyTT1qGp3DtAru")
lend_plot(lend)
borrow_plot(borrow)








