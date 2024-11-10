please according the following text, please generate the entire python source code of the project:

Portainer command line interface tool for Status Checker and List endpointsA simple Python script command line interface to check the status and list endpoints of a Portainer server using its API.

Features - Authentication with Portainer server - Retrieves server status information -Retrieve server endpoints - Uses only Python standard library (no external dependencies) - Supports both HTTP and HTTPS connections - Optional SSL verification - Supports configuration via command line arguments or .env file ## Usage ### Command Line

```
python portainer_cli.py <portainer_url> <username> <password> [--verify-ssl]
```

Examples:

```
# For HTTP connection
python portainer_cli.py http://portainer.example.com admin mypassword

# For HTTPS connection without SSL verification (default)
python portainer_status.py https://portainer.example.com admin mypassword

# For HTTPS connection with SSL verification
python portainer_status.py https://portainer.example.com admin mypassword --verify-ssl
```

### Environment FileAlternatively, you can create a `.env` file in the project directory with the following variables:

```
PORTAINER_URL=https://portainer.example.com
PORTAINER_USERNAME=admin
PORTAINER_PASSWORD=your_password
PORTAINER_VERIFY_SSL=false
```

Then simply run:

```
python portainer_cli.py
```

The script will automatically read the configuration from the `.env` file if no command line arguments are provided.

## OutputThe script will display:

- Authentication status - Portainer version - Instance ID ## Error HandlingThe script includes error handling for:
- Authentication failures - Network connection issues - SSL/TLS related issues - Invalid responses - Missing or incorrect command line arguments - Missing or invalid environment variables ## Security NoteBy default, SSL certificate verification is disabled to allow connections to servers with self-signed certificates. Use the `--verify-ssl` flag or set `PORTAINER_VERIFY_SSL=true` in the .env file to enable SSL certificate verification for production environments.

## Configuration Priority 1. Command line arguments (if provided) 2. Environment variables from .env file (if command line arguments are not provided)