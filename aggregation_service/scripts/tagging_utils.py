import re

TAG_RULES = {
    "Python": ["python", "django", "flask", "pandas", "numpy"],
    "Programming": ["programming", "coding", "software development", "computer science"],
    "Machine Learning": ["machine learning", "deep learning", "ai", "artificial intelligence"],
    "Data Science": ["data science", "analytics", "data analysis", "data visualization"],
    "Beginner": ["beginner", "introduction", "basic", "getting started"],
    "Intermediate": ["intermediate", "advanced concepts", "practical"],
    "Advanced": ["advanced", "expert", "in-depth"]
}

def generate_tags(title, description):
    combined_text = f"{title} {description}".lower()
    tags = set()

    for tag, keywords in TAG_RULES.items():
        if any(re.search(rf"\b{keyword}\b", combined_text) for keyword in keywords):
            tags.add(tag)

    return list(tags)
