import json

def apply_user_id_to_xml(xml, userid):
    if not isinstance(xml, str):
        xml = xml.decode('utf-8')
    return xml.replace('<eprint>', f'''<eprint>
    <userid>{userid}</userid>
''').encode('utf-8')
