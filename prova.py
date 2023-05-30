import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from functools import partial
from pydub import AudioSegment
from audio_processor import AudioProcessor, EchoEffect, FlangerEffect, RobotEffect, PitufoEffect, LowEffect, LowPassFilter
from PIL import Image
from PIL import ImageTk
import ffmpeg
import os

#from audio_processor import RobotEffect

class SoundFix:
    def __init__(self, root):
        self.root = root
        self.root.title("SoundFix")
        self.root.geometry("800x700")
        
        # Agregar un fondo visualmente atractivo
        self.background_image = tk.PhotoImage(file="backgr.png")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Agregar un logo
        self.logo_image = tk.PhotoImage(file="logo.png")
        self.logo_label = tk.Label(self.root, image=self.logo_image)
        self.logo_label.pack(pady=10)
        self.logo_label.place(relx=0.5, rely=0.4, anchor=tk.S)
        
        self.input_file = None
        self.output_file = None

        self.create_widgets()

    def create_widgets(self):
        # Label para mostrar el archivo de entrada seleccionado
        self.label_input = ttk.Label(self.root, text="Archivo de entrada: ")
        self.label_input.pack()
        self.label_input.place(relx=0.5, rely=0.1, anchor=tk.S)

        # Botón para seleccionar el archivo de entrada
        self.btn_browse_input = ttk.Button(self.root, text="Seleccionar archivo de entrada", command=self.browse_input)
        self.btn_browse_input.pack()
        self.btn_browse_input.place(relx=0.5, rely=0.15, anchor=tk.S)
        
        # Botón para convertir un archivo MP3 a WAV
        self.btn_convert_to_wav = ttk.Button(self.root, text="Convertir a WAV", command=self.convert_to_wav)
        self.btn_convert_to_wav.pack()
        self.btn_convert_to_wav.place(relx=0.7, rely=0.15, anchor=tk.S)        

        # Botón para recortar el audio
        button_img = Image.open("tall.png")
        button_photo = ImageTk.PhotoImage(button_img)
        self.btn_trim_audio = ttk.Button(self.root, text="Recortar Audio", image=button_photo, compound="left", command=self.trim_audio)
        self.btn_trim_audio.pack()
        self.btn_trim_audio.place(relx=0.2, rely=0.85, anchor=tk.S)

        # Botón para cargar y reproducir el audio
        self.btn_load_and_play = ttk.Button(self.root, text="Cargar y Reproducir", command=self.load_and_play_audio)
        self.btn_load_and_play.pack()
        self.btn_load_and_play.place(relx=0.5, rely=0.85, anchor=tk.S)

        # Botó per aplicar l'efecte robot
        self.btn_robot_effect = ttk.Button(self.root, text="Aplicar Efecto Robot", command=self.apply_robot_effect)
        self.btn_robot_effect.pack()
        self.btn_robot_effect.place(relx=0.8, rely=0.5, anchor=tk.S)

        # Botó per aplicar l'efecto eco
        self.btn_echo_effect = ttk.Button(self.root, text="Aplicar Efecto Eco", command=self.apply_echo_effect)
        self.btn_echo_effect.pack()
        self.btn_echo_effect.place(relx=0.2, rely=0.5, anchor=tk.S)
        
        # Botó per aplicar l'efecte flanger
        self.btn_flanger_effect = ttk.Button(self.root, text="Aplicar Efecte Flanger", command=self.apply_flanger_effect)
        self.btn_flanger_effect.pack()
        self.btn_flanger_effect.place(relx=0.5, rely=0.5, anchor=tk.S)

        # Botó per aplicar l'efecte pitufo
        self.btn_pitufo_effect = ttk.Button(self.root, text="Aplicar Efecte Pitufo", command=self.apply_pitufo_effect)
        self.btn_pitufo_effect.pack()
        self.btn_pitufo_effect.place(relx=0.2, rely=0.65, anchor=tk.S)
        
        # Botó per aplicar l'efecte Low
        self.btn_low_effect = ttk.Button(self.root, text="Aplicar Efecte Low", command=self.apply_low_effect)
        self.btn_low_effect.pack()
        self.btn_low_effect.place(relx=0.5, rely=0.65, anchor=tk.S)
        
        # Botó per aplicar l'efecte LPF
        self.btn_lowPass_effect = ttk.Button(self.root, text="Aplicar Efecte LPF", command=self.apply_lowPass_effect)
        self.btn_lowPass_effect.pack()
        self.btn_lowPass_effect.place(relx=0.8, rely=0.65, anchor=tk.S)

    def browse_input(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
        self.label_input.config(text="Archivo de entrada: " + self.input_file)

    def convert_to_wav(self):
        if self.input_file:
            input_filename, input_extension = os.path.splitext(self.input_file)
            output_file_wav = input_filename + ".wav"
            try:
                ffmpeg.input(self.input_file).output(output_file_wav).run()
                messagebox.showinfo("Convertir a WAV", "La conversión se ha realizado correctamente.")
            except ffmpeg.Error as e:
                messagebox.showerror("Error", f"Ocurrió un error durante la conversión: {str(e)}")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un archivo de entrada.")
    
    def trim_audio(self):
        if self.input_file:
            start_time = simpledialog.askfloat("Recortar Audio", "Ingrese el punto de inicio (en segundos):")
            duration = simpledialog.askfloat("Recortar Audio", "Ingrese la duración del recorte (en segundos):")
            input_filename, input_extension = os.path.splitext(self.input_file)
            output_file_trimmed = input_filename + "*_Tall.wav"

            audio_processor = AudioProcessor(self.input_file)
            audio_processor.trim_audio(output_file_trimmed, start_time, duration)

            messagebox.showinfo("Audio Recortado", "El audio se ha recortado correctamente.")

        else:
            messagebox.showerror("Error", "Por favor, seleccione un archivo de entrada.")
            
    def load_and_play_audio(self):
        if self.input_file:
            audio_processor = AudioProcessor(self.input_file)
            audio_processor.play_audio()
        else:
            messagebox.showerror("Error", "Por favor, seleccione un archivo de entrada.")
            
    def apply_robot_effect(self):
        if self.input_file:
            robot_effect = RobotEffect(self.input_file)
            input_filename, input_extension = os.path.splitext(self.input_file)
            output_file_robot = input_filename + "_Robot.wav"
            robot_effect.apply_robot_effect(output_file_robot)
            messagebox.showinfo("Efecte Robot", "L'efecte Robot s'ha aplicat correctament!.")
        else:
            messagebox.showerror("Error", "Si us plau, seleccioni un fitxer d'entrada.")
    
    def apply_echo_effect(self):
        if self.input_file:
            echo_effect = EchoEffect(self.input_file)
            input_filename, input_extension = os.path.splitext(self.input_file)
            output_file_echo = input_filename + "_Echo.wav"
            echo_effect.apply_echo_effect(output_file_echo)
            messagebox.showinfo("Efecte Eco", "L'efecte Eco s'ha aplicat correctament!.")
        else:
            messagebox.showerror("Error", "Si us plau, seleccioni un fitxer d'entrada.")
    
    def apply_flanger_effect(self):
        if self.input_file:
            flanger_effect = FlangerEffect(self.input_file)
            input_filename, input_extension = os.path.splitext(self.input_file)
            output_file_flanger = input_filename + "Flanger.wav"
            flanger_effect.apply_flanger_effect(output_file_flanger)
            messagebox.showinfo("Efecte Flanger", "L'efecte Flanger s'ha aplicat correctament!.")
        else:
            messagebox.showerror("Error", "Si us plau, seleccioni un fitxer d'entrada.")
    
    def apply_pitufo_effect(self):
        if self.input_file:
            pitufo_effect = PitufoEffect(self.input_file)
            input_filename, input_extension = os.path.splitext(self.input_file)
            output_file_pitufo = input_filename + "_Pitufo.wav"
            pitufo_effect.apply_pitufo_effect(output_file_pitufo)
            messagebox.showinfo("Efecte Pitufo", "L'efecte Pitufo s'ha aplicat correctament!.")
        else:
            messagebox.showerror("Error", "Si us plau, seleccioni un fitxer d'entrada.")
            
    def apply_low_effect(self):
        if self.input_file:
            low_effect = LowEffect(self.input_file)
            input_filename, input_extension = os.path.splitext(self.input_file)
            output_file_low = input_filename + "_Low.wav"
            low_effect.apply_low_effect(output_file_low)
            messagebox.showinfo("Efecte Low", "L'efecte Low s'ha aplicat correctament!.")
        else:
            messagebox.showerror("Error", "Si us plau, seleccioni un fitxer d'entrada.")
    
    def apply_lowPass_effect(self):
        if self.input_file:
            lowPass_effect = LowPassFilter(self.input_file)
            input_filename, input_extension = os.path.splitext(self.input_file)
            output_file_lowPass = input_filename + "_LowPass.wav"
            lowPass_effect.apply_lowpass_filter(output_file_lowPass)
            messagebox.showinfo("Efecte LPF", "L'efecte Low Pass Filter s'ha aplicat correctament!.")
        else:
            messagebox.showerror("Error", "Si us plau, seleccioni un fitxer d'entrada.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SoundFix(root)
    root.mainloop()