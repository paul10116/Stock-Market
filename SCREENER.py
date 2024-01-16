from tkinter import messagebox
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

btn_color = "#2d661b"
input_clr = "#d3d5d7"
high_clr = "#27a300"
active_btn = "#5c0000"


root = Tk()
root.title("Pair Finder")
root.geometry("1800x700+0+0")
root.iconbitmap('images\programIcon.ico')
root.configure(background="BLACK", padx=20, pady=20)
# root.eval("tk::PlaceWindow . center")

# program menu line

program_menu = Menu(root)
root.config(menu=program_menu)
subMenu1 = Menu(program_menu, tearoff=0, font=("Helvetica", 12))
subMenu2 = Menu(program_menu, tearoff=0, font=("Helvetica", 12))

program_menu.add_cascade(label="File", menu=subMenu1)
subMenu1.add_command(label="Exit Program", command=root.quit)


# Pair Finder Frame

def getTickers():
    longs = longTickers.get()
    shorts = shortTickers.get()
    pair(longs, shorts)
    submitBtn.flash()


pairFinderFrame = LabelFrame(root, text="Pair Finder", padx=20,
                             pady=20, fg="WHITE", font=("Helvetica", 20, "bold"), labelanchor="n", borderwidth=6, background="BLACK", relief="ridge")
longTickers = Entry(pairFinderFrame,
                    width=100,
                    bg=input_clr,
                    font=("Helvetica", 16),
                    highlightcolor=high_clr,
                    highlightthickness=3)
longLabel = Label(pairFinderFrame, text="Enter Long Tickers:",
                  font=("Helvetica", 14), background="BLACK", fg="WHITE")

shortTickers = Entry(pairFinderFrame,
                     width=100,
                     bg=input_clr,
                     font=("Helvetica", 16),
                     highlightcolor=high_clr,
                     highlightthickness=3)
shortLabel = Label(
    pairFinderFrame, text="Enter Short Tickers:", font=("Helvetica", 14), background="BLACK", fg="WHITE")

submitBtn = Button(pairFinderFrame,
                   text="Compare",
                   command=getTickers,
                   font=("Helvetica", 16, "bold"),
                   background=btn_color,
                   cursor="exchange",
                   activebackground=active_btn,
                   activeforeground=btn_color)

longLabel.grid(row=0, column=0, padx=5, pady=5, sticky="W")
longTickers.grid(row=1, column=0, padx=10, pady=10)
shortLabel.grid(row=2, column=0, padx=5, pady=5, sticky="W")
shortTickers.grid(row=3, column=0, padx=10, pady=10)
submitBtn.grid(row=4, column=0, padx=10, pady=10, sticky="E")


# Watchlist window

def openWatchlistWindow():
    top = Toplevel()
    top.geometry("1200x800")
    top.title("Watchlist")
    top.iconbitmap('images\programIcon.ico')
    label = Label(top, text="Watchlist window").pack()

    watchlist_menu = Menu(top)
    top.config(menu=watchlist_menu)
    subMenu1 = Menu(watchlist_menu, tearoff=0)

    watchlist_menu.add_cascade(label="File", menu=subMenu1)
    subMenu1.add_command(label="Exit Program", command=top.destroy)

    def openFile():
        global image
        top.filename = filedialog.askopenfilename(initialdir="images\cyclicals",  title="Cyclicals", filetypes=(
            ("png files", "*.png"), ("all files", "*.*")))
        label = Label(top, text=top.filename).pack()
        image = ImageTk.PhotoImage(Image.open(top.filename))
        screenImg = Label(image=image).pack()

    imgBtn = Button(top, text="Open Image", command=openFile).pack()


# Open Positions window

def openPositionWindow():
    top = Toplevel()
    top.geometry("1200x800")
    top.title("Open Positions")
    top.iconbitmap('images\programIcon.ico')
    label = Label(top, text="Watchlist window").pack()

    positions_menu = Menu(top)
    top.config(menu=positions_menu)
    subMenu1 = Menu(positions_menu, tearoff=0)

    positions_menu.add_cascade(label="File", menu=subMenu1)
    subMenu1.add_command(label="Exit Program", command=top.destroy)


# Program menu lines

program_menu.add_cascade(label="Windows", menu=subMenu2)
subMenu2.add_command(label="Watchlist", command=openWatchlistWindow)
subMenu2.add_separator()
subMenu2.add_command(label="Open Positions", command=openPositionWindow)


pairFinderFrame.pack(padx=20, pady=20)
root.mainloop()
