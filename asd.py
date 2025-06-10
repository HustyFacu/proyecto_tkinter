import tkinter as tk
import time
import requests # <-- 1. Importamos la librería para peticiones web

ventana = tk.Tk()
backgr = 'lightblue'
ventana.title('Reloj y Clima')
ventana.geometry('1280x720')
ventana.config(background=backgr)

# --- 2. Contenedor para agrupar reloj y clima ---
# Así se moverán juntos
container = tk.Frame(ventana, bg=backgr)

# --- Reloj (ahora dentro del 'container') ---
reloj = tk.Label(container, font=('Arial', 60), bg=backgr, fg='#000')
reloj.pack()

# --- 3. Etiqueta para el Clima (también en el 'container') ---
weather_label = tk.Label(container, font=('Arial', 18), bg=backgr, fg='#000')
weather_label.pack()

def hora():
    tiempo_actual = time.strftime('%H:%M') # Añadí segundos para ver que no se congela
    reloj.config(text=tiempo_actual)
    ventana.after(1000, hora)

# --- 4. Función para obtener y actualizar el clima ---
def actualizar_clima():
    try:
        # Usamos tu ubicación actual. Puedes cambiar "Presidencia Roque Saenz Peña" por otra ciudad.
        # El formato ?format=j1 nos da una respuesta JSON simple.
        ciudad = "Presidencia Roque Saenz Peña"
        url = f"https://wttr.in/{ciudad}?format=j1&lang=es" # lang=es para descripción en español
        
        respuesta = requests.get(url, timeout=10) # timeout para no esperar indefinidamente
        respuesta.raise_for_status()  # Lanza un error si la petición falló (ej. 404)
        
        clima_data = respuesta.json()
        
        # Extraemos los datos que necesitamos del JSON
        condicion_actual = clima_data['current_condition'][0]
        temp_c = condicion_actual['temp_C']
        desc_es = condicion_actual['lang_es'][0]['value']
        
        # Formateamos el texto y lo ponemos en la etiqueta
        texto_clima = f"{ciudad.split(',')[0]}: {temp_c}°C, {desc_es}"
        weather_label.config(text=texto_clima)

    except requests.exceptions.RequestException as e:
        weather_label.config(text="Error al obtener el clima")
        print(f"Error de red o API: {e}")
    except (KeyError, IndexError):
        # Por si la respuesta del servidor no es la esperada
        weather_label.config(text="Error al procesar datos del clima")

    # Se volverá a ejecutar en 30 minutos (1800000 milisegundos)
    ventana.after(1800000, actualizar_clima)


# --- 5. Lógica de movimiento MEJORADA (ahora mueve el 'container') ---
x_pos, y_pos = 0, 0
x_vel, y_vel = 2, 2 # Velocidad de movimiento

def mover_widget():
    global x_pos, y_pos, x_vel, y_vel
    
    # Actualiza la posición según la velocidad
    x_pos += x_vel
    y_pos += y_vel
    
    # Obtenemos las dimensiones de la ventana y del widget
    win_width = ventana.winfo_width()
    win_height = ventana.winfo_height()
    widget_width = container.winfo_width()
    widget_height = container.winfo_height()

    # Lógica de rebote en los bordes
    if x_pos + widget_width > win_width or x_pos < 0:
        x_vel *= -1 # Invertir dirección horizontal

    if y_pos + widget_height > win_height or y_pos < 0:
        y_vel *= -1 # Invertir dirección vertical
    
    container.place(x=x_pos, y=y_pos)
    ventana.after(30, mover_widget) # Intervalo de la animación

# --- 6. Iniciar todo ---
container.place(x=x_pos, y=y_pos) # Coloca el contenedor inicialmente

hora() # Inicia el reloj
actualizar_clima() # Llama por primera vez para obtener el clima
mover_widget() # Inicia la animación

ventana.mainloop()