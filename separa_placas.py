from PIL import Image, ImageFilter  
import numpy as np
import os
import difflib
import shutil
import sys
import pytesseract
import cv2

ERROR_TOL= 2

leet_dict = {
    'A': '4', 'B': '8', 'C': '(', 'E': '3',
    'G': '6', 'H': '#', 'I': '1',
    'O': '0', 'S': '5', 'T': '7', 'Z': '2'
}

l337_dict = {
    '4': 'A', '8': 'B', '(': 'C', '3': 'E',
    '6': 'G', '#': 'H', '1': 'I',
    '0': 'O', '5': 'S', '7': 'T', '2': 'Z'
}

charsToDeny = '!@#$%¨&*()_+={[]}^~<>;:/|\.,?- '
custom_config = f'--oem 3 --psm 6 -c tessedit_char_blacklist={charsToDeny}'

def createDir(output, subdir):
    path = output + subdir
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)
    return path

def leetVerify(chars, dictionary):
    new_letters = ""
    for char in chars:
        if char in dictionary:
            new_letters += dictionary[char]
        else:
            new_letters += char

    return new_letters

def logWriter(originalDiff, plate_found, plate):
    with open('log.txt', 'a') as log:
        log.write('----------------------------------------------------\n')
        log.write(f'Placa encontrada: {plate_found}\n')
        log.write(f'Placa original: {plate}\n\n')
        log.write(f'Número de caracteres não encontrados: {len(originalDiff)}\n')
        log.write(f'Caracteres Não Encontrados: {originalDiff}\n')

def plateClassifier(plates_dir, output, amount):
    # Files preparation
    plates = os.listdir(plates_dir)
    aprovedPath = createDir(output, '/boas')
    reprovedPath = createDir(output, '/ruins')
    if os.path.exists('log.txt'):
        os.remove('log.txt')

    print(f'Processing ...')
    i = 0
    for plate in plates:
        if i == amount:
            break 
        image_path = os.path.join(plates_dir, plate)
        # Image reading and resizing
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # Image binarization
        _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Image inversion
        image_inverted = cv2.bitwise_not(binary_image)

        # Image blurring using PIL
        binary_image_pil = Image.fromarray(image_inverted)
        binary_image_pil = binary_image_pil.filter(ImageFilter.GaussianBlur(2))
        blurred_image = np.array(binary_image_pil)

        # Sharpen the image 
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) 
        blurred_image = cv2.filter2D(blurred_image, -1, kernel) 

        # Char recognition
        plate_found = pytesseract.image_to_string(blurred_image, config=custom_config).replace(" ", "").strip().upper()
        letters = plate_found[0:3]
        numbers = plate_found[3:7]

        # String split processing using leet code
        new_letters = leetVerify(letters, l337_dict)
        new_numbers = leetVerify(numbers, leet_dict)
            
        # String concatenation
        plate_found = new_letters + '-' + new_numbers

        # Plate classification
        plate_found = plate_found + '.jpg'

        diff = difflib.ndiff(plate_found, plate)
        originalDiff = [line[2:] for line in diff if line.startswith('+ ')]

        if(len(originalDiff) <= ERROR_TOL):
            shutil.copy(image_path, aprovedPath)
        else:
            shutil.copy(image_path, reprovedPath)
            logWriter(originalDiff, plate_found, plate)
        i+=1
    print(f'Processing finished! Processed Plates: {i} / Bad Recognized Plates: {len(os.listdir(reprovedPath))} / Good Recognized Plates: {len(os.listdir(aprovedPath))}')

def main():
    dir = sys.argv[1]
    output = sys.argv[2]
    amount = int(sys.argv[3])
    plateClassifier(dir, output, amount)

if __name__ == "__main__":
    main()
