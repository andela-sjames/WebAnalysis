import sys
from time import process_time
from importlib import reload

import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk

from main import DeepWebAnalyzer


app = None
link = None
depthname = None


class RenderGui:
    pass

def display_gui(web='', dept=1):
    global app, link, depthname
    app =  tk.Tk()
    app.title("LINK ANALYSER")
    app.geometry('450x300+200+200')

    menubar = tk.Menu(app)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Quit", command=app.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About Us", command=about_project)
    menubar.add_cascade(label="Help", menu=helpmenu)

    app.config(menu=menubar)

    headertext2 = tk.StringVar()
    headertext2.set("")
    label10 = tk.Label(app, textvariable=headertext2, height=1)
    label10.pack()

    headertext = tk.StringVar()
    headertext.set("")
    label0 = tk.Label(app, textvariable=headertext, height=4)
    label0.pack()

    labeltext = tk.StringVar()
    labeltext.set("Website url")
    label1 = tk.Label(app, textvariable=labeltext, height=1)
    label1.pack()

    url = tk.StringVar(None)
    url.set(web)
    link = tk.Entry(app, textvariable=url,)
    link.pack()

    labeltext = tk.StringVar()
    labeltext.set("Depth")
    label1 = tk.Label(app, textvariable=labeltext, height=1)
    label1.pack()

    deptvalue = tk.IntVar(None)
    deptvalue.set(dept)
    depthname = tk.Entry(app, textvariable=deptvalue, text=dept)
    depthname.pack()

    button1 = tk.Button(app, text="Submit", width=20, command=change_label)
    button1.pack(side='bottom', padx=15, pady=15)

    app.mainloop()


def do_get(site, num):
    start = process_time()
    (_ROOT, _DEPTH, _BREADTH) = range(3)
    print(site, num)
    G=nx.Graph()
    crawl = DeepWebAnalyzer(site, num).start()
    if crawl == "Forbidden":
        app_mssg = f"403:Forbidden, not allowed to crawl {site}"
        tk.messagebox.showinfo(app_mssg)
        return

    for child in crawl:
        G.add_node(child)
        if crawl[child]['parent'] != 'root':
            G.add_edge(crawl[child]['parent'], child)

    nx.draw(G, node_size=20, alpha=0.5, node_color="blue", with_labels=True)
    #fig, ax = plt.subplots()
    plt.savefig("node_colormap.png") # save as png
    # print("Total time: " + clock() - start)
    plt.show()


def about_project():
    print("A simple web analysis project")
    

def change_label():
    global app, link, depthname
    site = link.get()
    num = depthname.get()
    
    if site[:7] != "http://" and site[:8] != "https://":
        tk.messagebox.showinfo("Error","The url is invalid")
        return
    elif int(num) < 1:
        tk.messagebox.showinfo("Error", "The depth should be greater than or equal to 1")
        return

    do_get(site, num)
    app.destroy()

display_gui()
