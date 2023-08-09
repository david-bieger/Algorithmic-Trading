import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import DerivativeTrading


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
        if i % 66 == 0:
            x.append(i)
            actual.append(brokerageValues[i])
            market.append(prices[i])
    print(prices)
    plt.plot(x, actual, color=color, marker='o')
    plt.plot(x, market, color='blue', marker='o')
    plt.title("Brokerage Value in red/green compared to actual price value in blue")
    plt.xlabel('Time (units of 1d)', fontsize=14)
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
            body = DerivativeTrading.main(stock, startDate)
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


# mod index by 66 to get every day
def main():
    window = establishWindow()
    createEventLoop(window)


main()
