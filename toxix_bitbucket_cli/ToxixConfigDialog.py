#!/usr/bin/python3

from tkinter import *
from .Client import Client
from .BitbucketRestClientExceptions import NotAuthenticatedError

class ToxixConfigDialog:
    def __init__(self, conf):

        self.conf = conf
        self.window=Tk()

        self.window.columnconfigure(0, minsize=20)
        self.window.columnconfigure(11, minsize=20)
        self.window.rowconfigure(1, minsize=20)

        lbl=Label(self.window, text="Configuration - Toxix Bitbucket Cli", font=("Helvetica", 16))
        lbl.grid(column=1, columnspan=10, row=10)
        lbl=Label(self.window, text="This tests and saves your credentials in your keyring, for later use with this application.", font=("Helvetica", 12))
        lbl.grid(column=1, columnspan=10, row=12)

        self.window.rowconfigure(15, minsize=80)


        lbl_bb_user=Label(self.window, text='Enter your Bitbucket user name (This is not your email! You can get it from "personal settings" -> "account settings"): ')
        lbl_bb_user.grid(column=3,row=20) 
        self.txt_fld_bb_user=Entry(self.window, text='bb_username', bd=2)
        self.txt_fld_bb_user.insert(0, self.conf['bb_username'])
        self.txt_fld_bb_user.grid(column=6, row=20)

        lbl_bb_pw=Label(self.window, text='Bitbucket App password (You can get/generate it in "personal settings" -> "app passwords"): ')
        lbl_bb_pw.grid(column=3,row=30) 
        self.txt_fld_bb_pw=Entry(self.window, text='bb_password', bd=2, show='*')
        self.txt_fld_bb_pw.insert(0, self.conf.get_password('bb_password'))
        self.txt_fld_bb_pw.grid(column=6, row=30)

        self.window.rowconfigure(35, minsize=10)

        self.lbl_bb_test_text=StringVar()
        self.lbl_bb_test=Label(self.window, textvariable=self.lbl_bb_test_text)
        self.lbl_bb_test.grid(column=2, columnspan=8, row=40)



        self.window.rowconfigure(99, minsize=30)
        btn=Button(self.window, text="cancel", fg='gray',  command=self.window.destroy)
        btn.grid(column=7, row=100,sticky =SE)

        btn=Button(self.window, text="test", fg='green',  command=self._test_config)
        btn.grid(column=8, row=100,sticky =SE)

        btn=Button(self.window, text="save", fg='blue',  command=self._save_config)
        btn.grid(column=10, row=100,sticky =SE)

        self.window.rowconfigure(101, minsize=8)

        self.window.title('Toxix Bitbucket Cli - Configuration')
        self.window.mainloop()
        exit(0)

        # old way of geting things from the cli
        print('')
        username = input('Enter your Bitbucket user name (This is not your email! You can get it from "personal settings" -> "account settings"): ')
        password =(stdiomask.getpass (prompt='Bitbucket App password (You can get/generate it in "personal settings" -> "app passwords"): '))


    def _test_config(self):
        # check config
        username=self.txt_fld_bb_user.get()
        password=self.txt_fld_bb_pw.get()

        try:
            Client(username, password).get_user()
            self.lbl_bb_test_text.set('Looking good. :)')
            self.lbl_bb_test.config(fg='green')
        except(NotAuthenticatedError):
            self.lbl_bb_test_text.set('Your provided configuration is not valid, or connection broken.')
            self.lbl_bb_test.config(fg='red')

    def _save_config(self):
        # store the config
        username=self.txt_fld_bb_user.get()
        password=self.txt_fld_bb_pw.get()

        self.conf['bb_username'] = username
        self.conf.set_password('bb_password',  password)
        self.conf.write()
        self.window.destroy()
