import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")
        
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.chat_area.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        self.message_entry = tk.Entry(master)
        self.message_entry.pack(padx=20, pady=5, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", self.msgrcv)
        
        self.name_entry = tk.Entry(master)
        self.name_entry.pack(padx=20, pady=5, fill=tk.X, expand=True)
        self.name_entry.insert(0, "Enter your name here...")
        
        self.connect_button = tk.Button(master, text="Connect", command=self.servcon)
        self.connect_button.pack(padx=20, pady=5)
        
        self.client_socket = None
        self.client_name = ""

    def servcon(self):
        self.client_name = self.name_entry.get().strip()
        if not self.client_name:
            messagebox.showwarning("Name Error", "Please enter a valid name.")
            return
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(('127.0.0.1', 12345))
            self.client_socket.send(self.client_name.encode())
            self.name_entry.config(state=tk.DISABLED)
            self.connect_button.config(state=tk.DISABLED)
            threading.Thread(target=self.msgrcv).start()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")

    def msgrcv(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.chat_area.config(state=tk.NORMAL)
                    self.chat_area.insert(tk.END, message + '\n')
                    self.chat_area.config(state=tk.DISABLED)
                    self.chat_area.yview(tk.END)
                else:
                    self.client_socket.close()
                    break
            except Exception as e:
                print(f"Error: {e}")
                self.client_socket.close()
                break

    def msgrcv(self, event=None):
        msg = self.message_entry.get().strip()
        if msg:
            self.client_socket.send(msg.encode('utf-8'))
            self.message_entry.delete(0, tk.END)
            if msg.lower() == 'bye':
                self.client_socket.close()
                self.master.quit()

def main():
    root = tk.Tk()
    client_gui = ClientGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
