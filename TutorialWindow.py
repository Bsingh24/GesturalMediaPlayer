from tkinter import *

# https://google.github.io/mediapipe/solutions/hands.html - Used this link to understand the hand model usage of Mediapipe
# https://www.youtube.com/watch?v=NZde8Xt78Iw - Used this video to understand real time hand tracking
# https://www.youtube.com/watch?v=9iEPzbG-xLE - Used this video to understand volume control with gestures
# https://pyautogui.readthedocs.io/en/latest/ - Used this link to understand PyAutoGUI and its interaction with hotkeys

root = Tk()

root.resizable(False, False)

w = 1280
h = 800

screenW = root.winfo_screenwidth()
screenH = root.winfo_screenheight()

x = int((screenW/2) - (w/2))
y = int((screenH/2) - (h/2))

root.geometry("{}x{}+{}+{}".format(w, h, x, y))
root.title('Tutorial Window')

global images, count
count = -1
def next():
    global count
    if count != 10:
        my_canvas.create_image(0, 0, image=images[count+1], anchor='nw')
        count += 1
    else:
        # will destroy the tutorial window
        root.destroy()
        #calls the HandVolumeTracking
        import HandVolumeTracking
    root.after(3000, next)

images = [
    PhotoImage(file="./images/1.png"),
    PhotoImage(file="./images/2.png"),
    PhotoImage(file="./images/3.png"),
    PhotoImage(file="./images/4.png"),
    PhotoImage(file="./images/5.png"),
    PhotoImage(file="./images/6.png"),
    PhotoImage(file="./images/7.png"),
    PhotoImage(file="./images/8.png"),
    PhotoImage(file="./images/9.png"),
    PhotoImage(file="./images/10.png"),
    PhotoImage(file="./images/11.png"),
]



my_canvas = Canvas(root, width=1280, height=800)
my_canvas.pack(fill="both", expand=True)


next()
root.mainloop()
