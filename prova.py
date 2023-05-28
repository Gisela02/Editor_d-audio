import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from functools import partial
from audio_processor import AudioProcessor, RobotEffect, EchoEffect

class SoundFix:
    def __init__(self, root):
        self.root = root
        self.root.title("SoundFix")
        self.root.geometry("400x200")

        self.input_file = None
        self.output_file = None

        self.create_widgets()

    def create_widgets(self):
        # Label para mostrar el archivo de entrada seleccionado
        self.label_input = ttk.Label(self.root, text="Archivo de entrada: ")
        self.label_input.pack()

        # Botón para seleccionar el archivo de entrada
        self.btn_browse_input = ttk.Button(self.root, text="Seleccionar archivo de entrada", command=self.browse_input)
        self.btn_browse_input.pack()

        # Label para mostrar el archivo de salida seleccionado
        #self.label_output = ttk.Label(self.root, text="Archivo de salida: ")
        #self.label_output.pack()

        # Botón para seleccionar el archivo de salida
        #self.btn_browse_output = ttk.Button(self.root, text="Seleccionar archivo de salida", command=self.browse_output)
        #self.btn_browse_output.pack()

        # Botó per aplicar l'efecte robot
        self.btn_robot_effect = ttk.Button(self.root, text="Aplicar Efecto Robot", command=self.apply_robot_effect)
        self.btn_robot_effect.pack()

        # Botó per aplicar l'efecto eco
        self.btn_echo_effect = ttk.Button(self.root, text="Aplicar Efecto Eco", command=self.apply_echo_effect)
        self.btn_echo_effect.pack()
        
        # Botó per aplicar l'efecte flanger
        self.btn_echo_effect = ttk.Button(self.root, text="Aplicar Efecte Flanger", command=self.apply_flanger_effect)
        self.btn_echo_effect.pack()

    def browse_input(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
        self.label_input.config(text="Archivo de entrada: " + self.input_file)

    #def browse_output(self):
     #   self.output_file = filedialog.asksaveasfilename(filetypes=[("Audio Files", "*.wav")])
      #  self.label_output.config(text="Archivo de salida: " + self.output_file)

    def apply_robot_effect(self):
        if self.input_file:
            robot_effect = RobotEffect(self.input_file)
            output_file = self.input_file.replace(".wav", "_robot.wav")
            robot_effect.apply_robot_effect(self.output_file)
            robot_effect.save_audio(output_file)
            messagebox.showinfo("Efecte Robot", "L'efecte Robot s'ha aplicat correctament!.")
        else:
            messagebox.showerror("Error", "Si us plau, seleccioni un fitxer d'entrada.")

    def apply_echo_effect(self):
        if self.input_file:
            echo_effect = EchoEffect(self.input_file)
            output_file = self.input_file.replace(".wav", "_echo.wav")
            echo_effect.apply_echo_effect(self.output_file)
            echo_effect.save_audio(output_file)
            messagebox.showinfo("Efecte Eco", "L'efecte Eco s'ha aplicat correctament!.")
        else:
            messagebox.showerror("Error", "Si us plau, seleccioni un fitxer d'entrada.")
            
    def apply_flanger_effect(self):
        if self.input_file:
            echo_effect = FlangerEffect(self.input_file)
            output_file = self.input_file.replace(".wav", "_flanger.wav")
            echo_effect.apply_flanger_effect(self.output_file)
            flanger_effect.save_audio(output_file)
            messagebox.showinfo("Efecte Flanger", "L'efecte Flanger s'ha aplicat correctament!.")
        else:
            messagebox.showerror("Error", "Si us plau, seleccioni un fitxer d'entrada.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SoundFix(root)
    root.mainloop()