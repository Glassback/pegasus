# coding=utf-8

import MySQLdb as mdb             #Library for MySQL connection
import os                         #Library for doing bash commands
import argparse                   #Library for commands
import random                     #Random library for strong random password
import string                     #Library used for generating password
import smtplib                    #Library for sending e-mail
import crypt                      

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import exit

#System configs
DataFolder = "/var/pegasus/"
SystemFolder = "/opt/pegasus/"
SendMailAddress = "noreply@pegasus.ch"
BackupFileFolder = "backup/SitesToBackup.txt"
Version = "2.09"

#MySQL config
MySQLUser = "root"
MySQLPassword = "Pa$$w0rd"

#Welcome screen

print(
"""############################################################
#       Welcome to the Official Pegasus Installer """ + Version + """       """ + """ #
############################################################

                 .-.   
           %%%%,/   :-.
           % `%%%, /   `\   _,
           |' )`%%|      '-' /
           \_/\  %%%/`-.___.'
            __/  %%%"--"'"-.%,
          /`__|  %%         \%%
          \\  \   /   |     /'%,
           \]  | /----'.   < `%,
               ||       `>> >
               ||       ///`
               /(      //(

               PEGASUS API


Copyright: Noe Ferrari

Loading script ...
""")

connect = mdb.connect('localhost', MySQLUser, MySQLPassword);
requestID = connect.cursor()
requestID.execute("select * from mysql.user;")

#Connection to MySQL database

print("Connecting to MySQL databse with User: " + MySQLUser + " Password: ****")

#Defining charset for strong password

char_set = string.ascii_uppercase + string.digits +string.ascii_lowercase

print("\n\nDefining charset for generating strong password")


#Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domainname", dest = 'domainname', action = 'store', help = "Domain name to host", required=True)
parser.add_argument("-u", "--username", dest = 'username', action = 'store', help = "The username", required=True)
parser.add_argument("-m", "--mailaddress", dest = 'mailaddress', action = 'store', help = "Mail adress of the user")
parser.add_argument("-e", "--espacedisk", dest = 'espacedisk', action = 'store', help = "Disk size quota in MO per user")
parser.add_argument("-b", "--bandwidch", dest = 'bandwidth', action = 'store', help = "Bandwidth quota per user")
parser.add_argument("-B", "--backup", dest = 'backup', action = 'store', default = 'no', help = "Backup web site")
parser.add_argument("-s", "--webserver", dest = 'webserver', action = 'store', default = 'apache2', help = "Apache2? Linghttp? NodeJs? Nginx?")
args = parser.parse_args()


#Control if Pegasus is installed
if not os.path.exists(DataFolder):
  print("Pegasus not installed, please install on official Github repository")
  sys.exit(0)

if not os.path.exists(DataFolder + str(args.username)): os.makedirs(DataFolder + str(args.username), 0710)
if os.path.exists(DataFolder + str(args.username) + "/" + str(args.domainname)):
    DeleteFolder = input("Domain already exist, do you want to overwrite? [y/n]")
    if DeleteFolder.lower() == "y":
        os.rmdir(DataFolder + str(args.username) + "/" + str(args.domainname))
        print("Folder deleted")
        os.makedirs(DataFolder + str(args.username) + "/" + str(args.domainname), 0710)
        print("Folder created")
    else:
        sys.exit(0)
else:
    PasswordUser = ''.join(random.sample(char_set*16, 16))
    os.makedirs(DataFolder + str(args.username) + "/domains/" + str(args.domainname), 0710)
    print("Generating folders: \n\n Creating " + DataFolder + str(args.username) + "/domains/" + str(args.domainname) + " CHMOD 710")
    os.makedirs(DataFolder + str(args.username) + "/domains/" + str(args.domainname) + "/web", 0750)
    print("\nCreating " + DataFolder + str(args.username) + "/domains/" + str(args.domainname) + "/web" + " CHMOD 750")
    os.system("useradd -m -d " + DataFolder + str(args.username) + "/domains/" + str(args.domainname)  + "/web/ -s /usr/bin/rssh -p $(openssl passwd -1 " + PasswordUser + ") "  + str(args.username) + str(requestID.rowcount))

    #print("\n\nCreating User: " + str(args.username) + str(requestID.rowcount + " with home folde = " + DataFolder + str(args.username) + "/domains/" + str(args.domainname)  + "/web/" + " with restricted rights (rssh)")
    os.system("usermod " + str(args.username) + str(requestID.rowcount) + " -g sftp")
    print("\nAdding user " + str(args.username) + str(requestID.rowcount) + " to SFTP group")
    os.system("chown -R pegasus:sftp " + DataFolder + str(args.username))
    print("\n Adding correct rights on folders")
    os.system("chown " + str(args.username) + str(requestID.rowcount) + ":sftp " + DataFolder + str(args.username) + "/domains/" + str(args.domainname)  + "/web/")
    os.makedirs(DataFolder + str(args.username) + "/domains/" + str(args.domainname) + "/mail", 0710)
    print("\n\n Creating folder " + DataFolder + str(args.username) + "/domains/" + str(args.domainname) + "/mail")
    os.makedirs(DataFolder + str(args.username) + "/domains/" + str(args.domainname) + "/backup", 0710)
    print("\nCreating folder " + DataFolder + str(args.username) + "/domains/" + str(args.domainname) + "/backup")
    if not os.path.exists(DataFolder + str(args.username) + "/log"):os.makedirs(DataFolder + str(args.username) + "/log", 0710)
    if not os.path.exists(DataFolder + str(args.username) + "/log"):print("\nCreating folder " + DataFolder + str(args.username) + "/log")
    if not os.path.exists(DataFolder + str(args.username) + "/log/apache2"):os.makedirs(DataFolder + str(args.username) + "/log/apache2", 0710)
    if not os.path.exists(DataFolder + str(args.username) + "/log/apache2"):print("Creating folder " + DataFolder + str(args.username) + "/log/apache2")
    if not os.path.exists(DataFolder + str(args.username) + "/conf"):os.makedirs(DataFolder + str(args.username) + "/conf", 0710)
    if not os.path.exists(DataFolder + str(args.username) + "/conf"):print("Creating folder " + DataFolder + str(args.username) + "/conf")
    if not os.path.exists(DataFolder + str(args.username) + "/conf/apache2"):os.makedirs(DataFolder + str(args.username) + "/conf/apache2", 0710)
    if not os.path.exists(DataFolder + str(args.username) + "/conf/apache2"):print("Creating folder " + DataFolder + str(args.username) + "/conf/apache2")
    if not os.path.exists(DataFolder + str(args.username) + "/conf/apache2/sites-enabled"):os.makedirs(DataFolder + str(args.username) + "/conf/apache2/sites-enabled", 0710)
    if not os.path.exists(DataFolder + str(args.username) + "/conf/apache2/sites-enabled"):print("Creating folder " + DataFolder + str(args.username) + "/conf/apache2/sites-enabled")

#Host file

file = open('/etc/hosts', 'a')
file.write('\n\n#Domain name: ' + str(args.domainname) + ' Username: '+ str(args.username) + '\n\n127.0.0.1      ' + str(args.domainname) + '\n127.0.0.1      ' + 'phpmyadmin.' + str(args.domainname) +'\n::1            ' + str(args.domainname))
file.close
print("\n\nFile /etc/hosts updated")

#Virtual host conf file

file = open('/etc/apache2/apache2.conf', 'a')
file.write('\nIncludeOptional ' + DataFolder + str(args.username) + '/conf/apache2/sites-enabled/' + str(args.domainname)  + '.conf')
file.close
print("\n\nApache2 configuration file generated")

#Virtual host apache file

file = open(DataFolder + str(args.username) + '/conf/apache2/sites-enabled/' + str(args.domainname)  + '.conf', 'w')
content = """<VirtualHost *:80>
    ServerAdmin webmaster@""" + str(args.domainname) + """
    ServerName """ + str(args.domainname) + """
    DocumentRoot """ + DataFolder + str(args.username) + "/domains/" + str(args.domainname) + "/web"  + """
    
    <Directory """ + DataFolder + str(args.username) + "/domains/" + str(args.domainname) + "/web" + """>
        Options -Indexes +FollowSymLinks +MultiViews
        AllowOverride All
        Order allow,deny
        Allow from all
        Require all granted
    </Directory>

ErrorLog """ + DataFolder + str(args.username) + "/log/apache2/" +  str(args.domainname) + """-apache2-error.log
LogLevel warn
CustomLog """ + DataFolder + str(args.username) + "/log/apache2/" + str(args.domainname) + """-apache2-access.log combined
</VirtualHost>
<VirtualHost *:80>
        ServerName      phpmyadmin.""" + str(args.domainname)  + """
        DocumentRoot    /usr/share/phpmyadmin
</VirtualHost>"""

file.write(content)
file.close

os.system('service apache2 reload')


FileName = DataFolder + str(args.username) + "/domains/" + str(args.domainname) + "/web/index.html"
file = open(FileName, 'w')
content = """
<html>
    <head>
        <meta charset=utf-8>
        <meta http-equiv=X-UA-Compatible content=IE=edge>
        <meta name=viewport content=width=device-width, initial-scale=1>
        <title>Domain """ + str(args.domainname) + """ active!</title>
        <style>
            html {
                height: 80%;
            }
            body {
                text-align:left;
                height:100%;
                background: #F3F3F3;
                font-size: 62.5%;
                font-family: 'Lucida Grande', Verdana, Arial, Sans-Serif;
                margin-top:10px;
                margin-bottom:10px;
                margin-right:10px;
                padding:0px;
            }
            body,td,th {
                font-family: Verdana, Arial, Helvetica, sans-serif;
                font-size: 9pt;
                color: #333333;
            }
            h1,h2,h3,h4,h5,h6 {
                font-family: Geneva, Arial, Helvetica, sans-serif;
            }
            h1 {
                font-size: 28px;
                font-weight:bold;
                color: #336;
                text-shadow:3px 3px 5px #BBBBBB;
            }
            a:link,a:visited,a:hover,a:active {
                color: #336;
                text-decoration:none;
            }
            ol{
                color:#336;
                font-size: 24px;
                font-weight:bold;
                text-shadow:3px 3px 5px #BBBBBB;
            }
            ol p{
                color:#CCCCCC;
                font: normal 12pt Verdana, Arial, Helvetica, sans-serif;
                color: #333333;
            }
            .content{
                background:#F1F4F6;
                background: #F1F4F6 url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAA6CAYAAAB4Q5OdAAAACXBIWXMAAAsTAAALEwEAmpwYAAAABGdBTUEAALGOfPtRkwAAACBjSFJNAAB6JQAAgIMAAPn/AACA6QAAdTAAAOpgAAA6mAAAF2+SX8VGAAABKklEQVR42mL8DwQMaAAggJgYsACAAMIqCBBAWAUBAgirIEAAYRUECCAWLJYzAAQQy38sKgECCKt2gADCKggQQFgFAQIIq0UAAYRVJUAAYRUECCCsggABhFUQIIBYsNjDABBAWFUCBBALAwOmUoAAwqoSIICwCgIEEFaLAAIIq0qAAMIqCBBAWAMEIICwqgQIIKyCAAGEVRAggLAKAgQQVkGAAMIqCBBAWJ0EEEBYVQIEEFZBgADCmmwAAgirSoAAwioIEEBYbQcIIKwqAQIIqyBAAGEVBAggrIIAAYQ14gACCKtKgADC6iSAAMKqEiCAsAoCBBBWQYAAwioIEEBYkyJAAGFVCRBAWAUBAgirjwACCGt0AAQQVu0AAYRVECCAsAoCBBDWAAEIMAAoCSZuy+v+UQAAAABJRU5ErkJggg==') repeat-x top;
                border:solid 1px #DFDFDF;
                margin: 10px 0;
                padding: 0 20px 10px;
                -moz-border-radius: 10px;
                border-radius: 10px;
                min-height: 90%;
            }
            .header_logo {
                display:block;
                max-width:263px;
                max-height:71px;
            }
            .header_logo img {
                width:100%;
                height:100%;
            }
            .poweredbox {
                font-family: Geneva, Arial, Helvetica, sans-serif;
                color:#333333;
                padding-left: 15px;
            }
        </style>
    </head>
    <body>
        <h1>Pegasus WebHost</h1>
        <div class=content>
            <h1>Your hosting space is ready... </h1>
            <p>Your web hosting space is now active and ready to be used.</p>
            <p>
              <b>To get started:</b>
            </p>
            <ol>
              <li><p>Login with your FTP account</p></li>  
              <li><p>Replace or delete this file (index.html)</p></li>
            </ol>
            <p></p>
            <p>Thank you for using Pegasus to manage your hosting!</p>
            <p>Kind regards,<br>
                Your hosting company.</p>
          </div>       
    </body>
</html>"""

file.write(content)
file.close()

#SFTP

#os.system('useradd -d ' + DataFolder + str(args.username) + '/domains/' + str(args.domainname) + '/web/ -s /usr/lib/sftp-server -M -N -g sftp ' + str(args.username))
#os.system('chown -R '+ str(args.username) +':sftp ' + DataFolder + str(args.username) + '/domains/' + str(args.domainname) + '/web')
#os.system('service ssh restart')

#Mysql
#Password
PasswordMySQL = ''.join(random.sample(char_set*16, 16))

request = connect.cursor()
request.execute("CREATE USER '" + str(args.username)[0:8] + str(requestID.rowcount) + "'@'" + str(args.domainname)  + "' IDENTIFIED BY '" + PasswordMySQL  + "';")
request.execute("CREATE DATABASE DB_" + str(args.domainname).replace(".","_"))
request.execute("GRANT ALL PRIVILEGES ON DB_" + str(args.domainname).replace(".","_")  + ".* to '" + str(args.username)[0:8] + str(requestID.rowcount) + "'@'localhost' IDENTIFIED BY '" + PasswordMySQL  + "';")
request.execute("FLUSH PRIVILEGES;")

#Send mail


msg = MIMEMultipart('alternative')
msg['Subject'] = "Your domain " + args.domainname + " is ready!"
msg['From'] = SendMailAddress
msg['To'] = args.mailaddress

htmlmail = """\
<html lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
        <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <title>Atropos Email Marketing</title>
    </head>
    <body style="margin:0; margin-top:30px; margin-bottom:30px; padding:0; width:100%; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; background-color: #F4F5F7;">
        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="border:0; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; background-color: #F4F5F7;">
            <tbody>
                <tr>
                    <td align="center" style="border-collapse: collapse;">
                        <table cellpadding="0" cellspacing="0" border="0" width="560" style="border:0; border-collapse:collapse; background-color:#ffffff; border-radius:6px;">
                            <tbody>
                                <tr>
                                    <td style="border-collapse:collapse; vertical-align:middle; text-align center; padding:20px;">
                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" align="center" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;">
                                            <tbody>
                                                <tr>
                                                    <td width="100%" style="font-family: helvetica, Arial, sans-serif; font-size: 18px; letter-spacing: 0px; text-align: center;">	
                                                        <a href="#" style="text-decoration: none;">
                                                        <img src="http://img4.hostingpics.net/pics/445990logoweb.png">
                                                        </a>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <!-- spacer before the line -->
                                                    <td width="100%" height="20"></td>
                                                </tr>
                                                <tr>
                                                    <!-- line -->
                                                    <td width="100%" height="1" bgcolor="#d9d9d9"></td>
                                                </tr>
                                                <tr>
                                                    <!-- spacer after the line -->
                                                    <td width="100%" height="30"></td>
                                                </tr>
                                                <tr>
                                                    <td width="100%" style=" font-size: 14px; line-height: 24px; font-family:helvetica, Arial, sans-serif; text-align: center; color:#87919F;"><strong>Depuis 2015</strong> un nouvelle solution d'hébergement web est né. Notre équipe cherches à vous offrir des solutions sans limite pour un prix hors norme.
                                                        Notre objectif est de vous fournir toutes les ressources nécéssaires pour vos créations afin de permettre une créativité sans limite.
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td width="100%" height="15"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table width="100%" border="0" cellpadding="0" cellspacing="0" align="left" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;">
                            <tbody>
                                <tr>
                                    <td width="100%" height="30"></td>
                                </tr>
                            </tbody>
                        </table>
                        <table cellpadding="0" cellspacing="0" border="0" width="560" style="border:0; border-collapse:collapse; background-color:#ffffff; border-radius:6px;">
                            <tbody>
                                <tr>
                                    <td style="border-collapse:collapse; vertical-align:middle; text-align center; padding:20px;">
                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" align="center" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;">
                                            <tbody>
                                                <tr>
                                                    <!-- spacing top -->
                                                    <td width="100%" height="20"></td>
                                                </tr>
                                                <tr>
                                                    <td width="100%" style="font-family: helvetica, Arial, sans-serif; font-size: 18px; letter-spacing: 0px; text-align: center; color:#F07057;">	
                                                        Votre domaine <strong>""" + args.domainname + """</strong> est prêt
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <!-- spacing bottom -->
                                                    <td width="100%" height="30"></td>
                                                </tr>
                                                <tr>
                                                    <td width="100%" style="font-family:helvetica, Arial, sans-serif; font-size: 14px; text-align: center; color:#87919F; line-height: 24px;">Votre site web est désomais hébergé par nos soins. Voici les données de connection à garder soigneusement. <br>Si vous perdez cet e-mail, pas de panique! Vous serez toujours en mesure de créer un nouveau mot de passe en cas d'oublis</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" align="left" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;">
                                            <tbody>
                                                <tr>
                                                    <td width="100%" height="20"></td>
                                                </tr>
                                                <tr>
                                                    <td width="100%" height="1" bgcolor="#d9d9d9"></td>
                                                </tr>
                                                <tr>
                                                    <td width="100%" height="20"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" align="right" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;">
                                            <tbody>
                                                <tr>
                                                    <td width="100%">
                                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" align="left" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;">
                                                            <tbody>
                                                                <tr>
                                                                    <td width="100%" height="20"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" style="font-family: helvetica, Arial, sans-serif; font-size: 18px; letter-spacing: 0px; text-align: left; color:#F07057;">Base de donnée <strong>MySQL</strong></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" height="10"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" style="font-family:helvetica, Arial, sans-serif; font-size: 14px; text-align: left; color:#87919F; line-height: 24px;">Grâce à phpMyAdmin vous pourez facilement gérer votre base donnée pour et permettre à votre site d'être entièrement dynamique</td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" height="30"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" style="font-family:helvetica, Arial, sans-serif; font-size: 14px; text-align: left; color:#87919F; line-height: 24px;">Domaine:		 <strong>phpmyadmin.""" + args.domainname  + """</strong></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" style="font-family:helvetica, Arial, sans-serif; font-size: 14px; text-align: left; color:#87919F; line-height: 24px;">Identifiant:		 <strong>""" + str(args.username)[0:8] + str(requestID.rowcount) + """</strong></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" style="font-family:helvetica, Arial, sans-serif; font-size: 14px; text-align: left; color:#87919F; line-height: 24px;">Mot de passe:		 <strong>""" + PasswordMySQL + """</strong></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" height="30"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" style="text-align:left;">
                                                                        <a href=phpmyadmin.""" + args.domainname  + """ style="text-decoration:none; font-family: helvetica, Arial, sans-serif; font-size: 12px; letter-spacing: 0px; text-align: center; text-transform: uppercase; padding:10px; color:#ffffff; background-color:#F07057; border-radius:6px;">Accéder à phpMyAdmin</a>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td width="100%" height="50"></td>
                                                </tr>
                                                <tr>
                                                    <td width="100%" height="1" bgcolor="#d9d9d9"></td>
                                                </tr>
                                                <tr>
                                                    <td width="100%" height="20"></td>
                                                </tr>
                                                <tr>
                                                    <td width="100%">
                                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" align="left" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;">
                                                            <tbody>
                                                                <tr>
                                                                    <td width="100%" height="20"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" style="font-family: helvetica, Arial, sans-serif; font-size: 18px; letter-spacing: 0px; text-align: left; color:#F07057;">Compte <strong>SFTP</strong></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" height="10"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" style="font-family:helvetica, Arial, sans-serif; font-size: 14px; text-align: left; color:#87919F; line-height: 24px;">Gérer vos fichiers de votre site internet comme vous le voulez avec votre compte FTP. Votre serveur de fichiers est sécurisé grâce à la technologie SFTP.</td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" height="30"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" style="font-family:helvetica, Arial, sans-serif; font-size: 14px; text-align: left; color:#87919F; line-height: 24px;">Domaine:		 <strong>""" + args.domainname  + """</strong></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" style="font-family:helvetica, Arial, sans-serif; font-size: 14px; text-align: left; color:#87919F; line-height: 24px;">Port:		 <strong>22</strong></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" style="font-family:helvetica, Arial, sans-serif; font-size: 14px; text-align: left; color:#87919F; line-height: 24px;">Identifiant:		 <strong>""" + str(args.username)[0:8] + str(requestID.rowcount) +  """</strong></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" style="font-family:helvetica, Arial, sans-serif; font-size: 14px; text-align: left; color:#87919F; line-height: 24px;">Mot de passe:		 <strong>""" + PasswordUser  + """</strong></td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" align="left" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;">
                                            <tbody>
                                                <tr>
                                                    <td width="100%" height="20"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table width="100%" border="0" cellpadding="0" cellspacing="0" align="left" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;">
                            <tbody>
                                <tr>
                                    <td width="100%" height="10"></td>
                                </tr>
                            </tbody>
                        </table>
                        <table cellpadding="0" cellspacing="0" border="0" width="560" style="border:0; border-collapse:collapse; background-color:#ffffff; border-radius:6px;">
                            <tbody>
                                <tr>
                                    <td style="border-collapse:collapse; vertical-align:middle; text-align center; padding:20px;">
                                        <table width="100%" border="0" cellpadding="0" cellspacing="0" align="center" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;">
                                            <tbody>
                                                <tr>
                                                    <td width="100%" style="font-family: helvetica, Arial, sans-serif; font-size: 11px; text-align: center; line-height: 24px;">
                                                        <center>Copyright © 2015. Tout droits réservés.</center>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
            </tbody>
        </table>
    </body>
</html>
"""


if str(args.backup) == 'y':
    file = open(SystemFolder + BackupFileFolder, 'a')
    file.write('\n' + DataFolder + str(args.username) + '/domains/' + str(args.domainname))
    file.close
 
part2 = MIMEText(htmlmail, 'html')
msg.attach(part2)
s = smtplib.SMTP('localhost')
s.sendmail(SendMailAddress, args.mailaddress, msg.as_string())
s.quit()


print("Mysql user with password created")
print("MySQL username: " + str(args.username) + "-" + str(args.domainname).replace(".","_") + "\nPassword: " + PasswordMySQL + "\n\nSFTP\n\nPassword:" + PasswordUser)
