# Order-&-Inventory-Lite

Built a Sales Order & Inventory Management System where:
- Admin can manage products, inventory, and dealers
- Dealers can place orders for products

## Tech Stack

- python 3.14
- Dajngo 6.0
- Django Rest Framework 3.17
- SQLite
- RESTful JSON API's
- API testable : REST Client (vscode extension)

## Installation

Project can be installed and run in two ways:
1. Dev Containers with dind ( isolated debian container running a another django docker container inside)
- pre-requsite : [vscode](https://code.visualstudio.com/download) installed, [docker desktop](https://www.docker.com/products/docker-desktop/) installed
- just git clone the project or download and extract , open in vscode , click on the popup in vscode notification tray.

2. local Installation 
- you will to install [uv python package manager](https://docs.astral.sh/uv/getting-started/installation/)
- in your vscode terminal , run


```bash
cd backend
uv sync
cd src
uv run manage.py runserver
```

