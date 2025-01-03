# Property Management API

This is a simple property management system API built using FastAPI. It allows users to create property listings, search properties based on different filters, and manage their property portfolios.

## Features

- **Create Property Listing**: Users can add a new property listing with details like location, price, type, description, and amenities.
- **Search Properties**: Users can search properties based on various criteria like price range, location, and property type with pagination support.
- **Shortlisted Properties**: Users can manage their shortlisted properties.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (for running the server)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/harshagarwal13/propertylisting.git
2. Navigate to the project directory:

    ```bash
   cd property-management-api
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
   
4. Run the uvicorn application:

    ```bash
   uvicorn app.main:app --reload

You can use the APIs when you will go to /docs