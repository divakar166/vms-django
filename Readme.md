# Vendor Management System
This is a Vendor Management System built with Django and Django Rest Framework, designed to handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Installation
1. Clone the repository
   ``` bash
   git clone https://github.com/divakar166/vms-django.git
   ```
2. Navigate to the project directory
   ``` bash
   cd vms-django
   ```
3. Create a virtual environment
   ``` bash
   python3 -m venv venv
   ```
4. Activate the virtual environment
   * On macOS and Linux
     ``` bash
     source venv/bin/activate
     ```
   * On Windows (PowerShell)
     ``` bash
     .\venv\Scripts\Activate
     ```
5. Install dependencies
   ``` bash
   pip install -r requirements.txt
   ```
6. Apply database migrations
   ``` bash
   python manage.py makemigrations vendors purchase_orders
   python manage.py migrate
   ```
7. Create a superuser
   ``` bash
   python manage.py createsuperuser
   ```
8. Start the development server
   ``` bash
   python manage.py runserver
   ```
9. Generate an authentication token
   * To access the API endpoints, you need to generate an authentication token for your user account.
   * Log in to the Django admin panel at http://localhost:8000/admin/ using the superuser credentials created in step 7.
   * Navigate to the "Token" section under "Authentication and Authorization" and click on "Add Token".
   * Select your user account from the dropdown list and click "Save". This will generate an authentication token for your user account.
10. Open your web browser and navigate to http://localhost:8000/admin/ to access the admin panel
11. You can also explore the API endpoints:
    * http://localhost:8000/api/vendors/ - API endpoint for managing vendors.
    * http://localhost:8000/api/vendors/{id}/performance - API endpoint for fetching vendor's performance.
    * http://localhost:8000/api/vendors/{id}/pos - API endpoint for fetching all purchase order's associated to vendor.
    * http://localhost:8000/api/vendors/{id}/historical_perf - API endpoint for fetching vendor's historical performances.
    * http://localhost:8000/api/purchase_orders/ - API endpoint for managing purchase orders.
    * http://localhost:8000/api/purchase_orders/{id}/acknowledge - API endpoint for acknowledging a purchase order.
    * http://localhost:8000/api/purchase_orders/{id}/complete - API endpoint for changing purchase order's status to completed.
    * http://localhost:8000/api/purchase_orders/{id}/cancel - API endpoint for changing purchase order's status to cancelled.

## Usage
1. Admin Panel
   * Use the Django admin panel at http://localhost:8000/admin/ to manage vendors, purchase orders, and historical performance records.
2. API Endpoints
   * Access the API endpoints for managing vendors, purchase orders, and historical performance data. Refer to the Installation section for the URLs.
   * Use Postman or ThunderClient to test APIs.
3. Authentication Token:
   * To make requests to the API endpoints, include the generated authentication token in the request headers:
     ``` bash
     Authorization: Token <your-authentication-token>
     ```

## Running Tests
To run the test suite for the Vendor Management System, follow these steps:
1. Activate the virtual environment if not already activated:
   ``` bash
   source venv/bin/activate   # On macOS and Linux
   .\venv\Scripts\Activate.ps1   # On Windows (PowerShell)
   ```
2. Run the test command:
   ``` bash
   python manage.py test
   ```
This command will execute all the test cases defined in the project and display the results in the terminal.

## Contributing
Contributions are welcome! Please feel free to fork the repository and submit pull requests to contribute new features, improvements, or fixes.
