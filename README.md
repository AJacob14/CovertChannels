# Covert Channels

## Table of Contents

- [Description](#description)
- [Quick Start](#quick-start)
  - [Step 1: Install Wireshark](#step-1-install-wireshark)
  - [Step 2: Install Python 3.12](#step-2-install-the-python-312)
  - [Step 3: Clone the Repository](#step-3-clone-the-repository)
  - [Step 4: Install the Required Packages](#step-4-install-the-required-packages)
  - [Step 5: Install the Project](#step-5-install-the-project)
  - [Step 6: Start the GUI](#step-6-start-the-gui)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
  - [WARNING: Wireshark is installed, but cannot read manuf !](#warning-wireshark-is-installed-but-cannot-read-manuf-)

## Description

This project is a visualization tool for covert channels. It is a GUI application that allows users to send and receive
messages using covert channels. The covert channels are separated into a client and server. The GUI starts the client 
and server in separate processes to simulate a covert channel. The GUI will send a message the user inputs to the client
and the client will send the message to the server using the specified covert channel. The server will then receive the
message and send it back to the GUI to display the message.

### Covert Channel Types

- IP ID: The IP ID covert channel uses the ID field in the IP header to send messages.
- TCP Port: The TCP Port covert channel uses the port field in the TCP header to send messages.
- UDP Port: The UDP Port covert channel uses the port field in the UDP header to send messages.
- HTTP Endpoint: The HTTP covert channel uses a specific endpoint on a web server to send messages.

## Quick Start

### Step 1: Install Wireshark

Wireshark can be downloaded from the [Wireshark website](https://www.wireshark.org/download.html).
Follow the instructions on the website to install Wireshark.

### Step 2: Install the Python 3.12

Python 3.12 can be downloaded from the [Python website](https://www.python.org/downloads/).

### Step 3: Clone the Repository

Clone the repository using the following command: `git clone https://github.com/AJacob14/CovertChannels.git`

### Step 4: Install the Required Packages

Navigate to the project directory and run the following command: `pip install -r requirements.txt`

### Step 5: Install the Project

Run the following command to install the project: `pip install .`

### Step 6: Start the GUI

Run the following command to start the GUI: `python3 ./Gui.py`

## Usage

### Step 1: Start the GUI

Run the following command to start the GUI: `python3 ./Gui.py`

### Step 2: Start Wireshark

Start Wireshark and select the loopback network interface to start capture packets on.

### Step 3: Select the Covert Channel

Select the covert channel you want to use from the dropdown menu.

### Step 4: Start the Covert Channel

Click the "Start" button to start the covert channel. The client and server will start in separate processes.

### Step 5: Send a Message

Enter a message in the text box and click the "Send" button to send the message using the covert channel.

### Step 6: Receive a Message

The server will receive the message and send it back to the GUI to display the message. (Not implemented yet)

### Step 7: Observe the captured packets in Wireshark

Observe the captured packets in Wireshark to see the covert channel in action.

## Troubleshooting

### WARNING: Wireshark is installed, but cannot read manuf !

This warning occurs when scapy cannot find the manuf file. To fix this issue, navigate to the wireshark directory and 
run this command: `tshark -G manuf > manuf`. This will generate the manuf file in the current directory. You may need 
administrator privileges to run this command in the Wireshark directory. You may also need to edit the manuf file to 
remove the last empty line in the file.
