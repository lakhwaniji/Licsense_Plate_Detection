import string
import easyocr

def read_licsense_plate(licsense_plate_crop):
    reader=easyocr.Reader(['en'],gpu=False)
    dict_char_to_int = {'0': '0',
                        'I': '1',
                        'J': '3',
                        'A': '4',
                        'G': '6',
                        'S': '5'}
    Sdict_int_to_char = {'0': 'O',
                         '1': 'I',
                         '3': 'J',
                         '4': 'A',
                         '6': '6',
                         '5': 'S'}
    detections=reader.readtext(licsense_plate_crop)
    for detection in detections:
        bbox, text,score=detection
        text=text.upper().remove(' ','')
        return (text,score)

