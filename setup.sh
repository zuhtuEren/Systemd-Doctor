#!/bin/bash

# Systemd-Doctor v1.6.2 - Automated Setup Assistant

echo "------------------------------------------------"
echo "        Systemd-Doctor Installation             "
echo "------------------------------------------------"

# 1. Create Virtual Environment
echo "[*] Creating virtual environment (venv)..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create virtual environment. Please install python3-venv."
    exit 1
fi

# 2. Install Dependencies
echo "[*] Installing required libraries..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install rich InquirerPy
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies."
    exit 1
fi

# 3. Create Directories
echo "[*] Creating snapshots and data directories..."
mkdir -p snapshots
mkdir -p data

# 4. Create the 'doctor' Launcher Script
echo "[*] Generating the launcher script..."
cat << 'EOF' > doctor
#!/bin/bash
# Systemd-Doctor Launcher Script
# Automatically uses the virtual environment
SOURCE_DIR=$(dirname "$(readlink -f "$0")")
source "$SOURCE_DIR/venv/bin/activate"
python3 -m src.main "$@"
EOF

# 5. Set Permissions
chmod +x doctor
chmod +x setup.sh

echo "------------------------------------------------"
echo "Installation Successful!"
echo "------------------------------------------------"
echo "Usage Instructions:"
echo "1. Analyze system:   ./doctor --blame"
echo "2. Show dashboard:   ./doctor --summary"
echo "3. Full help:        ./doctor --help"
echo "------------------------------------------------"
