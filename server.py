import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

clients = []
clientnames = {}

class ServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Server")
        
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.chat_area.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        self.servstart()

    def servstart(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 12345))
        server_socket.listen()
        self.msglog("Server listening on port 12345")
        
        threading.Thread(target=self.accept_connections, args=(server_socket,)).start()

    def accept_connections(self, server_socket):
        while True:
            conn, addr = server_socket.accept()
            clients.append(conn)
            threading.Thread(target=self.clientthread, args=(conn, addr)).start()

    def clientthread(self, conn, addr):
        try:
            self.msglog(f"Connected by {addr}")
            clientname = conn.recv(1024).decode('utf-8')
            clientnames[conn] = clientname
            self.msglog(f"Client name: {clientname}")

            while True:
                msg = conn.recv(1024).decode('utf-8')
                if msg:
                    fullmsg = f"{clientname}: {msg}"
                    self.msglog(fullmsg)
                    self.broadcast(fullmsg)
                else:
                    self.conremove(conn)
                    break
        except Exception as e:
            self.msglog(f"Error: {e}")
            self.conremove(conn)

    def broadcast(self, message):
        for client in clients:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                self.msglog(f"Broadcast error: {e}")
                self.conremove(client)

    def conremove(self, conn):
        if conn in clients:
            conn.close()
            clients.remove(conn)
            if conn in clientnames:
                del clientnames[conn]
            self.msglog(f"Connection closed: {conn}")

    def msglog(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

def main():
    root = tk.Tk()
    server_gui = ServerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
