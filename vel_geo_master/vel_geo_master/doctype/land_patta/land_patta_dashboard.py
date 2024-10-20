

def get_data():
	return {
		"heatmap": False,
		"fieldname": "title",
		"non_standard_fieldnames": {
			"Property Payment": "property",
		},
		"dynamic_links": {"property_type": ["Land Patta", "property"]},
		"transactions": [
			{"label": "Property Payments", "items":
				["Property Payment"]
			 },
		]
	}
