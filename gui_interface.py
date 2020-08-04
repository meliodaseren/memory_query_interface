#!/usr/bin/env python3

import re
import os
import sys
import Pmw
import tkinter as tk
from argparse import ArgumentParser

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

    proc_list = ("n5", "n7", "n12")
    proc_var = tk.StringVar()
    proc_var.trace_add('write', lambda *args: print(proc_var.get()))
    proc_var.set(proc_list[0])
    proc_label = tk.Label(sel_frame, text="Process: ")
    proc_label.grid(row=0, column=0)
    proc_opt = tk.OptionMenu(sel_frame, proc_var, *proc_list)
    proc_opt.grid(row=0, column=1)
    
    cmp_list = ("compiler 1", "compiler 2")
    cmp_var = tk.StringVar()
    cmp_var.trace_add('write', lambda *args: print(cmp_var.get()))
    cmp_var.set(cmp_list[0])
    cmp_label = tk.Label(sel_frame, text="Compiler: ")
    cmp_label.grid(row=1, column=0)
    cmp_opt = tk.OptionMenu(sel_frame, cmp_var, *cmp_list)
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
    bw_var.trace_add('write', lambda *args: print(bw_var.get()))
    bw_var.set(bw_list[0])
    bw_label = tk.Label(cfg_frame, text="Byte Write: ")
    bw_label.grid(row=2, column=0)
    bw_opt = tk.OptionMenu(cfg_frame, bw_var, *bw_list)
    bw_opt.grid(row=2, column=1)


if __name__ == '__main__':

    from time import time
    from datetime import datetime, timedelta

    start_time = time()
    datetime_now = datetime.now().strftime('%Y%m%d-%H%M%S')
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}")

    window = tk.Tk()
    app = Application(window)
    window.mainloop()

    elapsed_time_secs = time() - start_time
    print(f"Runtime: %s (wall clock time)" % timedelta(seconds=elapsed_time_secs))
