# gui.py
"""
用户界面，单击下载并预测按钮后调用主逻辑
"""

import pandas as pd
import mplfinance as mpf
import tushare as ts
import subprocess
import matplotlib
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from main import Config
from model import MyNet

matplotlib.rcParams['font.sans-serif'] = ['SimHei'] # 定义字体

pro = ts.pro_api('d89cb447ef5604b531219055280c32fd932e25707c01608100d81930') # 自己的Tushare接口token

class StockPredictionApp:
    def download_and_predict(self):
        stock_code = self.entry_stock_code.get()
        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()

        start_date = datetime.strptime(start_date, "%Y%m%d")
        end_date = datetime.strptime(end_date, "%Y%m%d")

        df = pro.daily(ts_code=stock_code, start_date=start_date.strftime("%Y%m%d"),
                       end_date=end_date.strftime("%Y%m%d"))

        if df.empty:
            messagebox.showerror("错误", "没有找到与指定日期范围匹配的股票数据。")
            return

        df.index = pd.to_datetime(df.trade_date)
        df = df.iloc[::-1]

        if len(df) < 50:
            messagebox.showerror("错误", "数据点数量不足以绘制图表，至少需要50个数据点。")
            return

        mpf.plot(df[-50:], type='candle', title=f'股票{stock_code}预测') # 绘制最近50天的数据
        df.to_csv('./data/stock_data.csv')  # 保存指定日期范围的股票数据
        self.run_main(stock_code, start_date, end_date)

    def run_main(self, stock_code, start_date, end_date):
        # 使用 subprocess.run
        subprocess.run(["python", "main.py", stock_code, start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d")])

    def __init__(self, root, model):
        self.root = root
        self.root.title("股票预测系统")

        self.label_stock_code = ttk.Label(root, text="股票代码:")
        self.label_stock_code.grid(row=0, column=0, padx=10, pady=10)
        self.entry_stock_code = ttk.Entry(root)
        self.entry_stock_code.grid(row=0, column=1, padx=10, pady=10)

        self.label_start_date = ttk.Label(root, text="起始日期:")
        self.label_start_date.grid(row=1, column=0, padx=10, pady=10)
        self.entry_start_date = ttk.Entry(root)
        self.entry_start_date.grid(row=1, column=1, padx=10, pady=10)

        self.label_end_date = ttk.Label(root, text="结束日期:")
        self.label_end_date.grid(row=2, column=0, padx=10, pady=10)
        self.entry_end_date = ttk.Entry(root)
        self.entry_end_date.grid(row=2, column=1, padx=10, pady=10)

        self.button_predict = ttk.Button(root, text="下载并预测", command=self.download_and_predict)
        self.button_predict.grid(row=4, column=0, columnspan=2, pady=10)

        self.model = model

if __name__ == "__main__":
    root = tk.Tk()
    con = Config()
    model = MyNet(con)
    app = StockPredictionApp(root, model)
    root.mainloop()
