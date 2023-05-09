import tkinter as tk
import sqlite3

defaultfont = ('Times New Roman', 12)
database = 'C:\\Users\\User\\Documents\\GitHub\\login-screen\\login-screen\\users.db'

class Gui:
    def __init__(self):   
        self.preparedb()
        
        self.root = tk.Tk()
        self.outmsg = tk.StringVar()
        self.fastusers = self.getTableContent(table='fastusers')
        self.activeframe = None
        
        if len(self.fastusers) == 0:
            self.registering()
        else:
            self.choose()
        
        self.outmsg.set('-')
        self.root.title('Login/Register')
        self.root.geometry('400x450')
        
        self.root.mainloop()
    
    # Methods
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
        # TODO: Melhorar isso aqui :P
    @staticmethod
    def getTableContent(table):
        with sqlite3.connect(database) as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            out = [register for register in cursor.execute(f'select * from {table}')]
            cursor.close()
        return out if out is not None else list()
    
    @staticmethod
    def isEmailUnique(email, table):
        with sqlite3.connect(database) as con:
            cursor = con.cursor()
            cursor.execute(f'select * from {table} where email = ?', (email,))
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
    
    def isRegisterValid(self, name, email, password):
        if name.strip() == '' or password.strip() == '' or not self.isEmailUnique(email, table='users'):
            return False
        return True
                    
    def activate(self, frame):
        if self.activeframe is not None:
            self.activeframe.destroy()
        self.activeframe = frame
        self.activeframe.pack()
        
    def newFastUser(self, name, email, password):
        if len(self.fastusers) >= 3:
            self.outmsg.set('Você já atingiu o limite de Logins Rápidos.')
            return
        if not self.isEmailUnique(email, table='fastusers'):
            self.outmsg.set('Email já registrado nos Logins Rápidos.')
            return
        
        with sqlite3.connect(database) as con:
            cursor = con.cursor()
            cursor.execute('''insert into fastusers(name, email, password)
                           values(?, ?, ?)''', (name, email, password))
            cursor.close()
            con.commit()
        self.outmsg.set('Adicionado aos Logins Rápidos.')
        self.fastusers = self.getTableContent(table='fastusers')
    
    def delFastUser(self, email):
        with sqlite3.connect(database) as con:
            cursor = con.cursor()
            cursor.execute(f'delete from fastusers where email = ?', (email,))
            cursor.close()
        self.fastusers = self.getTableContent(table='fastusers')
        self.outmsg.set('Removido dos Logins Rápidos.')
    
    def newUser(self, name, email, password):
        if not self.isRegisterValid(name, email, password):
            self.outmsg.set('[ERRO: Parâmetro(s) Inválido(s)/Email já em Uso]')
            return
        if 12 < len(password.strip()) < 6:
            self.outmsg.set('[ERRO: A senha deve ter entre 6 e 12 caracteres]')
            return
        
        with sqlite3.connect(database) as con:
            cursor = con.cursor()
            cursor.execute('''insert into users(name, email, password)
                        values(?, ?, ?)''', (name, email, password))
            cursor.close()
            con.commit()
        self.outmsg.set('Cadastrado. Por favor, fazer login.')
        self.login()
    
    # Specific Methods
    def onoff_FastUser(self, name, email, password):
        if self.isEmailUnique(email, table='fastusers'):
            self.newFastUser(name, email, password)
        else:
            self.delFastUser(email)
        self.logged(email, password)
        
    
    # Frames
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
                  command=lambda: self.newUser(name.get().strip(), 
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
        
        tk.Label(login_, textvariable=self.outmsg, font=defaultfont).pack(side='bottom', pady=20)
        tk.Button(login_, text='Cadastrar', font=('Times New Roman', 10), command=self.registering).pack(side='bottom')
        tk.Label(login_, text='Não tem uma conta?', font=('Times New Roman', 10)).pack(side='bottom')
        self.activate(login_)
        
    def logged(self, email, password):
        
        if not self.isLoginValid(email, password):
            self.outmsg.set('[ERRO: Parâmetro(s) Inválido(s)/Senha Incorreta].')
            return
        
        with sqlite3.connect(database) as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            info = [x for x in cursor.execute('select * from users where email = ?', (email,))][0]
            
        logged_ = tk.Frame(self.root, width=500, height=400)
        tk.Label(logged_, text=f'Logado! Informações da Conta:', font=('Times New Roman', 16)).place(y=12, x=200, anchor='center')
        
        tk.Label(logged_, text=f'Nome = {info["name"]}', font=defaultfont).place(y=30, x=0)
        tk.Label(logged_, text=f'Email = {info["email"]}', font=defaultfont).place(y=60, x=0)
        tk.Label(logged_, text=f'Senha = {info["password"]}', font=defaultfont).place(y=90, x=0)
        FLstatus = 'Ativado' if not self.isEmailUnique(info['email'], table='fastusers') else 'Desativado'
        tk.Label(logged_, text=f'Login Rápido = {FLstatus}', font=defaultfont).place(y=120, x=0)
        
        tk.Button(logged_, text='[On/Off] Login Rápido', font=defaultfont,
                  command=lambda: self.onoff_FastUser(info['name'],
                                                      info['email'],
                                                      info['password'])).place(y=155, x=5)
        
        tk.Button(logged_, text='Sair', font=defaultfont, command=self.login).place(y=200, x=5)
        
        tk.Label(logged_, textvariable=self.outmsg, font=defaultfont).place(y=230, x=200, anchor='center')
        self.activate(logged_)
        
    def choose(self):
        choose_ = tk.Frame(self.root, width=500, height=400)
        tk.Label(choose_, text='Você Tem Logins Rápidos Salvos', 
                 font=('Times New Roman', 16)).place(y=12, x=200, anchor='center')


        if len(self.fastusers) >= 1:
            account1 = self.fastusers[0]
        
            tk.Label(choose_, text=f'> {account1["name"]} ({account1["email"]})',
                     font=('Times New Roman', 14)).place(x=5, y=50)
            tk.Button(choose_, text='Logar', font=defaultfont, 
                      command=lambda: self.logged(account1['email'], account1['password'])).place(x=5, y=80)
            tk.Button(choose_, text='Remover de Logins Rápidos', font=defaultfont,
                      command=lambda: self.delFastUser(account1['email'])).place(x=60, y=80)
        else:
            tk.Label(choose_, text='> Conta 1 (Vazio)', font=('Times New Roman', 14)).place(x=5, y=50)
            
            
        if len(self.fastusers) >= 2:
            account2 = self.fastusers[1]
            
            tk.Label(choose_, text=f'> {account2["name"]} ({account2["email"]})',
                     font=('Times New Roman', 14)).place(x=5, y=150)
            tk.Button(choose_, text='Logar', font=defaultfont, 
                      command=lambda: self.logged(account2['email'], account2['password'])).place(x=5, y=180)
            tk.Button(choose_, text='Remover de Logins Rápidos', font=defaultfont,
                      command=lambda: self.delFastUser(account2['email'])).place(x=60, y=180)
        else:
            tk.Label(choose_, text='> Conta 2 (Vazio)', font=('Times New Roman', 14)).place(x=5, y=150)
        
        
        if len(self.fastusers) >= 3:
            account3 = self.fastusers[2]
            
            tk.Label(choose_, text=f'> {account3["name"]} ({account3["email"]})',
                     font=('Times New Roman', 14)).place(x=5, y=250)
            tk.Button(choose_, text='Logar', font=defaultfont, 
                      command=lambda: self.logged(account3['email'], account3['password'])).place(x=5, y=280)
            tk.Button(choose_, text='Remover de Logins Rápidos', font=defaultfont,
                      command=lambda: self.delFastUser(account3['email'])).place(x=60, y=280)
        else:
            tk.Label(choose_, text='> Conta 3 (Vazio)', font=('Times New Roman', 14)).place(x=5, y=250)    
        
        
        tk.Label(choose_, text='Quer acessar outra conta?', font=('Times New Roman', 9)).place(y=330, x=200, anchor='center')
        tk.Button(choose_, text='Login', font=('Times New Roman', 9), command=self.login).place(y=350, x=200, anchor='center')

        self.activate(choose_)

Gui()
