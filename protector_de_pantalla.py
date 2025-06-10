import tkinter as tk
import time
ventana = tk.Tk()
backgr = 'lightblue'
ventana.title('protector de pantalla')
ventana.geometry('600x600')
ventana.config(background=backgr)
reloj = tk.Label(ventana, font =
('Arial', 60), bg = backgr , fg = '#000')
def hora():
 tiempo_actual = time.strftime('%H:%M')
 reloj.config(text = tiempo_actual)
 ventana.after(1000, hora)
reloj.pack(anchor = 'nw')

#configuro el movimiento del widget
x_pos = 0
y_pos = 0
# x_vel = 3
# y_vel = 2 
ancho = reloj.winfo_width()
alto = ventana.winfo_height() 
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
    widget_width = reloj.winfo_width()
    widget_height = reloj.winfo_height()

    # Lógica de rebote en los bordes
    if x_pos + widget_width > win_width or x_pos < 0:
        x_vel *= -1 # Invertir dirección horizontal

    if y_pos + widget_height > win_height or y_pos < 0:
        y_vel *= -1 # Invertir dirección vertical
    
    reloj.place(x=x_pos, y=y_pos)
    ventana.after(30, mover_widget) # Intervalo de la animación


mover_widget()

hora()
ventana.mainloop()
