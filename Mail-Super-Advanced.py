import os
import smtplib
import imghdr
from email.message import EmailMessage

Selected_file = input("Enter a file name (Include .txt): ")

with open(Selected_file, 'r') as f1:                                 #File name, can be changed with little problem, just keep order same
    cnt = 0
    line = f1.readline().replace('\n', '')                          #Line 1 - Send addresses, Line 2 - Subject, Line 3+ - Body

    EMAIL_RECIPIENT = line.split(',')                               #First line is email addresses
    SUBJECT = 'Your personalized list of qualified candidates from AMMInnovation!'            #Declairing all values
    NumOpenings = ''
    Education = ''
    GPA = ''
    Major = ''
    WorkExperience = ''
    Score = ''
    BODY = ''
    Anon = ''
    Names = ['John Doe', 'Emma Frost', 'Sam Smith', 'Scott Webster']                 #When connected to a proper databse we would just accept the names from the doc
    while line:
        line = f1.readline()                                        #Reads through line by line and assigns values to subject and body

        if cnt == 0:
            NumOpenings = line.replace('\n', '')                    #Ensuring no random \ns in variables
        elif cnt == 1:
            Education = line.replace('\n', '')
        elif cnt == 2:
            GPA = line.replace('\n', '')
        elif cnt == 3:
            line = line.replace('\n', '')
            Major = line.split(',')                                 #Makes a list of majors chosen
        elif cnt == 4:
            WorkExperience = line.replace('\n', '')                 #0=dont include
        elif cnt == 5:
            Score = line.replace('\n', '')                          #Should be 1 or 0, 1=has score and compute, 0=dont include
        elif cnt == 6:
            Anon = line.replace('\n', '')                           #1 = remain anonymous,0 = doesn't matter
        cnt += 1

contacts = EMAIL_RECIPIENT                                          #Converts array to list to be used later

EMAIL_ADDRESS = os.environ.get('SunHacksEmail')                 #Sender email address
EMAIL_PASSWORD = os.environ.get('SunHacksPass')                 #Sender password

BigCounter = 0                                                  #Num of openings is currently maxed at 3 for simpicity of presentation
files = ''
files2 = ''
int_NumOpenings = int(NumOpenings)
MajorLength = len(Major) - 1
NamesLength = len(Names) - 1

while BigCounter < int_NumOpenings:                                         #Stops sending emails at last employee

    BODY = '\nQualified applicant found!\n'

    if Anon == '0':
        BODY += '\n\t\t' + Names[NamesLength] + ':'

    if NamesLength != 0:
        NamesLength -= 1

    if Anon == '1':
        BODY += '\n\t\tAnonymous: '

    BODY += '\n\t\t\tEducation: ' + '\t\t\t     ' + Education + '\n\t\t\tGPA: ' + '\t\t\t\t       ' + GPA + '\n\t\t\tMajor:  ' + '\t\t\t        ' + Major[MajorLength]

    if MajorLength != 0:
        MajorLength -= 1

    if WorkExperience != '0':
        BODY += '\n\t\t\tWork Experience: \t       ' + WorkExperience

    RandoScore = ['99', '90', '89', '92']

    if Score == '1':
        BODY += '\n\t\t\tHacker Rank Score: \t  ' + '   ' + RandoScore[BigCounter]              #If connected to database, would pull from doc

    BODY += '\n\nThank you for choosing AMMInnovation - Recruiting made simple'     #Closing statement
    BODY += '\nContact support at: ContactAMMInnovation@gmail.com'

    msg = EmailMessage()
    msg['Subject'] = SUBJECT                                            #Sets values from doc to prep for email
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = contacts                                                #can push different emails depending on desire
    msg.set_content(BODY)

    if BigCounter == 0:                                                 #Decides what attatchment to add
        files = 'Matthew.jpg'                                           #In full program it would be pulled from the doc
    if BigCounter == 1:                                                 #Replace with desired
        files = 'Alex.jpg'
    if BigCounter == 2:
        files = 'Michael.jpg'

    with open(files, 'rb') as f:                                        #Opens image from selected path
        file_data = f.read()
        file_type = imghdr.what(f.name)                                 #Passes name to get file type
        file_name = f.name

    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

    if BigCounter == 0:
        files2 = 'Matthew_Resume.pdf'                                  #Plan to replace with file reader with names
    if BigCounter == 1:                                                #Replace with desired
        files2 = 'Alex_Resume.pdf'
    if BigCounter == 2:
        files2 = 'Michael_Resume.pdf'

    with open(files2, 'rb') as f:                                     #Opens image from selected path
        file_data2 = f.read()
        file_name2 = f.name

    msg.add_attachment(file_data2, maintype='application', subtype='octet-stream', filename=file_name2)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)                       #Login to mail server with your email and password
        smtp.send_message(msg)                                          #First EMAIL_ADDRESS is source, second is destination

    BigCounter += 1
