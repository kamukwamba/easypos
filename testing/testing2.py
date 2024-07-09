import customtkinter as ctk
import pywinstyles



class CustomCTkButton(ctk.CTkFrame):
    def __init__(self, parent, shadow_color='lightgrey', **kwargs):
        super().__init__(parent, fg_color='transparent')
        self.shadow = ctk.CTkFrame(self, fg_color=shadow_color)
        self.button = ctk.CTkLabel(self, bg_color="#000001", **kwargs)
        self.button.place(x=0, y=0)
        h = self.button.cget('height')
        w = self.button.cget('width')
        cr = self.button.cget('corner_radius')
        self.shadow.configure(height = h, width = w, corner_radius = cr)
        self.shadow.place(x=0, y=4)
        self.button.lift()
        pywinstyles.set_opacity(self.button, color="#000001")


# Example usage
if __name__ == '__main__':
    app = ctk.CTk()
    custom_button = CustomCTkButton(app, text="Custom", width=200, height=80, corner_radius = 32)
    custom_button.pack()
    app.mainloop()