with open("src/insight_generator.py", "r") as f:
    code = f.read()
code = code.replace("for {subject.lower().replace('the ', '')}.", "for {subject.lower().replace('the market for ', '').replace('the national market for ', '').replace('the agricultural sector in ', '')}.")
with open("src/insight_generator.py", "w") as f:
    f.write(code)
