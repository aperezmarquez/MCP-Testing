# MCP - Pizza Restaurant

This project is just for testing the MCP technology, using as an excuse a college assignment. I created an MCP (Model Context Protocol) server for a pizza restaurant with a quick and shitty back-end using python and mysql.

<details>
<summary>Table of contents</summary>

    - [About](#about-the-project)
    - [Installation](#installation)
    - [Run the client](#run-the-client)

</details>

## About the project

This project is not a good or elaborate project, is just a testing area for MCP. I used the next architecture:

![MCP architecture](/imgs/MCP-Arquitectura.png)

## Installation

> [!IMPORTANT]
> Python3 is needed to run this project.

To run this project, you need to create a new virtual environment and install the dependencies.

- To create a virtual environment:
```bash
cd MCP

python3 -m venv myenv

source myenv/bin/activate
```

- Once the venv is created and activated, install the dependencies:
```bash
pip install -r requirements.txt
```

- When the dependencies are installed, create a .env file:
```bash
touch .env

echo "DB_USER=user" >> .env
echo "DB_PASSWORD=pass" >> .env
echo "DB_NAME=db" >> .env

echo "ANTHROPIC_API_KEY=apikey" >> .env
```

- Now all left is run the server. If you need to deactivate the venv, run:
```bash
deactivate
```

## Run the client

To run the client all you need to do is run the following command:
```bash
python client.py ../server/mcp_pizza_server.py
```

Now you can start chatting with Claude and see the changes it does inside MySQL.
