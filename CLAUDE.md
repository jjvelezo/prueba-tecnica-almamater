# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based RPA (Robotic Process Automation) technical test project that generates fake user credentials and handles user registration. The project consists of two main components:

1. **Credential Generator** (`generador_credenciales.py`) - Generates fake user data including names, emails, passwords, addresses, and phone numbers
2. **User Registration** (`registro_usuarios.py`) - Currently empty, intended for user registration functionality  
3. **Configuration Data** (`config.json`) - Contains generated user credentials in JSON format

## Development Environment

- **Python Version**: 3.11.0
- **Virtual Environment**: Located in `venv/` directory
- **Dependencies**: Uses `faker` library for generating fake data

## Key Architecture

### Data Generation System
The credential generator (`generador_credenciales.py`) uses a modular approach:
- `generar_contrasena()`: Creates secure passwords with customizable length and symbol inclusion
- `fecha_nacimiento_aleatoria()`: Generates realistic birth dates within age ranges
- `numero_celular_eeuu()`: Creates US-format phone numbers
- `generar_usuario()`: Orchestrates user data generation with consistent email format (`{name}.{surname}{index}@pruebatecnica.com`)

### Data Structure
User records contain:
- Personal info (name, surname, email, gender, birth date)
- Contact details (phone, address, city, state, zip, country)
- Authentication (password)
- Company affiliation

## Common Commands

### Environment Setup
```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies (if requirements.txt exists)
pip install faker
```

### Running the Application
```bash
# Generate new user credentials
python generador_credenciales.py

# Run user registration (when implemented)
python registro_usuarios.py
```

### Development Tasks
```bash
# Check Python version
python --version

# Install additional dependencies
pip install [package_name]

# Generate requirements file
pip freeze > requirements.txt
```

## File Structure
- `generador_credenciales.py` - Main credential generation logic
- `registro_usuarios.py` - User registration module (to be implemented)
- `config.json` - Generated user data storage
- `venv/` - Python virtual environment