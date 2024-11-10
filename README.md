# Portainer CLI Tool

A command line interface tool to check the status and list endpoints of a Portainer server using its API.

## Features

- Authentication with Portainer server
- Retrieves server status information
- Retrieve server endpoints
- Uses only Python standard library (no external dependencies)
- Supports both HTTP and HTTPS connections
- Optional SSL verification
- Supports configuration via command line arguments or .env file

## Installation

No installation required. Just clone the repository and ensure you have Python 3.6 or higher installed.

## Usage

### Command Line

```bash
python portainer_cli.py <portainer_url> <username> <password> [--verify-ssl]
```

Examples:

```bash
# For HTTP connection
python portainer_cli.py http://portainer.example.com admin mypassword

# For HTTPS connection without SSL verification (default)
python portainer_cli.py https://portainer.example.com admin mypassword

# For HTTPS connection with SSL verification
python portainer_cli.py https://portainer.example.com admin mypassword --verify-ssl
```

### Environment File

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your Portainer details:
   ```env
   PORTAINER_URL=https://portainer.example.com
   PORTAINER_USERNAME=admin
   PORTAINER_PASSWORD=your_password
   PORTAINER_VERIFY_SSL=false
   ```

3. Run the script:
   ```bash
   python portainer_cli.py
   ```

## Output

The script will display:
- Authentication status
- Portainer version
- Instance ID
- List of endpoints with their details

## Error Handling

The script includes comprehensive error handling for:
- Authentication failures
- Network connection issues
- SSL/TLS related issues
- Invalid responses
- Missing or incorrect command line arguments
- Missing or invalid environment variables

## Security Note

By default, SSL certificate verification is disabled to allow connections to servers with self-signed certificates. Use the `--verify-ssl` flag or set `PORTAINER_VERIFY_SSL=true` in the .env file to enable SSL certificate verification for production environments.

## Configuration Priority

1. Command line arguments (if provided)
2. Environment variables from .env file (if command line arguments are not provided)