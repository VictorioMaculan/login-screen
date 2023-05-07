import tkinter as tk
import sqlite3

defaultfont = ('Times New Roman', 12)
database = 'C:\\Users\\User\\Documents\\GitHub\\login-screen\\login-screen\\users.db'

class Gui:
    def __init__(self):   
        self.preparedb()
        
        self.root = tk.Tk()
        self.outmsg = tk.StringVar()
        self.fastusers = self.getSavedUsers()
        self.activeframe = None
        
        self.choose()
        
        self.outmsg.set('-')
        self.root.title('Login/Register')
        self.root.geometry('400x500')
        
        self.root.mainloop()
    
    @staticmethod
    def isRegisterValid(name, email, password):
        if name.strip() == '' or password.strip() == '':
            return False
        with sqlite3.connect(database) as con:
            cursor = con.cursor()
            cursor.execute(f'select * from users where email = ?', (email,))
            out = cursor.fetchall()
            cursor.close()
        return (len(out) == 0)

    @staticmethod
    def isLoginValid(email, password):
        with sqlite3.connect(database) as con:
            cursor = con.cursor()
            cursor.execute('select * from users where email = ? and password = ?', (email, password))
            out = cursor.fetchall()
            cursor.close()
        return len(out) > 0
    
    @staticmethod
    def getSavedUsers():
        with sqlite3.connect(database) as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            out = [register for register in cursor.execute('select * from fastusers')]
            cursor.close()
        return out
    
    @staticmethod
    def preparedb():
        with sqlite3.connect(database) as con:
            cursor = con.cursor()
            try:
                cursor.execute('''create table users(id integer primary key autoincrement,
                    name text,
                    email text,
                    password text)''')
                cursor.execute('''create table fastusers(id integer primary key autoincrement,
                               name text,
                               email text,
                               password text)''')
            except sqlite3.OperationalError:
                return
            finally:
                cursor.close()
                con.commit()
                    
    def activate(self, frame):
        if self.activeframe is not None:
            self.activeframe.destroy()
        self.activeframe = frame
        self.activeframe.pack()
        self.outmsg.set('-')    
        
    def newFastUser(self, name, email, password):
        if len(self.fastusers) <= 3:
            self.outmsg.set('Você já atingiu o limite de Logins Rápidos.')
            return
        
        with sqlite3.connect(database) as con:
            cursor = con.cursor()
            cursor.execute('''insert into fastusers(name, email, password)
                           values(?, ?, ?, ?)''', (name, email, password))
            cursor.close()
            con.commit()
        self.outmsg.set('Adicionado aos Logins Rápidos.')
            
    def newuser(self, name, email, password):
        if not self.isRegisterValid(name, email, password):
            self.outmsg.set('[ERRO: Parâmetro(s) Inválido(s)/Email já em Uso]')
            return
        
        with sqlite3.connect(database) as con:
            cursor = con.cursor()
            cursor.execute('''insert into users(name, email, password)
                        values(?, ?, ?)''', (name, email, password))
            cursor.close()
            con.commit()
        self.outmsg.set('Cadastrado. Por favor, fazer login.')
        self.login()
        
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

        tk.Button(register, text='Registrar', font=defaultfont, 
                  command=lambda: self.newuser(name.get().strip(), 
                                               email.get().strip(), 
                                               password.get().strip())).pack(pady=10)

        tk.Label(register, textvariable=self.outmsg, font=defaultfont).pack(side='bottom', pady=20)
        tk.Button(register, text='Login', font=('Times New Roman', 10), command=self.login).pack(side='bottom')
        tk.Label(register, text='Ja tem uma conta?', font=('Times New Roman', 10)).pack(side='bottom')
        self.activate(register)
        
    def login(self):
        login_ = tk.Frame(self.root)
        
        tk.Label(login_, text='Faça seu Login!', font=('Times New Roman', 16)).pack(pady=20)
        
        tk.Label(login_, text='Email', font=defaultfont).pack(pady=10)
        email = tk.Entry(login_, font=defaultfont, width=35)
        email.pack()
        
        tk.Label(login_, text='Senha', font=defaultfont).pack(pady=10)
        password = tk.Entry(login_, font=defaultfont, width=35)
        password.pack()
        
        tk.Button(login_, text='Login', font=defaultfont, command=lambda: self.logged(
            email.get().strip(), password.get().strip(),)).pack(pady=10)
        
        tk.Checkbutton()
        
        tk.Label(login_, textvariable=self.outmsg, font=defaultfont).pack(side='bottom', pady=20)
        tk.Button(login_, text='Cadastrar', font=('Times New Roman', 10), command=self.registering).pack(side='bottom')
        tk.Label(login_, text='Não tem uma conta?', font=('Times New Roman', 10)).pack(side='bottom')
        self.activate(login_)
        
    def logged(self, email, password):
        if not self.isLoginValid(email, password):
            self.outmsg.set('[ERRO: Parâmetro(s) Inválido(s)/Senha Incorreta]. ')
            return
        
        with sqlite3.connect(database) as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            account = [x for x in cursor.execute('select * from users where email = ?', (email,))][0]
            
        
        logged_ = tk.Frame(self.root, width=500, height=400)
        tk.Label(logged_, text=f'Logado! Informações da Conta:', font=('Times New Roman', 16)).place(y=12, x=200, anchor='center')
        
        tk.Label(logged_, text=f'Nome = {account["name"]}', font=defaultfont).place(y=30, x=0)
        tk.Label(logged_, text=f'Email = {account["email"]}', font=defaultfont).place(y=60, x=0)
        tk.Label(logged_, text=f'Senha = {account["password"]}', font=defaultfont).place(y=90, x=0)

        tk.Button(logged_, text='Ativar Login Rápido', font=defaultfont,
                  command=lambda: self.newFastUser(account['name'],
                                                   account['email'],
                                                   account['password'])).place(y=125, x=5)
        
        tk.Button(logged_, text='Sair', font=defaultfont, command=self.login).place(y=165, x=5)
        
        tk.Label(logged_, textvariable=self.outmsg, font=defaultfont).place(y=215, x=200, anchor='center')
        self.activate(logged_)
        
    def choose(self):
        choose_ = tk.Frame(self.root, width=500, height=400)
        tk.Label(choose_, text='Você Tem Logins Rápidos Salvos', 
                 font=('Times New Roman', 16)).place(y=12, x=200, anchor='center')

        # TODO: Mostrar contas disponíveis para Fast-Login
        
        tk.Label()

        self.activate(choose_)
Gui()
