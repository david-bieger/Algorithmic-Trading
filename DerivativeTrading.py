import yfinance as yf

#global variables
stock = "spy"
prevPrice = 0.0
price = 0.0
down = False
up = False
startingCash = 500.0
cash = 500.0
currentlyHeld = False
interval = "5m"
brokerageValue = 0
originalPrice = 1

def shouldIBuy():
    global down, up, prevPrice, price
    if price > prevPrice and down:
        down = False
        up = True
        return True
    else: return False

def shouldISell():
    global down, up, prevPrice, price
    if price < prevPrice and up:
        up = False
        down = True
        return True
    else: return False

def getPriceHistory(stock):
    global interval
    stock = yf.Ticker(stock)
    startDate = "2023-07-24"

    prices = []
    while (int(startDate.split('-')[1]) < 8):
        year = startDate.split('-')[0]
        month = int(startDate.split('-')[1])
        endDay = int(startDate.split('-')[2])
        if (endDay < 27): endDay +=1
        else:
            endDay = 1
            month += 1
        month = str(month)
        if endDay < 10: endDay = "0" + str(endDay)
        else: endDay = str(endDay)
        endDate = year + "-" + month + "-" + endDay
        stock_history = stock.history(start=startDate, end=endDate, interval=interval)
        for i, j in stock_history.iterrows():
            price = float(j[0])
            prices.append(price)
        startDate = endDate
    return prices

def makeDecision(count):
    global price, prevPrice, currentlyHeld, cash, up, down, brokerageValue, originalPrice
    if currentlyHeld:
        brokerageValue = cash + price
    else:
        brokerageValue = cash
    if count == 0:
        originalPrice = price
        cash -= price
        currentlyHeld = True
    else:
        if shouldISell() and currentlyHeld:
            cash += price
            currentlyHeld = False
        elif shouldIBuy():
            cash -= price
            currentlyHeld = True
    prevPrice = price

def main():
    global cash, up, down, price, prevPrice, currentlyHeld, stock, startingCash, brokerageValue, originalPrice
    count = 0
    for price in getPriceHistory(stock):
        makeDecision(count)
        count += 1
    actual_yield = str(brokerageValue / startingCash)
    expected_yield = str(price / originalPrice)
    returnOverExpected = float(actual_yield) - float(expected_yield)
    print("\npercent return: \n    Actual: " + actual_yield + "\n    Expected: " + expected_yield)
    if returnOverExpected > 0:
        print("Beat expectations by: " + str(returnOverExpected))
    else:
        print("Lost to expectations by: " + str(returnOverExpected) + " percent.")


main()





