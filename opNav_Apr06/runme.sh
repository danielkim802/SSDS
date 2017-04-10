echo -e "#######################################################\n"
echo -n "Initializing IVPort..."
sudo python init_ivport.py
echo -e "done."
echo -e "Checking if IVPort and PiCamera modules are detected...\n"
i2cdetect -y 1
vcgencmd get_camera
echo -e "\n----> You should be getting both '0x70'and '0x64' as the"
echo -e "----> addresses of 'ivport v2' and 'camera module v2'."
echo -e "----> Also, 'supported' and 'detected' must be 1."
echo -e "----> If not, try 'rpi-update'.\n"

echo -e "Running 'main.py'...\n"
#sudo python main.py

# Test code for IVPORT
sudo python test_ivport_quad.py
