from tkinter import *


def disableChildren(parent):
    for child in parent.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ('Frame', 'Labelframe'):
            child.configure(state='disable')
        else:
            disableChildren(child)


def enableChildren(parent):
    for child in parent.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ('Frame', 'Labelframe'):
            child.configure(state='normal')
        else:
            enableChildren(child)


def buildOuterLabelFrame(obj, root, label):
    return LabelFrame(root,
                      text=label,
                      bd=1,
                      highlightthickness=1,
                      highlightcolor=obj.ACTIVEFRAMEBORDER,
                      highlightbackground=obj.ACTIVEFRAMEBORDER,
                      bg=obj.ACTIVEBACKGROUND,
                      padx=5,
                      pady=10,
                      relief=FLAT,
                      foreground=obj.TEXTCOLOR)


def buildInnerLabelFrame(obj, root, label):
    return LabelFrame(root,
                      text=label,
                      bd=0,
                      highlightthickness=0,
                      bg=obj.ACTIVEBACKGROUND,
                      labelanchor=N,
                      padx=5,
                      foreground=obj.TEXTCOLOR)


def buildFunctionCheckButton(obj, root, variable, command):
    return Checkbutton(root,
                       variable=variable,
                       bg=obj.ACTIVEBACKGROUND,
                       bd=0,
                       activebackground=obj.ACTIVEBACKGROUND,
                       activeforeground=obj.ACTIVEFIELDBACKGROUND,
                       selectcolor=obj.ACTIVEFRAMEBORDER,
                       relief=FLAT,
                       highlightcolor=obj.ACTIVEBACKGROUND,
                       command=command)


def buildEntry(obj, root, textvariable, width=8):
    return Entry(root,
                 width=width,
                 justify=CENTER,
                 relief=FLAT,
                 textvariable=textvariable,
                 bg=obj.ACTIVEFIELDBACKGROUND,
                 foreground=obj.TEXTCOLOR,
                 disabledbackground=obj.INACTIVEFIELDBACKGROUND)


def buildFlagCheckButton(obj, root, variable):
    return Checkbutton(root,
                       variable=variable,
                       bg=obj.ACTIVEBACKGROUND,
                       bd=0,
                       activebackground=obj.ACTIVEBACKGROUND,
                       activeforeground=obj.ACTIVEFIELDBACKGROUND,
                       selectcolor=obj.ACTIVEFRAMEBORDER,
                       relief=FLAT,
                       highlightcolor=obj.ACTIVEBACKGROUND)


def roundPolygon(canvas, x, y, sharpness, **kwargs):
    if sharpness < 2:
        sharpness = 2

    ratioMultiplier = sharpness - 1
    ratioDividend = sharpness

    # Array to store the points
    points = []

    # Iterate over the x points
    for i in range(len(x)):
        # Set vertex
        points.append(x[i])
        points.append(y[i])

        # If it's not the last point
        if i != (len(x) - 1):
            # Insert submultiples points. The more the sharpness, the more these points will be
            # closer to the vertex.
            points.append((ratioMultiplier * x[i] + x[i + 1]) / ratioDividend)
            points.append((ratioMultiplier * y[i] + y[i + 1]) / ratioDividend)
            points.append((ratioMultiplier * x[i + 1] + x[i]) / ratioDividend)
            points.append((ratioMultiplier * y[i + 1] + y[i]) / ratioDividend)
        else:
            # Insert submultiples points.
            points.append((ratioMultiplier * x[i] + x[0]) / ratioDividend)
            points.append((ratioMultiplier * y[i] + y[0]) / ratioDividend)
            points.append((ratioMultiplier * x[0] + x[i]) / ratioDividend)
            points.append((ratioMultiplier * y[0] + y[i]) / ratioDividend)
            # Close the polygon
            points.append(x[0])
            points.append(y[0])

    return canvas.create_polygon(points, **kwargs, smooth=TRUE)


def rounded_rect(canvas, x, y, w, h, c):
    canvas.create_arc(x,
                      y,
                      x + 2 * c,
                      y + 2 * c,
                      start=90,
                      extent=90,
                      style="arc")
    canvas.create_arc(x + w - 2 * c,
                      y + h - 2 * c,
                      x + w,
                      y + h,
                      start=270,
                      extent=90,
                      style="arc")
    canvas.create_arc(x + w - 2 * c,
                      y,
                      x + w,
                      y + 2 * c,
                      start=0,
                      extent=90,
                      style="arc")
    canvas.create_arc(x,
                      y + h - 2 * c,
                      x + 2 * c,
                      y + h,
                      start=180,
                      extent=90,
                      style="arc")
    canvas.create_line(x + c, y, x + w - c, y)
    canvas.create_line(x + c, y + h, x + w - c, y + h)
    canvas.create_line(x, y + c, x, y + h - c)
    canvas.create_line(x + w, y + c, x + w, y + h - c)
