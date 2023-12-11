import json

def fix_json(file_path):
    try:
        # Try to load the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        print("JSON file is valid.")
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
        # Attempt to fix common JSON issues
        with open(file_path, 'r+') as file:
            file_contents = file.read()
            # Add a comma and closing bracket if missing
            if not file_contents.strip().endswith('}'):
                file.seek(0)
                file_contents = file_contents.rstrip(' \t\n\r,') + ',}'
                file.write(file_contents)
                file.truncate()
            elif not file_contents.strip().endswith(']'):
                file.seek(0)
                file_contents = file_contents.rstrip(' \t\n\r,') + ',]'
                file.write(file_contents)
                file.truncate()
        print("Attempted to fix the JSON file. Please check the file for correctness.")

# Replace 'your_file.json' with the path to your JSON file
fix_json('game_data_og.json')

def convert_json_to_jsonl(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as input_file:
            data = json.load(input_file)

        with open(output_file_path, 'w') as output_file:
            for item in data:
                json.dump(item, output_file)
                output_file.write('\n')

        print(f"Converted JSON to JSONL. Output file: {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

input_file_path = 'game_data_og.json'  # Replace with your actual JSON file path
output_file_path = 'game_data_og.jsonl'     # Replace with your desired JSONL file path

convert_json_to_jsonl(input_file_path, output_file_path)
