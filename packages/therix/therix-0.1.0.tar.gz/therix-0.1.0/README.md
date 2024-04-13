# Therix

`therix` is a Python library designed to simplify and enhance your development experience. This initial version provides a handy function to add two numbers, demonstrating the ease of use and potential of the library.

## Features

- Simple and intuitive function to add numbers.
- Easily extensible for future features.

## Getting Started

### Installation

You can install `therix` directly from PyPI:

```sh
pip install therix
```

This command will install the latest version of `therix` along with its dependencies.

### Configuring Database Connection

To fully utilize `therix` in projects that interact with a database, you'll need to configure your database connection settings. This is done by setting the following environment variables:

- `THERIX_DB_TYPE`: The database type (e.g., `postgresql`, `mysql`). Default is `postgresql`.
- `THERIX_DB_USERNAME`: Your database username.
- `THERIX_DB_PASSWORD`: Your database password.
- `THERIX_DB_HOST`: The hostname of your database server.
- `THERIX_DB_PORT`: The port your database server listens on.
- `THERIX_DB_NAME`: The name of your database.

For development purposes, you can set these environment variables manually in your terminal session or use a `.env` file at the root of your project with the following content:

```plaintext
DB_TYPE=postgresql
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydatabase
```

Replace the placeholders with your actual database configuration details. If you're using a `.env` file, make sure to load it with a library like `python-dotenv` at the start of your application:

```python
from dotenv import load_dotenv

load_dotenv()
```

### Usage

Using `therix` is straightforward. Here's a quick example:

```python
from therix import add

result = add(5, 7)
print(f"The result is {result}")
```

## Development

`therix` is actively developed, aiming to introduce new features and improvements regularly. Contributions are welcome!

### Building From Source

To build `therix` from source:

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/therix.git
   ```

2. Navigate to the `therix` directory and install dependencies:
   ```sh
   pip install -e .
   ```

3. To build a distributable package:
   ```sh
   python setup.py sdist bdist_wheel
   ```

## Contributing

We welcome contributions! Please read our contributing guide located in the repository to see how you can participate in the development of `therix`.

## License

`therix` is made available under the MIT License. For more details, see the LICENSE file in the repository.

## Setting Up the Development Environment

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. Follow the steps below to set up your development environment.

### Prerequisites

Ensure you have Python installed on your system. This project requires Python version X.X (replace "X.X" with the specific version required for your project). You can download Python from [python.org](https://www.python.org/downloads/).

### Installing Poetry

Poetry provides an easy way to manage project dependencies. If you don't have Poetry installed, follow these steps to install it:

#### On macOS / Linux / BashOnWindows:

Open a terminal and run the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### On Windows (PowerShell):

Open PowerShell and run the following command:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### Configuring Poetry

After installation, ensure Poetry's `bin` directory is in your system's `PATH`. The installer will suggest how to do this on your specific system.

### Cloning the Project

If you haven't already, clone the project repository by running:

```bash
git clone <repository-url>
```

Replace `<repository-url>` with the URL of the project repository.

### Installing Project Dependencies

Navigate to the project directory:

```bash
cd path/to/project
```

Install the project dependencies by running:

```bash
poetry install

```
Install the project dev dependencies only by running:

```bash
poetry add --dev dependencies

```

This command creates a virtual environment and installs all the dependencies specified in the `pyproject.toml` file.

### Activating the Virtual Environment

To activate the project's virtual environment, run:

```bash
poetry shell
```

This command activates the virtual environment, allowing you to run project scripts and commands within the isolated environment.

To run the project, use the command:
```bash
poetry run -vvv python main.py
```

### Deactivating the Virtual Environment

When you're done working in the virtual environment, you can deactivate it by simply running:

```bash
exit
```

or by closing the terminal window.

