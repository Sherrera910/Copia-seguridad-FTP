#####################################################
#                                                   #
#                  Samuel Herrera                   #
#                                                   #
#                Copia-seguridad-FTP                #
#                                                   #
#                                                   #
#                                                   #
#                                                   #
#####################################################


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#import pdb
import ftplib
import os
import shutil
from datetime import datetime
#pdb.set_trace()

#Para ejecutar 10 veces el script, solo de prueba luego quitar.
#noseque = input()

# configurar servidor FTP
ftp_server = "192.168...."
ftp_username = "***"
ftp_password = "***"

# directorio local a copiar
local_dir = '/home/pi/...'

#(directorio desde donde comenzamos a archivar)
local_dir1 = './'

#nombre del archivo de copia de seguridad
now = datetime.now()
backup_archivo = f'backup{now.year}{now.month}{now.day}'
#backup_archivo += noseque

#comprimir el directorio local
shutil.make_archive(backup_archivo, 'zip', local_dir, local_dir1)

#conectar al servidor FTP
ftp = ftplib.FTP(ftp_server)
ftp.login(ftp_username, ftp_password)

#subir el archivo de copia de seguridad al servidor (with para dar contexto, uan configuración inicial y una final, ejemplo:
# abrir un archivo)

with open(backup_archivo+'.zip', 'rb') as file:
        ftp.storbinary('STOR ' + backup_archivo+'.zip', file)

#eliminar el archivo de copia de seguridad local
os.remove(backup_archivo+'.zip')
#------------------eliminar copias de seguridad antiguas-------------
# Obtener lista de archivos en el servidor FTP
files = ftp.nlst()

#Contar el número de archivos de copia de seguridad
backup_count = len([file for file in files if file.startswith("backup")])

#Borrar la copia de seguridad más antigua si se ha alcanzado el límite de 10
if backup_count == 11:
        oldest_backup = sorted(files)[0]
        ftp.delete(oldest_backup)


#Cerrar la conexión FTP
ftp.quit()




#Enviamos el correo
def send_email(to_email, subject, content_html, content_text):
        gmail_user = ''
        gmail_password = ''

        msg = MIMEMultipart("alternative")
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject

        html = MIMEText(content_html, "html")
        text = MIMEText(content_text)

        msg.attach(html)
        msg.attach(text)

        #Capa de sockets seguros 465 (SSL)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, msg.as_string())
        server.close()
        print("El correo electrónico se ha enviado exitosamente.")

send_email(to_email=gmail_user, subject='subject', content_html='<p>La copia de seguridad se ha hecho exitosame>')


