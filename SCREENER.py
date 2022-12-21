from components.pairFinder import pair
from components.correlation import correlation
from components.openPositions import open_position
from PIL import ImageTk, Image
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


root = Tk()
root.title("Pair Finder")
root.geometry("1800x800")
root.iconbitmap('images\programIcon.ico')
root.configure(background="BLACK", padx=20, pady=20)

# program menu line

program_menu = Menu(root)
root.config(menu=program_menu)
subMenu1 = Menu(program_menu, tearoff=0, font=("Helvetica", 14))
subMenu2 = Menu(program_menu, tearoff=0, font=("Helvetica", 14))

program_menu.add_cascade(label="File", menu=subMenu1)
subMenu1.add_command(label="Exit Program", command=root.quit)


# Pair Finder Frame

def getTickers():
    longs = longTickers.get()
    shorts = shortTickers.get()
    pair(longs, shorts)


pairFinderFrame = LabelFrame(
    root, text="Pair Finder", padx=20, pady=20, font=("Helvetica", 20), background="GREY")
longTickers = Entry(pairFinderFrame, width=100,
                    borderwidth=3, font=("Helvetica", 14))
longLabel = Label(pairFinderFrame, text="Enter Long Tickers:",
                  font=("Helvetica", 14), background="GREY", fg="WHITE")

shortTickers = Entry(pairFinderFrame, width=100,
                     borderwidth=3, font=("Helvetica", 14))
shortLabel = Label(
    pairFinderFrame, text="Enter Short Tickers:", font=("Helvetica", 14), background="GREY", fg="WHITE")

submitBtn = Button(pairFinderFrame, text="Compare",
                   command=getTickers, font=("Helvetica", 16), background="GREEN")

longLabel.grid(row=0, column=0, padx=5, pady=5)
longTickers.grid(row=1, column=0, padx=10, pady=10)
shortLabel.grid(row=2, column=0, padx=5, pady=5)
shortTickers.grid(row=3, column=0, padx=10, pady=10)
submitBtn.grid(row=4, column=0, padx=10, pady=10)


# Correlation Frame

def corrButton():
    corr_data = corrInput.get()
    correlation(corr_data)


corrFrame = LabelFrame(root, text="Correlation", padx=20,
                       pady=20, font=("Helvetica", 20), background="GREY")
corrLabel = Label(corrFrame, text="Enter Tikcers", font=(
    "Helvetica", 16), background="GREY", fg="WHITE")
corrInput = Entry(corrFrame, width=150, borderwidth=3, font=("Helvetica", 14))
corrBtn = Button(corrFrame, text="Check Correlation",
                 command=corrButton, font=("Helvetica", 18), background="GREEN")
corrLabel.grid(row=0, column=0, padx=5, pady=5)
corrInput.grid(row=1, column=0, padx=10, pady=10)
corrBtn.grid(row=2, column=0, padx=10, pady=10)


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


corrFrame.pack(padx=20, pady=20)
pairFinderFrame.pack(padx=20, pady=20)
root.mainloop()
