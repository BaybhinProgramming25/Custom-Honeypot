import time
import re
from kibana_post import post_to_kibana

# Keep a set of processed_entries to ensure no duplicates
processed_jsons = set()

# Parse the timestamp
def parse_timestamp(line):
    return line[:10]

# Parse the ip address 
def parse_ip(line):
    pattern = r'\[(?:[^\]]*,){2}(?P<ip>\d+\.\d+\.\d+\.\d+)'

    # Search for the IP address
    match = re.search(pattern, line)

    if match:
        ip_address = match.group('ip')
        return ip_address
    return ""

# Call different functions to do different things  
def parse_log_line(line):

    timestamp_str = parse_timestamp(line)
    ip_str = parse_ip(line)

    # Dont accept the ip_str
    if len(ip_str) == 0:
        return None 
    
    # Create a unique string as sort of our identifier 
    combined_str = timestamp_str + " " + ip_str

    if combined_str not in processed_jsons:

        # Add it to the set 
        processed_jsons.add(combined_str)
    
        # Final Json
        log_data = {
            "timestamp": timestamp_str,
            "ip_address": ip_str,
        }

        return log_data
    return {}

def follow_log(file_path):
    try:
        with open(file_path, 'r') as file:
            # Move the pointer to the end of the file so we avoid reading old data and read new data directly 
            file.seek(0, 2)
            
            while True:
                # Read the next line (blocking until a new line is available)
                line = file.readline()
                
                if line:
                    parsed_data = parse_log_line(line.strip())
                    if not parsed_data:
                        # Empty JSON so we just continue
                        continue 
                    else:
                        # Send this to Kibana 
                        post_to_kibana(parsed_data)
                else:
                    # If no new line, wait for a while and check again
                    time.sleep(0.1)
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Define the path to the cowrie.log file
    log_file_path = '/mnt/honeypot-log/cowrie.log'
    follow_log(log_file_path)
