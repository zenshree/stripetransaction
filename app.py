from flask import Flask, request
import stripe
import json
from dhooks import Webhook, Embed

stripe.api_key = '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'
hook = Webhook(
    "https://discord.com/api/webhooks/819433584519675924/ZZ2JTOQCpiixRTfKzXWIJ3g9_O9H9feMkp-QL48Mca5cUN62XqapGQ3oumCnCF_RrYST")
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    event = json.loads(payload)
    if event['type'] == 'issuing_authorization.created':
        issuing_authorization = event['data']['object']
        status = json.dumps(issuing_authorization)
        status1 = json.loads(status)
        balancedata = status1["balance_transactions"]
        merchantdata = status1["merchant_data"]
        mer = json.dumps(merchantdata)
        des = json.dumps(balancedata)
        merc = json.loads(mer)
        desc = json.loads(des)
        amount2 = status1["amount"]
        finalamount2 = float(abs((amount2 / 100)))
        formatted_finalamount2 = "{:.2f}".format(finalamount2)
        mercinfo = merc["name"]
        try:
            desc1 = desc[len(desc) - 1]
        except:
            a = 'Declined'
            embed = Embed(
                description='**Stripe Decline**',
                color=0xe74c3c,
                timestamp='now'
            )
            image1 = "https://i.imgur.com/DtBTf0A.png"
            image2 = "https://i.imgur.com/VOrFuWz.png"
            embed.add_field(name='Amount', value=f"${formatted_finalamount2}")
            embed.add_field(name='Status', value=f"{a}")
            embed.add_field(name='Merchant', value=f"{mercinfo}", inline=False)
            embed.set_footer(text='Made by Zenshree', icon_url=image2)
            embed.set_thumbnail(image1)
            hook.send(embed=embed)
            return '', 200
        desc3 = json.dumps(desc1)
        desc2 = json.loads(desc3)
        amount = desc2["net"]
        finalamount = float(abs((amount / 100)))
        type = desc2["type"]
        if type == 'issuing_authorization_release':
            a = 'Closed'
            embed = Embed(
                description='**New Stripe Authorization**',
                color=0x5CDBF0,
                timestamp='now'
            )
            image1 = "https://i.imgur.com/DtBTf0A.png"
            image2 = "https://i.imgur.com/VOrFuWz.png"
            embed.add_field(name='Amount', value=f"${formatted_finalamount2}")
            embed.add_field(name='Status', value=f"{a}")
            embed.add_field(name='Merchant', value=f"{mercinfo}", inline=False)
            embed.set_footer(text='Made by Zenshree', icon_url=image2)
            embed.set_thumbnail(image1)
            hook.send(embed=embed)

        elif type == 'issuing_authorization_hold':
            a = 'Pending'
            embed = Embed(
                description='**New Stripe Authorization**',
                color=0x5CDBF0,
                timestamp='now'
            )
            image1 = "https://i.imgur.com/DtBTf0A.png"
            image2 = "https://i.imgur.com/VOrFuWz.png"
            embed.add_field(name='Amount', value=f"${formatted_finalamount2}")
            embed.add_field(name='Status', value=f"{a}")
            embed.add_field(name='Merchant', value=f"{mercinfo}", inline=False)
            embed.set_footer(text='Made by Zenshree', icon_url=image2)
            embed.set_thumbnail(image1)
            hook.send(embed=embed)
        else:
            a = 'Declined or other reason'



    elif event['type'] == 'issuing_authorization.updated':
        issuing_authorization = event['data']['object']
        status = json.dumps(issuing_authorization)
        status1 = json.loads(status)
        balancedata = status1["balance_transactions"]
        merchantdata = status1["merchant_data"]
        mer = json.dumps(merchantdata)
        des = json.dumps(balancedata)
        merc = json.loads(mer)
        desc = json.loads(des)
        mercinfo = merc["name"]
        desc1 = desc[len(desc) - 1]
        desc3 = json.dumps(desc1)
        desc2 = json.loads(desc3)
        type = desc2["type"]
        if type == 'issuing_authorization_release':
            a = 'Closed'
        elif type == 'issuing_authorization_hold':
            a = 'Pending'
        else:
            a = 'Reversed'
        amount = desc2["net"]
        finalamount2 = float(abs((amount / 100)))
        formatted_finalamount2 = "{:.2f}".format(finalamount2)
        embed = Embed(
            description='**Stripe Authorization Updated**',
            color=0x5CDBF0,
            timestamp='now'
        )
        image1 = "https://i.imgur.com/DtBTf0A.png"
        image2 = "https://i.imgur.com/VOrFuWz.png"
        embed.add_field(name='Amount', value=f"${formatted_finalamount2}")
        embed.add_field(name='Status', value=f"{a}")
        embed.add_field(name='Merchant', value=f"{mercinfo}",inline=False)
        embed.set_footer(text='Made by Zenshree',icon_url=image2)
        embed.set_thumbnail(image1)
        hook.send(embed=embed)

    else:
        return 'Unexpected event type', 400

    return '', 200

# @app.route('/privwebhook', methods=['POST'])
# def webhook2():
#     payload3 = request.data
#     if True:
#         print(payload3)
#         return '',200
#     else:
#         print(payload3)
#         return '',400