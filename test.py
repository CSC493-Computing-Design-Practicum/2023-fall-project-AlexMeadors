import tkinter as tk 
from PIL import ImageTk,Image  

def tkinter_setup():
    global root
    root = tk.Tk()  
    return root


class screen():
    def __init__(self):
        image = Image.open("chronokeeper_logo.png")
        image_size = (100,100)
        resize_image = image.resize(image_size)
        logo = ImageTk.PhotoImage(resize_image)
        
        canvas = tk.Canvas(
                root, 
                width = 100, 
                height = 100
                )  
        canvas.pack()  
        #img = ImageTk.PhotoImage(Image.open('chronokeeper_logo.png')) 
        
        canvas.create_image(0, 0, 
                anchor=tk.NW, 
                image=logo
                )  


def main():
    root = tkinter_setup()
     


    root.mainloop()

main()