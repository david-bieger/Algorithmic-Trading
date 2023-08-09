import yfinance as yf

# global variables
stock = "spy"
expectedReturn = 1.10
startingCash = 500.0
cash = 500.0
currentlyHeld = False
interval = "1d"
fiveMinuteIntervalsInAYear = 105120
expectedReturnInOneDay = 1.0 + (0.1/252)
brokerageValue = 0
originalPrice = 1
startDate = "2020-01-01"


def shouldIBuy(price, expectedValue):
    global currentlyHeld
    if price < 0.98 * expectedValue and not currentlyHeld: return True  # buy if value is 2.5 percent lower than expected
    return False


def shouldISell(price, expectedValue):
    global currentlyHeld
    if price > 1.02 * expectedValue and currentlyHeld: return True  # sell if value is 2.5 percent higher than expected
    return False


def getPriceHistory(stock):
    global interval, startDate
    stock = yf.Ticker(stock)

    prices = []
    stock_history = stock.history(start=startDate, end="2023-08-07", interval=interval)
    for i, j in stock_history.iterrows():
        price = float(j[0])
        prices.append(price)
    return prices


def makeDecision(count, expetedValue, price):
    global currentlyHeld, cash, brokerageValue
    if count == 0:
        cash -= price
        currentlyHeld = True
    else:
        if shouldISell(expetedValue, price):
            cash += price
            currentlyHeld = False
        elif shouldIBuy(expectedValue, price):
            cash -= price
            currentlyHeld = True
    if currentlyHeld:
        brokerageValue = cash + price
    else:
        brokerageValue = cash


def main():
    global cash, currentlyHeld, stock, startingCash, brokerageValue, originalPrice, expectedReturnInOneDay, expectedValue, price, startDate
    count = 0
    for price in getPriceHistory(stock):
        if count == 0:
            expectedValue = price
            originalPrice = price
        else:
            expectedValue = expectedValue * expectedReturnInOneDay
            print(str(expectedValue))
            if count % 100 == 0: expectedValue = price
        makeDecision(count, expectedValue, price)
        count += 1

    actual_yield = str(brokerageValue / startingCash)
    expected_yield = str(price / originalPrice)
    returnOverExpected = float(actual_yield) - float(expected_yield)
    print("\npercent return: \n    Actual: " + actual_yield + "\n    Expected: " + expected_yield)
    if returnOverExpected > 0:
        print("Beat expectations by: " + str(returnOverExpected))
    else:
        print("Lost to expectations by: " + str(returnOverExpected) + " percent.")
    print("original price: " + str(originalPrice))
    print("price: " + str(price) + "\n")
    print("caluclated expected value: " + str(expectedValue))


main()
