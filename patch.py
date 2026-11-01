with open("src/insight_generator.py", "r") as f:
    code = f.read()
code = code.replace("focus = prompt_focus.lower()", "focus = prompt_focus.lower()\n    import sys\n    print('DEBUG FOCUS:', focus, file=sys.stderr)\n    print('DEBUG DF EMPTY:', df.empty, file=sys.stderr)\n    print('DEBUG MATCH:', 'overall monthly price' in focus, file=sys.stderr)")
with open("src/insight_generator.py", "w") as f:
    f.write(code)
