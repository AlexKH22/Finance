import pandas as pd
import yahoo_finance as yf
import quandl
import datetime
from pprint import pprint
import matplotlib.pyplot as plt


def grabQuandl(stock):
    try:
        income = quandl.get("RAYMOND/" + stock + "_NET_INCOME_Q", authtoken="ZMgsGy3pecNd1Xs3n953", start_date="2011-01-31", end_date=datetime.date.today())
        income.columns = ['Income']
        # revenue = quandl.get("RAYMOND/" + stock + "_REVENUE_Q", authtoken="ZMgsGy3pecNd1Xs3n953", start_date="2011-01-31", end_date=datetime.date.today())
        # revenue.columns = ['Revenue']

        income.plot()
        plt.grid(True)
        plt.ylabel("Income")
        plt.legend().remove()
        plt.title(stock + " Income")
        plt.show()

        # ax1 = plt.subplot2grid((2, 1), (0, 0))
        # income.plot(ax=ax1)
        # ax1.grid(True)
        # plt.ylabel("Income")
        # plt.legend().remove()
        # plt.title(stock + " Income")

        # ax2 = plt.subplot2grid((2, 1), (1, 0), sharex=ax1)
        # revenue.plot(ax=ax2)
        # ax2.grid(True)
        # plt.ylabel("Revenue")
        # plt.legend().remove()
        # plt.title(stock + " Revenue")

        plt.show()
    except:
        print("No information for ", stock)


def russellCompanies():
    companies = pd.read_html('http://www.kibot.com/Historical_Data/Russell_3000_Historical_Intraday_Data.aspx')
    print(companies[1][1][1:])
    return companies[1][1][1:].tolist()


def s_pCompanies():
    companies = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    print(companies[0][0][1:].tolist)
    return companies[0][0][1:].tolist()


def yahooKeyStats(stock):
    try:
        share = yf.Share(stock)
    except:
        return None
    P_B = share.get_price_book()
    PEG = share.get_price_earnings_growth_ratio()
    PE12 = share.get_price_earnings_ratio()

    # pprint(share.get_historical('2014-04-25', '2014-04-29'))
    print('Stock Name:', stock)
    print('Price/Book:', P_B)
    print('PEG Ratio:', PEG)
    print('Trailing PE (12 month):', PE12)
    if not P_B or not PEG or not PE12:
        print()
        return None
    if float(P_B) < 1:
        print('Price/Book:', stock, P_B + ' Extremely low!!!')
        if 0 < float(PEG) < 1.5 and float(PE12) < 15:
            print(stock, "Looks nice\n")
            return stock
    print()
    return None


def showGood(stock):
    try:
        share = yf.Share(stock)
    except:
        return None
    P_B = share.get_price_book()
    PEG = share.get_price_earnings_growth_ratio()
    PE12 = share.get_price_earnings_ratio()

    print("==============================")
    print('Stock Name:', stock)
    print('Price/Book:', P_B)
    print('PEG Ratio:', PEG)
    print('Trailing PE (12 month):', PE12)
    print("==============================")

    grabQuandl(stock)


# Parse companies
# sp500 = s_pcompanies()
# f = open('S&P500_list.txt', 'w')
# for i in sp500:
#     f.write(i + ',')
# f.close()
#
# russell = russellcompanies()
# f = open('russell3000.txt', 'w')
# for i in russell:
#     f.write(i + ',')
# f.close()

# f = open('russell3000.txt', 'r')
# russell = f.readlines()[0].split(',')[:-1]
# russellshort = russell[:20]
#
# good_companies = []
# for company in russell:
#     temp = yahooKeyStats(company)
#     if not temp:
#         continue
#     else:
#         good_companies.append(temp)
#
# f = open('goodrussell3000.txt', 'w')
# for i in good_companies:
#     f.write(i + ',')
# f.close()

f = open('goodrussell3000.txt', 'r')
goodrussell = f.readlines()[0].split(',')[:-1]

showCharts = input('Would you like to show the historical financial data (Quandl) charts? (Y/N): ')

if showCharts.lower() == 'y':
    print('okay, charts will be shown')
    [showGood(stock) for stock in goodrussell]

elif showCharts.lwoer() == 'n':
    print('okay, charts will NOT be shown.')

else:
    print('invalid input, charts will NOT be shown.')
