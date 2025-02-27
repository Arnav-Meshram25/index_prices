import tkinter as tk
from tkinter import Listbox, Scrollbar, RIGHT, Y, END, Frame, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import io
import matplotlib.pyplot as plt

# Sample stock index data
data = """index_name,index_date,open_index_value,high_index_value,low_index_value,closing_index_value,points_change,change_percent,volume,turnover_rs_cr,pe_ratio,pb_ratio,div_yield
Nifty 50,2024-03-22,21932.20,22180.70,21883.30,22096.75,84.80,0.39,388656439,39023.19,22.81,3.87,1.21
Nifty Next 50,2024-03-22,58987.10,59326.25,58644.30,59188.90,270.60,0.46,239966115,10207.54,25.60,4.75,1.24
Nifty 100,2024-03-22,22476.70,22709.35,22414.50,22633.80,94.90,0.42,630024734,49320.98,23.48,4.04,1.19
Nifty 200,2024-03-22,12084.35,12204.85,12050.50,12168.75,54.25,0.45,1921544340,67660.17,23.64,4.00,1.15
Nifty 500,2024-03-22,19855.00,20048.60,19806.70,19994.60,97.20,0.49,2601583232,82714.83,24.25,4.02,1.11
Nifty Midcap 50,2024-03-22,13262.80,13357.75,13210.90,13329.95,24.55,0.18,699267974,9603.95,20.40,3.62,1.17"""

# Load data into Pandas DataFrame
df = pd.read_csv(io.StringIO(data))

# Color Scheme
BG_COLOR = "#000000"
TEXT_COLOR = "#FFFFFF"
ACCENT_COLOR = "#FFD700"
BAR_COLORS = ["#3498DB", "#E74C3C", "#F39C12", "#2ECC71"]
PANEL_BG = "#1C1C1C"

# Create main window
root = tk.Tk()
root.title("Stock Index Viewer")
root.geometry("1600x900")
root.configure(bg=BG_COLOR)

# Header
header_frame = Frame(root, bg=BG_COLOR)
header_frame.pack(fill="x")
title_label = Label(header_frame, text="Stock Index Insights", font=("Georgia", 36, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR)
title_label.pack(pady=(10, 0))
description_label = Label(header_frame, text="Explore indices", font=("Georgia", 18), fg=TEXT_COLOR, bg=BG_COLOR)
description_label.pack(pady=(0, 10))

# Sidebar
frame_left = Frame(root, bg=PANEL_BG, padx=12, pady=12)
frame_left.pack(side="left", fill="y")
listbox = Listbox(frame_left, font=("Segoe UI", 16), bg="#333", fg=TEXT_COLOR, selectbackground=ACCENT_COLOR, relief="flat", height=20)
listbox.pack(side="left", fill="y", padx=8, pady=8)
scrollbar = Scrollbar(frame_left, command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
index_names = df["index_name"].tolist()
for index in index_names:
    listbox.insert(END, index)

# Right Panel
frame_right = Frame(root, bg=BG_COLOR, padx=20, pady=20)
frame_right.pack(side="right", fill="y")

info_label = Label(frame_right, text="Index Details", font=("Georgia", 22, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR)
info_label.pack(pady=(10, 10))

info_text = tk.Text(frame_right, font=("Georgia", 16), bg=BG_COLOR, fg=TEXT_COLOR, bd=2, relief="solid", height=10, width=40)
info_text.pack(pady=(10, 20))

# Matplotlib Figure
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor(BG_COLOR)

def plot_data(event):
    try:
        selected_index = listbox.get(listbox.curselection())
        index_data = df[df["index_name"] == selected_index].iloc[0]
        ax.clear()
        
        labels = ["Open", "High", "Low", "Close"]
        values = [index_data["open_index_value"], index_data["high_index_value"], index_data["low_index_value"], index_data["closing_index_value"]]
        min_val = min(values) * 0.98
        max_val = max(values) * 1.02
        ax.set_ylim(min_val, max_val)

        bars = ax.bar(labels, values, color=BAR_COLORS, alpha=0.95, edgecolor="gold", linewidth=1.5)
        for bar in bars:
            bar.set_edgecolor('gold')
            bar.set_linewidth(2)
        
        ax.set_title(f"{selected_index} Index", fontsize=28, color=ACCENT_COLOR, pad=15, fontfamily="Georgia", fontweight="bold")
        ax.set_ylabel("Index Value", fontsize=18, color=TEXT_COLOR, fontfamily="Georgia", fontweight="bold")
        ax.set_facecolor(BG_COLOR)
        ax.grid(axis="y", linestyle="--", alpha=0.4, color=TEXT_COLOR)
        ax.spines["bottom"].set_color(TEXT_COLOR)
        ax.spines["left"].set_color(TEXT_COLOR)
        ax.tick_params(colors=TEXT_COLOR, labelsize=14)

        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, value, f"{value:,.2f}", ha="center", va="bottom", fontsize=16, fontweight="bold", color=TEXT_COLOR, fontfamily="Georgia", bbox=dict(facecolor='black', alpha=0.8, edgecolor="gold"))

        # Update right panel
        details = f"""Date: {index_data["index_date"]}
Volume: {index_data["volume"]:,}
Turnover (Cr): {index_data["turnover_rs_cr"]:,}
PE Ratio: {index_data["pe_ratio"]}
PB Ratio: {index_data["pb_ratio"]}
Dividend Yield: {index_data["div_yield"]}
Points Change: {index_data["points_change"]}
Change Percent: {index_data["change_percent"]}%"""

        info_text.config(state=tk.NORMAL)
        info_text.delete(1.0, tk.END)
        info_text.insert(tk.END, details)
        info_text.config(state=tk.DISABLED)

        canvas.draw()
    except tk.TclError:
        pass

listbox.bind("<<ListboxSelect>>", plot_data)

frame_graph = Frame(root, bg=BG_COLOR, padx=0, pady=0)
frame_graph.pack(side="right", fill="both", expand=True)

canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root.mainloop()
