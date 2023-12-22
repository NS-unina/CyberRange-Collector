import re
import sys
from datetime import datetime
import pytz

REGEX = r'\]0;.*'

def is_valid_timestamp(tmp):
    """
    Returns true if it is a valid timestamp in the form 10:29:11.734 (12 chars)
    """
    return len(tmp) == 12

# This function removes the NonAscii characters
def removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<126 and ord(i)>31)
# This function removes escape codes from the input content string
def remove_escape_codes(content: str) -> str:
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', content)

# This function can be used to remove extra timestamp inside the output
def remove_timestamps(input_string):
    timestamp_regex = r"\d{2}:\d{2}:\d{2}\.\d{3}"
    output_string = re.sub(timestamp_regex, "", input_string)
    return output_string

if __name__ == '__main__':
    # line = sys.argv[1]
    with open("/tmp/log-collector/session_4.log", "r") as log_f:
        print(log_f)
        logs = log_f.read()
        content_without_escape_codes = remove_escape_codes(logs)
        matches = re.finditer(r"┌──[^\n]*\n", content_without_escape_codes)
        print(matches)
        for match in matches:
            try:
                working_directory = match.group().split("[")[1].split("]")[0]
            except IndexError:
                working_directory = ""
            try:
                timestamp = content_without_escape_codes[match.end():].split("\n")[0]
                if (timestamp == ""):
                    continue
                tmp = removeNonAscii(timestamp)
                now = datetime.now()
                correct_date = now.date()
                if is_valid_timestamp(tmp):
                    time_obj = datetime.combine(correct_date, datetime.strptime(tmp, '%H:%M:%S.%f').time())
                    timezone = pytz.utc
                    localized_time_obj = timezone.localize(time_obj)
                    iso_time = localized_time_obj.isoformat()
                else:
                    print("[-] not valid iso_time, will skip")
                    iso_time = None
                
            except IndexError:
                timestamp = ""
            # try:
            #     command = commands[index]
            #     index=index+1
            # except IndexError:
            #     command = ""
            dirty_out = []
            i = 2
            while i < len(content_without_escape_codes[match.end():].split("\n")) and not content_without_escape_codes[match.end():].split("\n")[i].startswith("┌──"):
                dirty_out.append(remove_timestamps(removeNonAscii(content_without_escape_codes[match.end():].split("\n")[i].rstrip())))
                i += 1
            str_output="".join(dirty_out)
            output = re.sub(REGEX, '', str_output)
            print(output)