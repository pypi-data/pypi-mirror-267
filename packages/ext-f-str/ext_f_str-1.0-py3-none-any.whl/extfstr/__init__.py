import string


class ExtractException(Exception):
    def __init__(self, e, *args: object) -> None:
        super().__init__('Failed to extract data from f-str', e, *args)


def extract(format_string: str, sentence: str):
    try:
        sentence_sheets = []
        mapping = {}
        for i, (literal_text, field_name, format_spec, conversion) in enumerate(string.Formatter.parse(None, format_string)):
            sentence_sheets.append((literal_text, False))  # ~, is_field
            if field_name:
                sentence_sheets.append((field_name, True))

        for i, (text, is_field) in enumerate(sentence_sheets):
            if not is_field:
                sentence = sentence.replace(text, '')
            else:
                end_index = len(sentence)
                for i_, (_text, _is_field) in enumerate(sentence_sheets[i+1:]):
                    if not _is_field:
                        end_index = sentence.find(_text)
                        break
                value = sentence[0:end_index]
                mapping[text] = value
                sentence = sentence.replace(value, '')

        return mapping
    except Exception as e:
        raise ExtractException(e)
