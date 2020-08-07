#!/usr/bin/env python

import re
import os
import sys
import json
# import Pmw
import tkinter as tk
import tkinter.font as tkFont
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


def load_json(control_json):
    with open(control_json) as f:
        menu = json.load(f)
    return menu


class Application(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.master.title('Memory PPA Query')
        self.master.geometry('1024x768')
        self.master.minsize(640, 768)
        # self.master.resizable(width=0, height=0)
        # self.master.configure(bg='grey')

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(4, weight=1)

        self.title_font_stype = tkFont.Font(family= 'Ubuntu Light', size=14, weight='bold')
        self.frame_font_stype = tkFont.Font(family= 'Ubuntu Light', size=12, weight='normal')
        self.label_font_stype = tkFont.Font(family= 'Ubuntu Light', size=10, weight='normal')

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

        self.menu_dict = self.load_proc_cmp_menu()
        self.proc_cmp_dict = dict()
        self.update_proc_cmp_dict(self.menu_dict)
        self.inst_pvt_dict = dict()
        self.pvt_list = ""

        #NOTE: --- Draw the GUI interface
        self.title_frame = tk.Label(self.master, text='Memory PPA Query', font=self.title_font_stype)
        self.title_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        #NOTE: [1] Selection : Compiler selection frame
        self.sel_frame = tk.LabelFrame(self.master, text='1. Compiler Selection', font=self.frame_font_stype)
        self.sel_frame.grid(row=1, column=0, sticky='NEWS')

        #NOTE: [1-1] Process option menu
        self.proc_var = tk.StringVar()
        self.proc_label = tk.Label(self.sel_frame, text="Process: ", font=self.label_font_stype)
        self.proc_label.grid(row=0, column=0, padx=5, pady=0, sticky='E')
        self.proc_opt = tk.OptionMenu(self.sel_frame, self.proc_var, *self.menu_dict.keys())
        self.proc_opt.grid(row=0, column=1, padx=5, pady=0, sticky='W')

        #NOTE: [1-2] Compiler option menu
        self.cmp_var = tk.StringVar()
        self.cmp_label = tk.Label(self.sel_frame, text="Compiler: ", font=self.label_font_stype)
        self.cmp_label.grid(row=1, column=0, padx=5, pady=0, sticky='E')
        self.cmp_opt = tk.OptionMenu(self.sel_frame, self.cmp_var, '')
        self.cmp_opt.grid(row=1, column=1, padx=5, pady=0, sticky='W')

        #NOTE: [2] Selection : Configuration frame
        self.cfg_frame = tk.LabelFrame(self.master, text='2. Configuration', font=self.frame_font_stype)
        self.cfg_frame.grid(row=1, column=1, sticky='NEWS')

        self.word_label = tk.Label(self.cfg_frame, text="Word: ", font=self.label_font_stype)
        self.word_label.grid(row=0, column=0, padx=5, pady=0, sticky='E')
        self.word_entry = tk.Entry(self.cfg_frame)
        self.word_entry.grid(row=0, column=1, padx=5, pady=0, sticky='W')

        self.bit_label = tk.Label(self.cfg_frame, text="Bit: ", font=self.label_font_stype)
        self.bit_label.grid(row=1, column=0, padx=5, pady=0, sticky='E')
        self.bit_entry = tk.Entry(self.cfg_frame)
        self.bit_entry.grid(row=1, column=1, padx=5, pady=0, sticky='W')

        self.bw_list = ("0", "1")
        self.bw_var = tk.StringVar()
        self.bw_var.set(self.bw_list[0])
        self.bw_label = tk.Label(self.cfg_frame, text="Byte Write: ", font=self.label_font_stype)
        self.bw_label.grid(row=2, column=0, padx=5, pady=0, sticky='E')
        self.bw_opt = tk.OptionMenu(self.cfg_frame, self.bw_var, *self.bw_list)
        self.bw_opt.grid(row=2, column=1, padx=5, pady=0, sticky='W')

        #NOTE: Click button frame -> return instance from database
        self.click_frame = tk.LabelFrame(self.master, text='3. Select Instance', font=self.frame_font_stype)
        self.click_frame.grid(row=2, column=0, columnspan=2, sticky='NEWS')
        self.click_submit = tk.Button(self.click_frame,
                                           text='Click',
                                           command=self.query_instance,
                                           borderwidth=3,
                                           font=self.label_font_stype)
        self.click_submit.pack(side='top', fill='x')

        #NOTE: [3] Preview : Instance frame
        self.prev_frame = tk.LabelFrame(self.master, text='4. Preview Instance', font=self.frame_font_stype)
        self.prev_frame.grid(row=3, column=0, sticky='NEWS')

        #NOTE: [3-1] Instance list
        self.inst_var = tk.StringVar()
        self.inst_label = tk.Label(self.prev_frame, text="    Selected Instance: ", font=self.label_font_stype)
        self.inst_label.grid(row=0, column=0, padx=5, pady=0, sticky='W')
        self.inst_opt = tk.Radiobutton(self.prev_frame, variable=self.inst_var, text='', value='')
        self.inst_opt.grid(row=1, column=0, padx=5, pady=0, sticky='W')

        #NOTE: [4] Preview : PVT selection frame
        self.pvt_frame = tk.LabelFrame(self.master, text='5. PVT', font=self.frame_font_stype)
        self.pvt_frame.grid(row=3, column=1, sticky='NEWS')

        #NOTE: [4-1] PVT list
        self.pvt_var = tk.StringVar()
        self.pvt_label = tk.Label(self.pvt_frame, text="PVT List: ", font=self.label_font_stype)
        self.pvt_label.pack(side='left')
        self.pvt_entry = tk.Entry(self.pvt_frame, textvariable=self.pvt_var, width=10)
        self.pvt_entry.pack(side='top', fill='x')
        self.pvt_scrollbar = tk.Scrollbar(self.pvt_frame)
        self.pvt_scrollbar.pack(side='right', fill='y')
        self.pvt_listbox = tk.Listbox(self.pvt_frame, yscrollcommand=self.pvt_scrollbar.set)
        self.pvt_listbox.pack(side='top', fill='both')
        self.pvt_scrollbar.config(command=self.pvt_listbox.yview)

        #NOTE: [5] PPA : timing frame
        self.timing_frame = tk.LabelFrame(self.master, text='6. Timing', font=self.frame_font_stype)
        self.timing_frame.grid(row=4, column=0, sticky='NEWS')
        self.timing_label = tk.Label(self.timing_frame, text="Timing: ")
        self.timing_label.grid(row=0, column=0, sticky='W')

        #NOTE: [6] PPA : power frame
        self.power_frame = tk.LabelFrame(self.master, text='7. Power', font=self.frame_font_stype)
        self.power_frame.grid(row=4, column=1, sticky='NEWS')
        self.power_label = tk.Label(self.power_frame, text='Power: ')
        self.power_label.grid(row=0, column=0, sticky='W')

        #NOTE: --- Set default value, and trace user selection
        ## set default value
        default_proc = list(self.proc_cmp_dict.keys())[0]
        self.proc_var.set(default_proc)
        default_compiler = list(self.proc_cmp_dict[default_proc])[0]
        self.cmp_var.set(default_compiler)

        ## trace value by user select
        self.proc_var.trace_add('write', self.update_cmp_menu)
        self.inst_var.trace_add('write', self.update_pvt_menu)
        self.pvt_listbox.bind("<<ListboxSelect>>", self.query_ppa)

        ### ----------------------------------------------------------------- ###
        # TODO: Waiting
        # print("Waiting ...")
        # self.proc_opt.wait_variable(self.proc_var)
        # print("Done waiting.")
        ### ----------------------------------------------------------------- ###

    def load_proc_cmp_menu(self, *args):
        control_json = 'menu.json'
        menu_dict = load_json(control_json)
        return menu_dict

    def update_proc_cmp_dict(self, menu, *args):
        """
        Load compiler list to list, and update to dictionary
        """
        for process in menu.keys():
            cmplist_path = menu[process]['cmp_list']
            with open(cmplist_path, 'r') as f:
                cmp_list = [cmp for cmp in map(str.strip, f)]
            self.proc_cmp_dict[process] = cmp_list

    def remove_instance_radiobutton(self, *args):
        ## Remove original radiobutton
        ## https://stackoverflow.com/questions/23189610/remove-widgets-from-grid-in-tkinter
        self.instance = ""
        for radio_opt in self.prev_frame.grid_slaves():
            if int(radio_opt.grid_info()["row"]) > 0:
                radio_opt.grid_forget()

    def create_instance_radiobutton(self, inst_list, *args):
        ## Create selected instance radiobutton
        for num, inst in enumerate(inst_list):
            self.inst_opt = tk.Radiobutton(self.prev_frame, variable=self.inst_var, text=inst, value=inst)
            self.inst_opt.grid(row=num+1, column=0, sticky='W')

    def query_instance(self, *args):
        """
        Click button to query memory instance and create radiobutton
        """
        self.remove_instance_radiobutton()
        self.process = self.proc_var.get()
        self.compiler = self.cmp_var.get()
        self.word = self.word_entry.get()
        self.bit = self.bit_entry.get()
        self.bytewrite = self.bw_var.get()
        # HACK: hacking bigdata path (input: process)        
        self.bigdata = 'bigdata path'
        # HACK: hacking instance list (input: compiler, word, bit)
        if self.process == 'n5' and self.compiler == 'n5compilerA':
            self.instance = ["n5compilerA_2KX4_B256M8", "n5compilerA_2KX4_B512M8", "n5compilerA_2KX4_B64M4"]
        elif self.process == 'n7' and self.compiler == 'n7compilerA':
            self.instance = ["n7compilerA_2KX4_B256M8", "n7compilerA_2KX4_B512M8"]
        self.create_instance_radiobutton(self.instance)

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
        #HACK: hacking pvt list
        inst = self.inst_var.get()
        self.inst_pvt_dict[inst] = ["pvvt1", "pvvt2"]
        print(f'{msg.debug} selece instance {self.inst_var.get()} -> {self.inst_pvt_dict[self.inst_var.get()]}')
        pvt_list = self.inst_pvt_dict[inst]
        self.pvt_listbox.delete(0, 'end')
        for pvt in pvt_list:
            self.pvt_listbox.insert("end", pvt)
        self.pvt_list = pvt_list

    def query_ppa(self, *args):
        inst = self.inst_var.get()
        pvt_idx_tuple = self.pvt_listbox.curselection()
        pvt = [self.pvt_list[int(pvt_idx)] for pvt_idx in pvt_idx_tuple][0]
        print(f'{msg.debug} query PPA: instance = {inst}, pvt = {pvt}')


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
