#!/usr/bin/env python3
"""
Docker entrypoint script for music-recommendations.
Handles file path mapping between container and host volumes.
"""

import os
import sys
import shutil
import subprocess

def main():
    # Define paths
    data_dir = "/app/data"
    input_file = os.path.join(data_dir, "input.txt")
    local_input = "/app/input.txt"
    
    output_file = "/app/output.txt"
    outroot_file = "/app/outroot.txt"
    
    data_output = os.path.join(data_dir, "output.txt")
    data_outroot = os.path.join(data_dir, "outroot.txt")
    
    # Check if running in interactive mode
    interactive_mode = len(sys.argv) > 1 and "-i" in sys.argv
    
    if not interactive_mode:
        # File mode: copy input file from data volume to working directory
        if os.path.exists(input_file):
            shutil.copy2(input_file, local_input)
            print(f"Using input file from: {input_file}")
        else:
            print(f"Error: Input file not found at {input_file}")
            print("Please ensure input.txt exists in your mounted data directory.")
            sys.exit(1)
    
    # Run the original musicrecs.py script
    try:
        result = subprocess.run([sys.executable, "musicrecs.py"] + sys.argv[1:], 
                              check=True, capture_output=False)
    except subprocess.CalledProcessError as e:
        print(f"Error running musicrecs.py: {e}")
        sys.exit(e.returncode)
    
    # Copy output files to data volume for host access
    if os.path.exists(output_file):
        shutil.copy2(output_file, data_output)
        print(f"Output file saved to: {data_output}")
    
    if os.path.exists(outroot_file):
        shutil.copy2(outroot_file, data_outroot)
        print(f"Root analysis file saved to: {data_outroot}")
    
    print("Music recommendations completed successfully!")

if __name__ == "__main__":
    main()
