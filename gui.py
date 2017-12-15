from Tkinter import * # Tkinter -> tkinter in Python3

class App(object):
    def __init__(self):
        self.root = Tk()

    # create a Frame for the Text and Scrollbar
        txt_frm = Frame(self.root, width=600, height=600)
        txt_frm.pack(fill="both", expand=True)
        # ensure a consistent GUI size
        txt_frm.grid_propagate(False)
        # implement stretchability
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)

    # create a Text widget
        self.txt = Text(txt_frm, borderwidth=3, relief="sunken")
        self.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    # create a Scrollbar and associate it with txt
        scrollb = Scrollbar(txt_frm, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set
    
app = App()

def Enter_pressed(event):
    input_get = input_field.get()
    print(input_get)
    app.txt.insert(INSERT, '%s\n' % input_get)
    # label = Label(window, text=input_get)
    input_user.set('')
    app.txt.see("end")  
    # label.pack()
    return "break"

input_user = StringVar()
input_field = Entry(app.root, text=input_user)
input_field.pack(side=BOTTOM, fill=X)

input_field.bind("<Return>", Enter_pressed)

app.root.mainloop()
