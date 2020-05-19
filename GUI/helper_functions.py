from tkinter import *


def disableChildren(parent):
    for child in parent.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ('Frame','Labelframe'):
            child.configure(state='disable')
        else:
            disableChildren(child)

def enableChildren(parent):
    for child in parent.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ('Frame','Labelframe'):
            child.configure(state='normal')
        else:
            enableChildren(child)

def buildOuterLabelFrame(obj, root, label):
    return LabelFrame(root, text=label, bd=1, highlightthickness=1,
                      highlightcolor=obj.ACTIVEFRAMEBORDER,
                      highlightbackground=obj.ACTIVEFRAMEBORDER, bg=obj.ACTIVEBACKGROUND,
                      padx=5, relief=FLAT, foreground=obj.TEXTCOLOR)

def buildInnerLabelFrame(obj, root, label):
    return LabelFrame(root, text=label,
                      bd=0, highlightthickness=0, bg=obj.ACTIVEBACKGROUND,
                      labelanchor=N, padx=5, pady=5, foreground=obj.TEXTCOLOR)

def buildFunctionCheckButton(obj, root, variable, command):
    return Checkbutton(root, variable=variable,
                       bg=obj.ACTIVEBACKGROUND, bd=0, activebackground=obj.ACTIVEBACKGROUND,
                       activeforeground=obj.ACTIVEFIELDBACKGROUND, selectcolor=obj.ACTIVEFRAMEBORDER,
                       relief=FLAT, highlightcolor=obj.ACTIVEBACKGROUND, command=command)

def buildEntry(obj, root, textvariable, width=3):
    return Entry(root, width=width, justify=CENTER, relief=FLAT,
                 textvariable=textvariable, bg=obj.ACTIVEFIELDBACKGROUND, 
                 foreground=obj.TEXTCOLOR, disabledbackground=obj.INACTIVEFIELDBACKGROUND)

def buildFlagCheckButton(obj, root, variable):
    return Checkbutton(root, variable=variable,
                       bg=obj.ACTIVEBACKGROUND, bd=0, activebackground=obj.ACTIVEBACKGROUND,
                       activeforeground=obj.ACTIVEFIELDBACKGROUND, selectcolor=obj.ACTIVEFRAMEBORDER,
                       relief=FLAT, highlightcolor=obj.ACTIVEBACKGROUND)
