FEATURES_PROMPTS = {
    "problem": "Given the product description in this url {product_url}, Describe the problem the product \"{product_name}\" addresses",
    "market": "Given the product description in this url {product_url}, Describe the market of the product \"{product_name}\""
}

COMPANY_PRODUCTS_PROMPT = """list all products by \"{company_url}\"
output ONLY actual distinct products by the company, do not list aspects of a single product! if company has only one product, list it and it alone
output in a single list of jsons in the following manner only!:
{{
    "output":
    [
        {{
            "product_name": <product name>,
            "product_url": <product description url>
        }}
    ]
}}
"""