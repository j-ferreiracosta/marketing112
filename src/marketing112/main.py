import sys
import os
from dotenv import load_dotenv
load_dotenv()  
# Import the TextFileReader class
from marketing112.utils.util import TextFileReader

# Use the correct Crew class name
from marketing112.crew import MarketingInfoProductCrew

# Define the input filename (assuming it's in a 'knowledge' subdir)
INPUT_FILENAME = "inputs.txt" # Path relative to main.py

def run():
    """Reads raw text input using TextFileReader and kicks off the crew."""
    raw_text_input = ""
    try:
        # Construct the full path relative to the main.py script's location
        # Or use an absolute path if preferred
        script_dir = os.path.dirname(__file__)
        file_path = os.path.abspath(os.path.join(script_dir, INPUT_FILENAME))

        # Instantiate the reader
        reader = TextFileReader(filepath=file_path)

        # Read the raw content
        raw_text_input = reader.read_content()

    except FileNotFoundError:
        sys.exit(1) # Error message printed by reader
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    if not raw_text_input:
        print("Error: Input file was empty or could not be read.")
        sys.exit(1)

    # Prepare inputs dictionary for the crew
    # The key 'knowledge_base_text' must match what the first task expects
    crew_inputs = {
        'knowledge_base_text': raw_text_input
    }

    print("Raw text input loaded, kicking off the crew...")
    try:
      MarketingInfoProductCrew().crew().kickoff(inputs=crew_inputs)
      print("Crew finished.")
    except Exception as e:
      print(f"An error occurred during crew kickoff: {e}")
      # raise e

def train():
    """
    Train the crew for a given number of iterations.
    Note: Training inputs remain hardcoded for now. Needs adaptation
          if you want to train on unstructured text examples too.
    """
    print("Warning: Training function currently uses structured inputs.")
    print("Adaptation needed if training requires unstructured text examples.")
    train_inputs = {
        # These inputs don't match the new unstructured format.
        # You would need to provide example 'knowledge_base_text' strings
        # for training if you want the first agent to learn extraction.
        'topic': 'Marketing Automation for Enterprise',
        'customer_domain': 'crewai.com',
        'project_description': """
CrewAI, a leading provider of multi-agent systems... (rest of description)
"""
    }
    try:
        if len(sys.argv) < 2:
             print("Usage: python main.py train <number_of_iterations>")
             sys.exit(1)

        n_iterations = int(sys.argv[1])
        print(f"Starting training for {n_iterations} iterations...")
        # This training call might fail or behave unexpectedly if the crew
        # now expects 'knowledge_base_text' as the primary input.
        MarketingInfoProductCrew().crew().train(n_iterations=n_iterations, inputs=train_inputs)
        print("Training finished.")

    except ValueError:
         print("Error: The number of iterations must be an integer.")
         sys.exit(1)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

# --- Main Execution Block ---
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'train':
        sys.argv.pop(1) # Remove 'train' argument
        train()
    else:
        run()