# Rhino RMCS-2303 & Rhino Motors – Modbus ASCII Setup & Control + Ros2 Teleoperation setup

This project documents the complete setup and control process for Rhino RMCS-2303 Digital Servo Motor Drivers and Rhino High-Precision Servo Motors on Linux (Ubuntu), with a focus on Modbus ASCII communication using Python.

It provides:

  1.Hardware wiring guides for connecting RMCS-2303 to USB-to-TTL converters (CP2102) and Rhino motors.
  
  2.Instructions for assigning Modbus slave addresses and configuring driver parameters via the Rhino Motor Configuration Tool (Windows).
  
  3.Linux setup steps for Python control, including required packages and communication settings.

  4.Assigning of Slave ID to Motor Drivers.

  5.Working Modbus ASCII control scripts to set motor speed, acceleration, and direction directly from Python.

Hardware Requirements:
---

1.RMCS-2303 drivers

2.Rhino servo motors

3.CP2102  USB-to-TTL adapter

4.Power supply for motors

5.Windows PC for initial configuration

6.Ubuntu PC for control

7.Jumper wires


 Software Requirements:
---
1.  Rhino DC Servo Config (Download From Robokits)
   

Wiring Connection:
---

  ![Screenshot 2025-08-09 070010](https://github.com/user-attachments/assets/28536727-0c2d-48cb-8dca-48efa416d777)
  
Assigning Modbus Slave Address:
---

  Step-by-step for using Rhino Motor Configuration Tool on Windows:

  1.Connect CP2102 to driver(Use the above Circuit diagram)
  
  2.Assign unique Slave IDs to each motor driver (Modbus Slave Address Assign different slave address for each Motor)

  ![Screenshot 2025-08-05 055026 (1)](https://github.com/user-attachments/assets/a96a07b1-5225-4d1e-8ab0-a0726a318140)

  3. Operation Mode = Digital Speed Control

  4. Write Parameters

Ubuntu Setup:
----
1. Connect The CP2102 to the Ubuntu Laptop
   
2. Install the Following Packages 
   
        sudo apt update
        sudo apt install python3-pip
        pip3 install pyserial minimalmodbus

3. Check the port address of CP2102
   
        ls /dev/ttyUSB*

4.  change the slave address in the code in frames (0x09) to your slave address and also in stop_frame(0x09).

5.  Run the Python code:

        python3 single_motor.py
    
6. Change The Motor Direction  to ClockWise or Anti Clockwise in frames Section
        
         CW enable = 0x0101
         CCW enable = 0x0109

Ros2 Setup & Teleoperation 
----
1. Install Ros2 Humble and Source 

2. Open a terminal and create a directory

        mkdir -p ./teleop_ws/src

3. Open the directory

       cd teleop_ws/src

4. Create & edit python file 

       touch teleop.py
       nano teleop.py

5. Copy and paste the teleop.py from the github repository

6. Make it Executable using 

        chmod +x teleop.py
      ### Or Else you can build the package in the src folder of the workspace 

7. Open a teminal and source the workspace 

          cd teleop_ws/src
          source install/setup.bash

8. Run the python file either using ros2 or Python3
           
          python3 teleop.py

9. Open new Terminal and run teleop_twist_keyboard

            ros2 run teleop_twist_keyboard teleop_twist_keyboard 

10. In your Keyboard press the following buttons displayed in the screen.


11. You can use the same python file to receive velocity/cmd for autonomous navigation.(Create a package and then add the python file and build using colcon build)
   










References:
---
##DataSheet
https://robokits.download/downloads/RMCS-2303%20updated%20datasheet.pdf

##Configuration Software
https://robokits.co.in/motor-drives-drivers/encoder-dc-servo/rhino-dc-servo-driver-10v-30v-50w-5a-compatible-with-modbus-uart-ascii-for-encoder-dc-servo-motor?srsltid=AfmBOorf4oCw3-fyqpk-_24beLDRS_gAD10JJI-YQoMn7oCLBttM9KNZ



  
