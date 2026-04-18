import json
import re

#  Configuration & Rules
FAST_TRACK_THRESHOLD = 25000
FRAUD_KEYWORDS = ["fraud", "inconsistent", "staged", "suspicious"]

# Mandatory fields for the - Manual Review
MANDATORY_FIELDS = [
    "policy_number",
    "policyholder_name",
    "incident_date",
    "incident_location",
    "claim_type",
    "initial_estimate"
]


class InsuranceClaimAgent:  

    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.extracted_data = {}
        self.missing_fields = []

    def clean_text(self, value):
        """Helper to clean up extracted text, removing extra newlines and headers."""
        if value:
            # Remove common form headers that get caught in regex
            value = re.split(r'\n|DATE|POLICY|NAME|LOCATION', value)[0]
            return value.strip()
        return None

    def extract_fields(self):
        """Extracts fields based on the ACORD form structure using regex."""
        
        # Regex patterns for the specific ACORD 2 structure
        patterns = {
            "policy_number": r"POLICY NUMBER[:\s]+([\w-]+)",
            "policyholder_name": r"NAME OF INSURED\s*\((.*?)\)|NAME OF INSURED\s+([A-Z\s]+)",
            "effective_dates": r"DATE \(MM/DD/YYYY\)\s+(\d{2}/\d{2}/\d{4})",
            "incident_date": r"DATE OF LOSS AND TIME\s+(\d{2}/\d{2}/\d{4})",
            "incident_time": r"(\d{1,2}:\d{2}\s?[AP]M)",
            "incident_location": r"STREET:\s+(.*?)(?=CITY|$)",
            "incident_description": r"DESCRIPTION OF ACCIDENT[:\s]+(.*?)(?=\n[A-Z ]+:|$)",
            "claimant": r"OWNER'S NAME AND ADDRESS\s+(.*)",
            "third_parties": r"DRIVER'S NAME AND ADDRESS\s+(.*)",
            "contact_details": r"PRIMARY PHONE #\s+([\d-]+)",
            "asset_id_vin": r"V\.I\.N\.:\s+(\w+)",
            "estimated_damage": r"ESTIMATE AMOUNT:\s+\$?([\d,]+)"
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, self.raw_text, re.IGNORECASE | re.DOTALL)
            if match:
                # Take the first non-null group
                val = next((g for g in match.groups() if g), None)
                self.extracted_data[field] = self.clean_text(val)
            else:
                self.extracted_data[field] = None

        # Fixed logic for specific required fields
        self.extracted_data["asset_type"] = "Automobile" 
        self.extracted_data["attachments"] = "None detected"
        
        # Handle the Initial Estimate as a float
        est_str = self.extracted_data.get("estimated_damage") or "0"
        clean_est = re.sub(r'[^\d.]', '', str(est_str))
        self.extracted_data["initial_estimate"] = float(clean_est) if clean_est else 0.0

        # Determine Claim Type 
        desc = (self.raw_text).lower()
        if "injury" in desc or "bodily" in desc:
            self.extracted_data["claim_type"] = "injury"
        else:
            self.extracted_data["claim_type"] = "property_damage"


    def evaluate_routing(self):
        """Applies the 4 Routing Rules from the Assignment Brief."""
        
        # Missing Mandatory Fields -> Manual Review
        for field in MANDATORY_FIELDS:
            if not self.extracted_data.get(field):
                self.missing_fields.append(field)
        
        if self.missing_fields:
            return "Manual review", f"Missing mandatory fields: {', '.join(self.missing_fields)}"

        # Fraud Keywords -> Investigation Flag
        desc = (self.extracted_data["incident_description"] or "").lower()
        if any(word in desc for word in FRAUD_KEYWORDS) and "no fraud" not in desc:
                return "Investigation Flag", "Potential fraud keywords detected in description."

        # Injury Claim -> Specialist Queue
        if self.extracted_data["claim_type"] == "injury":
            return "Specialist Queue", "Claim involves reported injuries."

        # Damage < 25,000 -> Fast-track
        if self.extracted_data["initial_estimate"] < FAST_TRACK_THRESHOLD:
            return "Fast-track", f"Damage estimate ${self.extracted_data['initial_estimate']} is below threshold."

        return "Standard Workflow", "Claim processed through standard routing."


    def get_json_output(self):
        self.extract_fields()
        route, reason = self.evaluate_routing()
        
        output = {
            "extractedFields": self.extracted_data,
            "missingFields": self.missing_fields,
            "recommendedRoute": route,
            "reasoning": reason
        }
        return json.dumps(output, indent=4)



if __name__ == "__main__":

    # Dummy OCR data mimicking the PDF provided
    sample_ocr = """
    AUTOMOBILE LOSS NOTICE
    POLICY NUMBER: ABC-123456
    NAME OF INSURED John Doe
    DATE OF LOSS AND TIME 04/15/2026 10:30 AM
    STREET: 123 Maple Avenue CITY: Springfield
    DESCRIPTION OF ACCIDENT: Rear-end collision. No fraud.
    ESTIMATE AMOUNT: 4500
    V.I.N.: 1HGCM82635A
    """
    
    agent = InsuranceClaimAgent(sample_ocr)
    print(agent.get_json_output())