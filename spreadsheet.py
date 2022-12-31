
import datetime
import gspread
import random
from oauth2client.service_account import ServiceAccountCredentials
import emailing as em

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Face recognition").sheet1

max_intime = '21:00:00'

presentStudents = []


def enroll_person_to_sheet(name, email):
    nrows = len(sheet.col_values(1))
    pin = random.randint(999, 9999)
    sheet.update_cell(nrows+1, 1, name)
    sheet.update_cell(nrows+1, 2, email)
    sheet.update_cell(nrows+1, 3, pin)
    em.email_pin(email, pin)

def write_to_sheet(name):
    
    now = datetime.datetime.now()
    date = now.strftime('%m/%d/%Y').replace('/0', '/')
    if (date[0] == '0'):
        date = date[1:]
    time = now.strftime('%H:%M:%S')
    namecell = sheet.find(name)
    datecell = sheet.find(date)

    if name in presentStudents:
        return


    if (sheet.cell(namecell.row, datecell.col).value == 'absent' or sheet.cell(namecell.row, datecell.col).value == None):
        if (time < max_intime):
            sheet.update_cell(namecell.row, datecell.col, 'present')
            print('%s is Present' % name)
            presentStudents.append( name )
            em.send_email(sheet.cell(namecell.row, 2).value, "present")

        else:
            # sheet.update_cell(namecell.row,datecell.col,'late')
            print('late')
            em.send_email(sheet.cell(namecell.row, 2).value, "absent")
    else:
        print('already recorded')
        return

def mark_absent():
    
    now = datetime.datetime.now()
    date = now.strftime('%m/%d/%Y').replace('/0', '/')
    if (date[0] == '0'):
        date = date[1:]
    time = now.strftime('%H:%M:%S')
    datecell = sheet.find(date)

    for i in range( 2 ,7 ):
         if sheet.cell( i , datecell.col ).value == None :
            sheet.update_cell( i , datecell.col ,  'absent' )


