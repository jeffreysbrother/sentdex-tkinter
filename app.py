import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import Tkinter as tk
import ttk
import urllib2
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 0)

f = Figure()
a = f.add_subplot(111)

exchange = "BTC-e"
DatCounter = 9000
programName = "btce"

def changeExchange(toWhat, pn):
    global exchange
    global DatCounter
    global programName

    exchange = toWhat
    programName = pn
    DatCounter = 9000


def popupmsg(msg):
    popup = tk.Tk()
    
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def animate(i):
    dataLink = 'https://btc-e.com/api/3/trades/btc_usd?limit=2000'
    # data = urllib.request.urlopen(datalink)
    data = urllib2.urlopen(dataLink).read()
    data = data.decode("utf-8")
    data = json.loads(data)
    data = data["btc_usd"]
    data = pd.DataFrame(data)

    buys = data[(data['type']=="bid")]
    buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
    buyDates = (buys["datestamp"]).tolist()

    sells = data[(data['type']=="ask")]
    sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
    sellDates = (sells["datestamp"]).tolist()

    a.clear()

    a.plot_date(buyDates, buys["price"], "#00A3E0", label="buys")
    a.plot_date(sellDates, sells["price"], "#183A54", label="sells")

    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
             ncol=2, borderaxespad=0)

    title = "BTC-e BTCUSD Prices\nLastPrice: " + str(data["price"][1999])
    a.set_title(title)
        


class BLM(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="favicon.ico")
        tk.Tk.wm_title(self, "doxastico voluntarismo")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not supported yet"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        exchangeChoice = tk.Menu(menubar, tearoff=1)
        exchangeChoice.add_command(label="BTC-e",
                                     command=lambda: changeExchange("BTC-e","btce"))
        exchangeChoice.add_command(label="Bitfinex",
                                     command=lambda: changeExchange("Bitfinex","bitfinex"))
        exchangeChoice.add_command(label="Bitstamp",
                                     command=lambda: changeExchange("Bitstamp","bitstamp"))
        exchangeChoice.add_command(label="Huobi",
                                     command=lambda: changeExchange("Huobi","huobi"))

        menubar.add_cascade(label="Exchange", menu=exchangeChoice)


        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, BTCe_Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def qf(param):
    print(param)



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Hey", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # if ttk is imported, then we can use ttk.Button instead of tk.Button
        button1 = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_frame(BTCe_Page))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree",
                            command=quit)
        button2.pack()



# a new page
# class PageOne(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="blah blah blah", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)

#         button1 = ttk.Button(self, text="Back to Home",
#                             command=lambda: controller.show_frame(StartPage))
#         button1.pack()




# another page
class BTCe_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="PAIGE THREE", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



app = BLM()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=5000)
app.mainloop()