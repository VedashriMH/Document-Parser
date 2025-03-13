import json
from lxml import etree

def xml_to_json(xml_file):
    """Converts an XML file to JSON format."""
    tree = etree.parse(xml_file)
    root = tree.getroot()

    def xml_to_dict(element):
        """Recursively converts an XML element and its children to a dictionary."""
        data = {}
        if element.text and element.text.strip():
            data["text"] = element.text.strip()
        for child in element:
            child_data = xml_to_dict(child)
            if child.tag in data:
                if isinstance(data[child.tag], list):
                    data[child.tag].append(child_data)
                else:
                    data[child.tag] = [data[child.tag], child_data]
            else:
                data[child.tag] = child_data
        return data

    json_data = {root.tag: xml_to_dict(root)}
    return json_data

def save_json(json_data, output_file):
    """Saves JSON data to a file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    input_xml = "Source.xml"  # Replace with your XML file
    output_json = "preprocessed.json"

    # Convert XML to JSON
    json_data = xml_to_json(input_xml)

    # Save JSON to a file
    save_json(json_data, output_json)

    print(f"Preprocessed JSON saved to {output_json}")
