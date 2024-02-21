import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import h5py, os
from numpy import array, savetxt

VERSION="1.1"

def button_single_click():
    filename = filedialog.askopenfilename()
    input_var.set(filename)
    update_label()

def get_files(dir, ext):
    files = os.listdir(dir)
    return list(filter(lambda f:f.endswith(ext), files))

def button_multi_click():
    dirname = filedialog.askdirectory()
    input_var.set(dirname)
    update_label()

def profile_selection(event):
    selected_option = profile_var.get()

def convert_click():

    input = input_var.get()
    output = filedialog.askdirectory()


    if os.path.isdir(output):
        if os.path.isfile(input) and input.endswith('.mat'):
            convert_single(input, output)

        elif os.path.isdir(input):
            convert_multiple(input, output)

        else:
            notify_input_error()


def convert_single(input, output):
    convert_and_save(input, output)



def convert_multiple(dir, output):
    files = get_files(dir, '.mat')
    if len(files)<=0:
        notify_mat_not_found()
    else:
        for file in files:
            convert_and_save(dir + '/' + file, output)

def convert_and_save(input, output):
    notify_convert_start()
    print('Convert and save: %s' % input)
    outfile = input.split('/')[-1].replace('.mat','.txt')
    outpath = output + '/' + outfile
    print('Outfile: %s' % outpath)
    f = h5py.File(input)
    key_list = PROFILES[profile_var.get()].split('/')
    for k in key_list:
        f = f[k]
    arr = array(f)[0]
    print(arr)
    savetxt(outpath, arr, fmt='%.6f')
    notify_convert_done()




def get_profile_dict():
    f = open('keys.config','r')
    lines = f.read().splitlines()
    return dict([e.split(' ') for e in lines])

def update_label():
    if input_var.get() in [None, '']:
        label_var.set('No input selected!')
    else:
        label_var.set('Input: %s' % input_var.get())

def notify_input_error():
    label_var.set('Input error!')

def notify_mat_not_found():
    label_var.set('No .mat files found in %s' % input_var.get())

def notify_convert_start():
    label_var.set('Converting...')

def notify_convert_done():
    label_var.set('Converted!')

# Create the main window
root = tk.Tk()
root.title("Mat2Txt - v%s" % VERSION)

# Create variables
PROFILES = get_profile_dict()
options = list(get_profile_dict().keys())
input_var = tk.StringVar()
label_var = tk.StringVar()
profile_var = tk.StringVar()
profile_var.set(options[0])

p = tk.StringVar()
p.set("Profile: ")

# Create buttons
button_single = tk.Button(root, text="Load single MAT", command=button_single_click)
button_multi  = tk.Button(root, text="Load directory of MATs", command=button_multi_click)

# Create profile list
profile_label = tk.Label(root, textvariable=p)
profile = ttk.Combobox(root, values=options, textvariable=profile_var)
profile.bind("<<ComboboxSelected>>", profile_selection)

# Create text label
label = tk.Label(root, textvariable=label_var)

# Create another button
button3 = tk.Button(root, text="Convert to...", command=convert_click)

# Place widgets in the grid
button_single.grid(row=0, column=0, padx=5, pady=5)
button_multi.grid(row=0, column=1, padx=5, pady=5)
label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
profile_label.grid(row=2, column=0, padx=5, pady=5)
profile.grid(row=2, column=1,padx=5 , pady=5)
button3.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Start the Tkinter event loop
update_label()
root.mainloop()
