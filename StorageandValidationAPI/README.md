# Storage and ValidationAPI

A simple system to upload and track inventory batches using Python, Rails API, and MongoDB.

## Tools Used
- Ruby on Rails (API server)
- MongoDB (Database)
- Python (Client script)

## Files that I coded and a brief explanation

`app/controllers/inventory_uploads_controller.rb` - Handles API requests: saves uploaded inventory and lists batches

`app/models/inventory_unit.rb` - Defines the inventory item model (fields: name, quantity, price, batch_id)

`config/routes.rb` - Connects API URLs to the controller actions ('POST' and 'GET')

`pythonclient/inventory_client.py` - Python client: generates CSV, uploads data, or lists uploads

## How to run

1. Start MongoDB server - open cmd and run `mongod`
1. Run Rails API server - Open cmd in `\StorageandValidationAPI` and run `rails s`
1. Run `python3 inventory_client.py` - You will be asked: Generate CSV, Upload CSV to API, List uploaded batches

## Client capabilities
1. Generate Inventory File:  
   Run the Python script and select the coresponding option to generate an `inventory.csv` file containing the inventory data.
1. Upload to Rails API:  
   Upload the generated `inventory.csv` file to the Rails API. The API will save the inventory data to MongoDB.
1. View Uploads:  
   After uploading, you can list all the uploads, which will display the following details for each batch:
   - batch_id
   - Number of units
   - Average price per item
   - Total quantity of items

## Check results
You can view saved inventory in MongoDB: Run in cmd:
```bash
mongosh
> use inventory_api_development
> db.inventory_units.find().pretty()
```

You can also view saved inventory at 'http://localhost:3000/inventory_uploads.json'

## Notes
Make sure MongoDB and Rails server are running before using the Python script