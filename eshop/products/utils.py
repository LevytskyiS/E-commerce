def my_slugify_function(content):
    slug = content.replace(".", "").replace(" ", "-").lower()
    return slug
