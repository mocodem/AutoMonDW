# importing the crawling setups and other relevant libraries
import selenium_bot_headless, selenium_bot, seleniumpro_bot_headless, seleniumpro_bot, requestpro_bot, request_bot, honeypots
import time, csv
from random import randint



# stress test
def stress(triggerbot, onion: str, captcha: bool = False) -> (bool, str, int):
    # defining range of each rate
    rates_sleep = {"slow": (5,10), "medium": (1,3), "fast": (0,1)}

    # variable to count number of requests
    number_of_request = 0

    # iterate over each rate
    for rate, sec in rates_sleep.items():
        for i in range(10):
            number_of_request += 1
            # manual captcha solving which spawns a selenium browser and rxtract cookies
            if captcha:
                cookies = selenium_bot.get_cookies(onion)
                input("waiting for captcha solved: ")
                captcha = False
            # sending the requests with the respective crawler and cookies if captcha is present
            status = triggerbot.run(onion, cookies = None)
            print("status:", status, "with rate:", rate, "run", i+1, "/ 10")
            # check returned status code
            if status != 200:
                return True, rate, number_of_request
            # wait for each rate
            time.sleep(randint(sec[0], sec[1]))
        # wait between each rate
        if rate != "fast":
            time.sleep(60)
    return False, "none", number_of_request

# main function to test all crawling setups and write results to file
def main():
    # defining all crawling setups
    triggerbots = [seleniumpro_bot, seleniumpro_bot_headless, selenium_bot, selenium_bot_headless, requestpro_bot, request_bot]
    onion = None
    captcha = True
    # initiate results file
    f = open("results.csv", "a")
    writer = csv.writer(f)
    # test each crawling setup
    for i in triggerbots:
        print("testing", str(i).split("/")[-1][:-5], "on:", onion)
        # stress test
        busted, fail_rate, number_of_request = stress(i, onion, captcha)
        # honeypot test
        honeypot = honeypots.run(onion)
        print("results: busted ", busted, "fail rate:", fail_rate, "honeypot:", honeypot, "number of request:", number_of_request, "captcha:", captcha)
        # write result to csv file (triggerbot, busted, title, onion, ip, rate, honeypot, number_of_request)
        writer.writerow([str(i).split("/")[-1][:-5], busted, title, onion, "small proxy", fail_rate, honeypot, number_of_request, captcha])
    f.close()

# selfhost function to tagret the selfhosted hidden service
def selfhost():
    print("-------- starting ---------")
    triggerbots = [seleniumpro_bot, seleniumpro_bot_headless, selenium_bot, selenium_bot_headless, requestpro_bot, request_bot]
    onion = None # self-hosted
    captcha = False
    # test each crawling setup
    for bot in triggerbots:
        print("testing", str(bot).split("/")[-1][:-5], "on:", onion)
        bot.run(onion)
