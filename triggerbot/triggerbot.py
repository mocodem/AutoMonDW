import seleniumpro_bot, selenium_bot, requestpro_bot, request_bot, honeypots
import time, csv
from random import randint




def stress(triggerbot, onion: str, captcha: bool = False) -> (bool, str, int):
    rates_sleep = {"slow": (5,10), "medium": (1,3), "fast": (0,1)}
    number_of_request = 0

    for rate, sec in rates_sleep.items():
        for i in range(10):
            number_of_request += 1
            status = triggerbot.run(onion)
            if captcha:
                input("waiting for captcha solved: ")
                captcha = False
            print("status:", status, "with rate:", rate, "run", i+1, "/ 10")
            if status != 200:
                return True, rate, number_of_request
            time.sleep(randint(sec[0], sec[1]))
        if rate != "fast":
            time.sleep(60)
    return False, "none", number_of_request


def main():
    triggerbots = [seleniumpro_bot, selenium_bot, requestpro_bot, request_bot]
    onion = None
    captcha = False
    f = open("results.csv", "a")
    writer = csv.writer(f)
    # headless, selenium, requests meta, requests light
    for i in triggerbots:
        print("testing", str(i).split("/")[-1][:-5], "on:", onion)
        busted, fail_rate, number_of_request = stress(i, onion, captcha)
        # honeypot = honeypots.run(onion)
        honeypot = False
        print("results: busted ", busted, "fail rate:", fail_rate, "honeypot:", honeypot, "number of request:", number_of_request, "captcha:", captcha)
        # triggerbot, busted, title, onion, ip, rate, honeypot, number_of_request
        writer.writerow([str(i).split("/")[-1][:-5], busted, title, onion, "small proxy", fail_rate, honeypot, number_of_request, captcha])
    f.close()

def selfhost():
    print("-------- starting ---------")
    triggerbots = [seleniumpro_bot, selenium_bot, requestpro_bot, request_bot]
    onion = None # sel-hosted
    captcha = False
    for bot in triggerbots:
        print("testing", str(bot).split("/")[-1][:-5], "on:", onion)
        bot.run(onion)

