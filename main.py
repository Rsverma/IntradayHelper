from tkinter import *
from tkinter import messagebox
from math import sqrt as sqr
from datetime import datetime, timedelta
from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import pandas as pd
# BDay is business day, not birthday...
from pandas.tseries.offsets import BDay


def getPrice(sym):
    try:
        ts = TimeSeries(key='5QVVSVATKIPYFZNH', output_format='pandas')
        data, meta_data = ts.get_intraday(symbol='NSE:'+sym, interval='60min')
        x = data.iloc[0]
        yesterday = (pd.datetime.today() - BDay(1)).replace(hour=5, minute=45, second=0)
        y = data.loc[yesterday.strftime("%Y-%m-%d %H:%M:%S")]
        #print(x)
        return x, y
    except KeyError:
        messagebox.showinfo("Issue", "Something went wrong")



class Application(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.topFrame = Frame(master)
        self.topFrame.pack(padx=10,pady=20)
        self.bottomFrame = Frame(master)
        self.bottomFrame.pack(padx=10)

        self.symbolLabel = Label(self.topFrame, text="Symbol", font=("Arial", 15))
        self.symbolLabel.pack(side=LEFT, padx=10)
        self.entry = Entry(self.topFrame, width=14, font=("Arial", 15))
        self.entry.pack(side=LEFT)

        self.label1 = Label(self.bottomFrame, text="Buy Stop Order for Long ", font=("Arial", 15))
        self.label1.grid(row=1, column=0, sticky=W)
        self.label2 = Label(self.bottomFrame, text="Target for Long ", font=("Arial", 15))
        self.label2.grid(row=2, column=0, sticky=W)
        self.label3 = Label(self.bottomFrame, text="Stop for Long ", font=("Arial", 15))
        self.label3.grid(row=3, column=0, sticky=W)
        self.label4 = Label(self.bottomFrame, text="Sell Stop Order for Short ", font=("Arial", 15))
        self.label4.grid(row=4, column=0, sticky=W)
        self.label5 = Label(self.bottomFrame, text="Target for Short ", font=("Arial", 15))
        self.label5.grid(row=5, column=0, sticky=W)
        self.label6 = Label(self.bottomFrame, text="Stop for Long ", font=("Arial", 15))
        self.label6.grid(row=6, column=0, sticky=W)
        self.label7 = Label(self.bottomFrame, text="=", font=("Arial", 15))
        self.label7.grid(row=1, column=1)
        self.label8 = Label(self.bottomFrame, text="=", font=("Arial", 15))
        self.label8.grid(row=2, column=1)
        self.label9 = Label(self.bottomFrame, text="=", font=("Arial", 15))
        self.label9.grid(row=3, column=1)
        self.label10 = Label(self.bottomFrame, text="=", font=("Arial", 15))
        self.label10.grid(row=4, column=1)
        self.label11 = Label(self.bottomFrame, text="=", font=("Arial", 15))
        self.label11.grid(row=5, column=1)
        self.label12 = Label(self.bottomFrame, text="=", font=("Arial", 15))
        self.label12.grid(row=6, column=1)
        self.label13 = Label(self.bottomFrame, text="", font=("Arial", 15))
        self.label13.grid(row=1, column=2, sticky=W)
        self.label14 = Label(self.bottomFrame, text="", font=("Arial", 15))
        self.label14.grid(row=2, column=2, sticky=W)
        self.label15 = Label(self.bottomFrame, text="", font=("Arial", 15))
        self.label15.grid(row=3, column=2, sticky=W)
        self.label16 = Label(self.bottomFrame, text="", font=("Arial", 15))
        self.label16.grid(row=4, column=2, sticky=W)
        self.label17 = Label(self.bottomFrame, text="", font=("Arial", 15))
        self.label17.grid(row=5, column=2, sticky=W)
        self.label18 = Label(self.bottomFrame, text="", font=("Arial", 15))
        self.label18.grid(row=6, column=2, sticky=W)
        self.bottomFrame.grid_columnconfigure(2, minsize=200)
        self.button = Button(self.bottomFrame, text="Calculate", command=self.check)
        self.button.grid(row=7, column=1, pady=30)

    def check(self):
        txt = self.entry.get()
        if txt and not txt.isspace():
            self.calculate(txt)
        else:
            messagebox.showerror("Symbol Needed", "Please provide a valid symbol")

    def calculate(self, symbol):
        pricesnow, priceprev = getPrice(symbol)
        pdr = priceprev['2. high'] - priceprev['3. low']
        f1 = 0.4333 * pdr
        f2 = 0.7666 * pdr
        f3 = 1.3333 * pdr
        oprange = pricesnow.get(key='2. high') - pricesnow.get(key='3. low')

        if f1 > oprange:
            factor = f1
        elif f2 > oprange:
            factor = f2
        else:
            factor = f3
        buy = pricesnow.get(key='3. low') + factor
        self.label13['text'] = '%.4f' % buy
        self.label14['text'] = '%.4f' % (buy * 1.005)
        self.label15['text'] = '%.4f' % (buy * 0.99)
        sell = pricesnow.get(key='2. high') - factor
        self.label16['text'] = '%.4f' % sell
        self.label17['text'] = '%.4f' % (sell * 0.995)
        self.label18['text'] = '%.4f' % (sell * 1.01)

root = Tk()
root.title("IntraDay Helper")
root.geometry('600x350')
app = Application(root)
root.mainloop()
