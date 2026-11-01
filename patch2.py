with open("src/insight_generator.py", "r") as f:
    code = f.read()
code = code.replace('state_match = re.search(r"state:([\w\s]+)", prompt_focus, re.IGNORECASE)', 'state_match = re.search(r"state:([^:]+)\s+commodity:", prompt_focus, re.IGNORECASE)')
code = code.replace('comm_match = re.search(r"commodity:([\w\s]+)", prompt_focus, re.IGNORECASE)', 'comm_match = re.search(r"commodity:([\w\s]+)", prompt_focus, re.IGNORECASE)')
with open("src/insight_generator.py", "w") as f:
    f.write(code)
