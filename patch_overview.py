with open("src/pages/1_Overview.py", "r") as f:
    code = f.read()

new_logic = """        subject = "The market"
        if comm_str != "All" and state_str != "All":
            subject = f"The market for **{comm_str.title()}** in **{state_str.title()}**"
        elif comm_str != "All":
            subject = f"The national market for **{comm_str.title()}**"
        elif state_str != "All":
            subject = f"The agricultural sector in **{state_str.title()}**"
            
        if comm_str.lower() == "potato":
            return (f"**Temporal Price Dynamics:** {subject} demonstrates a distinct bimodal price distribution typical of tuber supply chains. "
                    f"The pricing peak in {max_month} (₹{max_price:,.2f}) reflects the critical exhaustion of cold-storage stocks just before fresh harvests arrive. "
                    f"Conversely, the {min_month} drop to ₹{min_price:,.2f} perfectly aligns with post-harvest market gluts. "
                    f"This +{pct_change:.1f}% intra-year variance highlights the storage-dependent nature of the potato economy.")
        elif comm_str.lower() == "onion":
            return (f"**Temporal Price Dynamics:** {subject} is notoriously volatile and sensitive to supply shocks. "
                    f"The data reveals a dramatic +{pct_change:.1f}% surge, peaking in {max_month} (₹{max_price:,.2f}) and bottoming out in {min_month} (₹{min_price:,.2f}). "
                    f"This characteristic spike typically occurs when stored Rabi crops deplete rapidly and the incoming Kharif harvest is delayed by erratic late monsoons, creating a temporary but severe supply vacuum.")
        elif comm_str.lower() == "tomato":
            return (f"**Temporal Price Dynamics:** Unlike root vegetables, Tomatoes are highly perishable with minimal cold-storage buffering. "
                    f"This is perfectly reflected in the extreme +{pct_change:.1f}% volatility for {subject}. Prices spike sharply to ₹{max_price:,.2f} in {max_month} "
                    f"and collapse to ₹{min_price:,.2f} in {min_month}. This indicates that pricing is almost entirely dictated by real-time harvest yields and immediate logistical bottlenecks.")
        elif comm_str.lower() == "wheat":
            return (f"**Temporal Price Dynamics:** {subject}, being a heavily regulated staple with Minimum Support Price (MSP) buffering, exhibits uniquely subdued volatility. "
                    f"The +{pct_change:.1f}% variance between {min_month} (₹{min_price:,.2f}) and {max_month} (₹{max_price:,.2f}) represents a steady, controlled depletion of granary stocks "
                    f"rather than the erratic market panics seen in perishables.")
        
        return (f"**Temporal Price Dynamics:** {subject} exhibits a clear seasonal trajectory. "
                f"The lowest median aggregate prices occurred in {min_month} (₹{min_price:,.2f}), "
                f"while prices peaked significantly in {max_month} at ₹{max_price:,.2f}. "
                f"This represents a maximum intra-year variance of +{pct_change:.1f}%. This specific pricing "
                f"shift heavily correlates with the seasonal availability and localized harvest cycles for {subject.lower().replace('the market for ', '').replace('the national market for ', '').replace('the agricultural sector in ', '')}.")"""

import re
# We need to replace the old subject logic with this new block
code = re.sub(r'        subject = "The market".*?localized harvest cycles for \{subject\.lower\(\)\.replace.*?\}\."\)', new_logic, code, flags=re.DOTALL)

with open("src/pages/1_Overview.py", "w") as f:
    f.write(code)
