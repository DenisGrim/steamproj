input_file = "tags.txt"
output_file = "clean_tags.txt"

seen = set()

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:

    for line in infile:
        tag = line.strip()
        if tag and tag not in seen:
            seen.add(tag)
            outfile.write(tag + "\n")
