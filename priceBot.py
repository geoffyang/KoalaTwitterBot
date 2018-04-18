
import requests
import time
import os
import yaml as yaml
import sys
import tweepy

class PriceBot(object):

    def __init__(self,
                    consumer_key, consumer_secret,
                    access_key, access_secret,
                    coin_name, full_name):
        """twitter price bot instance"""
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret
        self.coin_name = coin_name
        self.full_name = full_name
        self.LiquidEnough = 5


    @classmethod
    def geminiPrice(self, coin, bidask):
        r = requests.get("https://api.gemini.com/v1/book/{}usd".format(coin))
        r = r.json()
        for order in r[bidask+'s']:
                if float(order['amount'])>= self.LiquidEnough:
                    return float(order['price'])


    @classmethod
    def updateTweet(self):

        """variables geminiBTCUSD, BTCKRW"""
        
        urls = {# 0)
                # "geminiETHUSD":"https://api.gemini.com/v1/book/ethusd",
                # "alternateFiatRates": "http://api.fixer.io/latest?base=USD",
                "FiatRates":"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=KRW&apikey=HJF04AFE2CAS4PEE",
                # "bithumbBTCKRW":"https://api.cryptowat.ch/markets/bithumb/btckrw/orderbook",
                # "geminiBTCUSD":"https://api.gemini.com/v1/book/BTCUSD",
                "Bithumb": "https://api.bithumb.com/public/orderbook"
        }

        datas = {}
        for key, url in urls.items():
            r = requests.get(url)
            datas[key] = r.json()

# Gemini order book has its own function, geminiPrice
        try:
            geminiAsk = geminiPrice('btc','ask')
            print("\nGemini Ask: {}".format(geminiAsk))
        except:
            print("no {} coin liquidity in Gemini".format(self.LiquidEnough))

# bithumb KRW bid price
        bithumbOrderBook = datas['bithumb']['data']['bids']
        try:
            for order in bithumbOrderBook:
                if float(order['quantity']) >= self.LiquidEnough:
                    BithumbBid = float(order['price'])
                    break
        except:
            print("no {} BTC liquidity on Bithumb\n".format(self.LiquidEnough))

#KRW fiat rate from alphavantage
        KRWUSD = float(datas["FiatRates"]["Realtime Currency Exchange Rate"][ "5. Exchange Rate"])

#Potential Revenue
        BithumbBidUSD = BithumbBid / KRWUSD
        SpreadToKorea =  int(BithumbBidUSD - geminiask)
        print("Bithumb Bid: {}".format(int(BithumbBidUSD)))
        print("Spread: ${} {:.2%}".format(SpreadToKorea, (SpreadToKorea/geminiask)))


        # last = data['result']['price']['last']
        # high = data['result']['price']['high']
        # low = data['result']['price']['low']
        # percentage = data['result']['price']['change']['percentage']
        # absolute_change = data['result']['price']['change']['absolute']
     
        #BTC secret ratio embedded in ETHkoala
        #BTCRMB / BTCUSD
        # BTCUSD = requests.get(urls[2])
        # BTCUSD = BTCUSD.json()
        # BTCUSD = float(BTCUSD['ask'])
        #
        # #get RMB price from fixer.io
        # CNY = requests.get(urls[3])
        # CNY = CNY.json()
        # CNY = CNY['rates']["CNY"]
        #
        #
        # #get VND price from alphavantage.co
        # VND = requests.get(urls[4])
        # VND = VND.json()
        # VND = float(VND["Realtime Currency Exchange Rate"][ "5. Exchange Rate"])
        #
        #
        # impliedFX = BTCUSD * VND * 0.80
        
        #ChineseTweet = "考拉现在买比特币价格：\n\n￥%5.0f 现金\n\n上海朋友私信我吧" % (impliedFX)
        # VietTweet = "Koala đang mua đồ bitcoin ngày hôm nay: \n\n₫ {:9,.0f} tiền mặt.\n\nBạn Sài Gòn xin vui lòng liên hệ với tôi\n".format(impliedFX)

                       
        ETHhashtag = '\n#Ethereum $ETH'
        ChineseHashtag = '\n#比特币'
        VietHashtag = '\n#Bitcoin'

        if coin_name == 'eth': 
            tweet = "Spread: ${} {:.2%}".format(SpreadToKorea, (SpreadToKorea/geminiask))
        elif coin_name== 'btc':
            tweet = VietTweet + VietHashtag

#        now = datetime.datetime.now()


        #tweet go!
        api.update_status(status=tweet)



if __name__ == "__main__":

    desktop_path = os.path.expanduser('~')+'\Documents\\Github\\Pricebots\\'
    config_file = desktop_path + 'config.yml'
        

    with open(config_file, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)


    for bot in cfg:
        consumer_key = cfg[bot]['consumer_key']
        consumer_secret = cfg[bot]['consumer_secret']
        access_key = cfg[bot]['access_key']
        access_secret = cfg[bot]['access_secret']
        coin_name = cfg[bot]['coin_name']
        full_name = cfg[bot]['full_name']


        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)

        bot = PriceBot(consumer_key, consumer_secret, access_key,
        access_secret, coin_name, full_name)

        bot.updateTweet()
