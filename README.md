"# ST-to-Python-Transpiler

A comprehensive tool for converting Structured Text (ST) programs from B&R Automation Studio to Python code.

## 🚀 Features

- **Automated ST to Python Conversion**: Transpiles Structured Text code to equivalent Python implementations
- **Library Mapping**: Maps B&R function blocks to Python equivalents using AI assistance
- **Documentation Integration**: Extracts and processes PDF documentation for function mapping
- **1:1 Code Translation**: Direct translation preserving original logic structure
- **Modular Architecture**: Separate libraries for different control domains (Ramp Control, Signal Processing, etc.)

## 📁 Project Structure

```
ST-to-Python-Transpiler/
├── 1to1_replace/           # Direct 1:1 translations
├── AS Projekti/            # Original Automation Studio projects
├── Dokumentacija/          # B&R documentation PDFs
├── py_libs/               # Python library implementations
├── Python/                # Transpiler scripts and tools
│   ├── skripte/          # Core transpilation scripts
│   ├── outputs/          # Generated files and logs
│   └── testiranje/       # Testing utilities
└── README.md
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/cetko4/ST-to-Python-Transpiler.git
cd ST-to-Python-Transpiler
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Basic Transpilation

1. Configure your project paths in `Python/skripte/config.py`
2. Run the main transpilation pipeline:
```bash
python Python/skripte/make.py
```

### Testing Different Projects

Use the test script to switch between different B&R projects:
```bash
# For RampController project
python Python/testiranje/test.py 1

# For SignalTools project  
python Python/testiranje/test.py 2
```

## 🧩 Components

### Core Scripts

- **`compare_functions.py`**: Extracts and compares function calls between ST and Python
- **`api_req.py`**: Uses AI to map ST function blocks to Python implementations
- **`replace.py`**: Performs code replacement and generation
- **`make.py`**: Orchestrates the complete transpilation pipeline

### Libraries

- **RampController**: Implements ramp control and deadband filtering
- **SignalLib**: Signal processing, limiting, and integration functions
- **ArUser**: User authentication and role management

## 🔧 Configuration

Edit `Python/skripte/config.py` to set your project paths:

```python
FILE_PATH_PROGRAM = 'path/to/your/program.st'
FILE_PATH_FUN = 'path/to/your/library.fun'
FILE_PATH_PY_LIB = 'path/to/output/library.py'
# ... other paths
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- B&R Automation for the Automation Studio platform
- Contributors to the open-source Python ecosystem" 
