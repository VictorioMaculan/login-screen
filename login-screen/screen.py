import tkinter as tk
import sqlite3
defaultfont = ('Times New Roman', 12)

class Gui:
    def __init__(self):   
        self.root = tk.Tk()
        self.activeframe = None
        
        self.registering()
        self.root.title('Login/Register')
        self.root.geometry('400x500')
        self.root.mainloop()
       
    @staticmethod
    def newuser(name, email, password):
        con = sqlite3.connect('users.db')
        cursor = con.cursor()
        try:
            cursor.execute('''create table users(id integer primary key autoincrement,
                           name text,
                           email text,
                           password text)''')
        except sqlite3.OperationalError:
            pass
        finally:
            cursor.execute('''insert into users (name, email, password)
                           values(?, ?, ?)''', (name, email, password))
            con.commit()
            cursor.close()
            con.close()
            
        
    def activate(self, frame):
        if self.activeframe is not None:
            self.activeframe.destroy()
        self.activeframe = frame
        self.activeframe.pack()
        
    def registering(self):
        register = tk.Frame(self.root)

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
        
        tk.Button(register, text='Login', font=('Times New Roman', 10), command=self.login).pack(side='bottom')
        tk.Label(register, text='Ja tem uma conta?', font=('Times New Roman', 10)).pack(side='bottom')
        self.activate(register)
    
    def login(self):
        login_ = tk.Frame(self.root)
        
        tk.Label(login_, text='Faça seu Login!', font=('Times New Roman', 16)).pack(pady=20)
        
        tk.Label(login_, text='Nome ou Email', font=defaultfont).pack(pady=10)
        user = tk.Entry(login_, font=defaultfont, width=35)
        user.pack()
        
        tk.Label(login_, text='Senha', font=defaultfont).pack(pady=10)
        password = tk.Entry(login_, font=defaultfont, width=35)
        password.pack()
        
        tk.Button(login_, text='Login', font=defaultfont).pack(pady=10)
        
        tk.Button(login_, text='Cadastrar', font=('Times New Roman', 10), command=self.registering).pack(side='bottom')
        tk.Label(login_, text='Não tem uma conta?', font=('Times New Roman', 10)).pack(side='bottom')
        self.activate(login_)
        
    def emailverification(self, email='-'):
        verify = tk.Frame(self.root)
        
        tk.Label(verify, text='Verificação do Email', font=('Times New Roman', 16)).pack(pady=20)
        tk.Label(verify, text=f'Um código será enviado a {email}', font=defaultfont).pack(pady=10)
        tk.Label(verify, text='Insira o código de três digitos abaixo:').pack(pady=10)
        
        code = tk.Entry(verify, font=('Times New Roman', 22), width=3)
        code.pack()
        
        tk.Button(verify, text='Continuar', font=defaultfont).pack(pady=10)
        self.activate(verify)
        
        

Gui.newuser('Roberto', '167761', '167761')