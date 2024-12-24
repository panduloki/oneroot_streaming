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
        
        # Ensure self._data is a dictionary
        if not isinstance(self._data, dict):
            raise ValueError("JSONHandler: The loaded data is not a dictionary.")
        
    def get_value_from_key(self, key, default=None):
        """
        Get the value of a key safely.
        Returns `default` if the key doesn't exist.
        """
        
        try:
            if key not in self._data:
                raise KeyError(f"Key '{key}' not found in the dictionary {self._data} JSON data.")
            else:
                print(f"Getting value from Key '{key}' from json  successfully.")
                return self._data.get(key, default)
            
        except KeyError as e:
            print(f"Error get_value_from_key JSON data: {e}")
            

    def update_value_to_key(self, key, value):
        """
        Update the value of an existing key in the JSON data.
        Raise an error if the key does not exist.
        """
        try:
            if key not in self._data:
                raise KeyError(f"Key '{key}' not found in the dictionary {self._data} JSON data.")
            else:
                self._data[key] = value
        except KeyError as e:
            print(f"Error update_value_to_key JSON data: {e}")
        else:
            print(f"Key '{key}'= value '{value}' in json updated successfully.")

    def save_json_file(self, file_path):
        """
        Save the data back to a JSON file.
        """
        try:
            with open(file_path, 'w') as json_file:
                json.dump(self._data, json_file, indent=4)
            print(f"JSON data successfully saved to {file_path}.")
        except IOError as e:
            print(f"Error saving JSON data to file: IOError {e}")
        except Exception as e:
            print(f"Error saving JSON data to file: {e}")


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
