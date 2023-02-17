# active_monitor_screenshot
Short python screenshotting script to only screenshot the monitor your mouse cursor is in and save it to Screenshots folder.

# How to use

The application needs to open to screenshot. To automatically launch this program silently in the background when booting up your computer, do:
> Step 1: Download the latest version
> 
> Step 2: Unzip the file, find "ActiveMonitorScreenshot", right click, choose "Create Shortcut"
> 
> Step 3: Click the windows icon, press "Run". Then, type in `shell:startup`
> 
> Step 4: Move the shortcut you just created into this folder

This will automatically launch this application on startup.

While the app is open, simply press PrntScreen to screenshot. This will play a simple sound effect.

If there's instead an error sound effect and no screenshot was taken, check the filepath! It may be invalid on your computer.

# Config

Inside the folder you unzipped, you can find a folder called "config.txt". You can change a couple settings here:

1. filename: Filename of the screenshot. You can define variables with `{variable}`. Default filename is: `Screenshot 20{year}-{month}-{day} {hour}.{minute}.{second}{repeat_empty}{repeat}`. You can use `/` to define subfolders with variables, if you like.
-    {year}: last two digits of the year
-    {month}: month number
-    {day}: day number
-    {hour}: hour number
-    {minute}: minute number
-    {second}: second number
-    {resolution_x}: pixel width of the monitor screenshot
-    {resolution_y}: pixel height of the monitor screenshot
-    {monitor}: ID of the monitor screenshot
-    {repeat}: if the name with this filename already exists, increment a number here. Will be empty if there is no duplicate.
-    {repeat_empty}: if the name with this filename already exists, place a space here. Will be empty if there is no duplicate.

2. image_scale. Percentage resolution of the screenshot. Defaults to 100. It can be higher than than 100, but I'd recommend against it.
3. output_location_relative_to_pictures_folder. defines whether the path set below is to relative of the Pictures folder. Defaults to True.
4. output_location. path to save the screenshots. Defaults to `Screenshots/`
5. play_sound_effect. play a sound effect when a screenshot is taken. Defaults to true. The file it plays is `screenshot_taken.wav` and can be changed with any other sound file if you want.
