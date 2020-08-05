#!/usr/bin/env python

import re
import os
import sys
import Pmw
import tkinter as tk
# from argparse import ArgumentParser


class msg:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    DEBUG = '\033[38;5;228m'
    TRACE = '\033[38;5;249m'
    FATAL = '\033[95m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    info = f'{BOLD}[INFO]{ENDC}'
    ok = f'{BOLD}{OKGREEN}[PASS]{ENDC}'
    warn = f'{BOLD}{WARNING}[WARN]{ENDC}'
    error = f'{BOLD}{FAIL}[ERROR]{ENDC}'
    debug = f'{BOLD}{DEBUG}[DEBUG]{ENDC}'
    trace = f'{BOLD}{TRACE}[TRACE]{ENDC}'

    def disable(self):
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.DEBUG = ''
        self.TRACE = ''
        self.FATAL = ''
        self.ENDC = ''
        self.BOLD = ''
        self.UNDERLINE = ''
# print(msg.info, msg.ok, msg.warn, msg.error, msg.debug, msg.trace)


class Application(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.master.title('Memory Query')
        self.master.geometry('640x480')
        self.master.resizable(width=0, height=0)
        # self.master.configure(bg='grey')

        #NOTE: GUI menu
        self.menu = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(menu=self.filemenu, label='File')
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.master.quit)
        self.master.config(menu=self.menu)

        #NOTE: Memory information
        self.process = ""
        self.compiler = ""
        self.word = ""
        self.bit = ""
        self.bytewrite = ""
        self.instance = ""
        self.pvt = ""
        self.bigdata = ""
        self.proc_dict = {
            'n5': ["n5compilerA", "n5compilerB"],
            'n7': ["n7compilerA", "n7compilerB"]
        }
        self.pvt_dict = dict()
        self.pvt_dict = {
            'n5compilerA_2KX4_B256M8': ['pvt1', 'pvt2'],
            'n5compilerA_2KX4_B512M8': ['pvt1', 'pvt2']
        }

        #NOTE: [1] Compiler selection frame
        self.sel_frame = tk.LabelFrame(self.master, text='1. Compiler Selection')
        self.sel_frame.grid(row=0, column=0, sticky='NW')

        self.proc_var = tk.StringVar()        
        self.proc_label = tk.Label(self.sel_frame, text="Process: ")
        self.proc_label.grid(row=0, column=0, sticky='E')
        self.proc_opt = tk.OptionMenu(self.sel_frame, self.proc_var, *self.proc_dict.keys())
        self.proc_opt.grid(row=0, column=1, sticky='W')

        self.cmp_var = tk.StringVar()
        self.cmp_label = tk.Label(self.sel_frame, text="Compiler: ")
        self.cmp_label.grid(row=1, column=0, sticky='E')
        self.cmp_opt = tk.OptionMenu(self.sel_frame, self.cmp_var, '')
        self.cmp_opt.grid(row=1, column=1, sticky='W')

        #NOTE: [2] Configuration frame
        self.cfg_frame = tk.LabelFrame(self.master, text='2. Configuration')
        self.cfg_frame.grid(row=0, column=1, sticky='NW')

        self.word_label = tk.Label(self.cfg_frame, text="Word: ")
        self.word_label.grid(row=0, column=0, sticky='E')
        self.word_entry = tk.Entry(self.cfg_frame)
        self.word_entry.grid(row=0, column=1, sticky='W')

        self.bit_label = tk.Label(self.cfg_frame, text="Bit: ")
        self.bit_label.grid(row=1, column=0, sticky='E')
        self.bit_entry = tk.Entry(self.cfg_frame)
        self.bit_entry.grid(row=1, column=1, sticky='W')

        self.bw_list = ("0", "1")
        self.bw_var = tk.StringVar()
        self.bw_var.set(self.bw_list[0])
        self.bw_label = tk.Label(self.cfg_frame, text="Byte Write: ")
        self.bw_label.grid(row=2, column=0, sticky='E')
        self.bw_opt = tk.OptionMenu(self.cfg_frame, self.bw_var, *self.bw_list)
        self.bw_opt.grid(row=2, column=1)

        #NOTE: Click button frame
        self.click_frame = tk.LabelFrame(self.master, text='')
        self.click_frame.grid(row=2, column=0, columnspan=2)
        self.cfg_submit = tk.Button(self.click_frame, text='Click', command=self.save_select, borderwidth=3)
        self.cfg_submit.grid(row=0, column=0, columnspan=2)

        ## set default process to option menu
        default_proc = list(self.proc_dict.keys())[0]
        default_compiler = list(self.proc_dict[default_proc])[0]
        self.proc_var.set(default_proc)
        self.cmp_var.set(default_compiler)
        ## trace process variable when user select
        self.proc_var.trace_add('write', self.update_cmp_menu)

        # print("Waiting ...")
        # self.proc_opt.wait_variable(self.proc_var)
        # print("Done waiting.")

    def update_cmp_menu(self, *args):
        """
        Based on process selection to update compiler list
        ref: https://stackoverflow.com/questions/17252096/change-optionmenu-based-on-what-is-selected-in-another-optionmenu
        """
        cmp_list = self.proc_dict[self.proc_var.get()]
        self.cmp_var.set(cmp_list[0])
        menu = self.cmp_opt['menu']
        menu.delete(0, 'end')
        for cmp in cmp_list:
            menu.add_command(label=cmp, command=lambda nation=cmp: self.cmp_var.set(nation))

    def save_select(self):
        return (overwrite_var(self.proc_var.get(), self.process),
                overwrite_var(self.cmp_var.get(), self.compiler),
                overwrite_var(self.word_entry.get(), self.word),
                overwrite_var(self.bit_entry.get(), self.bit),
                overwrite_var(self.bw_var.get(), self.bytewrite))


def overwrite_var(selection, global_var):
    global_var = selection
    print(global_var)


if __name__ == '__main__':

    from time import time
    from datetime import datetime, timedelta

    start_time = time()
    datetime_now = datetime.now().strftime('%Y%m%d-%H%M%S')
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}")

    root = tk.Tk()
    Application(root)
    root.mainloop()
    
    elapsed_time_secs = time() - start_time
    print(f"Runtime: %s (wall clock time)" % timedelta(seconds=elapsed_time_secs))
