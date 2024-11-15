import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import ttk
import colorsys


def rgb_to_cmyk(r, g, b):
    r_prime, g_prime, b_prime = r / 255.0, g / 255.0, b / 255.0
    k = 1 - max(r_prime, g_prime, b_prime)
    if k < 1:
        c = (1 - r_prime - k) / (1 - k)
        m = (1 - g_prime - k) / (1 - k)
        y = (1 - b_prime - k) / (1 - k)
    else:
        c = m = y = 0
    return round(c * 100, 2), round(m * 100, 2), round(y * 100, 2), round(k * 100, 2)


def cmyk_to_rgb(c, m, y, k):
    c_prime, m_prime, y_prime, k_prime = c / 100.0, m / 100.0, y / 100.0, k / 100.0
    r = 255 * (1 - c_prime) * (1 - k_prime)
    g = 255 * (1 - m_prime) * (1 - k_prime)
    b = 255 * (1 - y_prime) * (1 - k_prime)
    return round(r), round(g), round(b)


def update_color():
    global is_updating
    if is_updating:
        return
    is_updating = True
    update_cmyk_from_rgb()
    update_hls_from_rgb()
    r, g, b = round(float(r_var.get())), round(float(g_var.get())), round(float(b_var.get()))
    color_label.config(bg=f"#{r:02x}{g:02x}{b:02x}")
    is_updating = False


def update_from_cmyk():
    global is_updating
    if is_updating:
        return
    is_updating = True
    update_rgb_from_cmyk()
    update_hls_from_rgb()
    r, g, b = round(float(r_var.get())), round(float(g_var.get())), round(float(b_var.get()))
    color_label.config(bg=f"#{r:02x}{g:02x}{b:02x}")
    is_updating = False


def choose_color():
    color = askcolor()[0]
    if color:
        r_var.set(f"{color[0]:.2f}")
        g_var.set(f"{color[1]:.2f}")
        b_var.set(f"{color[2]:.2f}")
        update_color()


def update_from_hls():
    global is_updating
    if is_updating:
        return
    is_updating = True
    h, l, s = float(h_var.get()), float(l_var.get()), float(s_var.get())
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l / 100.0, s / 100.0)
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    r_var.set(f"{r:.2f}")
    g_var.set(f"{g:.2f}")
    b_var.set(f"{b:.2f}")
    update_cmyk_from_rgb()
    color_label.config(bg=f"#{r:02x}{g:02x}{b:02x}")
    is_updating = False


def update_cmyk_from_rgb():
    r, g, b = round(float(r_var.get())), round(float(g_var.get())), round(float(b_var.get()))
    c, m, y, k = rgb_to_cmyk(r, g, b)
    c_var.set(f"{c:.2f}")
    m_var.set(f"{m:.2f}")
    y_var.set(f"{y:.2f}")
    k_var.set(f"{k:.2f}")


def update_rgb_from_cmyk():
    c, m, y, k = float(c_var.get()), float(m_var.get()), float(y_var.get()), float(k_var.get())
    r, g, b = cmyk_to_rgb(c, m, y, k)
    r_var.set(f"{r:.2f}")
    g_var.set(f"{g:.2f}")
    b_var.set(f"{b:.2f}")


def update_hls_from_rgb():
    r, g, b = round(float(r_var.get())), round(float(g_var.get())), round(float(b_var.get()))
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    h_var.set(f"{h * 360:.2f}")
    l_var.set(f"{l * 100:.2f}")
    s_var.set(f"{s * 100:.2f}")


def create_entry(parent, variable, label_text, from_, to, update_func):
    frame = ttk.Frame(parent)
    frame.pack(pady=5, fill="x")
    validate_cmd = frame.register(lambda v: v.replace('.', '', 1).isdigit() and from_ <= float(v) <= to if v else True)

    label = ttk.Label(frame, text=label_text, width=5)
    label.pack(side="left")
    entry = ttk.Entry(frame, textvariable=variable, width=10, validate="key", validatecommand=(validate_cmd, '%P'))
    entry.pack(side="left", padx=5)
    entry.bind("<Return>", lambda e: update_func())
    slider = tk.Scale(
        frame, from_=from_, to=to, orient="horizontal", length=200, showvalue=False,
        resolution=0.01,
        variable=variable,
        command=lambda e: update_func(),
        sliderlength=5,
    )
    slider.pack(side="left", fill="x", expand=True)


root = tk.Tk()
root.title("Color Converter")
root.geometry("1000x800")

r_var = tk.StringVar(value="255.00")
g_var = tk.StringVar(value="255.00")
b_var = tk.StringVar(value="255.00")

c_var = tk.StringVar(value="0.00")
m_var = tk.StringVar(value="0.00")
y_var = tk.StringVar(value="0.00")
k_var = tk.StringVar(value="0.00")

h_var = tk.StringVar(value="0.00")
l_var = tk.StringVar(value="100.00")
s_var = tk.StringVar(value="100.00")

is_updating = False

tk.Label(root, text="RGB").pack(pady=5)
create_entry(root, r_var, "R:", 0, 255, update_color)
create_entry(root, g_var, "G:", 0, 255, update_color)
create_entry(root, b_var, "B:", 0, 255, update_color)

tk.Label(root, text="CMYK").pack(pady=5)
create_entry(root, c_var, "C:", 0, 100, update_from_cmyk)
create_entry(root, m_var, "M:", 0, 100, update_from_cmyk)
create_entry(root, y_var, "Y:", 0, 100, update_from_cmyk)
create_entry(root, k_var, "K:", 0, 100, update_from_cmyk)

tk.Label(root, text="HLS").pack(pady=5)
create_entry(root, h_var, "H:", 0, 360, update_from_hls)
create_entry(root, l_var, "L:", 0, 100, update_from_hls)
create_entry(root, s_var, "S:", 0, 100, update_from_hls)

tk.Button(root, text="Choose Color", command=choose_color).pack(pady=10)

color_label = tk.Label(root, text="Color Display", bg="white", width=80, height=20)
color_label.pack(pady=20)

root.mainloop()