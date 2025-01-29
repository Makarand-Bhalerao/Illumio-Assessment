import os
# Function to read the lookup table and populate lookup_dictionary
def read_lookup_table(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Lookup table file not found at: {file_path}")
    # Dictionary to store port/protocol and tags combination
    lookup_dictionary = {}

    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("dstport"):
                continue
            # Parse each line of the csv file into a list
            parts = line.strip().split(",")
            if len(parts) == 3:
                dstport, protocol, tags = parts
                key = (int(dstport), protocol.lower())
                # Incase tags map to more than one port/protocol combinations
                # Assumption made is if two tags map to a port/protocol combination they will be separated by ";" delimiter
                #lower all the tags for case insensitive matching
                tags_list = [tag.strip().lower() for tag in tags.split(";")]
                if key not in lookup_dictionary:
                    lookup_dictionary[key] = []
                lookup_dictionary[key].extend(tags_list)
            # If any entry in the lookup table is not in specified format skip it
            else:
                print(f"Error: Skipping line : {line.strip()} , invalid format")
                continue
    # Check if lookup table is empty
    if not lookup_dictionary: 
        raise ValueError("The lookup table is empty. Please provide a valid lookup table.")
    return lookup_dictionary

# Function to read the flow log file and update counts and port_protocol
def read_flow_log(file_path, lookup_dictionary, counts, port_protocol):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f" file not found at: {file_path}")
    # Protocol mapping to extract various protocols from flow logs data
    protocol_mapping = {
        "1": "icmp",
        "6": "tcp",
        "17": "udp",
        "50": "esp",
        "51": "ah",
        "47": "gre",
        "58": "icmpv6",
        "89": "ospf",
        "-": "unknown"
    }

    # To check if log file contains records
    file_processed = False
    with open(file_path, "r") as file:
        for line in file:
            fields = line.split()
            if len(fields) >= 8:
                file_processed = True
                # Extract dstport and protocol from the flow log
                dstport = fields[6]
                protocol_code = fields[7]
                # If the dstport or protocol was not computed skip the record
                if dstport == '-' or protocol_code == '-':
                    continue

                protocol = protocol_mapping.get(protocol_code, "unknown")

                key = (int(dstport), protocol)
                # Count port/protocol combination
                port_protocol[key] = port_protocol.get(key, 0) + 1

                # Check if key exists in lookup_dictionary
                tags = lookup_dictionary.get(key)
                if tags:
                    for tag in tags:
                        counts[tag] = counts.get(tag, 0) + 1
                else:
                    counts["untagged"] = counts.get("untagged", 0) + 1 
            else:
                print("Incomplete record for default format")
                continue

        # If log file was empty raise error
        if not file_processed:
            raise ValueError("The log file is empty. Please provide a valid log file.")

# Function to write the output to the specified file
def write_output(file_path, counts, port_protocol):
    try:
        with open(file_path, "w") as output_file:
            output_file.write("Tag counts:\n")
            for tag, count in counts.items():
                output_file.write(f"{tag}: {count}\n")

            # Write port/protocol combination counts to the output file
            output_file.write("\nPort/Protocol combination counts:\n")
            for key, count in port_protocol.items():
                output_file.write(f"{key[0]},{key[1]},{count}\n")
    except FileNotFoundError:
        raise FileNotFoundError(f"Output file path is invalid or directory does not exist: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied while trying to write to: {file_path}")
    except Exception as exception:
        raise Exception(f"An unexpected error occurred while writing to the file: {exception}")

# Main function to execute the workflow
def main():
    try:
        look_up_filepath = input("Enter the path from where lookup table is to be fetched: ").strip()
        flowlog_file_path = input("Enter the path from where flow log file is to be fetched: ").strip()
        output_file_path = input("Enter the path where generated output file is to be stored: ").strip()

        lookup_dictionary = read_lookup_table(look_up_filepath)
        # Dictionary to store count of each tag
        counts = {}
        port_protocol = {}

        read_flow_log(flowlog_file_path, lookup_dictionary, counts, port_protocol)
        write_output(output_file_path, counts, port_protocol)
        print(f"Output successfully written to: {output_file_path}")

    except FileNotFoundError as incorrect_path:
        print(f"Error: {incorrect_path}")
    except PermissionError as permissionerror:
        print(f"Error: {permissionerror}")
    except ValueError as value_error:
        print(f"Error: {value_error}")
    except Exception as exception:
        print(f"An unexpected error occurred: {exception}")

if __name__ == "__main__":
    main()
