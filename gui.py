import time
from Tkinter import *

class Example(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.text = Text(self, height=30, width=100)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)        

#if __name__ == "__main__":
root = Tk()
frame = Example(root)

def Enter_pressed(event):
    input_get = input_field.get()
    frame.text.insert(INSERT, '%s\n' % input_get)
    input_user.set('')
    frame.text.see("end")  
    return "break"

input_user = StringVar()
input_field = Entry(root, text=input_user)
input_field.pack(side=BOTTOM, fill=X)    
input_field.bind("<Return>", Enter_pressed)

frame.pack(fill="both", expand=True)
root.mainloop()