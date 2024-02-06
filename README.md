# OpenPayments-Web-Application

## Overview

The OpenPayments Web Application is a Django-based web application that allows users to import, search, and analyze data related to payments made to healthcare professionals. It leverages the Open Payments API and Dataset Downloads provided by the Centers for Medicare & Medicaid Services (CMS).

## Features

- Import the most recent year's Open Payments data.
- Regularly check for and update the data.
- Build a search tool with a typeahead for easy data retrieval.
- Export search results to an Excel file.

## Getting Started

### Prerequisites

- Python 3.9
- Pipenv (for virtual environment management)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/openpayments-webapp.git
   cd openpayments-webapp
   ```
2. Clone the repository:
   ```bash
   pipenv install
   ```
3. Activate the virtual environment:
   ```bash
   pipenv shell
   ```
4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
5. Run crons to fill up database:
   ```bash
   python manage.py runcrons
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```
7. Go to [http://localhost:8000/paymentswebapp/search/](http://localhost:8000/paymentswebapp/search/)
    
License
This project is licensed under the MIT License.

Acknowledgments
Thanks to the Centers for Medicare & Medicaid Services (CMS) for providing the Open Payments API and Dataset Downloads.
