# A basic example of overlapping image and button
import customtkinter
from PIL import Image
import pywinstyles

HEIGHT = 500
WIDTH = 500
IMAGEINH = "testing/image.png"

app = customtkinter.CTk()
app.title("example")
app.geometry((f"{WIDTH}x{HEIGHT}"))
app.resizable(False, False)

Label1 = customtkinter.CTkLabel(master=app, text="", image=customtkinter.CTkImage(Image.open(IMAGEINH), size=(500,500)),
                                width=500, height=500)
Label1.place(x=0, y=0)

Button1 = customtkinter.CTkLabel(master=app, width=150, height=40, corner_radius=5,
                                  text='BUTTON', bg_color="#000001", fg_color="#0761DC", text_color="white") 
Button1.place(x=120, y=57)

pywinstyles.set_opacity(Button1, color="#000001") # just add this line

pywinstyles.apply_style(app, "mica")
pywinstyles.change_header_color(app, color="#00524d")  

app.mainloop()