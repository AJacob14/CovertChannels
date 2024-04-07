# Covert Channels

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

## Installation

To install the project, clone the repository and run the following command: `pip install -r requirements.txt`. 
Once the requirements are installed, run the following command to install the project: `pip install .`. Once the project
is installed, run the following command to start the GUI: `python3 ./Gui.py`.