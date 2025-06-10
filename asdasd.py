import tkinter as tk
from tkinter import ttk
import time
import requests
import threading
from datetime import datetime
import json
import os

class WeatherWidget:
    def __init__(self):
        self.setup_window()
        self.setup_variables()
        self.setup_weather_icons()
        self.setup_ui()
        self.setup_cache()
        
    def setup_window(self):
        """Configuración de la ventana principal"""
        self.ventana = tk.Tk()
        self.ventana.title('Widget Clima')
        self.ventana.geometry('1280x720')
        self.ventana.configure(bg='#2c3e50')
        self.ventana.attributes('-topmost', True)
        
        # Debug: imprimir información del sistema
        print("Ventana creada correctamente")
        
    def setup_variables(self):
        """Inicialización de variables"""
        self.ciudad = "Presidencia Roque Saenz Peña"
        self.cache_file = "weather_cache.json"
        self.cache_duration = 1800
        
        # Variables de movimiento
        self.x_pos, self.y_pos = 100, 100
        self.x_vel, self.y_vel = 2, 1.5
        
        # Variables de estado
        self.weather_data = None
        self.last_weather_update = 0
        self.is_updating_weather = False
        self.icon_frame = 0
        
        print("Variables inicializadas")
        
    def setup_weather_icons(self):
        """Iconos usando caracteres Unicode compatibles"""
        self.weather_icons = {
            # Soleado
            'sunny': ['☀', '●'],
            'clear': ['☽', '○'],
            
            # Nublado  
            'cloudy': ['☁', '▓'],
            'partly_cloudy': ['⛅', '▒'],
            'overcast': ['▓▓', '███'],
            
            # Lluvia
            'light_rain': ['☂', '░▒'],
            'rain': ['☔', '▒▓'],
            'heavy_rain': ['⛈', '▓█'],
            'thunderstorm': ['⚡', '▲▼'],
            
            # Nieve
            'snow': ['❄', '❅'],
            'heavy_snow': ['❅❅', '***'],
            
            # Otros
            'fog': ['≡≡', '~~~'],
            'mist': ['≈≈', '---'],
            'wind': ['≋≋', '<<<'],
            'default': ['?', '---']
        }
        
        # Mapeo simplificado
        self.condition_mapping = {
            'soleado': 'sunny',
            'despejado': 'clear', 
            'sol': 'sunny',
            'claro': 'clear',
            'nublado': 'cloudy',
            'nubes': 'cloudy',
            'parcialmente': 'partly_cloudy',
            'lluvia': 'rain',
            'llovizna': 'light_rain',
            'tormenta': 'thunderstorm',
            'nieve': 'snow',
            'niebla': 'fog',
            'neblina': 'mist',
            'viento': 'wind'
        }
        
        print("Iconos configurados")
        
    def get_weather_icon(self, condition):
        """Obtener icono basado en condición"""
        if not condition:
            return self.weather_icons['default'][0]
            
        condition_lower = condition.lower()
        
        for key, icon_type in self.condition_mapping.items():
            if key in condition_lower:
                icons = self.weather_icons[icon_type]
                return icons[self.icon_frame % len(icons)]
        
        return self.weather_icons['default'][0]
    
    def get_weather_color(self, condition):
        """Colores según condición"""
        if not condition:
            return '#ffffff'
            
        condition_lower = condition.lower()
        
        if any(word in condition_lower for word in ['sol', 'despejado', 'claro']):
            return '#f39c12'  # Naranja
        elif any(word in condition_lower for word in ['lluvia', 'tormenta']):
            return '#3498db'  # Azul
        elif any(word in condition_lower for word in ['nube', 'nublado']):
            return '#95a5a6'  # Gris
        elif 'nieve' in condition_lower:
            return '#ecf0f1'  # Blanco
        else:
            return '#ffffff'  # Blanco por defecto
        
    def setup_ui(self):
        """Interfaz de usuario simplificada"""
        print("Creando interfaz...")
        
        # Contenedor principal con fondo visible
        self.container = tk.Frame(
            self.ventana,
            bg='#34495e',
            relief='raised',
            bd=3,
            padx=30,
            pady=25
        )
        
        # Título
        self.titulo = tk.Label(
            self.container,
            text="🌤 CLIMA WIDGET",
            font=('Arial', 16, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        self.titulo.pack(pady=(0, 15))
        
        # Ciudad
        self.ciudad_label = tk.Label(
            self.container,
            text=self.ciudad,
            font=('Arial', 12, 'bold'),
            bg='#34495e',
            fg='#bdc3c7'
        )
        self.ciudad_label.pack(pady=(0, 10))
        
        # Reloj
        self.reloj = tk.Label(
            self.container,
            text='--:--:--',
            font=('Arial', 36, 'bold'),
            bg='#34495e',
            fg='#1abc9c'
        )
        self.reloj.pack(pady=(0, 10))
        
        # Fecha
        self.fecha_label = tk.Label(
            self.container,
            text='Cargando fecha...',
            font=('Arial', 11),
            bg='#34495e',
            fg='#bdc3c7'
        )
        self.fecha_label.pack(pady=(0, 20))
        
        # Icono del clima (grande)
        self.weather_icon = tk.Label(
            self.container,
            text='?',
            font=('Arial', 48, 'bold'),
            bg='#34495e',
            fg='#f39c12'
        )
        self.weather_icon.pack(pady=(0, 10))
        
        # Temperatura
        self.temp_label = tk.Label(
            self.container,
            text='--°C',
            font=('Arial', 32, 'bold'),
            bg='#34495e',
            fg='#e74c3c'
        )
        self.temp_label.pack(pady=(0, 10))
        
        # Descripción
        self.desc_label = tk.Label(
            self.container,
            text='Cargando clima...',
            font=('Arial', 14),
            bg='#34495e',
            fg='#ecf0f1',
            wraplength=300
        )
        self.desc_label.pack(pady=(0, 15))
        
        # Detalles en una línea
        self.details_label = tk.Label(
            self.container,
            text='Sensación: --°C | Humedad: --% | Viento: -- km/h',
            font=('Arial', 10),
            bg='#34495e',
            fg='#95a5a6'
        )
        self.details_label.pack(pady=(0, 15))
        
        # Estado
        self.status_label = tk.Label(
            self.container,
            text='● Iniciando...',
            font=('Arial', 10),
            bg='#34495e',
            fg='#f39c12'
        )
        self.status_label.pack()
        
        print("Interfaz creada correctamente")
        
    def setup_cache(self):
        """Sistema de caché"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    if time.time() - cache_data.get('timestamp', 0) < self.cache_duration:
                        self.weather_data = cache_data.get('data')
                        self.update_weather_display()
                        print("Datos cargados desde caché")
        except Exception as e:
            print(f"Error al cargar caché: {e}")
    
    def save_cache(self, data):
        """Guardar caché"""
        try:
            cache_data = {
                'timestamp': time.time(),
                'data': data
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            print("Caché guardado")
        except Exception as e:
            print(f"Error al guardar caché: {e}")
    
    def actualizar_hora(self):
        """Actualizar reloj y fecha"""
        try:
            now = datetime.now()
            tiempo_actual = now.strftime('%H:%M:%S')
            fecha_actual = now.strftime('%A, %d de %B %Y')
            
            # Traducir al español
            dias = {
                'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
                'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
            }
            
            meses = {
                'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
                'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
                'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
                'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
            }
            
            for eng, esp in dias.items():
                fecha_actual = fecha_actual.replace(eng, esp)
            for eng, esp in meses.items():
                fecha_actual = fecha_actual.replace(eng, esp)
            
            self.reloj.config(text=tiempo_actual)
            self.fecha_label.config(text=fecha_actual)
            
        except Exception as e:
            print(f"Error actualizando hora: {e}")
        
        self.ventana.after(1000, self.actualizar_hora)
    
    def animate_icon(self):
        """Animar icono del clima"""
        try:
            if self.weather_data:
                self.icon_frame += 1
                condition = self.weather_data.get('desc_es', '')
                new_icon = self.get_weather_icon(condition)
                color = self.get_weather_color(condition)
                self.weather_icon.config(text=new_icon, fg=color)
        except Exception as e:
            print(f"Error animando icono: {e}")
        
        self.ventana.after(2000, self.animate_icon)  # Cada 2 segundos
    
    def obtener_clima_async(self):
        """Obtener clima en hilo separado"""
        if self.is_updating_weather:
            print("Ya se está actualizando el clima")
            return
            
        def fetch_weather():
            self.is_updating_weather = True
            print("Obteniendo datos del clima...")
            
            try:
                self.ventana.after(0, lambda: self.status_label.config(text='● Actualizando...', fg='#f39c12'))
                
                url = f"https://wttr.in/{self.ciudad}?format=j1&lang=es"
                print(f"URL: {url}")
                
                respuesta = requests.get(url, timeout=15)
                respuesta.raise_for_status()
                
                clima_data = respuesta.json()
                condicion_actual = clima_data['current_condition'][0]
                
                weather_info = {
                    'temp_c': condicion_actual['temp_C'],
                    'desc_es': condicion_actual.get('lang_es', [{}])[0].get('value', 'Desconocido'),
                    'humidity': condicion_actual.get('humidity', 'N/A'),
                    'wind_speed': condicion_actual.get('windspeedKmph', 'N/A'),
                    'feels_like': condicion_actual.get('FeelsLikeC', condicion_actual['temp_C'])
                }
                
                print(f"Datos obtenidos: {weather_info}")
                
                self.weather_data = weather_info
                self.last_weather_update = time.time()
                self.save_cache(weather_info)
                
                self.ventana.after(0, self.update_weather_display)
                self.ventana.after(0, lambda: self.status_label.config(text='● Conectado', fg='#27ae60'))
                
            except requests.exceptions.RequestException as e:
                print(f"Error de red: {e}")
                self.ventana.after(0, lambda: self.status_label.config(text='● Sin conexión', fg='#e74c3c'))
                self.ventana.after(0, lambda: self.desc_label.config(text="Error de conexión"))
            except Exception as e:
                print(f"Error general: {e}")
                self.ventana.after(0, lambda: self.status_label.config(text='● Error', fg='#e74c3c'))
                self.ventana.after(0, lambda: self.desc_label.config(text="Error al procesar datos"))
            finally:
                self.is_updating_weather = False
        
        threading.Thread(target=fetch_weather, daemon=True).start()
    
    def update_weather_display(self):
        """Actualizar visualización del clima"""
        if not self.weather_data:
            print("No hay datos del clima para mostrar")
            return
            
        try:
            temp = self.weather_data['temp_c']
            desc = self.weather_data['desc_es']
            humidity = self.weather_data.get('humidity', 'N/A')
            feels_like = self.weather_data.get('feels_like', temp)
            wind_speed = self.weather_data.get('wind_speed', 'N/A')
            
            # Actualizar elementos
            self.temp_label.config(text=f"{temp}°C")
            self.desc_label.config(text=desc.title())
            
            # Detalles en una línea
            details_text = f"Sensación: {feels_like}°C | Humedad: {humidity}% | Viento: {wind_speed} km/h"
            self.details_label.config(text=details_text)
            
            # Icono y color
            icon = self.get_weather_icon(desc)
            color = self.get_weather_color(desc)
            self.weather_icon.config(text=icon, fg=color)
            
            print(f"Display actualizado: {temp}°C, {desc}")
            
        except Exception as e:
            print(f"Error actualizando display: {e}")
    
    def actualizar_clima_periodico(self):
        """Actualización periódica"""
        current_time = time.time()
        if current_time - self.last_weather_update > self.cache_duration:
            print("Actualizando clima periódicamente")
            self.obtener_clima_async()
        
        self.ventana.after(300000, self.actualizar_clima_periodico)  # 5 minutos
    
    def mover_widget(self):
        """Movimiento del widget"""
        try:
            self.x_pos += self.x_vel
            self.y_pos += self.y_vel
            
            win_width = self.ventana.winfo_width()
            win_height = self.ventana.winfo_height()
            widget_width = self.container.winfo_reqwidth()
            widget_height = self.container.winfo_reqheight()
            
            # Rebote
            if self.x_pos + widget_width >= win_width or self.x_pos <= 0:
                self.x_vel *= -1
                self.x_pos = max(0, min(self.x_pos, win_width - widget_width))
            
            if self.y_pos + widget_height >= win_height or self.y_pos <= 0:
                self.y_vel *= -1
                self.y_pos = max(0, min(self.y_pos, win_height - widget_height))
            
            self.container.place(x=int(self.x_pos), y=int(self.y_pos))
            
        except Exception as e:
            print(f"Error en movimiento: {e}")
        
        self.ventana.after(30, self.mover_widget)
    
    def on_click(self, event):
        """Actualizar al hacer clic"""
        print("Clic detectado - Actualizando clima")
        self.obtener_clima_async()
    
    def iniciar(self):
        """Iniciar widget"""
        print("Iniciando widget...")
        
        # Posicionar contenedor
        self.container.place(x=self.x_pos, y=self.y_pos)
        
        # Eventos
        self.container.bind("<Button-1>", self.on_click)
        
        # Iniciar procesos
        print("Iniciando procesos...")
        self.actualizar_hora()
        self.animate_icon()
        self.obtener_clima_async()
        self.actualizar_clima_periodico()
        self.mover_widget()
        
        print("Widget iniciado correctamente")
        
        try:
            self.ventana.mainloop()
        except KeyboardInterrupt:
            print("Widget cerrado por el usuario")
        finally:
            if hasattr(self, 'ventana'):
                self.ventana.quit()

# Ejecutar
if __name__ == "__main__":
    print("=== INICIANDO WIDGET DE CLIMA ===")
    try:
        widget = WeatherWidget()
        widget.iniciar()
    except Exception as e:
        print(f"Error crítico: {e}")
        input("Presiona Enter para cerrar...")
