# Illumio-Assessment

## Instructions to Run the Code
- Run the script using the command : python3 assessment.py<br>
- After running the program, when prompted, provide the file paths from where to fetch the lookup table csv file and flow log file and the filepath where you want to store the output file.<br>
- The script will process the files and generate the output showing tag counts and port/protocol combination counts.


## Assumptions made
- The program only supports default log format for version 2 and above
- The code was tested on default log format for version 2 and above
- In case two tags map to the same port/protocol combination they will be separated by the delimiter ";"
- The code was tested on AWS VPC Flow logs format
- The flow log data only contains protocols which are listed in the protocol_mappings dictionary in the `read_flow_log` function
- The code supports only the protocols which are listed in the protocol_mapping dictionary, any other protocol is tagged as unknown

## Code Explanation

### 1. `read_lookup_table`
This function reads a CSV-based lookup table from the given file. The table maps **port/protocol** combinations to associated **tags**. Each line is parsed to extract:
- `dstport` (destination port),
- `protocol` (protocol type),
- `tags` (associated tags).

If the lookup table is empty or contains an invalid format, an error is raised.

### 2. `read_flow_log`
This function processes a **flow log file** and updates the following:
- **`counts`**: The count of each tag from the lookup table.
- **`port_protocol`**: The count of each **port/protocol** combination.

It extracts `dstport` and `protocol` from each log entry and checks the **`lookup_dictionary`** for associated tags.
- If tags are found, their counts are incremented.
- If no tags are found, the `"untagged"` count is incremented.

If the file is empty or in an invalid format, an error is raised.

### 3. `write_output`
This function writes the processed results to a specified output file. The output includes two sections:
- **Tag counts**: The count for each tag.
- **Port/Protocol combination counts**: The count for each **port/protocol** combination.

The function also handles errors like invalid file paths, permission issues, or any other unexpected failures during the write process.


