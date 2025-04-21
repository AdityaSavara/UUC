import re

###This python script was used to add in "ae" entry for any case where "ae" entry was missing and "en" entry was present.
###Could be useful for adding in more languages, in future.
filename = "Units.txt"
output_filename = "Updated" + filename

# Read the file
with open(filename, "r", encoding="utf-8") as file:
    lines = file.readlines()

updated_lines = []

# Process each line
for line in lines:
    if "en: '" in line and "ae:" not in line:  # Find exact "en:" format and check if "ae:" is missing
        updated_line = re.sub(r"(en: '([^']+)')", r"\1, ae: '\2'", line)  # Insert "ae" directly after "en"
    else:
        updated_line = line  # Keep unchanged if no "en:" or "ae:" is already present

    updated_lines.append(updated_line)

# Write back to a new file
with open(output_filename, "w", encoding="utf-8") as file:
    file.writelines(updated_lines)

print(f"File modification complete. Saved as {output_filename}")
