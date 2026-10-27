import tkinter as tk
from tkinter import scrolledtext
import re

BG = "#d9d9d9"

def copiar(txt):
    root.clipboard_clear()
    root.clipboard_append(txt)
    status.config(text=f"Copiado: {txt}")

def processar():
    for w in frame_results.winfo_children():
        w.destroy()
    texto = entrada.get("1.0", tk.END)
    linhas = re.findall(r'transfer\s+\d+\s+to\s+.+', texto, re.IGNORECASE)

    if not linhas:
        tk.Label(frame_results,text="Nenhum transfer encontrado.",font=("Arial",10,"bold")).pack(pady=5)
        return

    for linha in linhas:
        linha = linha.strip()
        row = tk.Frame(frame_results,bg=BG)
        row.pack(fill="x", pady=6)

        caixa = tk.Entry(row,font=("Arial",12,"bold"),bd=3,relief="solid")
        caixa.insert(0, linha)
        caixa.pack(side="left",fill="x",expand=True,padx=(0,10),ipady=8)

        tk.Button(row,text="COPY",font=("Arial",12,"bold"),
                  command=lambda t=linha: copiar(t),
                  bd=3,relief="solid").pack(side="right")

def copy_all():
    texto = entrada.get("1.0", tk.END)
    linhas = re.findall(r'transfer\s+\d+\s+to\s+.+', texto, re.IGNORECASE)
    if linhas:
        root.clipboard_clear()
        root.clipboard_append("\n".join([x.strip() for x in linhas]))
        status.config(text="COPY ALL realizado.")

root = tk.Tk()
root.title("Loot Splitter")
root.geometry("850x650")
root.configure(bg=BG)

tk.Label(root,text="SPLITTER LOOT",font=("Arial",24,"bold"),bg=BG).pack(pady=15)

frame_results = tk.Frame(root,bg=BG)
frame_results.pack(fill="x",padx=25,pady=10)

btnframe = tk.Frame(root,bg=BG)
btnframe.pack(pady=8)

tk.Button(btnframe,text="LOOT",font=("Arial",16,"bold"),command=processar,bd=4,relief="solid").pack(side="left",padx=10)
tk.Button(btnframe,text="COPY ALL",font=("Arial",16,"bold"),command=copy_all,bd=4,relief="solid").pack(side="left",padx=10)

tk.Label(root,text="PASTE COPY LOOT",font=("Arial",18,"bold"),bg=BG).pack()

entrada = scrolledtext.ScrolledText(root,height=14,font=("Consolas",12),bd=4,relief="solid")
entrada.pack(fill="both",expand=True,padx=25,pady=10)
entrada.bind("<Control-v>", lambda e: root.after(150, processar))

status = tk.Label(root,text="",bg=BG,font=("Arial",10,"italic"))
status.pack(pady=5)

root.mainloop()
