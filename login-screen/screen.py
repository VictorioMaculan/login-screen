import tkinter as tk
import sqlite3

defaultfont = ('Times New Roman', 12)
database = 'C:\\Users\\User\\Documents\\GitHub\\login-screen\\login-screen\\users.db'
message_file = 'C:\\Users\\User\\Documents\\GitHub\\login-screen\\login-screen\\msg.txt'
systememail = '-'

class Gui:
    def __init__(self):   
        self.root = tk.Tk()
        self.outmsg = tk.StringVar()
        self.activeframe = None
        
        self.registering()
        self.preparedb()
        
        self.outmsg.set('-')
        self.root.title('Login/Register')
        self.root.geometry('400x500')
        
        self.root.mainloop()
    
    @staticmethod
    def isRegisterValid(name, email, password):
        if name.strip() == '' or email.strip() == '' or password.strip() == '':
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
    def sendemail(email, sendcode='000'):
        import smtplib
        from email.message import EmailMessage
        
        message = EmailMessage()
        with open(message_file) as msg:
            message.set_content(msg.read().replace('{sendcode}', str(sendcode)))
        
        message['Subject'] = 'Registro (Login/Registering System)'
        message['From'] = systememail
        message['To'] = email
        
        with smtplib.SMTP(host='localhost') as host:
            host.send_message(message)
        # TODO: Finish and fix this.    
        
            
    @staticmethod
    def preparedb():
        with sqlite3.connect(database) as con:
            cursor = con.cursor()
        try:
            cursor.execute('''create table users(id integer primary key autoincrement,
                name text,
                email text,
                password text)''')
        except sqlite3.OperationalError:
            return
        
    def newuser(self, name, email, password):
        with sqlite3.connect(database) as con:
            cursor = con.cursor()
            cursor.execute('''insert into users(name, email, password)
                        values(?, ?, ?)''', (name, email, password))
            cursor.close()
            con.commit()
        self.outmsg.set('Cadastrado. Por favor, fazer login.')
        self.login()
                
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

        tk.Button(register, text='Registrar', font=defaultfont, 
                  command=lambda: self.finalver(name.get(), email.get(), password.get())).pack(pady=10)

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
        
        tk.Button(login_, text='Login', font=defaultfont, command=lambda: self.loggedscreen(email.get(), password.get())).pack(pady=10)
        
        tk.Label(login_, textvariable=self.outmsg, font=defaultfont).pack(side='bottom', pady=20)
        tk.Button(login_, text='Cadastrar', font=('Times New Roman', 10), command=self.registering).pack(side='bottom')
        tk.Label(login_, text='Não tem uma conta?', font=('Times New Roman', 10)).pack(side='bottom')
        self.activate(login_)
        
    def finalver(self, name, email, password):
        from random import randint
        
        if not self.isRegisterValid(name, email, password):
            self.outmsg.set(('[ERRO: Parâmetro(s) inválido(s)].'))
            return

        sendcode = str(randint(100, 999))
        self.outmsg.set(sendcode)
        # self.sendemail(email, sendcode)
        
        verify = tk.Frame(self.root)
        
        tk.Label(verify, text='Verificação do Email', font=('Times New Roman', 16)).pack(pady=20)
        tk.Label(verify, text=f'Um código será enviado a {email}', font=defaultfont).pack(pady=10)
        tk.Label(verify, text='Insira o código de três digitos abaixo:').pack(pady=10)
        
        code = tk.Entry(verify, font=('Times New Roman', 22), width=3)
        code.pack()
        
        compare = lambda: self.newuser(name, email, password) if code.get() == sendcode else self.outmsg.set('Código Inválido')
        tk.Button(verify, text='Continuar', font=defaultfont, command=compare).pack(pady=10)
        
        tk.Label(verify, textvariable=self.outmsg, font=defaultfont).pack(side='bottom', pady=20)
        self.activate(verify)

    def loggedscreen(self, email, password):
        if not self.isLoginValid(email, password):
            self.outmsg.set('[ERRO: Parâmetro(s) Inválido(s)/Senha Incorreta]. ')
            return
        
        logged = tk.Frame(self.root)
        tk.Label(logged, text=f'Olá {email}, agora você está logado(a)!', font=defaultfont).pack(pady=20)
        
        tk.Button(logged, text='Sair', font=defaultfont, command=self.login).pack(pady=20)
        self.activate(logged)

Gui()