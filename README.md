# Client Server SOcket

## Contents
* [Introduction](#introduction)
* [Setup](#setup)
* [Video](#Video)
* [Applied technologies and libraries](#applied-technologies-and-libraries)
* [Version History](#version-history)
* [License](#license)

## Introduction

This Python script demonstrates a simple client-server communication setup using sockets. The server provides essential functionalities, including server uptime, server information retrieval, a list of available commands, and user management. Users can have either admin or user rights, and the server allows sending and managing messages between clients. All data is stored in json files

## Setup

* To start the server and client in two separate terminal windows, follow these steps:

    * Open a terminal in the folder where the main.py and client.py files are located.
    * In the first terminal window, start the server by running the following command:

    ```
    py main.py
    ```

    * In the second terminal window, start the client by running the following command:

    ```
    py client.py
    ```

## Video

https://youtu.be/tgf30V91FGI

## Version History

### v0.1.0
* Initial release of the client-server socket application.
* Added server uptime, info, help, stop functionality.

### v0.1.5
* User management: creating and deleting users.
* User login and logout functionality.

### v0.2.0
* Enhanced messaging system:
    * Users can send messages to each other.
    * Users can delete their messages.
    * Users can view all messages and mark them as read.
    * Users can view a specific message and mark it as read.

* Improved error handling for user and messages commands

### v0.2.5
* Adding unit tests in modules related to users and sending messages

## Applied technologies and libraries

* Environment
    * Pyhton 3.10.7
    * Visual Studio Code 1.79

* Libraries
    * socket
    * json
    * datetime

## License

This project is open-source and available under the MIT License.




