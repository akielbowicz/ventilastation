import tempfile
from PIL import Image, ImageSequence
from to_led import to_led
from pathlib import Path

def from_gif_to_bytes(file_path):
    "Crea archivos .bytes a partir de un .gif"
    file_path = Path(file_path)
    input_file_name = file_path.name.split('.')[0]

    picture_folder = file_path.parent.joinpath(input_file_name)
    picture_folder.mkdir(exist_ok=True)

    im = Image.open(file_path)
    temp_path = tempfile.mkdtemp()

    output_folder_name = str(picture_folder)

    for index,frame in enumerate(ImageSequence.Iterator(im)):
        file_name = 'frame{:d}'.format(index)
        temp_file = ''.join([temp_path, '/', file_name, '.png'])
        frame.save(temp_file)
        out_file = ''.join([output_folder_name, '/', file_name, '.bytes'])
        # print(index, file_name, temp_file, out_file,sep='\n')
        with open(out_file, 'wb') as f:
            f.write(to_led(temp_file))
