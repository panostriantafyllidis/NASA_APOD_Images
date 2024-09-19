from logging import error
from random import choice

from win10toast import ToastNotifier

from src.API_utility import APOD_API_KEY, changeBG
from src.object_parser import *


def startSetWallpaperProcedure():
    if APOD_API_KEY is None:
        print("API key is not set!")
        return

    response = get_data(APOD_API_KEY)

    # Check if the response contains an error
    if "error" in response:
        print(f"Error from API: {response['error']['message']}")
        print(f"The API key used was: {APOD_API_KEY}")
        return

    print(response)
    url = get_url(response)
    media_type = get_media_type(response)
    if media_type == "image":
        try:
            # Best case, we'll get an HD wallpaper for the day.
            hd_url = get_hdurl(response)
        except:
            hd_url = getOneWorkingImageFromArchive()
    else:
        hd_url = getOneWorkingImageFromArchive()

    wallpaper_image_path = download_image(hd_url, get_date(response))
    print(wallpaper_image_path)
    changeBG(wallpaper_image_path)
    n.show_toast("NASA Wallpaper", "Wallpaper changed!", duration=10)


def getOneWorkingImageFromArchive():
    responses_array = get_data_array(APOD_API_KEY)
    print("Checking archives:")
    archive_responses_list = []

    for res in responses_array:
        try:
            hd_url = get_hdurl(res)
            archive_responses_list.append(hd_url)
        except:
            pass

    if len(archive_responses_list) == 0:
        n.show_toast("NASA Wallpaper", "Archive retrieval failed", duration=10)
        return error
    else:
        return choice(archive_responses_list)


n = ToastNotifier()

if __name__ == "__main__":
    print("Program Started")
    if not is_connected():
        print("Internet Not Connected")
        n.show_toast("NASA Wallpaper", "Internet not connected")
    else:
        print("Internet is connected")
        startSetWallpaperProcedure()
