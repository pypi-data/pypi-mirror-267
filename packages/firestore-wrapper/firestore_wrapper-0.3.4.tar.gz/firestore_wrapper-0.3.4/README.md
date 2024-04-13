# firestore-wrapper

`firestore-wrapper` is a custom Python wrapper designed to simplify and streamline operations with Google Firestore. By
abstracting the complexities of direct Firestore interaction, it provides an easier and more Pythonic way to work with
Firestore databases, including document management, querying, and batch operations.

## Features

- Simplified document addition, update, and retrieval
- Batch operations support
- Automated backup and restoration capabilities
- Customizable query methods

## Installation

Install `firestore-wrapper` using pip:

```bash
pip install firestore-wrapper
```

Ensure you have a Google Cloud project with Firestore enabled and service account credentials available.

## Quick Start

First, set up your Firestore credentials:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to IAM & Admin > Service Accounts.
3. Create a service account and download the JSON credentials file.

Next, initialize `FirestoreDB` with your credentials:

```python
from firestore_wrapper import FirestoreDB

# Path to your Firestore credentials JSON file
credentials_path = 'path/to/your/credentials.json'
database_url = 'your-database-url'  # Optional, if using a custom Firestore database

# Initialize the FirestoreDB instance
db = FirestoreDB(credentials_path=credentials_path, database=database_url)
```

### Adding a Document

```python
# Define your document data
data = {
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'signup_date': '2023-01-01'
}

# Add a document to the 'users' collection
document_name = db.add_document(collection_name='users', data=data, document_name='user_johndoe')
print(f'Document added with name: {document_name}')
```

### Retrieving a Document

```python
# Retrieve a document by name
user_document = db.get_document_data(collection_name='users', document_name='user_johndoe')
print(user_document)
```

### Updating a Document

```python
# Update a document with new data
update_data = {'email': 'new.email@example.com'}
db.update_document(collection_name='users', document_name='user_johndoe', data=update_data)
```

## Getting Help

If you encounter any issues or have questions about using `firestore-wrapper`,
please create an issue in the [GitHub repository](https://github.com/AntonioVentilii/firestore-wrapper/issues).

## Contributing

Contributions to `firestore-wrapper` are welcome!
Whether it's bug reports, feature requests, or code contributions, please feel free to make a contribution. For code
contributions, please:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

`firestore-wrapper` is released under the MIT License. See the LICENSE file for more details.
