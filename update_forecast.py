with open("src/pages/5_Price_Forecast.py", "r") as f:
    lines = f.readlines()
    
new_lines = []
for line in lines:
    if line.strip() == "st.info(analysis)":
        new_lines.append("        with st.expander('Insights', expanded=True):\n")
        new_lines.append("            st.markdown(analysis)\n")
    elif line.strip() == "st.subheader(\"Automated Trend Analysis\")":
        continue
    else:
        new_lines.append(line)
        
with open("src/pages/5_Price_Forecast.py", "w") as f:
    f.writelines(new_lines)
