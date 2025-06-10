import tkinter as tk
import time

ventana = tk.Tk()
backgr = 'lightblue'
ventana.title('Reloj simple')
ventana.geometry('600x600')
#ventana.config(background=backgr)

x_pos = 3
y_pos = 3
x_vel = 3
y_vel = 2

modo_noche_activo = False

reloj = tk.Label(ventana, font =('Arial', 60), fg = '#000')
reloj.place(x=0, y=0)

def actualizar_modo_noche():
    global modo_noche_activo
    hora_actual = int(time.strftime('%H'))

    if 20 >= hora_actual or hora_actual < 6:
        #Modo noche
        if not modo_noche_activo:
            ventana.config(background="black")
            reloj.config(bg="black", fg="white")
            modo_noche_activo = True
    else:
        #Modo dia
        if modo_noche_activo:
            ventana.config(background="lightblue")
            reloj.config(bg="lightblue", fg="black")
            modo_noche_activo = False
    ventana.after(60000, actualizar_modo_noche)

def hora():
    tiempo_actual = time.strftime('%H:%M')
    reloj.config(text = tiempo_actual)
    ventana.after(1000, hora)


#configuro el movimiento del widget

ancho = reloj.winfo_width()
alto = ventana.winfo_height() 

def mover_reloj():
    global x_pos, y_pos, x_vel, y_vel
    
    #actualizar tamaño actual de ventana y widget
    ventana.update_idletasks()
    ancho_ventana = ventana.winfo_width()
    alto_ventana = ventana.winfo_height()
    ancho_reloj = reloj.winfo_width()
    alto_reloj = reloj.winfo_height()

    #mover reloj
    x_pos += x_vel
    y_pos += y_vel

    #detecta colisiones con los bordes y rebotar
    if x_pos <= 0 or x_pos + ancho_reloj >= ancho_ventana:
        x_vel *= -1
    if y_pos <= 0 or y_pos + alto_reloj >= alto_ventana:
        y_vel *= -1

    reloj.place(x=x_pos, y=y_pos)
    ventana.after(30, mover_reloj)




hora()
mover_reloj()
actualizar_modo_noche()
ventana.mainloop()
