import winsound
from PIL import Image
from ctypes import windll, Structure, c_long, byref
from pynput.keyboard import Key, Listener
from time import gmtime, strftime
from os import path
from mss import mss
from pathlib import Path

monitor_limits = []
settings = {
    "filename": "Screenshot 20{year}-{month}-{day} {hour}.{minute}.{second}{repeat_empty}{repeat}",
    "image_scale": 100,
    "output_location_relative_to_pictures_folder": True,
    "output_location": "Screenshots/",
    "play_sound_effect": True
}

resolution_x = []
resolution_y = []


def main():
    with mss() as sct:
        # there's always 1 more monitor than plugged in, which contains a concatenations
        # of every other monitor.
        monitor_count = len(sct.monitors) - 1

        # get monitor limits:
        # If monitor 1 starts at x:0 and ends at x:1920,
        # and monitor 2 starts at x:1921 and ends at x:3840...
        # the list is: [0,1920,3840]

        monitor_limits.append(sct.monitors[0]["left"])
        i = 1
        while i < monitor_count + 1:
            monitor_limits.append((sct.monitors[i]["left"] + sct.monitors[i]["width"]))
            resolution_x.append(sct.monitors[i]["width"])
            resolution_y.append(sct.monitors[i]["height"])
            i += 1

        for f in monitor_limits:
            print(f)


    # check for key presses constantly
    with Listener(on_press=on_press) as listener:
        listener.join()


def take_screenshot():
    read_config()

    with mss() as sct:
        mouse_x = query_mouse_position()["x"]

        # Find the monitor with the mouse cursor on it
        active_monitor = 0
        i = 0
        while i < len(monitor_limits) - 1:
            if monitor_limits[i] < mouse_x < monitor_limits[i + 1]:
                active_monitor = i
                break

            i += 1

        # If it could not find it, default to the primary screenshot (with the 0 initial value)
        # https://python-mss.readthedocs.io/examples.html
        print(f"Taking screenshot of monitor #{active_monitor}")

        # grabs the screen data...
        sct_img = sct.grab(sct.monitors[active_monitor + 1])

        # and does some pillow stuff with it
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        scale = settings["image_scale"]
        if scale != "100":
            print(f"Downscaling Image to {scale}% of the resolution")
            img = resize_image(img, int(resolution_x[active_monitor] * int(scale) * 0.01))

        filename = "screenshot"
        repeat = 0
        while True:
            name = format_filename(repeat, active_monitor)
            filename = f"{get_output_folder()}{name}.png"
            if not path.exists(filename):
                break
            repeat += 1
            if repeat > 1000:
                break

        print(filename)
        img.save(filename)

        if settings["play_sound_effect"] == "True":
            winsound.PlaySound('screenshot_taken.wav', winsound.SND_FILENAME)


# resizes image while keeping aspect ratio
def resize_image(image, width):
    print(width)
    percent = (width / float(image.size[0]))
    size = int((float(image.size[1]) * float(percent)))
    img = image.resize((width, size), Image.Resampling.LANCZOS)
    return img


def get_output_folder():
    # https://stackoverflow.com/questions/26618844/platform-independent-way-to-fetch-pictures-folder
    if settings["output_location_relative_to_pictures_folder"] == "True":
        return str(Path.home() / "Pictures") + "/" + settings["output_location"]
    else:
        return settings["output_location"]


# properly formats the name of the file according to filename in config
def format_filename(_repeat, _monitor):
    _hour = strftime("%H", gmtime())
    _minute = strftime("%M", gmtime())
    _second = strftime("%S", gmtime())
    _year = strftime("%Y", gmtime())
    _year = _year[2:]
    _month = strftime("%m", gmtime())
    _day = strftime("%d", gmtime())

    _resolution_x = resolution_x[_monitor]
    _resolution_y= resolution_y[_monitor]

    _repeat_empty = " "
    if _repeat == 0:
        _repeat_empty = ""

    _repeat2 = _repeat
    if _repeat == 0:
        _repeat2 = ""

    filename = settings["filename"]
    #print(filename)
    return slugify(filename.format(
        year=_year, month=_month, day=_day, hour=_hour, minute=_minute, second=_second, repeat=_repeat2,
        resolution_x=_resolution_x, resolution_y=_resolution_y, monitor=_monitor, repeat_empty=_repeat_empty))


def slugify(text):
    length = len(text)
    i = 0

    chars = list(text)

    while i < length:
        char = chars[i]
        if "?\\|<>:\"*".find(char) != -1:
            chars[i] = "-"
        i += 1

    output = ""
    for a in chars:
        output += a

    return output


def read_config():
    if path.exists("config.txt"):
        f = open("config.txt", "r")
        lines = f.readlines()
        for line in lines:
            a = line.split("=")
            if len(a) < 2:
                break

            settings[a[0]] = a[1].replace("\n", "")

        f.close()
    else:
        f = open("config.txt", "x")
        for key in settings.keys():
            f.write(f"{key}={settings[key]}\n")
        f.close()


def on_press(key):
    if key == Key.print_screen:
        take_screenshot()


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def query_mouse_position():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
