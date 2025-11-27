from tkinter import filedialog
import tkinter.messagebox
from customtkinter import *
from tkinter import * 
from tkinter import filedialog
import numpy as np
import tkinter.messagebox
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from openpyxl import Workbook
import re

class App:

    # Constructor
    def __init__(self, master):

        # Atributos/Características de la clase

        self.state_stop = False
        self.cont_headers = 0
        self.master = master
        self.master.title("Análisis bibliográficos de textos")
        self.master.state("zoomed")
        self.master.resizable(0, 0) 
        self.ancho = master.winfo_screenwidth()
        self.alto = master.winfo_screenheight()
        self.file_name_t = ""

        # Botones
        self.txts_btn = CTkButton(master, text = "Selecciona la ruta del archivo a examinar", command = self.elegirPathTXTs, width = self.ancho/3, height = self.alto/12)
        self.txts_btn.place(x = self.ancho/12, y = self.alto/12)

        self.periodo_btn = CTkButton(master, text = "Año", command = self.TablaTiempo, width = self.ancho/14, height = self.alto/15)
        self.periodo_btn.place(x = self.ancho/12, y = self.alto/4)
        self.autores_btn = CTkButton(master, text = "Autores", command = self.TablaAutores, width = self.ancho/14, height = self.alto/15)
        self.autores_btn.place(x = self.ancho/12*2, y = self.alto/4)
        self.titulos_btn = CTkButton(master, text = "Títulos", command = self.TablaTitulos, width = self.ancho/14, height = self.alto/15)
        self.titulos_btn.place(x = self.ancho/12*3, y = self.alto/4)
        self.editorial_btn = CTkButton(master, text = "Editorial", command = self.TablaEditorial, width = self.ancho/14, height = self.alto/15)
        self.editorial_btn.place(x = self.ancho/12*4, y = self.alto/4)
        self.guardar_btn = CTkButton(master, text = "Guardar", command = self.guardarDatos, width = self.ancho/18, height = self.alto/20)
        self.guardar_btn.place(x = self.ancho / 8  * 4, y = self.alto / 35 * 28)

        # Inhabilitar botones de info
        self.checkButInfo(0)
        
        self.graf_Tiempo_btn = CTkButton(master, text = "Graficar Año", command = self.graficarTiempo, width = self.ancho/14, height = self.alto/15)
        
        self.graf_Autores_btn = CTkButton(master, text = "Graficar Autores", command = self.graficarAutores, width = self.ancho/14, height = self.alto/15)
   
        self.graf_Titulos_btn = CTkButton(master, text = "Graficar Titulos", command = self.graficarTitulos, width = self.ancho/14, height = self.alto/15)
        
        self.graf_Editorial_btn = CTkButton(master, text = "Graficar Editorial", command = self.graficarEditorial, width = self.ancho/14, height = self.alto/15)
        

        # Etiquetas
        self.info = CTkLabel(master, text = "Mostrar información disponible:", anchor = 'w', width = self.ancho/3, height = self.alto/19) 
        self.info.place(x = self.ancho/12, y = self.alto/12 * 2.2) 
        
        # Crear frame que va a tener el textbox y su scrollbar
        self.text_frame = CTkFrame(master, fg_color="transparent")
        self.text_frame.place(x = self.ancho/12, y = self.alto/12*4)
        # Crear el textbox
        self.tk_textbox = CTkTextbox(self.text_frame, activate_scrollbars=False, width = self.ancho/3, height = self.alto/12*6, fg_color="#54982F")
        self.tk_textbox.grid(row=0, column=0, sticky="nsew")

        # Crear el scrollbar
        self.ctk_textbox_scrollbar = CTkScrollbar(self.text_frame, command = self.tk_textbox.yview)
        self.ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")

        self.tk_textbox.configure(yscrollcommand=self.ctk_textbox_scrollbar.set)

        # Nombre de los desarroladores
        self.dev_label = CTkLabel(master, text = "Developers: Jazmín, Alexis & Emiliano", anchor = 'w', width = self.ancho/6, height = self.alto/25)  
        self.dev_label.place(x = self.ancho / 8 * 6, y = self.alto / 35 * 28)

    # Métodos
    def elegirPathTXTs(self):

        # Try and except para cachar los errores al cargar el achivo
        try:
            self.cont = 0
            # Inicializar los renglones del archivo             
            self.archivos_procesados = []  #CAMBIO DICCIONARIO
            self.path_carpeta, self.array_files = self.obtener_path_carpeta()  #En self.array_files están guardados los archivos

            for filefound in self.array_files:
                self.filename = self.path_carpeta + "\\" + filefound
                

                if self.filename != "":                   
                    self.file_name_t = os.path.basename(self.filename)   # Obtener solo el nombre del archivo sin todo el path                   
                    self.nombre_header = "PROTOCOLO DE INVESTIGACIÓN"    # Nombre que aparece en la cabecera de cada página   
                    self.lineas_archivo_actual = []                      # "Barrer" el archivo línea por línea
                    with open(self.filename, "r", encoding="utf-8-sig", errors="replace") as archivo:
                        for linea in archivo:                          
                            if linea != "" and linea.isspace() == False and self.eliminarHeader(self.nombre_header, linea):  # linea.isspace(): la línea contiene puros espacios en blanco  
                                self.lineas_archivo_actual.append(linea.rstrip()) # rstrip() elimina el salto de línea al final 
                                self.cont += 1                                    # Imprimir en consola la fila "cont"
                    self.archivos_procesados.append(self.lineas_archivo_actual)  


            # Títuloa de proyectos
            self.getTituloArchivo()

            #Filetitulo = self.getTituloArchivo(self.filas)
            self.extraerReferenciasAPA7()

            # Ordenar datos
            self.ordenarInfo()

            tkinter.messagebox.showinfo(title = "Aviso", message="Archivo Cargado")
            self.checkButInfo(1)



        except FileNotFoundError:
            tkinter.messagebox.showinfo(title = "Error", message="El archivo no existe en la ruta especificada")
            # Deshabilitar botones de información
            self.checkButInfo(0)
            # Limpiar TextBox
            self.tk_textbox.delete("1.0", "end") 

        except Exception as e:
            print("Ocurrió un error al cargar el archivo", e)
            tkinter.messagebox.showinfo(title="Error", message="Un error ocurrió al momento de cargar el archivo")
            # Deshabilitar botones de información
            self.checkButInfo(0)
            # Limpiar TextBox
            self.tk_textbox.delete("1.0", "end")

    #Método que regresa la ruta y los files txt contenidos
    def obtener_path_carpeta(self):
        archivos_txt = []
        root = Tk()
        root.withdraw()  # Oculta la ventana principal de Tkinter
        carpeta_seleccionada = filedialog.askdirectory()

        #archivos_txt.append(carpeta_seleccionada)
        elementos = os.listdir(carpeta_seleccionada)
        for elemento in elementos:
        # La función 'endswith' verifica si el string termina con el sufijo dado
            if elemento.endswith(".txt"):
                archivos_txt.append(elemento)

        return carpeta_seleccionada, archivos_txt

    # Método para eliminar el header que tiene una imagen
    def eliminarHeader(self, text_b, lin):
        if text_b in lin:
            # Eliminar el header completo porque aparecen 3 líneas:
            # el número de páf, espacio y nómbre del header
            if(self.cont_headers != 0):
                # Eliminar las filas que pertenecen al header
                self.filas.pop() # Espacios en blanco
                self.filas.pop() # Número de página
                self.cont -= 2
                self.cont_headers += 1

            return False
        else:
            return True

    
    def getTituloArchivo(self):
        #ENCONTRANDO SECCIÓN DE REFERENCIA
        self.content_archivo = []   # nuevo diccionario para guardar resultados
        self.referencias_encontradas = []
        self.referencias_para_conteo = []
        self.nombres_t_archivos = []

        for filas_ in self.archivos_procesados:
            ini_ref = 0
            for i, fila in enumerate(filas_):
                if "REFERENCIAS" in fila.upper():
                    ini_ref = i
                    break

            contenido = filas_[:ini_ref]                              # Guardar contenido antes de las referencias en diccionario content_archivo
            self.content_archivo.extend(contenido)
            self.referencias_encontradas.append(filas_[ini_ref + 1:])
        
    

        # Encontrar el título del proyecto
        for f in self.content_archivo:
            if "TÍTULO DEL PROYECTO" in f.upper():
                try:
                    ini = f.index(":")
                    self.nombres_t_archivos.append(f[ini + 2:])
                except:
                    self.nombres_t_archivos.append("No encontrado")

    # Método para extraer las referencias en formato APA7
    def extraerReferenciasAPA7(self):
        self.referencias_separadas = []   # lista final de referencias ya separadas
        aux_referencias = ""
        self.archivos_ref = []
        todas_ref = []

        for i in range (0, len(self.array_files)):
            for fila in self.referencias_encontradas[i]:
                aux_referencias = aux_referencias + fila
                # Separar por DOI
                if "HTTP" in fila.upper():
                    #if self.validarReferencia(aux_referencias):
                    print(fila)
                    self.referencias_separadas.append(aux_referencias)
                    todas_ref.append(aux_referencias)
                    aux_referencias = ""
                    print(len(self.referencias_separadas))
            self.archivos_ref.append(self.referencias_separadas)
            print(self.archivos_ref)
            self.referencias_separadas = []


        for i, ref in enumerate(todas_ref):
            self.tk_textbox.insert(str(i + 1) + "." + "0", ref + "\n")


    #
    def validarReferencia(self, referencia):
        no_incluidas = []
        # Patrón básico: Apellido, Inicial. (Año). Título...
        patron = r"^[A-Z][a-z]+, [A-Z]\. \((\d{4})\)\. .+$"
        if re.match(patron, referencia): 
            return True
        else:
            no_incluidas.append(referencia)
            return False

    # Contar la cita de cada autor
    def contarAutores(self, ref):
        # Nombres de los autores
        autores = []
        indices = []
        apellidos = []
        # Frecuenncia del autor n
        freq_aut = []
        aux_aut = 0

        for a in ref:
            try:
                ind_aut = a.index(",")
                autores.append(a[:ind_aut])
            except ValueError:
                autores.append("No se encuentra")
        self.autores = autores
       
        
        for nombre_aut in autores:
            for cont in self.content_archivo:
                if nombre_aut in cont:
                    aux_aut += 1
            freq_aut.append(aux_aut)
            aux_aut = 0
        self.freq_aut = freq_aut

        print(self.autores)
        print(self.freq_aut)

        
    # Contar cuantos papers se lanzaron en cada año
    def contarTiempo(self, ref):

        freq_tiempo_ref = []
        aux_tiempo = 0

        periodo = list(range(1940, 2026))
        for i in periodo:
            for a in ref:
                if str(i) in a:
                    aux_tiempo += 1
            freq_tiempo_ref.append(aux_tiempo)
            aux_tiempo = 0
        self.periodo = periodo
        self.freq_tiempo_ref = freq_tiempo_ref

        print(self.periodo)
        print(self.freq_tiempo_ref)



    # Contar los la aparición de los títulos de las referencias
    def contarTitulo(self, ref):

        freq_titulo = []
        aux_titulo_nom = ""
        aux_titulo = 0
        titulos = []

        for t in ref:
            # Extraer el nombre del título para cada referencia
            try:
                ind_t = t.index(")")
                aux_titulo_nom = t[ind_t + 3:]
                ind_t = aux_titulo_nom.index(".")
                titulos.append(aux_titulo_nom[:ind_t])

            except ValueError:
                titulos.append("No se encuentra")

        # "Barrer" los títulos para checar si aparecen en cada refernecia
        # Es decir, sacar la frecuencia de cada título al barrer todas las referencias
        for nombre_t in titulos:
            for cont in ref:
                if nombre_t in cont:
                    aux_titulo += 1
            freq_titulo.append(aux_titulo)
            aux_titulo = 0
        self.titulos = titulos
        self.freq_titulo = freq_titulo

        print(self.titulos) 
        print(self.freq_titulo)

   

    # Contar la frecuencia de las editoriales
    def contarEditorial(self, ref):
        freq_editorial = []
        aux_editorial_nom = ""
        aux_editorial = 0
        editoriales = []

        for e in ref:
            # Extraer el nombre de las revistas/editoriales para cada referencias
            try:
                ind_e = e.index(")")
                aux_editorial_nom = e[ind_e + 3:]
                ind_e = aux_editorial_nom.index(".")
                aux_editorial_nom = aux_editorial_nom[ind_e + 2:]
                ind_e = aux_editorial_nom.index(".")
                editoriales.append(aux_editorial_nom[:ind_e])
            except ValueError:
                editoriales.append("No se encuentra")
            
        
        # "Barrer" los editoriales para checar si aparecen en cada refernecia
        # Es decir, sacar la frecuencia de cada editorial al barrer todas las referencias
        for nombre_e in editoriales:
            for cont in ref:
                if nombre_e in cont:
                    aux_editorial += 1
            freq_editorial.append(aux_editorial)
            aux_editorial = 0
        self.editoriales = editoriales
        self.freq_editorial = freq_editorial
        self.editoriales = editoriales
        self.freq_editorial = freq_editorial

        print(self.editoriales)
        print(self.freq_editorial)


    # Método para habilitar o dehabilitar botones que pueden mostrar la info
    def checkButInfo(self, estado):
        if estado == 0:
            self.periodo_btn.configure(state = 'disabled')
            self.autores_btn.configure(state = 'disabled')
            self.editorial_btn.configure(state = 'disabled')
            self.titulos_btn.configure(state = 'disabled')
        elif estado == 1:
            self.periodo_btn.configure(state = 'normal')
            self.autores_btn.configure(state = 'normal')
            self.editorial_btn.configure(state = 'normal')
            self.titulos_btn.configure(state = 'normal')   


     # Método que genera la tabla de autores
    
    def TablaAutores(self):
        self.graf_Autores_btn.place(x = self.ancho/12*7, y = self.alto/15)

    # Método que genera la tabla de tiempos
    def TablaTiempo(self):
        self.graf_Tiempo_btn.place(x = self.ancho/12*6, y = self.alto/15)

    # Método que genera la tabla de titulos
    def TablaTitulos(self):
        self.graf_Titulos_btn.place(x = self.ancho/12*8, y = self.alto/15)

    # Método que genera la tabla de Editoriales
    def TablaEditorial(self):
        self.graf_Editorial_btn.place(x = self.ancho/12*9, y = self.alto/15)

# Método que genera grafica de autores
    def graficarAutores(self):
        fig, ax = plt.subplots(figsize=(2,2), dpi = 100)      #DPI son puntos por pulgada

        ax.bar(self.autores, self.freq_aut)
        ax.set_title("Frecuencia por Autor")
        ax.set_xlabel("Autores")
        ax.set_ylabel("Frecuencia")
        plt.xticks(rotation=80)
        plt.subplots_adjust(bottom=0.20)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()

        widget = canvas.get_tk_widget()
        widget.place(x = self.ancho/6 * 3, y = self.alto/6)  


    # Método que genera gráfica de tiempo
    def graficarTiempo(self):
        fig, ax = plt.subplots(figsize=(2,2),dpi = 100)       #DPI son puntos por pulgada
        ax.bar(self.periodo, self.freq_tiempo_ref)
        ax.set_title("Frecuencia por Año")
        ax.set_xlabel("Año")
        ax.set_ylabel("Frecuencia")
        plt.xticks(rotation=45)
        plt.tight_layout()         #Ajuste automatco al layout

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()

        widget = canvas.get_tk_widget()
        widget.place(x = self.ancho/6 * 4, y = self.alto/6)  
    
    #Método que genera gráfica de titulos
    def graficarTitulos(self):
        fig, ax = plt.subplots(figsize=(2,2),dpi = 100)          #DPI son puntos por pulgada
        ax.plot(self.titulos, self.freq_titulo)
        ax.set_title("Frecuencia por Titulos")
        ax.set_xlabel("Titulo")
        ax.set_ylabel("Frecuencia")
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.70)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()

        widget = canvas.get_tk_widget()
        widget.place(x = self.ancho/6 * 3, y = self.alto/2)

    #Método que genera gráfica de editorial
    def graficarEditorial(self):
        fig, ax = plt.subplots(figsize=(2,2),dpi = 100)           #DPI son puntos por pulgada
        ax.plot(self.editoriales, self.freq_editorial)
        ax.set_title("Frecuencia por editorial")
        ax.set_xlabel("Editoriales")
        ax.set_ylabel("Frecuencia")
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.70)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()

        widget = canvas.get_tk_widget()
        widget.place(x = self.ancho/6 * 4, y = self.alto/2) 


    def ordenarInfo(self):

        # Autores
        data = {"Autores": [""], "Archivo 1": [0], "Archivo 2": [0], "Archivo 3": [0], "Archivo 4": [0], "Archivo 5": [0], 
                "Archivo 6": [0], "Archivo 7": [0], "Archivo 8": [0], "Archivo 9": [0], "Archivo 10": [0]}
        
        df1 = pd.DataFrame(data)
        inicio = 0
        aux = 0
        for archivo_i in range (0, len(self.archivos_ref)):
            self.contarAutores(self.archivos_ref[archivo_i])
            for i in range (inicio, len(self.freq_aut) + inicio):
                # Quitar caractéres especiales
                df1.loc[i, "Autores"] = re.sub(r'[^a-zA-Z]', '', str(self.autores[aux]))
                df1.iloc[i, archivo_i + 1] = int(self.freq_aut[aux])
                aux += 1
            inicio = len(self.freq_aut)
            aux = 0
        self.df1 = df1.replace(np.nan, 0)
        print(self.df1)


        # Títulos
        data = {"Titulos": [""], "Archivo 1": [0], "Archivo 2": [0], "Archivo 3": [0], "Archivo 4": [0], "Archivo 5": [0], 
                "Archivo 6": [0], "Archivo 7": [0], "Archivo 8": [0], "Archivo 9": [0], "Archivo 10": [0]}
        
        df2 = pd.DataFrame(data)
        inicio = 0
        aux = 0
        for archivo_i in range (0, len(self.archivos_ref)):
            self.contarTitulo(self.archivos_ref[archivo_i])
            for i in range (inicio, len(self.freq_titulo) + inicio):
                # Quitar caractéres especiales
                df2.loc[i, "Titulos"] = re.sub(r'[^a-zA-Z]', '', str(self.titulos[aux]))
                df2.iloc[i, archivo_i + 1] = int(self.freq_titulo[aux])
                aux += 1
            inicio = len(self.freq_titulo)
            aux = 0
        self.df2 = df2.replace(np.nan, 0)
        print(self.df2)

    
        # Editorial 
        data = {"Editorial": [""], "Archivo 1": [0], "Archivo 2": [0], "Archivo 3": [0], "Archivo 4": [0], "Archivo 5": [0], 
                "Archivo 6": [0], "Archivo 7": [0], "Archivo 8": [0], "Archivo 9": [0], "Archivo 10": [0]}
        
        df3 = pd.DataFrame(data)
        inicio = 0
        aux = 0
        for archivo_i in range (0, len(self.archivos_ref)):
            self.contarEditorial(self.archivos_ref[archivo_i])
            for i in range (inicio, len(self.freq_editorial) + inicio):
                # Quitar caractéres especiales
                df3.loc[i, "Editorial"] = re.sub(r'[^a-zA-Z]', '', str(self.editoriales[aux]))
                df3.iloc[i, archivo_i + 1] = int(self.freq_editorial[aux])
                aux += 1
            inicio = len(self.freq_editorial)
            aux = 0
        self.df3 = df3.replace(np.nan, 0)
        print(self.df3)
  

        # Años 
        data = {"Tiempo": [""], "Archivo 1": [0], "Archivo 2": [0], "Archivo 3": [0], "Archivo 4": [0], "Archivo 5": [0], 
                "Archivo 6": [0], "Archivo 7": [0], "Archivo 8": [0], "Archivo 9": [0], "Archivo 10": [0]}
        
        df4 = pd.DataFrame(data)
        inicio = 0
        aux = 0
        for archivo_i in range (0, len(self.archivos_ref)):
            self.contarTiempo(self.archivos_ref[archivo_i])
            for i in range (inicio, len(self.freq_tiempo_ref) + inicio):
                # Quitar caractéres especiales
                df4.loc[i, "Tiempo"] = str(self.periodo[aux])
                df4.iloc[i, archivo_i + 1] = int(self.freq_tiempo_ref[aux])
                aux += 1
            inicio = len(self.freq_tiempo_ref)
            aux = 0
        self.df4 = df4.replace(np.nan, 0)
        print(self.df4)

    def guardarDatos(self):
        self.path_datos = filedialog.askdirectory(parent = self.master, initialdir='C:/', title = 'Selecciona la ruta para guardar el archivo')  
        if self.path_datos != '':
            self.file_name = self.path_datos + "/" + "Frecuencias.xlsx"
            tkinter.messagebox.showinfo(title = "Archivo guardo", message="Se ha guardado el archivo")
            with pd.ExcelWriter(self.file_name) as writer:
                self.df1.to_excel(writer, sheet_name='Autores', index=False)
                self.df2.to_excel(writer, sheet_name='Títulos', index=False)
                self.df3.to_excel(writer, sheet_name='Editorial', index=False)
                self.df4.to_excel(writer, sheet_name='Años', index=False)
            
GUI = CTk()
AppTXTs = App(GUI)
AppTXTs.master.mainloop()

