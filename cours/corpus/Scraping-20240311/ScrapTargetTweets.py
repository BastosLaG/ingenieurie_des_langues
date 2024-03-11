import scrapy
from multiprocessing import Process
import scrapy.crawler as crawler
from twisted.internet import reactor
# from User import User
import sys, os
import json
import csv
# from Tweet import Tweet

class ScrapTargetTweets_Thread():

    def start(self):
        process = Process(target=self.work)
        process.start()

    def spider_closed(self, spider):
        print(spider.logned)

    def work(self):
        try:
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(ScrapTargetTweets)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
        except Exception as e:
            print(e)

class ScrapTargetTweets(scrapy.Spider):
    name = 'Test Login'

    ################################### Target Names ########################################
    targetUserName = [ 'billclinton', 'hillaryclinton', 'barackobama', 'realdonaldtrump',
                        'nancypelosi', 'tedcruz', 'jaredpolis', 'speakerryan',
                        'senfranken', 'berniesanders', 'senschumer', 'senwarren',
                        'senorrinhatch', 'senduckworth', 'senatemajldr', 'senatorleahy',
                        'randpaul', 'repjohnconyers', 'kyrstensinema', 'joebiden',
                        'senfeinstein', 'vp', 'markwarner', 'sengillibrand',
                        'senatorbaldwin', 'clairecmc', 'maziehirono', 'repmccaul',
                        'repseanmaloney', 'kamalaharris', 'gregformontana', 'darrellissa']
    index = 0
    #########################################################################################

    ####################################### Accounts ########################################
    accounts = [['votre_login+1@votre_compte.com','paris8'],
                ['votre_login+2@votre_compte.com','paris8'],
                ['votre_login+3@votre_compte.com','paris8'],
                ['votre_login+4@votre_compte.com','paris8'],
                ['votre_login+5@votre_compte.com','paris8'],
                ['votre_login+6@votre_compte.com','paris8']]
    accountIndex = 0
    #########################################################################################

    ################################### Next Page Id ########################################
    next_page_id = ''
    #########################################################################################

    ######################################### Status ########################################
    tweetsCount = 0
    notTweetsCount = 0
    #########################################################################################

    ######################################### Params ########################################
    saveAsJson = False
    JsonOutPutPath = 'Output\\Json'
    saveAsCsv = True
    CsvOutPutPath = 'Output\\Csv'
    #########################################################################################

    
    def start_requests(self):
        yield scrapy.Request(url='https://mobile.twitter.com/login', callback=self.parseLoginPage, errback=self.errCallBack, dont_filter=True)

    def parseLoginPage(self, response):
        token = response.css('input[name="authenticity_token"]::attr(value)').extract_first()
        data = {
            'authenticity_token': token,
            'session[username_or_email]': self.accounts[self.accountIndex][0],
            'session[password]': self.accounts[self.accountIndex][1],
            'remember_me': '1',
            'wfa': '1',
            'commit':  'Log in',
            'ui_metrics': ''
        }
        yield scrapy.FormRequest(url='https://mobile.twitter.com/sessions', formdata=data, callback=self.parseFormRequest, dont_filter=True)
    
    def parseFormRequest(self, response):
        yield scrapy.Request(url='https://mobile.twitter.com/account', callback=self.paresAccountResult, dont_filter=True)

    def paresAccountResult(self, response):
        myname = response.css('div[class="fullname"]::text').extract_first()
        if myname is not None:
            print("==================> Lognned As User  : " + myname)
            if self.next_page_id == '':
                yield scrapy.Request(url='https://mobile.twitter.com/' + self.targetUserName[self.index], callback=self.parseTweets, errback=self.errCallBack, dont_filter=True)
            else:
                print('https://mobile.twitter.com/' + self.targetUserName[self.index] + '?max_id=' + self.next_page_id)
                yield scrapy.Request(url='https://mobile.twitter.com/' + self.targetUserName[self.index] + '?max_id=' + self.next_page_id, callback=self.parseTweets, errback=self.errCallBack, dont_filter=True)

    def errCallBack(self, failure):
        response = str(failure.value.response.status).replace("\\n","")
        print(response)
        if response == '429':
            print("You've made a few too many attempts. Please try again later.")
            yield scrapy.Request(url='https://mobile.twitter.com/account', callback=self.parseLogout, errback=self.errCallBack, dont_filter=True)

    def parseLogout(self, response):
        token = response.css('input[name="authenticity_token"]::attr(value)').extract_first()
        print(token)
        data = {
            'authenticity_token': token,
            'commit':  'Log out'
        }
        yield scrapy.FormRequest(url='https://mobile.twitter.com/session/destroy', formdata=data, callback=self.parseLogoutFormRequest, dont_filter=True)
    
    def parseLogoutFormRequest(self, response):
        self.accountIndex = self.accountIndex + 1
        if self.accountIndex == len(self.accounts):
            self.accountIndex = 0
        print("Logged Off !")
        yield scrapy.Request(url='https://mobile.twitter.com/login', callback=self.parseLoginPage, errback=self.errCallBack, dont_filter=True)
    
    def parseTweets(self, response):

        #print(response.)
        #print("sss")
        #print(response.status)
        os.system('cls')
        print("Target : " + self.targetUserName[self.index])
        print("Account : " + self.accounts[self.accountIndex][0])
        print("Fetched Tweets : " + str(self.tweetsCount) + " | Coulndt Fetsh : " + str(self.notTweetsCount))

        t = response.css('div[class="fullname"]::text').extract_first()
        if t is None:
            print("Died !")

        tweets = response.css('div[class="tweet-text"]')
        var = response.css('div[class="w-button-more"]').extract_first()
        #print(var)
        self.next_page_id = response.css('div[class="w-button-more"]').css('a::attr(href)').extract_first()
        if self.next_page_id is None:
            print("Next Page Not Found")
        else:
            self.next_page_id = self.next_page_id.split('=')[1].replace("\n","").replace("\r","").replace(",","")
        #print(self.next_page_id)

        exists = os.path.isfile(self.CsvOutPutPath + '\\data.csv')

        d = csv.writer(open(self.CsvOutPutPath + '\\data.csv',"a"))
        if exists == False and self.saveAsCsv:
            d.writerow(["target", "tweet_id", "tweet_text", "next_page_id"])

        for t in tweets:
            tweet_id = t.css('div[class="tweet-text"]::attr(data-id)').extract_first()
            tweet_text = t.css('div[class="dir-ltr"]').css('div[class="dir-ltr"]::text').extract_first()

            try:
                if tweet_id is not None and tweet_text is not None:
                    tweet_id = tweet_id.replace("\n","").replace("\r","").replace(",","")
                    tweet_text = tweet_text.replace("\n","").replace("\r","").replace(",","")
                    if self.saveAsCsv:
                        d.writerow([self.targetUserName[self.index], tweet_id, tweet_text, self.next_page_id])
                    if self.saveAsJson:
                        tweet = Tweet(self.targetUserName[self.index], tweet_id, tweet_text, self.next_page_id)
                        with open(self.JsonOutPutPath + "\\" + tweet_id + '.json', 'w') as outfile:
                            json.dump(tweet.__dict__, outfile)
                    self.tweetsCount = self.tweetsCount + 1
            except:
                self.notTweetsCount = self.notTweetsCount + 1

        if self.next_page_id is not None:
            yield scrapy.Request(url='https://mobile.twitter.com/' + self.targetUserName[self.index] + '?max_id=' + self.next_page_id, callback=self.parseTweets, errback=self.errCallBack, dont_filter=True)
        elif self.index == len(self.targetUserName):
            sys.exit()
        else:
            self.index = self.index + 1
            yield scrapy.Request(url='https://mobile.twitter.com/' + self.targetUserName[self.index], callback=self.parseTweets, errback=self.errCallBack, dont_filter=True)


if __name__ == "__main__":
    ui = ScrapTargetTweets_Thread()
    ui.start()
