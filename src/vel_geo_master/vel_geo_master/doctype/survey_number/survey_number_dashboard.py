

def get_data():
	return {
		"heatmap": False,
		"fieldname": "survey_number",
		"transactions": [
			{"label": "Utility Connections", "items":
				["Telephone Connection", "Electricity Service Connection", "Water Supply Connection"]
			 },
			{
				"label": "Structures", "items": ["Building", "Water Well"]
			},
			{
				"label": "Documents", "items": [""]
			}
		]
	}
