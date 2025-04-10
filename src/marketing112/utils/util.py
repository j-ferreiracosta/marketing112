# utils/utils.py

import os

class TextFileReader:
    """Reads the entire content of a text file."""

    def __init__(self, filepath: str):
        """
        Initializes the TextFileReader.

        Args:
            filepath: The full path to the text input file.
        """
        self.filepath = filepath
        # Basic check, consider more robust path handling if needed
        if not os.path.exists(self.filepath):
             print(f"Warning: Filepath '{self.filepath}' provided to TextFileReader does not exist yet.")


    def read_content(self) -> str:
        """
        Reads and returns the entire content of the text file.

        Returns:
            A string containing the file's content.

        Raises:
            FileNotFoundError: If the input file cannot be found when read.
            Exception: For other potential I/O errors.
        """
        print(f"Attempting to read content from: {self.filepath}")
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"Successfully read content from {self.filepath}")
                return content
        except FileNotFoundError:
            print(f"Error: Input file not found at '{self.filepath}'")
            raise
        except Exception as e:
            print(f"An unexpected error occurred while reading '{self.filepath}': {e}")
            raise