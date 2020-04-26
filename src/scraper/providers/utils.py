def format_measurements(text, measurements):
    for m in measurements:
        if m in text:
            return text[: text.find(m) + len(m)] + " " + text[text.find(m) + len(m) :]
    return text
