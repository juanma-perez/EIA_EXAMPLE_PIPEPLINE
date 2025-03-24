import subprocess
import os
import sys
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import config  # Importa la configuración central

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de correo desde variables de entorno
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_TO = os.getenv('EMAIL_TO')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_SUBJECT = '❌ Error en el pipeline EIA'

def send_error_email(message):
    print("🚨 Enviando correo de error...")
    try:
        msg = MIMEText(message)
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        print("✅ Correo de error enviado")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")

def run_notebook(notebook_path, output_path):
    try:
        print(f"🚀 Ejecutando notebook: {notebook_path}")
        subprocess.check_call([
            'jupyter', 'nbconvert',
            '--to', 'notebook',
            '--execute', notebook_path,
            '--output', output_path
        ])
        print(f"✅ Notebook ejecutado exitosamente: {output_path}")
    except subprocess.CalledProcessError:
        error_msg = f"❌ Error al ejecutar {notebook_path}"
        print(error_msg)
        send_error_email(error_msg)
        sys.exit(1)

def validate_file(file_path):
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        error_msg = f"❌ Validación fallida. Archivo vacío o no existe: {file_path}"
        print(error_msg)
        send_error_email(error_msg)
        sys.exit(1)
    else:
        print(f"✅ Validación exitosa: {file_path}")

if __name__ == "__main__":
    # Tomar rutas directamente del config.py
    dl_file = os.path.join(config.FOLDER_DL, config.FILE_DL)
    dwh_file = os.path.join(config.FOLDER_DWH, config.FILE_FACT)

    try:
        # Ejecutar pipeline de Data Lake
        run_notebook("load_eia_dl.ipynb", "executed_load_eia_dl.ipynb")
        validate_file(dl_file)

        # Ejecutar pipeline de Data Warehouse
        run_notebook("load_eia_dwh.ipynb", "executed_load_eia_dwh.ipynb")
        validate_file(dwh_file)

        print("✅ Pipeline ejecutado completamente sin errores")
    except Exception as e:
        final_error = f"❌ Error inesperado en el pipeline: {str(e)}"
        print(final_error)
        send_error_email(final_error)
        sys.exit(1)