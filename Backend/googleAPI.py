from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

from regex import E
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
def createService(credentials):
    try:
        #Creating calendar service of Google and returning the service
        serviceCalendar = build("calendar", "v3", credentials=credentials) 
        serviceGmail = build('gmail', 'v1', credentials=credentials)
        return serviceCalendar, serviceGmail
    except IOError as e:
        return str(e)


# Function to get all calendars in calendar
def getCalendars(serviceCalendar):
    result = []
    calendars = serviceCalendar.calendarList().list().execute()
    for i in calendars["items"]:
        #Accepted values to append are summary, id, kind, etag, timeZone, colorId, backgroundColor, foregroundColor, selected, accessRole, defaultReminders, notificationSettings, primary, conferenceProperties
        result.append(i["summary"])
    if result:
        return result
    else:
        return "no calendars"


# Function to get all events in calendar
def getEvents(serviceCalendar):
    result = []
    # optParams = {'timeMax': '2022-6-27T23:59:59+00:00','timeMin': '2022-6-28T00:00:01+00:00'}
    events = serviceCalendar.events().list(calendarId='primary', pageToken=None).execute()
    for event in events['items']:
        try:
            result.append(event['summary'])
        except:
            result.append("No summary for this event")
    if result:
        return result
    else:
        return "No events"


def getMessageDetails(serviceGmail, message_id, format='metadata', metadata_headers=[]):
    try:
        result = serviceGmail.users().messages().get(
            userId = "me",
            id = message_id,
            format = format,
            metadataHeaders = metadata_headers
        ).execute()
        return result
    except Exception as e:
        return None


def searchEmails(serviceGmail, label_Ids, query):
    resultSubject = []
    try:
        result_mail = serviceGmail.users().messages().list(
            userId = "me",
            labelIds = label_Ids, 
            q = query
        ).execute()
        result = result_mail.get('messages')
        nextPageToken = result_mail.get('nextPageToken')
        while nextPageToken:
            result_mail = serviceGmail.users().messages().list(
                userId = "me",
                labelIds = label_Ids, 
                q = query,
                pageToken = nextPageToken
            ).execute()
            result.extend(result_mail.get('messages'))
            nextPageToken = result_mail.get('nextPageToken')
        print("Result: ", result)
        for i in result:
            messageId = i['threadId']
            messageDetial = getMessageDetails(serviceGmail, i['id'], format='full', metadata_headers=['parts'])
            messageDetialPayload = messageDetial.get('payload')
            for j in messageDetialPayload['headers']:
                if j['name'] == "Subject":
                    if j['value']:
                        messageSubject = '{0}'.format(j['value'])
                        resultSubject.append(str(messageSubject))
                    else:
                        messageSubject = 'No Subject'
                        resultSubject.append(str(messageSubject))
        return result, resultSubject
    except Exception as e:
        return str(e)


#Generating user credentials
credentials = getCreds()
#Creating claendar & gmail service
serviceCalendar, serviceGmail = createService(credentials)
#Get all calendars present
# calendars = getCalendars(service)
# print("Calendars", calendars)
#Get all events
# events = getEvents(service)
# print("Events", events)

# Gmail 
# result, resultSubject = searchEmails(serviceGmail, ['INBOX'], 'from:PlayStation')
# for k in resultSubject:
#     print(k)

