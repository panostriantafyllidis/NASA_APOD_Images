import threading
from datetime import date, timedelta
from tkinter import *

from tkcalendar import DateEntry
from win10toast import ToastNotifier

from src.API_utility import APOD_API_KEY, changeBG
from src.object_parser import *


def setWallpaperByDate(cal):
    disableButtons()
    response = get_data_by_date(APOD_API_KEY, cal.get_date())
    hd_url = setResultAndGetHdUrl(response)
    image_date = get_date(response)
    setWallpaperByHdUrl(hd_url, image_date)
    enableButtons()
    exit()


def setWallpaperByDateThreaded(cal):
    print("Setting wallpaper by date")
    t = threading.Thread(target=setWallpaperByDate, args=(cal,))
    t.start()


def setTodaysPicAsWallpaper():
    disableButtons()
    response = get_data(APOD_API_KEY)
    hd_url = setResultAndGetHdUrl(response)
    image_date = get_date(response)
    setWallpaperByHdUrl(hd_url, image_date)
    enableButtons()
    exit()


def setTodaysPicAsWallpaperThreaded():
    t = threading.Thread(target=setTodaysPicAsWallpaper)
    t.start()


def setResultAndGetHdUrl(response):
    try:
        print("Sending request")
        hd_url = get_hdurl(response)
        print("Request received")
        result.set("URL received! :)")
        return hd_url
    except:
        result.set("This date's post is not an image :(")
        return None


def setWallpaperByHdUrl(hd_url, image_date):
    print(f"HD URL's image date: {image_date}")
    if hd_url:
        image_downloaded_path = download_image(hd_url, image_date)
        changeBG(image_downloaded_path)
        result.set("Success! :)")
        n.show_toast("NASA Wallpaper", "Wallpaper changed!", duration=7)


def disableButtons():
    setButton["state"] = "disabled"
    useTodaysPic["state"] = "disabled"


def enableButtons():
    setButton["state"] = "normal"
    useTodaysPic["state"] = "normal"


root = Tk()
root.title("NASA APOD Image Setter")
root.configure(bg="light grey")

n = ToastNotifier()

result = StringVar()

Label(root, text="Status: ", bg="light grey").grid(row=3, sticky=W)
Label(root, text="", textvariable=result, bg="light grey").grid(
    row=3, column=1, sticky=W
)

yesterdayDate = date.today() - timedelta(days=1)
cal = DateEntry(root, maxdate=yesterdayDate, date_pattern="dd/mm/yyyy")
cal.grid(row=0, column=2, columnspan=2, rowspan=2, padx=5, pady=5)

setButton = Button(
    root,
    text="Set as wallpaper",
    command=lambda: setWallpaperByDateThreaded(cal),
    bg="white",
)
setButton.grid(row=2, column=2, columnspan=2, rowspan=2, padx=5, pady=5)

useTodaysPic = Button(
    root, text="Use today's Pic", command=setTodaysPicAsWallpaperThreaded, bg="white"
)
useTodaysPic.grid(row=4, column=2, columnspan=2, rowspan=2, padx=5, pady=5)

Label(root, text="Choose a day from when you need the pic from:", bg="light grey").grid(
    row=0, sticky=W
)

mainloop()
