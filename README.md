# Nasa Apod

```
███╗   ██╗ █████╗ ███████╗ █████╗      █████╗ ██████╗  ██████╗ ██████╗            
████╗  ██║██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗           
██╔██╗ ██║███████║███████╗███████║    ███████║██████╔╝██║   ██║██║  ██║           
██║╚██╗██║██╔══██║╚════██║██╔══██║    ██╔══██║██╔═══╝ ██║   ██║██║  ██║           
██║ ╚████║██║  ██║███████║██║  ██║    ██║  ██║██║     ╚██████╔╝██████╔╝           
╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═════╝            
                                                                                  
██╗    ██╗ █████╗ ██╗     ██╗     ██████╗  █████╗ ██████╗ ███████╗██████╗ ███████╗
██║    ██║██╔══██╗██║     ██║     ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝
██║ █╗ ██║███████║██║     ██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝███████╗
██║███╗██║██╔══██║██║     ██║     ██╔═══╝ ██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗╚════██║
╚███╔███╔╝██║  ██║███████╗███████╗██║     ██║  ██║██║     ███████╗██║  ██║███████║
 ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝
```																														

Repository base-code is forked from : https://github.com/ShikharSahu/NasaApodDesktopWallpaperSetter

This is a learning-to-code mini project for me, getting something thats already made up to a certain level, and trying to expand on it as I learn how it works.

### Changes made:

- Added a menu page , its better visually and easuer to manage everything and expand on features. 
- Buttons for script execution, API set/get , image save , path set.
- Use of threading to avoid crashing when having the menu open with a component running.
- minor chages to manual_wallpaper_setter and wallpaper_setter. 
- remade the API_utility to work better with the other three components.
- there's a list of a few more TO-DOs gradually being added.


### Features

- Automatically sets NASA Astronomical Picture of the Day as desktop wallpaper.
- Manually select a date from user friendly GUI and set that date's image as the desktop wallpaper.
- Saves the images in local user drive for future use.

## Run the Program

On the cmd, make sure the cloned repo is open.
Run:
```
python -m src.menu
```
The main menu window opens and you choose between manual (date selected) image pick or Automatically get Image of the day

### Using a batch file

Edit the batch file named "APOD_run.bat" as you see fit, setting the paths for python and the menu.py accordingly.
If you want to run the batch from elsewhere, create a shortcut to move around, leaving batch in place, or change the paths accordingly.

Note :
+ Make sure you can access internet through python on your device.


### Standalone Manual Image selection (no Menu window)
In the command promt, with the cloned repo open in it, run:
```
python -m manual_wallpaper_setter
```
(or press the respective button from the menu window)

### Automatic set image of the Day (no Menu window)
In the command promt, with the cloned repo open in it, run:
```
python -m wallpaper_setter
```
(or press the respective button from the menu window)
This componets is to be used within a different batch file, specifically for it, to establish scheduled automatic wallpaper changing, as instructed bellow.

### Set Automatic Wallpaper changer
(as instructed by :  https://github.com/ShikharSahu/NasaApodDesktopWallpaperSetter) 

You can refer to [this](https://www.geeksforgeeks.org/schedule-a-python-script-to-run-daily/) article to setup automatic Wallpaper changer.

1. Make sure you have edited the batch file and it is working.
2. Go to Windows search bar and search "Task Scheduler".
3. Click on ‘Create Basic Task….’ in the Actions Tab. And give a suitable Name like "NASA APOD Auto WAllpaper", and Description of your task that you want to Automate and click on Next.
4. In the next step, you have to select at what time intervals your script should be executed. Select ‘Daily’ and click Next. Now you need to specify at what time your Python Script should be executed daily and then Click on Next.
5. Click on browse and find and select the batch file you edited. Now click Next.
6. See if everything looks fine. Then click on finish.

### Note:

+ You are only allowed to make 30 API calls per hours. This is due to the demo key. You can bypass this by generating a real key from [here](https://api.nasa.gov/) and updating it in wallpaper_utility.py
+ Saved images are stored in "C:\Users\ [USERNAME]\Pictures\NasaApod"

## References:

+ NASA APOD : https://apod.nasa.gov/apod/

+ NASA APOD API: https://github.com/nasa/apod-api

+ Original baseline source-code repository : https://github.com/ShikharSahu/NasaApodDesktopWallpaperSetter

