import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'tesseract'

def ocr_image(img):
    custom_oem_psm_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_oem_psm_config)
    boxes_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=custom_oem_psm_config)
    boxes = []
    n = len(boxes_data['level'])
    for i in range(n):
        txt = boxes_data['text'][i].strip()
        if txt:
            x = boxes_data['left'][i]
            y = boxes_data['top'][i]
            w = boxes_data['width'][i]
            h = boxes_data['height'][i]
            boxes.append({'text': txt, 'box': [x, y, w, h], 'conf': boxes_data['conf'][i]})
    return {'text': text, 'boxes': boxes}
