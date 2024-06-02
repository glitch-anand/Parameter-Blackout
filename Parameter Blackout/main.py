import re


def compile_patterns(args_file, mask_file):
    patterns = {}
    with open(args_file, 'r') as i:
        for line in i:
            key, _ = line.strip().split("=")  
            if key:
                pattern = r"\b{}\b\s*(?:=)(?:\s*(\S*))(?=\s|$|\b$%^&*)".format(key)
                patterns[key] = re.compile(pattern)  

    mask_patterns = []
    with open(mask_file, 'r') as i:
        for line in i:
            mask_pattern = r"\b{}\b(?=\s|$|\b$%^&*)".format(re.escape(line.strip()))  
            mask_patterns.append(mask_pattern)

    return patterns, mask_patterns


def mask_line(line, arg_patterns, mask_patterns):
    
    masked_line = line
    for key, pattern in arg_patterns.items():
        match = pattern.search(line)
        if match:
            value = match.group(1)
            masked_line = line.replace(value, "masked")

    for pattern in mask_patterns:
        masked_line = re.sub(pattern, "masked", masked_line, flags=re.IGNORECASE)

    # Existing email masking logic
    masked_line = re.sub(r"([^\s]+)@(\S+\.(com|in|ae|org))", r"masked@email.com", masked_line)
    return masked_line


def main():
    log_file = "log.txt"
    args_file = "arguments.txt"
    mask_file = "mask_string.txt"
    masked_log = "masked_log.txt"

    arg_patterns, mask_patterns = compile_patterns(args_file, mask_file)

    with open(log_file, 'r') as i, open(masked_log, 'w') as n:
        chunk_size = 6000  
        for chunk in iter(lambda: i.read(chunk_size), ''):
            for line in chunk.splitlines():
                masked_line = mask_line(line, arg_patterns, mask_patterns)
                n.write(masked_line + "\n")


if __name__ == "__main__":
    main()
