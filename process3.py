import json
import xmltodict
import openai
from gpt4all import GPT4All

# Load and parse an XML file into JSON
def parse_file_xml(xml_path):
    with open(xml_path, "r", encoding="utf-8") as file:
        data_dict = xmltodict.parse(file.read())
    return data_dict


def convert_json_to_xml(json_data, example_xml):
    client = openai.OpenAI()  # ✅ New way to initialize the client

    prompt = f"""
    Convert the following JSON into XML in the same format as the example below.

    ## Example XML Format:
    {example_xml}

    ## JSON Data to Convert:
    {json.dumps(json_data, indent=4)}

    Provide only the XML output.
    """

    response = client.chat.completions.create(  # ✅ Updated API method
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You are an XML conversion assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=3000
    )
    return response.choices[0].message.content  # ✅ Updated way to access output


# Step 1: Parse Source XML File into JSON
source_json = parse_file_xml("Source.xml")
print("Extracted JSON:\n", json.dumps(source_json, indent=4))

# Step 2: Load Example Target XML Format
with open("Target.xml", "r", encoding="utf-8") as file:
    example_xml_format = file.read()

# Step 3: Convert JSON to Required XML Format
final_xml_output = convert_json_to_xml(source_json, example_xml_format)

# Step 4: Save the Final XML Output to a File
def save_xml(xml_string, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(xml_string)
    print(f"✅ XML file saved as {filename}")

save_xml(final_xml_output, "formatted_output.xml")

# Step 5: Print Final XML Output
print("\n✅ Final Converted XML:\n", final_xml_output)