from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
# import logging

#Function to create/get credentials 
def getCreds():
    scopes = ["https://www.googleapis.com/auth/calendar", "https://mail.google.com/"] # Give all(read/write/delete) access to this app 
    flow = InstalledAppFlow.from_client_secrets_file("Creds/client_secret.json", scopes)
    try:
        # Uses the previous credentials if existing
        credentials = pickle.load(open("Creds/user_token.pkl", "rb"))
        return credentials
    except:
        # This takes user to grant access screen of Google on a browser
        credentials = flow.run_console()
        pickle.dump(credentials, open("Creds/user_token.pkl", "wb"))
        return credentials


# Function to create calendar function
def createCalendarService(credentials):
    try:
        #Creating calendar service of Google and returning the service
        service = build("calendar", "v3", credentials=credentials) 
        return service
    except IOError as e:
        return str(e)

def createGmailService(credentials):
    serviceGmail = build('gmail', 'v1', credentials=credentials)
    return serviceGmail


# Function to get all calendars in calendar
def getCalendars(service):
    result = []
    calendars = service.calendarList().list().execute()
    for i in calendars["items"]:
        #Accepted values to append are summary, id, kind, etag, timeZone, colorId, backgroundColor, foregroundColor, selected, accessRole, defaultReminders, notificationSettings, primary, conferenceProperties
        result.append(i["summary"])
    if result:
        return result
    else:
        return "no calendars"


# Function to get all events in calendar
def getEvents(service):
    result = []
    # optParams = {'timeMax': '2022-6-27T23:59:59+00:00','timeMin': '2022-6-28T00:00:01+00:00'}
    events = service.events().list(calendarId='primary', pageToken=None).execute()
    for event in events['items']:
        try:
            result.append(event['summary'])
        except:
            result.append("No summary for this event")
    if result:
        return result
    else:
        return "No events"

def getEmails():
    result = []
    return result

#Generating user credentials
credentials = getCreds()
#Creating claendar service
service = createCalendarService(credentials)
serviceGmail = createGmailService(credentials)
results = serviceGmail.users().labels().list(userId='me').execute()
print("Results\n", results)
#Get all calendars present
# calendars = getCalendars(service)
# print("Calendars", calendars)
#Get all events
# events = getEvents(service)
# print("Events", events)

