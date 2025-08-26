# Copy and paste these to install

git clone https://github.com/username/repository-name.git
cd repository-name
wget -qO- https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.2/linux64/chrome-linux64.zip | busybox unzip -
wget -qO- https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.2/linux64/chromedriver-linux64.zip | busybox unzip -
sudo apt update
sudo apt install -y python3 python3-pip
pip install selenium

# Copy and paste these to provide permissions and run the script

chmod +x chrome-linux64/chrome
chmod +x chromedriver-linux64/chromedriver
python3 main.py