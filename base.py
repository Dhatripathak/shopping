# from flask import Flask, jsonify
# # from pymongo import MongoClient
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# app = Flask(__name__)

# uri = "mongodb+srv://hashmap:gbqwF77TFjZu54pa@invoices.cfa4zkk.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# # Connect to MongoDB
# # client = MongoClient('mongodb+srv://hashmap:gbqwF77TFjZu54pa@invoices.cfa4zkk.mongodb.net/?retryWrites=true&w=majority')
# db = client['invoices']  
# collection = db['invoices']  

# # Define routes
# @app.route('/invoice', methods=['GET'])
# def get_invoice():
#     # Fetch data from MongoDB
#     invoice_data = collection.find_one()
#     # Return the data as JSON
#     print(invoice_data)
#     return jsonify(invoice_data)

# if __name__ == '__main__':
#     app.run(debug=True)
