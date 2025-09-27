#!/usr/bin/env python3
import os
import sys
import subprocess
import signal

def kill_port(port):
    try:
        # Find the process using the port
        result = subprocess.run(
            ['lsof', '-t', f'-i:{port}'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 or not result.stdout.strip():
            print(f"No process found running on port {port}")
            return
            
        pids = result.stdout.strip().split('\n')
        
        # Kill each process
        for pid in pids:
            if pid.strip():  # Ensure we have a valid PID
                try:
                    os.kill(int(pid), signal.SIGKILL)
                    print(f"Successfully killed process {pid} on port {port}")
                except ProcessLookupError:
                    print(f"Process {pid} not found")
                except PermissionError:
                    print(f"Permission denied: Unable to kill process {pid}")
                except Exception as e:
                    print(f"Error killing process {pid}: {str(e)}")
                    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: kill_port.py <port_number>")
        sys.exit(1)
    
    try:
        port = int(sys.argv[1])
        kill_port(port)
    except ValueError:
        print("Error: Port must be a number")
        sys.exit(1)
