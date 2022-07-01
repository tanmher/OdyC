from tkinter import *
import basic

def lexical_analyzer():
    error.config(state='normal')
    output.config(state='normal')
    error.delete('1.0', END)
    output.delete('1.0', END)
    output_title.delete('1.0', END)
    output_title.config(state='disabled')
    output.insert(END, 'LEXEME \t\t\t\t TOKEN\n')
    input = entry1.get("1.0",END)

    text = input
    result, err = basic.lexical('<stdin>', text)


    if err: error.insert(END, err.as_string())
    else: 
        for token in result:
            type = token.type
            value = x[1]
            output.insert(END, f'{type} \t\t\t\t {value}')

    output.config(state='disabled') 
    error.config(state='disabled')
    
window = Tk()

window.geometry("1000x600")
window.configure(bg = "#1b1616")
canvas = Canvas(
    window,
    bg = "#1b1616",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    742.5, 326.5,
    image = entry0_img)
    
output_title = Text(
    bd = 0,
    bg = '#123213',
    highlightthickness = 0,
    padx=10,
    pady=10,
    font = ("Roboto Mono", 8)
)
output_title.place(
    x = 532.0, y = 79,
    width = 420.0,
)

output = Text(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,
    padx=10,
    pady=10,
    font = ("Roboto Mono", 8),
    state='disabled'
)

output.place(
    x = 532.0, y = 79,
    width = 420.0,
    height = 493)

error = Text(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,
    padx=10,
    pady=10,
    font = ("Roboto Mono", 8),
    state='disabled'
)

error.place(
    x = 46.0, y = 339,
    width = 430.0,
    height = 233)
    

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    261.0, 204.5,
    image = entry1_img)

entry1 = Text(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,
    font = ("Roboto Mono", 8))

entry1.place(
    x = 46.0, y = 79,
    width = 430.0,
    height = 249)

entry2_img = PhotoImage(file = f"img_textBox2.png")
entry2_bg = canvas.create_image(
    261.0, 456.5,
    image = entry2_img)


img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command= lexical_analyzer,
    relief = "flat")

b0.place(
    x = 232, y = 33,
    width = 71,
    height = 29)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    relief = "flat")

b1.place(
    x = 315, y = 33,
    width = 81,
    height = 29)

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    relief = "flat")

b2.place(
    x = 407, y = 33,
    width = 81,
    height = 29)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    102.5, 47.5,
    image=background_img)

window.resizable(False, False)
window.mainloop()
