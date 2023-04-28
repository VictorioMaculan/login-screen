import tkinter as tk
defaultfont = ('Times New Roman', 12)

root = tk.Tk()
root.title('Login/Register')
root.geometry('500x500')

# Tela de Registro
register = tk.Frame(root)
register.pack()

tk.Label(register, text='Faça seu Registro!', font=('Times New Roman', 16)).pack(pady=20)

tk.Label(register, text='Nome', font=defaultfont).pack(pady=10)
name = tk.Entry(register, font=defaultfont, width=35)
name.pack()

tk.Label(register, text='Email', font=defaultfont).pack(pady=10)
email = tk.Entry(register, font=defaultfont, width=35)
email.pack()

tk.Label(register, text='Senha', font=defaultfont).pack(pady=10)
password = tk.Entry(register, font=defaultfont, width=35)
password.pack()

tk.Button(register, text='Registrar', font=defaultfont).pack(pady=10)



tk.mainloop()