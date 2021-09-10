from py_exchangeratesapi import Api
import datetime
import matplotlib.pyplot as plt


ACCESS_KEY = "015235afaa5b47f43bf77268ca9d6f39"

api = Api(ACCESS_KEY)
last_time = ''
last_EUR_rate = {}


def check_time(time):
    if last_time == "" :
        return True
    if time[0] == last_time[0]:
        last_hours,last_minutes,last_seconds = last_time[1].split(":")
        new_hours, new_minutes, new_seconds = time[1].split(":")
        if last_hours == new_hours and (int(new_minutes)-int(last_minutes)) < 10:
            return False
    return True


def currency_rate_list(base_currency):
    current_time = str(datetime.datetime.now()).split(" ")
    if check_time(current_time):
        EUR_rates = api.get_rates(base=base_currency)['rates']
        # for currency,value in EUR_rates.items():
        #     print(currency, ":" , value)
        global last_EUR_rate, last_time
        last_EUR_rate = EUR_rates
        last_time = current_time
        print("Cash wasn`t used!")
        return EUR_rates
    else:
        print("Cash was used!")
        return last_EUR_rate


def exchange_to(quantity,base_currency, needed_currency ):
    return api.convert(quantity, base_currency, needed_currency)

def get_last_7_days_EUR_CAD_info(target_currency):
    # api.get_rate('EUR', target="CAD", start_date="2018-01-01", end_date="2018-01-01")
    # I could do it mush easier with using this service, but i need pay for it.
    # So, i found another way.

    EUR_rates = {}
    for day in range(7):
        current_day = str(datetime.datetime.today()- datetime.timedelta(days=day)).split(" ")[0]
        EUR_rate = api.get_rate("EUR", target=target_currency, start_date=f"{current_day}")
        EUR_rates[current_day] = EUR_rate

    rates = EUR_rates
    plt.plot([date[5:] for date in rates.keys()], list(rates.values()))
    plt.ylabel(f'{str(datetime.datetime.now())[:4]}')
    plt.savefig('plot.png', dpi=300, bbox_inches='tight')
    print(EUR_rates)
    return EUR_rates


def check_currency(message):
    if message in api.supported_currencies:
        return True
    return False