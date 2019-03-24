#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import numpy as nm

import pandas as pd
 
class UserInterface(tk.Frame):
    def __init__(self, master=None):
        self.Orders = []
        
        super().__init__(master)
        self.master = master
        self.initUI()
        self.create_widgets()
    
    def initUI(self):
        self.master.title("UserWindow")
        
        self.pack()
        
        self.centerWindow()
        
    def centerWindow(self):
        w = 1000
        h = 600
 
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
    def create_widgets(self):
        self.percentDownload = 10
        
        #Отправка одного заказа________________________________________________________________
        #Группа
        self.inputOrder = tk.LabelFrame(self, text='Input one oreder:')
        self.inputOrder.grid(row=0,column=0, padx=5, pady=5, sticky=tk.NW)
        #Бинды на значения
        self.nameProduct = tk.StringVar()
        self.amountProduct = tk.IntVar()
        
        self.deadlineProductDay = tk.IntVar()
        self.deadlineProductMonth = tk.IntVar()
        self.deadlineProductYear = tk.IntVar()
         
        #Подписис к полям (первая колонка)
        self.nameProduct_label = tk.Label(self.inputOrder, text="Name product:")
        self.nameProduct_label.grid(row=0, column=0, sticky="w")
        
        self.amountProduct_label = tk.Label(self.inputOrder, text="Amount product:")
        self.amountProduct_label.grid(row=1, column=0, sticky="w")
        
        self.deadlineProduct_label = tk.Label(self.inputOrder, text="Deadline product:")
        self.deadlineProduct_label.grid(row=2, column=0, sticky="w")
        
        #Поля (вторая полонка)
        self.nameProduct_entry = tk.Entry(self.inputOrder, textvariable=self.nameProduct)
        self.nameProduct_entry.grid(row=0,column=1, padx=5, pady=5, columnspan=3, sticky="WE")
        
        self.amountProduct_entry = tk.Spinbox(self.inputOrder, width=15, from_=0, to=nm.Infinity, textvariable=self.amountProduct)
        self.amountProduct_entry.grid(row=1,column=1, padx=5, pady=5, sticky="WE", columnspan=3)
        
        self.deadlineProductDay_frame = tk.LabelFrame(self.inputOrder, text='Day:')
        self.deadlineProductDay_frame.grid(row=2,column=1, padx=5, pady=5, sticky="w")
        self.deadlineProductDay_entry = tk.Spinbox(self.deadlineProductDay_frame, textvariable=self.deadlineProductDay, from_=0, to=31, width=2)
        self.deadlineProductDay_entry.grid(row=2,column=1, padx=5, pady=5, sticky="w")
        
        self.deadlineProductMonth_frame = tk.LabelFrame(self.inputOrder, text='Month:')
        self.deadlineProductMonth_frame.grid(row=2,column=2, padx=5, pady=5, sticky="w")
        self.deadlineProductMonth_entry = tk.Spinbox(self.deadlineProductMonth_frame, textvariable=self.deadlineProductMonth, from_=0, to=12, width=2)
        self.deadlineProductMonth_entry.grid(row=2,column=2, padx=5, pady=5, sticky="w")
        
        self.deadlineProductYear_frame = tk.LabelFrame(self.inputOrder, text='Year:')
        self.deadlineProductYear_frame.grid(row=2,column=3, padx=5, pady=5, sticky="w")
        self.deadlineProductYear_entry = tk.Spinbox(self.deadlineProductYear_frame, textvariable=self.deadlineProductYear, from_=0, to=nm.Infinity, width=6)
        self.deadlineProductYear_entry.grid(row=2,column=3, padx=5, pady=5, sticky="w")
        
        #Отправка заказа
        self.postOrder = tk.Button(self.inputOrder, text="Post", cursor="heart" , command=self.postOrder)
        self.postOrder.grid(row=3,column=3, padx=5, pady=5, sticky="WE")
        #_________________________________________________________________________________________
        
        #Группа
        self.inputFileOrders = tk.LabelFrame(self, text='Input file oreders:')
        self.inputFileOrders.grid(row=1,column=0, padx=5, pady=5, sticky="WE")
        
        self.pathFile = tk.StringVar()
      
        self.pathFile_label = tk.Label(self.inputFileOrders, text="File:")
        self.pathFile_label.grid(row=0, column=0, sticky="we")
        
        self.pathFile_entry = tk.Entry(self.inputFileOrders, textvariable=self.pathFile, state="disabled", width=25)
        self.pathFile_entry.grid(row=0,column=1, padx=5, pady=5, sticky="WE")
        
        self.pathFile_button = tk.Button(self.inputFileOrders, text="Open", command=self.downloadPathFile)
        self.pathFile_button.grid(row=0,column=2, padx=5, pady=5, sticky="WE")
        
        #Отправка заказа
        self.postOrder = tk.Button(self.inputFileOrders, text="Post", cursor="heart" , command=self.postOrders)
        self.postOrder.grid(row=1,column=2, padx=5, pady=5, sticky="WE")
        
        
        #Лист товаров__________________________________________________________________________
        self.listOrders = tk.LabelFrame(self, text='list orders:')
       # self.listOrders.pack(expand=tk.YES, padx=5, pady=5)
        self.listOrders.grid(row=0,column=1)
        
        self.table = ttk.Treeview(self.listOrders, show="headings", selectmode="browse")
        self.table["columns"]=("Name", "Amout", "Deadline")
        self.table["displaycolumns"]=("Name", "Amout", "Deadline")
  
        for head in ("Name", "Amout", "Deadline"):
            self.table.heading(head, text=head, anchor=tk.CENTER)
            self.table.column(head, anchor=tk.CENTER)
    
        self.scrolltable = tk.Scrollbar(self.listOrders, command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrolltable.set)
        self.scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)
        #______________________________________________________________________________________
        
        
        self.run = tk.Button(self, text="Run", fg="red", cursor="pirate", command=self.runСomputing)
        self.run.grid(row=1,column=1, padx=5, pady=5, sticky="WE")
    
        
        self.quit = tk.Button(self, text="QUIT", fg="red", cursor="pirate", command=self.master.destroy)
        self.quit.grid(row=1,column=2, padx=5, pady=5, sticky="WE")
        
    def runСomputing(self):
        self.prBar = ttk.Progressbar(self,
                                   orient='horizontal',
                                   mode='determinate',
                                   maximum=100)
        self.prBar.grid(row=2,column=1, padx=5, pady=5, sticky="WE")
        self.prBar.step(amount=10.0)
        self.prBar.start()
        
        
        import subprocess
        proc = subprocess.Popen("ping -c2 %s" % ip, shell=True, stdout=subprocess.PIPE)
        out = proc.stdout.readlines()
        
        #Лист товаров__________________________________________________________________________
        self.listResults = tk.LabelFrame(self, text='Result:')
       # self.listOrders.pack(expand=tk.YES, padx=5, pady=5)
        self.listResults.grid(row=2,column=1)
        
        self.table = ttk.Treeview(self.listResults, show="headings", selectmode="browse")
        self.table["columns"]=("equipment_Id", "order_id", "amount", "start", "finish")
        self.table["displaycolumns"]=("equipment_Id", "order_id", "amount", "start", "finish")
  
        for head in ("equipment_Id", "order_id", "amount", "start", "finish"):
            self.table.heading(head, text=head, anchor=tk.CENTER)
            self.table.column(head, anchor=tk.CENTER)
    
        self.scrolltable = tk.Scrollbar(self.listResults, command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrolltable.set)
        self.scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)
        #______________________________________________________________________________________
       
                       
    def postOrder(self):
        deadlineProduct = str(self.deadlineProductDay.get()) + '.' + str(self.deadlineProductMonth.get()) + '.' + str(self.deadlineProductYear.get())
        row = (self.nameProduct.get(), self.amountProduct.get(), deadlineProduct)
        self.Orders.append(row)
        self.nameProduct.set("")
        self.amountProduct.set(0)
        self.deadlineProductDay.set(0)
        self.deadlineProductMonth.set(0)
        self.deadlineProductYear.set(0)
        self.table.insert('', tk.END, values=tuple(row))
        
    def postOrders(self):
        typeFile = str(self.pathFile.get()).split('.')[1]
        if typeFile == "csv":
            inputOrders = pd.read_csv(str(self.pathFile.get()))
            nameProducts = inputOrders["product_id"]
            amountProducts = inputOrders["amount"]
            deadlineProducts = inputOrders["deadline"]
            
            for i in range(len(nameProducts)):
                row = (nameProducts[i], amountProducts[i], deadlineProducts[i])
                self.Orders.append(row)
                self.table.insert('', tk.END, values=tuple(row))
                
        self.pathFile.set("")
        
    def downloadPathFile(self):
        self.pathFile.set(filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("xlsx files","*.xlsx"),("csv files","*.csv"),("all files","*.*"))))
        
        
def main():
    root = tk.Tk()
    app = UserInterface(master=root)
    app.mainloop()  
 
if __name__ == '__main__':
    main()
