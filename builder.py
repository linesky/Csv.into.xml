import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import subprocess
import shutil
import os



class BareboneBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Barebone Builder")

        # Janela amarela
        self.root.configure(bg='yellow')

        # Área de texto
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack(pady=10)

        # Botões
        self.build_button = tk.Button(self.root, text="Build", command=self.build_kernel)
        self.build_button.pack(pady=5)

        self.run_button = tk.Button(self.root, text="Run", command=self.run_kernel)
        self.run_button.pack(pady=5)

        self.copy_button = tk.Button(self.root, text="new file", command=self.copy_file)
        self.copy_button.pack(pady=5)

    def execute_command(self, command,show:bool):
        try:
            
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
            self.text_area.insert(tk.END, result)
        except subprocess.CalledProcessError as e:
            if show:
                self.text_area.insert(tk.END,f"Error executing command:\n{e.output}")

    def build_kernel(self):
        
        self.text_area.delete(1.0, tk.END)
        self.execute_command("mkdir -p ./file/isodir/boot/grub",True)
        self.execute_command("mkdir -p ./file/isodir/boot/grub/i386-pc",True)
        self.execute_command("mkdir -p ./file/isodir/boot/grub/fonts",True)
        self.execute_command("mkdir -p ./file/isodir/etc",True)
        self.execute_command("cp /boot/grub/fonts/*.* ./file/isodir/grub/fonts",False)
        self.execute_command("cp /boot/grub/fonts/* ./file/isodir/grub/fonts",False)
        self.execute_command("cp /boot/grub/i386-pc/*.* ./file/isodir/grub/i386-pc",False)
        self.execute_command("mkdir -p ./file/isodir/bin",True)
        self.execute_command("cp /etc/init.d/console-setup.sh ./file/isodir/etc/init.rst",True)
        self.execute_command("cp /etc/init.d/console-setup.sh ./file/isodir/boot/init.rst",True)
        self.execute_command("cp ./image.gz ./file/isodir/boot",False)
        self.execute_command("cp ./vmlinuz ./file/isodir/boot",False)
        #self.execute_command("cp /initrd.img ./file/isodir/boot",False)
        #self.execute_command("cp /boot/initrd.img ./file/isodir/boot",False)
        #self.execute_command("cp /vmlinuz ./file/isodir/boot",False)
        self.execute_command("cp /boot/vmlinuz ./file/isodir/boot",False)
        self.execute_command("cp /usr/bin/bash ./file/isodir/bin",False)
        self.execute_command("cp /usr/bin/sh ./file/isodir/bin",False)
        self.execute_command("cp /etc/init.d/console-setup.sh ./file/isodir/boot",False)
        
        self.execute_command("cp ./file/grub.cfg ./file/isodir/boot/grub/grub.cfg",True)
        self.execute_command("grub-mkrescue -o myos.iso ./file/isodir",True)
    def run_kernel(self):
        self.text_area.delete(1.0, tk.END)
        self.execute_command("qemu-system-i386 -serial msmouse -cdrom myos.iso",True)
    def copy_file(self):
        self.text_area.delete(1.0, tk.END)
        filename = tk.filedialog.asksaveasfilename(title="Select file")
        if filename:
            shutil.copy( f"./file/new",filename+".c")
            self.text_area.insert(tk.END, f"File {filename} copied \n",True)


if __name__ == "__main__":
    root = tk.Tk()
    builder = BareboneBuilder(root)
    root.mainloop()
