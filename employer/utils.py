from pdf2image import convert_from_path
import os

def pdf_to_image(pdf_path):
    #Chemin où les images converties seront enregistrées
    output_dir = 'media/converted_pdf'
    
    # Créer le répertoire s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Conversion du fichier PDF en images
    images = convert_from_path(pdf_path)
    
    # Sauvegarde de chaque page sous forme d'image PNG
    for i, image in enumerate(images):
        image.save(f'{output_dir}/page_{i}.jpg', 'JPG')

    return [f'{output_dir}/page_{i}.jpg' for i in range(len(images))]
