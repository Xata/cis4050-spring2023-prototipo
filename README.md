# cis4050-spring2023-prototipo

This project is a prototype for a Fire Extinguisher Management System, created as part of the CIS4050 class during the Spring 2023 semester. Our group was called Team Asti, hence why we used prototipo (that's prototype in Italian). The prototype demonstrates the basic functionality of the application, which is designed to help manage and maintain fire extinguishers in a variety of settings. Users can add, edit, and delete extinguishers, as well as track maintenance and inspections through a ticketing system. This prototype serves as a proof-of-concept for the larger project, which aims to provide a comprehensive solution for campus fire safety management.

## Disclaimer

This Fire Extinguisher Management System prototype was developed as a student project for the CIS4050 class, and is intended for demonstration and educational purposes only. The scenarios and data used in this project are hypothetical, and do not represent any real-world organizations, situations, or data.

## Table of Contents

- [Disclaimer](#disclaimer)
- [🤔 Assumptions](#🤔-assumptions)
- [🚀 App Features](#🚀-app-features)
    - [🛣️ Roadmap](#🛣️-roadmap)
- [Requirements](#requirements)
    - [Windows 10 Environment Setup](#windows-10-environment-setup)
- [📖 Usage](#📖-usage)
    - [🐍 Backend Debug Demo](#🐍-backend-debug-demo)
- [📚 Resources](#📚-resources)

## 🤔 Assumptions

Here are some assumptions that the Fire Extinguisher Management System prototype is based on in its current version:

- 🔲 The warehouse is represented by the box with the ID of 1 in the database
- 🧐 The user has access to all data for each fire extinguisher, including the location, type, and inspection history
- 👀 All user types can view all components of the system, including fire extinguishers, inspections, and maintenance records
- ❌ No data can be deleted from the database, but it can be deactivated to prevent accidental removal
- 🏌️ User must login to use the application

## 🚀 App Features

The project is in the early stages of development but the current features include:

- 📊 The initial data model has been defined 
- 📝 Basic CRUD (Create, Read, Update, Delete) operations have been implemented
- 🔐 Users can authenticate
- ✏️ Users can modify objects within the database

### 🛣️ Roadmap

Here's a rough roadmap of the next steps for the Fire Extinguisher Management System prototype:

- ✅ Complete basic application functionality (current version)
- 🚀 Implement Single Sign-On (SSO) and Azure AD integration for enhanced security
- 🐳 Containerize the application using Podman for easier deployment
- 🛡️ Implement error checking and exception handling for improved stability
- 🎨 Generate front-end code for a user-friendly interface

## Requirements
- Python 3.11.3 or higher
- Visual Studio Code with the Python extensions

Before using this Fire Extinguisher Management System prototype, please ensure that you have installed Python 3.11.3 or a higher version, as well as Visual Studio Code with the Python extensions. This will ensure that you have all the necessary tools to run and edit the application.

### Windows 10 Environment Setup
To create the virtual environment needed for development and running the application in its current state please follow these steps:
1. Open PowerShell and navigate to the directory where venv will need to be. This is usually put in the backend folder.

2. Type the following command to create a new virtual environment:
    ```powershell
    python -m venv venv
    ```

3. Activate the virtual environment by running this command:
    ```powershell
    .\backend\venv\Scripts\Activate.ps1
    ```
    Note: Sometimes PowerShell commands block executing scripts. You may have to type this command if allowed:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    ```

4. Once venv is activated you need to install the required libraries with pip:
    ```powershell
    pip install -r requirements.txt
    ```

5. You should be ready to go and run the backend from main.py!

## 📖 Usage

### 🐍 Backend Debug Demo
1. To access the backend application, open your web browser and navigate to: http://127.0.0.1:8083/docs
2. The default username is: admin@example.com and the password is: $TeamAsti2023
    - 🔧 One of the things to finish is to make the application more modular. Currently, all the test data is hard coded. You can find the default admin credentials in:
        ```python
        config.py
        ```

## 📚 Resources

Here are some resources that we used when making the current iteration of the Fire Extinguisher Management System prototype:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Python documentation](https://docs.python.org/3/)
- [Pydantic documentation](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/14/)
- [SQLite documentation](https://www.sqlite.org/docs.html)



