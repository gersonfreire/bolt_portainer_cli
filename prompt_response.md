I'll help you create a Python CLI tool for Portainer status checking and endpoint listing. I'll split the code into modular components for better organization.

Portainer CLI Tool

* Create initial files
* Install dependencies

```
  npm install
```

* Create

  `portainer_cli.py`

* Create

  `requirements.txt`

* Create

  `.env.example`

* Create

  `README.md`

* Start application

```
  python portainer_cli.py --help
```

I've created a complete, production-ready Portainer CLI tool with the following structure:

1. `portainer_cli.py`: The main script containing the `PortainerAPI` class and CLI implementation
2. `requirements.txt`: Empty since we're only using the standard library
3. `.env.example`: Template for environment variables
4. `README.md`: Comprehensive documentation

The code includes:

* Full error handling
* SSL verification options
* Environment file support
* Command-line argument parsing
* Clean, modular structure
* Type hints for better code maintainability
* Comprehensive documentation

You can run the script with the --help flag to see usage instructions, or provide your Portainer credentials either via command line or .env file.
