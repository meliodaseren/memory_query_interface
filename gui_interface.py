#!/usr/bin/env python

import re
import os
import sys
import Pmw
import tkinter as tk
from argparse import ArgumentParser


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

        #NOTE: --- GUI menu
        self.menu = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(menu=self.filemenu, label='File')
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.master.quit)
        self.master.config(menu=self.menu)

        #NOTE: --- Memory information
        self.process = ""
        self.compiler = ""
        self.word = ""
        self.bit = ""
        self.bytewrite = ""
        self.instance = ""
        self.pvt = ""
        self.bigdata = ""
        self.proc_cmp_dict = {
            'n5': ["n5compilerA", "n5compilerB"],
            'n7': ["n7compilerA", "n7compilerB"]
        }
        self.inst_pvt_dict = dict()


        #NOTE: --- Draw the GUI interface
        #NOTE: [1] Selection : Compiler selection frame
        self.sel_frame = tk.LabelFrame(self.master, text='1. Compiler Selection')
        self.sel_frame.grid(row=0, column=0, sticky='NW')

        self.proc_var = tk.StringVar()        
        self.proc_label = tk.Label(self.sel_frame, text="Process: ")
        self.proc_label.grid(row=0, column=0, padx=3, pady=3, sticky='E')
        self.proc_opt = tk.OptionMenu(self.sel_frame, self.proc_var, *self.proc_cmp_dict.keys())
        self.proc_opt.grid(row=0, column=1, sticky='W')

        self.cmp_var = tk.StringVar()
        self.cmp_label = tk.Label(self.sel_frame, text="Compiler: ")
        self.cmp_label.grid(row=1, column=0, padx=3, pady=3, sticky='E')
        self.cmp_opt = tk.OptionMenu(self.sel_frame, self.cmp_var, '')
        self.cmp_opt.grid(row=1, column=1, sticky='W')

        #NOTE: [2] Selection : Configuration frame
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

        #NOTE: Click button frame -> return instance from database
        self.click_frame = tk.LabelFrame(self.master, text='')
        self.click_frame.grid(row=2, column=0, columnspan=2)
        self.cfg_submit = tk.Button(self.click_frame, text='Click', command=self.query_instance, borderwidth=3)
        self.cfg_submit.grid(row=0, column=0, columnspan=2)

        #NOTE: [3] Preview : Instance frame
        self.prev_frame = tk.LabelFrame(self.master, text='3. Preview')
        self.prev_frame.grid(row=3, column=0, sticky='NW')

        self.inst_var = tk.StringVar()
        self.inst_label = tk.Label(self.prev_frame, text="    Selected Instance: ")
        self.inst_label.grid(row=0, column=0, sticky='W')
        self.inst_opt = tk.Radiobutton(self.prev_frame, variable=self.inst_var, text='', value='')
        self.inst_opt.grid(row=1, column=0, sticky='W')

        #NOTE: [4] Preview : PVT selection frame
        self.pvt_frame = tk.LabelFrame(self.master, text='4. PVT')
        self.pvt_frame.grid(row=3, column=1, sticky='NW')

        self.pvt_var = tk.StringVar()
        self.pvt_label = tk.Label(self.pvt_frame, text="PVT: ")
        self.pvt_label.grid(row=0, column=0, sticky='E')
        self.pvt_opt = tk.OptionMenu(self.pvt_frame, self.pvt_var, '')
        self.pvt_opt.grid(row=0, column=1, sticky='W')

        #NOTE: [5] PPA : timing frame
        self.timing_frame = tk.LabelFrame(self.master, text='Timing')
        self.timing_frame.grid(row=5, column=0, sticky='NW')

        #NOTE: [6] PPA : power frame
        self.power_frame = tk.LabelFrame(self.master, text='Power')
        self.power_frame.grid(row=5, column=1, sticky='NW')


        #NOTE: --- Set default value, and trace user selection
        ## set default value
        default_proc = list(self.proc_cmp_dict.keys())[0]
        self.proc_var.set(default_proc)
        default_compiler = list(self.proc_cmp_dict[default_proc])[0]
        self.cmp_var.set(default_compiler)

        ## After click button -> update instance list
        self.inst_pvt_dict = {
            'n5compilerA_2KX4_B256M8': ['pvt1', 'pvt2'],
            'n5compilerA_2KX4_B512M8': ['pvt3', 'pvt4'],
            'n5compilerA_2KX4_B64M4': ['pvt5', 'pvt6']
        }
        self.inst_list = list(self.inst_pvt_dict.keys())
        # self.inst_var.set(self.inst_list[0])
        # for num, inst in enumerate(self.inst_list):
        #     self.inst_opt = tk.Radiobutton(self.prev_frame,
        #                                         variable=self.inst_var,
        #                                         text=inst,
        #                                         value=inst)
        #     self.inst_opt.grid(row=num, column=1, sticky='W')

        # pvt_list = self.inst_pvt_dict[self.inst_var.get()]
        # self.pvt_var.set(pvt_list[0])
        
        ## trace value by user select
        self.proc_var.trace_add('write', self.update_cmp_menu)
        self.inst_var.trace_add('write', self.update_pvt_menu)

        ###
        # print("Waiting ...")
        # self.proc_opt.wait_variable(self.proc_var)
        # print("Done waiting.")
        ###


    def update_cmp_menu(self, *args):
        """
        Based on process selection to update compiler list
        ref: https://stackoverflow.com/questions/17252096/change-optionmenu-based-on-what-is-selected-in-another-optionmenu
        """
        cmp_list = self.proc_cmp_dict[self.proc_var.get()]
        self.cmp_var.set(cmp_list[0])
        menu = self.cmp_opt['menu']
        menu.delete(0, 'end')
        for cmp in cmp_list:
            menu.add_command(label=cmp, command=lambda nation=cmp: self.cmp_var.set(nation))

    def update_pvt_menu(self, *args):
        """
        Based on instance selection to update pvt list
        """
        pvt_list = self.inst_pvt_dict[self.inst_var.get()]
        self.pvt_var.set(pvt_list[0])
        menu = self.pvt_opt['menu']
        menu.delete(0, 'end')
        for pvt in pvt_list:
            menu.add_command(label=pvt, command=lambda nation=pvt: self.pvt_var.set(nation))

    def query_instance(self):
        self.process = self.proc_var.get()
        self.compiler = self.cmp_var.get()
        self.word = self.word_entry.get()
        self.bit = self.bit_entry.get()
        self.bytewrite = self.bw_var.get()
        self.bigdata = 'bigdata path'
        self.instance = ["n5compilerA", "n5compilerB"]
        # for inst in self.instance:
        #     self.inst_pvt_dict[inst] = ["pvvt1", "pvvt2"]
        #     print(f'{inst}\n    {self.inst_pvt_dict[inst]}')
        self.create_instance_radiobutton(self.instance)

    def create_instance_radiobutton(self, inst_list):
        ## Remove original radiobutton
        for radio_opt in self.prev_frame.grid_slaves():
            if int(radio_opt.grid_info()["row"]) > 0:
                radio_opt.grid_forget()
        ## Create selected instance radiobutton
        for num, inst in enumerate(self.inst_list):
            self.inst_opt = tk.Radiobutton(self.prev_frame, variable=self.inst_var, text=inst, value=inst)
            self.inst_opt.grid(row=num+1, column=0, sticky='W')


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
