import subprocess, os
from docx2pdf import convert

def to_pdf(input_path):
    if input_path.lower().endswith('.docx'):
        output = input_path.replace('.docx', '.pdf')
        convert(input_path, output)
        return output
    elif input_path.lower().endswith(('.png','.jpg','.txt')):
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', input_path], cwd=os.path.dirname(input_path))
        return input_path.rsplit('.',1)[0] + '.pdf'
    return input_path