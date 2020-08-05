#!/usr/bin/env python

import re
import os
import sys
import Pmw
import tkinter as tk
from argparse import ArgumentParser

#NOTE: User global variable
process = ""
compiler = ""
word = ""
bit = ""
bytewrite = ""
instance = ""
pvt = ""


class ApplicationClass(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.master.title('Memory Query')
        self.master.geometry('800x600')
        self.master.configure(bg='grey')

        #NOTE: GUI menu
        self.menu = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(menu=self.filemenu, label='File')
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.master.quit)
        self.master.config(menu=self.menu)

        #NOTE: [1] Compiler selection
        self.sel_frame = tk.LabelFrame(self.master, text='1. Compiler Selection')
        self.sel_frame.grid(row=0, column=0)

        self.proc_dict = {
            'n5': ["n5_compiler 1", "n5_compiler 2"],
            'n7': ["n7_compiler 1", "n7_compiler 2"],
            'n12': ["n12_compiler 1", "n12_compiler 2"]
        }
        # self.proc_list = ("n5", "n7", "n12")
        # self.cmp_list = ("compiler 1", "compiler 2")

        ## set variable
        self.proc_var = tk.StringVar()
        self.cmp_var = tk.StringVar()

        ## trace variable when user select
        self.proc_var.trace_add('write', self.update_cmp_menu)
        # self.proc_var.trace_add('write', lambda *args: overwrite_var(self.proc_var.get(), process))
        # self.cmp_var.trace_add('write', lambda *args: overwrite_var(self.cmp_var.get(), compiler))

        ## place process/compiler label and option menu
        self.proc_label = tk.Label(self.sel_frame, text="Process: ")
        self.cmp_label = tk.Label(self.sel_frame, text="Compiler: ")
        self.proc_label.grid(row=0, column=0)
        self.cmp_label.grid(row=1, column=0)
        self.proc_opt = tk.OptionMenu(self.sel_frame, self.proc_var, *self.proc_dict.keys())
        self.cmp_opt = tk.OptionMenu(self.sel_frame, self.cmp_var, '')
        self.proc_opt.grid(row=0, column=1)
        self.cmp_opt.grid(row=1, column=1)

        ## set default value to option menu
        self.proc_var.set(list(self.proc_dict.keys())[0])
        # self.cmp_var.set(cmp_list[0])

        #NOTE: [2] Configuration
        self.cfg_frame = tk.LabelFrame(self.master, text='2. Configuration')
        self.cfg_frame.grid(row=0, column=1)

        self.word_label = tk.Label(self.cfg_frame, text="Word: ")
        self.word_label.grid(row=0, column=0)
        self.word_entry = tk.Entry(self.cfg_frame)
        self.word_entry.grid(row=0, column=1)

        self.bit_label = tk.Label(self.cfg_frame, text="Bit: ")
        self.bit_label.grid(row=1, column=0)
        self.bit_entry = tk.Entry(self.cfg_frame)
        self.bit_entry.grid(row=1, column=1)

        self.bw_list = ("0", "1")
        self.bw_var = tk.StringVar()
        self.bw_var.set(self.bw_list[0])
        self.bw_label = tk.Label(self.cfg_frame, text="Byte Write: ")
        self.bw_label.grid(row=2, column=0)
        self.bw_opt = tk.OptionMenu(self.cfg_frame, self.bw_var, *self.bw_list)
        self.bw_opt.grid(row=2, column=1)

        #NOTE: Click button to return user select instance
        self.cfg_submit = tk.Button(self.cfg_frame, text='Click', command=self.save_select)
        self.cfg_submit.grid(row=3)

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
        return (overwrite_var(self.proc_var.get(), process),
                overwrite_var(self.cmp_var.get(), compiler),
                overwrite_var(self.word_entry.get(), word),
                overwrite_var(self.bit_entry.get(), bit),
                overwrite_var(self.bw_var.get(), bytewrite))


def overwrite_var(selection, global_var):
    global_var = selection
    print(global_var)


def Application(window):
    window.title('Memory Query')
    window.geometry('800x600')
    window.configure(bg='grey')

    menu = tk.Menu(window)
    filemenu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(menu=filemenu, label='File')
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=window.quit)
    window.config(menu=menu)

    #TODO: [1] Compiler selection
    sel_frame = tk.LabelFrame(window, text='1. Compiler Selection')
    sel_frame.grid(row=0, column=0)

    proc_dict = {
        'n5': ["n5_compiler 1", "n5_compiler 2"],
        'n7': ["n7_compiler 1", "n7_compiler 2"],
        'n12': ["n12_compiler 1", "n12_compiler 2"]
    }

    proc_list = ("n5", "n7", "n12")
    cmp_list = ("compiler 1", "compiler 2")

    proc_var = tk.StringVar()
    cmp_var = tk.StringVar()

    def update_cmp_menu(*args):
        cmp_list = proc_dict[proc_var.get()]

    # proc_var.trace_add('write', update_cmp_menu)
    # proc_var.trace_add('write', lambda *args: print(proc_var.get()))
    proc_var.trace_add('write', lambda *args: overwrite_var(proc_var.get(), process))
    cmp_var.trace_add('write', lambda *args: overwrite_var(cmp_var.get(), compiler))

    proc_var.set(proc_list[1])
    # proc_var.set('Choose process')
    # cmp_var.set(cmp_list[0])
    cmp_var.set('Choose compiler')

    proc_label = tk.Label(sel_frame, text="Process: ")
    cmp_label = tk.Label(sel_frame, text="Compiler: ")
    proc_label.grid(row=0, column=0)
    cmp_label.grid(row=1, column=0)
    proc_opt = tk.OptionMenu(sel_frame, proc_var, *proc_list)
    cmp_opt = tk.OptionMenu(sel_frame, cmp_var, *cmp_list)
    proc_opt.grid(row=0, column=1)
    cmp_opt.grid(row=1, column=1)

    #TODO: [2] Configuration
    cfg_frame = tk.LabelFrame(window, text='2. Configuration')
    cfg_frame.grid(row=0, column=1)

    word_label = tk.Label(cfg_frame, text="Word: ")
    word_label.grid(row=0, column=0)
    word_entry = tk.Entry(cfg_frame)
    word_entry.grid(row=0, column=1)

    bit_label = tk.Label(cfg_frame, text="Bit: ")
    bit_label.grid(row=1, column=0)
    bit_entry = tk.Entry(cfg_frame)
    bit_entry.grid(row=1, column=1)

    bw_list = ("0", "1")
    bw_var = tk.StringVar()
    # bw_var.trace_add('write', lambda *args: overwrite_var(bw_var.get(), bytewrite))
    bw_var.set(bw_list[0])
    bw_label = tk.Label(cfg_frame, text="Byte Write: ")
    bw_label.grid(row=2, column=0)
    bw_opt = tk.OptionMenu(cfg_frame, bw_var, *bw_list)
    bw_opt.grid(row=2, column=1)

    def save_cfg():
        return (overwrite_var(word_entry.get(), word),
                 overwrite_var(bit_entry.get(), bit),
                 overwrite_var(bw_var.get(), bytewrite))

    cfg_submit = tk.Button(cfg_frame, text='Click', command=save_cfg)
    cfg_submit.grid(row=3)

    # print("Waiting ...")
    # proc_opt.wait_variable(proc_var)
    # print("Done waiting.")


if __name__ == '__main__':

    from time import time
    from datetime import datetime, timedelta

    start_time = time()
    datetime_now = datetime.now().strftime('%Y%m%d-%H%M%S')
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}")

    '''
    window = tk.Tk()
    Application(window)
    window.mainloop()
    '''
    # print(f'[DEBUG] global var = {process}, {compiler}, {word}, {bit}, {bytewrite}, {instance}, {pvt}')
    
    root = tk.Tk()
    # root.title('Memory Query')
    # root.geometry('800x600')
    # root.configure(bg='grey')
    ApplicationClass(root)
    root.mainloop()
    
    elapsed_time_secs = time() - start_time
    print(f"Runtime: %s (wall clock time)" % timedelta(seconds=elapsed_time_secs))
