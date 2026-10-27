import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import openpyxl
from openpyxl import Workbook
from datetime import datetime

def calcular_irrf(valor_frete):
    base_calculo = valor_frete * 0.10

    if base_calculo <= 2259.20:
        aliquota = 0.0
        deducao = 0.0
    elif base_calculo <= 2826.65:
        aliquota = 0.075
        deducao = 169.44
    elif base_calculo <= 3751.05:
        aliquota = 0.15
        deducao = 381.44
    elif base_calculo <= 4664.68:
        aliquota = 0.225
        deducao = 662.77
    else:
        aliquota = 0.275
        deducao = 896.0

    valor_irrf = (base_calculo * aliquota) - deducao
    return max(valor_irrf, 0.0), aliquota * 100  # garantir que o valor não seja negativo

def atualizar_aliquota_irrf(event):
    try:
        valor_frete = float(entry_valor_frete.get())
        valor_irrf, aliquota = calcular_irrf(valor_frete)
        entry_aliquota_irrf.config(state=tk.NORMAL)
        entry_aliquota_irrf.delete(0, tk.END)
        entry_aliquota_irrf.insert(0, f"{aliquota:.2f}")
        entry_aliquota_irrf.config(state=tk.DISABLED)
    except ValueError:
        entry_aliquota_irrf.config(state=tk.NORMAL)
        entry_aliquota_irrf.delete(0, tk.END)
        entry_aliquota_irrf.config(state=tk.DISABLED)

def calcular_imposto():
    try:
        titulo_frete = entry_titulo_frete.get()
        motorista = entry_motorista.get()
        cpf = entry_cpf.get()
        valor_frete = float(entry_valor_frete.get())
        
        # Alíquota INSS
        valor_inss = valor_frete * 0.11
        valor_inss = min(valor_inss, 856.46)

        # Alíquota INSS Patronal
        valor_inss_patronal = valor_frete * 0.20

        valor_irrf, _ = calcular_irrf(valor_frete)

        # Total de impostos
        total_impostos = valor_inss + valor_irrf + valor_inss_patronal
        
        # Exibir resultados na interface
        resultado = (
            f"Frete: {titulo_frete}\n"
            f"Motorista: {motorista} (CPF: {cpf})\n"
            f"INSS (11%): R$ {valor_inss:.2f}\n"
            f"IRRF: R$ {valor_irrf:.2f}\n"
            f"INSS Patronal (20%): R$ {valor_inss_patronal:.2f}\n"
            f"Total de impostos: R$ {total_impostos:.2f}"
        )
        label_resultado.config(text=resultado)

        # Salvar dados no Excel
        salvar_excel(titulo_frete, motorista, cpf, valor_frete, total_impostos)

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

def salvar_excel(titulo_frete, motorista, cpf, valor_frete, total_impostos):
    try:
        # Verificar se o arquivo Excel já existe ou criar um novo
        arquivo_excel = "dados_fretes.xlsx"
        try:
            wb = openpyxl.load_workbook(arquivo_excel)
        except FileNotFoundError:
            wb = Workbook()

        # Selecionar a planilha ativa (ou criar uma nova)
        if 'Fretes' in wb.sheetnames:
            ws = wb['Fretes']
        else:
            ws = wb.create_sheet(title='Fretes')

            # Adicionar cabeçalhos se a planilha for nova
            ws.append(['Rota do Frete', 'Data do Frete', 'Motorista', 'CPF', 'Valor do Frete', 'Total de Impostos'])

        # Obter a data atual
        data_frete = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Adicionar nova linha com os dados do frete calculado
        nova_linha = [titulo_frete, data_frete, motorista, cpf, valor_frete, total_impostos]
        ws.append(nova_linha)

        # Salvar o arquivo Excel
        wb.save(arquivo_excel)
        messagebox.showinfo("Sucesso", "Dados do frete salvos no Excel.")

    except Exception as e:
        messagebox.showerror("Erro ao Salvar", f"Ocorreu um erro ao salvar no Excel: {str(e)}")

# Configuração da janela principal
root = tk.Tk()
root.title("Calculadora de Impostos de Frete - Trator Peças")

# Definir o tamanho inicial da janela
root.geometry("600x500")  # Largura x Altura

# Carregar e exibir a logo (substitua pelo caminho da sua imagem)
logo_path = "logo.png"
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = ttk.Label(root, image=logo_photo)
logo_label.image = logo_photo
logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Criação dos widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

# Título do Frete
ttk.Label(frame, text="Rota do Frete:").grid(row=0, column=0, sticky=tk.W)
entry_titulo_frete = ttk.Entry(frame, width=30)
entry_titulo_frete.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

# Motorista
ttk.Label(frame, text="Motorista:").grid(row=1, column=0, sticky=tk.W)
entry_motorista = ttk.Entry(frame, width=30)
entry_motorista.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

# CPF
ttk.Label(frame, text="CPF:").grid(row=2, column=0, sticky=tk.W)
entry_cpf = ttk.Entry(frame, width=30)
entry_cpf.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

# Valor do Frete
ttk.Label(frame, text="Valor do Frete:").grid(row=3, column=0, sticky=tk.W)
entry_valor_frete = ttk.Entry(frame, width=20)
entry_valor_frete.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
entry_valor_frete.bind("<KeyRelease>", atualizar_aliquota_irrf)  # Atualizar alíquota do IRRF ao digitar

# Alíquota INSS
ttk.Label(frame, text="Alíquota INSS (%):").grid(row=4, column=0, sticky=tk.W)
entry_aliquota_inss = ttk.Entry(frame, width=20, state=tk.DISABLED)
entry_aliquota_inss.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
entry_aliquota_inss.insert(0, "11.00")

# Alíquota IRRF
ttk.Label(frame, text="Alíquota IRRF (%):").grid(row=5, column=0, sticky=tk.W)
entry_aliquota_irrf = ttk.Entry(frame, width=20, state=tk.DISABLED)
entry_aliquota_irrf.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

# Alíquota INSS Patronal
ttk.Label(frame, text="Alíquota INSS Patronal (%):").grid(row=6, column=0, sticky=tk.W)
entry_aliquota_inss_patronal = ttk.Entry(frame, width=20, state=tk.DISABLED)
entry_aliquota_inss_patronal.grid(row=6, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
entry_aliquota_inss_patronal.insert(0, "20.00")

# Botão Calcular
ttk.Button(frame, text="Calcular", command=calcular_imposto).grid(row=7, column=0, columnspan=2, pady=10)

# Label de resultado
label_resultado = ttk.Label(frame, text="", justify=tk.LEFT)
label_resultado.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E))

# Configuração do layout
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Execução da aplicação
root.mainloop()
