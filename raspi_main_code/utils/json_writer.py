import json

class JSONHandler:
    def __init__(self, source):
        """
        Initialize the JSONHandler with either a file path or a dictionary.

        if isinstance(source, str):
        :type source: str or dict
        """
        if isinstance(source, str):  # If the source is a file path
            with open(source, 'r') as json_file:
                self._data = json.load(json_file)
        elif isinstance(source, dict):
            self._data = source
        else:
            raise ValueError("Source must be a file path (str) or a dictionary.")

    def get(self, key, default=None):
        """
        Get the value of a key safely.
        Returns `default` if the key doesn't exist.
        """
        return self._data.get(key, default)

    def update(self, key, value):
        """
        Update or add a new key in the JSON data.
        """
        self._data[key] = value

    def save(self, file_path):
        """
        Save the data back to a JSON file.
        """
        with open(file_path, 'w') as json_file:
            json.dump(self._data, json_file, indent=4)


# # Example Usage
# file_path = "parameters.json"
#
# # Create a sample dictionary to simulate the file
# sample_data = {
#     "parameter1": "value1",
#     "parameter2": 42,
#     "parameter3": True
# }
#
# # Create the JSONHandler instance with the dictionary
# handler = JSONHandler(sample_data)
#
# # Access a value safely using `get()`
# print(handler.get("parameter1"))  # Output: value1
#
# # Update a value
# handler.update("parameter1", "updatedValue")
# handler.update("newParameter", "newValue")
#
# # Print updated data
# print(handler.get("parameter1"))  # Output: updatedValue
# print(handler.get("newParameter"))  # Output: newValue
#
# # Save the updated data to the file
# handler.save(file_path)
