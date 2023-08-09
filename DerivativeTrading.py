import yfinance as yf
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

def makeDecision(count, prices, brokerageValues):
    global price, prevPrice, currentlyHeld, cash, up, down, brokerageValue
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
    prices.append(price)
    brokerageValues.append(brokerageValue)
    return [prices, brokerageValues]

def main(stock = 'spy', startDate = '2023-08-01'):
    global cash, up, down, price, prevPrice, currentlyHeld, startingCash, brokerageValue, originalPrice
    count = 0
    prices = []
    brokerageValues = []
    for price in getPriceHistory(stock):
        pricesAndBrokerage = makeDecision(count, prices, brokerageValues)
        prices = pricesAndBrokerage[0]
        brokerageValues = pricesAndBrokerage[1]
        if count == 0:
            originalPrice = price
        count += 1
    actual_yield = str(brokerageValues[len(brokerageValues)-1] / startingCash)
    expected_yield = str(prices[len(prices)-1] / originalPrice)
    returnOverExpected = float(actual_yield) - float(expected_yield)
    print("\npercent return: \n    Actual: " + actual_yield + "\n    Expected: " + expected_yield)
    if returnOverExpected > 0:
        message = "Beat expectations by: " + str(returnOverExpected)
    else:
        message = "Lost to expectations by: " + str(abs(returnOverExpected)) + " percent."

    body = {}
    body["prices"] = prices
    body["brokerage values"] = brokerageValues
    body["message"] = message
    body["Actual Return"] = actual_yield
    body["original price"] = originalPrice

    return body



def establishWindow():
    sg.theme('BlueMono')
    layout = [
        [sg.Text("Hello from PySimpleGUI")],
        [sg.Button("Done")],
        [sg.Text('Stock', size=(8, 1)), sg.InputText()],
        [sg.Text("Start Date (formatted like '2023-08-09'): ", size=(8, 1)), sg.InputText()],
        [sg.Button("Submit")]
    ]

    # Create the window
    window = sg.Window(title="Algorithmic Trading GUI", layout=layout, margins=(400, 300))

    return window


def createPlot(prices, brokerageValues, body):
    global originalPrice
    if float(body["Actual Return"]) > 1.0:
        color = 'green'
    else:
        color = 'red'
    indexes = getListOfIndexes(brokerageValues)
    actual = []
    market = []
    x = []
    prices = body["prices"]
    print(len(prices))
    print(len(brokerageValues))

    for i in indexes:
        count = 0
        if i % 66 == 0:
            x.append(i)
            actual.append(brokerageValues[i]/startingCash)
            market.append(prices[i]/originalPrice)
            count += 1
    print(prices)
    plt.plot(x, actual, color=color, marker='o')
    plt.plot(x, market, color='blue', marker='o')
    plt.title("Brokerage Value in red or green compared to result of simply holding the stock in blue")
    plt.xlabel('Time (units of 5m intervals)', fontsize=14)
    plt.ylabel('Price (blue) and Brokerage Value (red/green)')
    plt.grid(True)
    return plt.gcf()


def getListOfIndexes(list):
    retList = []
    for i in range(len(list)):
        retList.append(i)
    return retList


def createEventLoop(window):
    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "Done" or event == sg.WIN_CLOSED:
            break
        if event == "Submit":
            stock = values[0]
            startDate = values[1]
            #print(stock, startDate)
            body = main(stock, startDate)
            print(body)
            brokerageValues = body["brokerage values"]
            message = body["message"]
            window = createGraph(window, body["prices"], brokerageValues, message, startDate, body)
    window.close()


def createGraph(window, prices, brokerageValues, message, startDate, body):
    layout = [
        [sg.Text("Showing Performance since " + startDate + " to present day.")],
        [sg.Canvas(size=(600, 400), key='-CANVAS-')],
        [sg.Button("Done")],
        [sg.Text(message)]
    ]
    window = sg.Window('Graph', layout, finalize=True, element_justification='center')
    draw_figure(window['-CANVAS-'].TKCanvas, createPlot(prices, brokerageValues, body))

    return window

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def display():
    window = establishWindow()
    createEventLoop(window)


display()