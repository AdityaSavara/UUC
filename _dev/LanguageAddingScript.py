import re
import json

###This python script was used to add in "ae" entry for any case where "ae" entry was missing and "en" entry was present.
###Could be useful for adding in more languages, in future.
import chardet #can be installed with pip install chardet

filename = "Units.txt"

with open(filename, "rb") as file:  # Read raw bytes
    raw_data = file.read()

encoding_info = chardet.detect(raw_data)
print(f"Detected encoding: {encoding_info['encoding']}")



# Sample JavaScript-like input string
js_data = """
{v: [1,0,0,0,0,0,0,0], id: 'm', name: {cz: 'metr', en: 'metre', ae: 'meter'}, k:1, SI: true, basic: true, prefix: 'all'},
{v: [0,1,0,0,0,0,0,0], id: 'kg', name: {cz: 'kilogram', en: 'kilogram'}, k:1, SI: true, basic: true, note: {
    cz: 'To protože kilogram se obtížně programuje, neboť samo "kilo" je předpona.',
    en: 'That\'s because kilogram is problematic to code, since the "kilo" itself is a prefix.'
}},
{v: [0,0,1,0,0,0,0,0], id: 's', name: {cz: 'sekunda', en: 'second'}, k:1, SI: true, basic: true, prefix: '-'},
{v: [0,0,0,1,0,0,0,0], id: 'A', name: {cz: 'ampér', en: 'ampere'}, k:1, SI: true, basic: true, prefix: 'all'},
{v: [0,0,0,0,1,0,0,0], id: 'K', name: {cz: 'kelvin', en: 'kelvin'}, k:1, SI: true, basic: true, prefix: 'all'}
"""
#We will actually read it from file a text file containing only the Units array, with square brackets removed.
#First tried with utf-8 coding, then tried changing.
with open("Units.txt", "r", encoding="utf-8") as file:
    js_data = file.read()


# Extract and store comments (single-line & multi-line)
comments = re.findall(r"(//.*|/\*.*?\*/)", js_data, flags=re.DOTALL)

# Remove comments from the string before processing
js_data_no_comments = re.sub(r"//.*|/\*.*?\*/", "", js_data, flags=re.DOTALL)

# Convert JavaScript-like syntax to valid JSON format
js_data_no_comments = re.sub(r"(\w+):", r'"\1":', js_data_no_comments)  # Convert keys to quoted strings
js_data_no_comments = re.sub(r"'", r'"', js_data_no_comments)  # Convert single quotes to double quotes
json_data = "[" + js_data_no_comments.strip() + "]"  # Wrap in an array

# Load JSON data
data = json.loads(json_data)

# Update entries
for entry in data:
    if "name" in entry and "en" in entry["name"] and "ae" not in entry["name"]:
        entry["name"]["ae"] = entry["name"]["en"]

# Convert back to JavaScript-like syntax
updated_js_data = json.dumps(data, indent=4).replace('"', "'")

# Restore comments at the end
for comment in comments:
    updated_js_data += "\n" + comment

#finally, save to a new file. We use the same encoding that was found to keep Cz letters.
with open("Updated" + filename, "w", encoding="utf-8") as file:
    file.write(updated_js_data)
