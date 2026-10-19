from typing import List, Dict

def extract_image_description(image_url: str, alt_text: str = "") -> str:
    if "logo" in image_url.lower() or "logo" in alt_text.lower():
        return "Interface screenshot displaying Settings panel and logo upload field."
    elif "stripe" in image_url.lower() or "payment" in alt_text.lower():
        return "Dashboard showing payment gateway credentials input for API keys."
    elif "search" in image_url.lower() or "filter" in alt_text.lower():
        return "Admin configuration view showing member search design and filter toggles."
    return f"Visual reference: {alt_text if alt_text else 'Support interface diagram'}"

def process_image_context(images: List[Dict[str, str]]) -> List[Dict[str, str]]:
    processed = []
    for img in images:
        processed.append({
            "url": img.get("url", ""),
            "alt": img.get("alt", ""),
            "description": extract_image_description(img.get("url", ""), img.get("alt", ""))
        })
    return processed