# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 09:11:34 2023

@author: Shreyaash
"""

from pickle import load,dump
import csv
import tkinter as tk

win=tk.Tk()
win.title("Scribe")
win.geometry("1200x500")
win.resizable(False,False)
win.iconbitmap('scribe.ico')
win.configure(bg='#f4bf96')

def addtask():
    task = aten.get()
    try:
        with open('tasklist.csv', 'a', newline='') as fh:
            wo = csv.writer(fh)
            wo.writerow([task])
    except FileNotFoundError:
        with open('tasklist.csv', 'w', newline='') as fh:
            wo = csv.writer(fh)
            wo.writerow([task])
    aten.delete(0, tk.END)
    tasklist()

def tasklist():
    tlist.delete(0, tk.END)
    tasks=[]
    try:
        with open('tasklist.csv','r') as fh:
            ro=csv.reader(fh)
            for i in ro:
                tasks.append(' '.join(i))
        for i in tasks:
            tlist.insert(tk.END, i)
    except FileNotFoundError:
        return

def deltask():
    selection = tlist.get(tlist.curselection())
    tasks=[]
    with open('tasklist.csv','r') as fh:
        ro=csv.reader(fh)
        for i in ro:
            if ' '.join(i)!=selection:
                tasks.append(i)
    with open('tasklist.csv', 'w', newline='') as fh:
        wo = csv.writer(fh)
        wo.writerows(tasks)
    tasklist()

def save():
    title = ten.get()
    con = tcon.get("1.0", tk.END)
    if title.strip() and con.strip():
        with open('notes.dat', 'rb') as fh:
            titlist=[]
            reclist=[]
            while True:
                try:
                    rec=load(fh)
                    titlist.append(rec['title'])
                    reclist.append(rec)
                except EOFError:
                    break
        if title in titlist:
            for i in reclist:
                if i['title']==title:
                    i['con']=con
        else:
            notes={}
            notes['title'] = title
            notes['con'] = con
            reclist.append(notes)
        with open('notes.dat', 'wb') as fh:
            for i in reclist:
                dump(i,fh)                
    loadlist()
    clearstuff()

def clearstuff():
    ten.delete(0, tk.END)
    tcon.delete("1.0", tk.END)

def dele():
    title = ten.get()
    if title.strip():
        found=False
        tlist=[]
        with open('notes.dat','rb') as fh:
            while True:
                try:
                    rec=load(fh)
                    if rec['title']==title:
                        found=True
                    else:
                        tlist.append(rec)
                except EOFError:
                    fh.close()
                    break
        if found==True:
            with open('notes.dat','wb') as fh:
                for i in tlist:
                    dump(i,fh)
    loadlist()
    clearstuff()

def loadlist():
    nbox.delete(0, tk.END)
    titlist=[]
    try:
        with open('notes.dat', 'rb') as fh:
            while True:
                try:
                    rec=load(fh)
                    titlist.append(rec['title'])
                except EOFError:
                    break
            for i in titlist:
                nbox.insert(tk.END, i)
    except FileNotFoundError:
        return
       
def loadnote(event):
    selection = nbox.get(nbox.curselection())
    with open('notes.dat', 'rb') as fh:
        while True:
            try:
                rec=load(fh)
                if rec['title']==selection:
                    ten.delete(0, tk.END)
                    ten.insert(tk.END, selection)
                    tcon.delete("1.0", tk.END)
                    tcon.insert(tk.END, rec['con'])
            except EOFError:
                break

def tasks():
    if todo.winfo_x()<0:
       todo.place(x=0, y=0)
       notes.place(x=700,y=0)
    else:
       todo.place(x=-500, y=0)
       notes.place(x=0,y=0)

todo=tk.Frame(win)
todo.pack(side=tk.LEFT, padx=10, pady=10)
todo.place(x=-200,y=0)
todo.configure(bg='#f4bf96')

tl=tk.Frame(todo)
tl.pack(side=tk.TOP,padx=10,pady=10)
tl.configure(bg='#ce5a67')

lifr=tk.Frame(tl)
lifr.pack(side=tk.LEFT,padx=10,pady=10)
lifr.configure(bg='#fcf5ed')

rifr=tk.Frame(tl)
rifr.pack(side=tk.RIGHT,padx=10,pady=10)
rifr.configure(bg='#ce5a67')

tlist=tk.Listbox(lifr, width=80,height=20)
tlist.pack(side=tk.LEFT,padx=10,pady=10)

delb=tk.Button(rifr,text='Delete Task',command=deltask)
delb.pack(side=tk.BOTTOM,padx=5,pady=5)

scroll2=tk.Scrollbar(lifr,command=tlist.yview)
scroll2.pack(side=tk.RIGHT,fill=tk.Y)
tlist.config(yscrollcommand=scroll2.set)

at=tk.Frame(todo)
at.pack(side=tk.BOTTOM,padx=10,pady=10)
at.configure(bg='#f4bf96')

atlab=tk.Label(at,text='Task:')
atlab.pack()
atlab.configure(bg='#f4bf96')

aten=tk.Entry(at,width=100)
aten.pack(side=tk.TOP, padx=10, pady=5)

ab=tk.Button(at,text="Add Task",command=addtask)
ab.pack(pady=5)

notes=tk.Frame(win)
notes.pack(side=tk.RIGHT, padx=10, pady=10)
notes.place(x=0,y=0)
notes.configure(bg='#f4bf96')

nfr=tk.Frame(notes)
nfr.pack(side=tk.LEFT,padx=10,pady=10)
nfr.configure(bg='#f4bf96')

todob=tk.Button(nfr,text='Tasks',command=tasks)
todob.pack(side=tk.LEFT,padx=10,pady=10)

nbox=tk.Listbox(nfr, width=35,height=20)
nbox.pack(side=tk.LEFT,padx=10,pady=10)
nbox.bind("<Double-Button-1>", loadnote)

scroll=tk.Scrollbar(nfr,command=nbox.yview)
scroll.pack(side=tk.RIGHT,fill=tk.Y)
nbox.config(yscrollcommand=scroll.set)

cfr=tk.Frame(notes)
cfr.pack(side=tk.RIGHT,padx=10,pady=10)
cfr.configure(bg='#fcf5ed')

tlab=tk.Label(cfr,text='Title:')
tlab.pack()
tlab.configure(bg='#fcf5ed')

ten=tk.Entry(cfr,width=100)
ten.pack(side=tk.TOP, padx=10, pady=5)

tlab2=tk.Label(cfr, text='Content:')
tlab2.pack()
tlab2.configure(bg='#fcf5ed')

tcon=tk.Text(cfr, width=100, height=20)
tcon.pack(padx=10,pady=5)

saveb=tk.Button(cfr,text="Save",command=save)
saveb.pack(side=tk.LEFT,padx=10,pady=5)

deleb=tk.Button(cfr,text="Delete",command=dele)
deleb.pack(side=tk.RIGHT,padx=10,pady=5)

tasklist()
loadlist()
tasks()
tasks()

win.mainloop()
