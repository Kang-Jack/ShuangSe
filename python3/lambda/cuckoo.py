import datetime
import boto3
from jinja2 import Template

# Start of some things you need to change
#
#
# Recipient emails or domains in the AWS Email Sandbox must be verified
# You'll want to change this to the email you verify in SES
FROM_ADDRESS='arise.laserk@gmail.com'
REPLY_TO_ADDRESS='arise.laserk@gmail.com'

# You'll also need to change these to email addresses you verify in AWS
CLIENTS = [
    # Format: [email, 'first name', 'last name', 'pet name']
    ['laserk@sina.com', 'Zoe', 'Washburne', 'Firefly II'],
    ['arise.laserk@gmail.com', 'Fernando', 'Medina Corey', 'Riley']                
]

EMPLOYEES = [
    # Content stored in this order: [email, first_name, last_name]
    # Change to any email you verify in SES
    ['laserk@sina.com', 'Homer', 'Simpson']
]

# Change to the bucket you create on your AWS account
TEMPLATE_S3_BUCKET = 'shuang-se-templates'
#
#
# End of things you need to change

def get_template_from_s3(key):
    """Loads and returns html template from Amazon S3"""
    s3 = boto3.client('s3')
    s3_file = s3.get_object(Bucket = TEMPLATE_S3_BUCKET, Key = key)
    try:
        template = Template(s3_file['Body'].read().decode('utf-8'))
    except Exception as e:
        print ('Failed to load template')
        raise e
    return template

def render_come_to_work_template(employee_first_name):
    subject = 'Work Schedule Reminder'
    template = get_template_from_s3('come_to_work.html')
    html_email = template.render(first_name = employee_first_name)
    plaintext_email = 'Hello {0}, \nPlease remember to be into work by 8am'.format(employee_first_name)
    return html_email, plaintext_email, subject

def render_daily_tasks_template():
    subject = 'Daily Tasks Reminder'
    template = get_template_from_s3('daily_tasks.html')
    tasks = {
        'Monday': '1. Clean the dog areas\n',
        'Tuesday': '1. Clean the cat areas\n',
        'Wednesday': '1. Feed the aligator\n',
        'Thursday': '1. Clean the dog areas\n',
        'Friday': '1. Clean the cat areas\n',
        'Saturday': '1. Relax!\n2. Play with the puppies! It\'s the weekend!',
        'Sunday': '1. Relax!\n2. Play with the puppies! It\'s the weekend!'
    }
    # Gets an integer value from 0 to 6 for today (Monday - Sunday)
    # Keep in mind this will run in GMT and you will need to adjust runtimes accordingly 
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    today = days[datetime.date.today().weekday()]
    html_email = template.render(day_of_week = today, daily_tasks = tasks[today])
    plaintext_email = (
        "Remember to do all of these today:\n"
        "1. Feed the dogs\n"
        "2. Feed the rabbits\n"
        "3. Feed the cats\n"
        "4. Feed the turtles\n"
        "5. Walk the dogs\n"
        "6. Empty cat litterboxes\n"
        "And:\n"
        "{0}".format(tasks[today])
    )
    return html_email, plaintext_email, subject

def render_pickup_template(client_first_name, client_pet_name):
    subject = 'Pickup Reminder'
    template = get_template_from_s3('pickup.html')
    html_email = template.render(first_name = client_first_name, pet_name = client_pet_name)
    plaintext_email = 'Hello {0}, \nPlease remember to pickup {1} by 7pm!'.format(client_first_name, client_pet_name)
    return html_email, plaintext_email, subject

def send_email(html_email, plaintext_email, subject, recipients):
    try:
        ses = boto3.client('ses',region_name='us-east-1')
        response = ses.send_email(
            Source=FROM_ADDRESS,
            Destination={
                'ToAddresses': recipients,
                'CcAddresses': [],
                'BccAddresses': []
            },
            Message={
                'Subject': {
                    'Data': subject,
                },
                'Body': {
                    'Text': {
                        'Data': plaintext_email
                    },
                    'Html': {
                        'Data': html_email
                    }
                }
            },
            ReplyToAddresses=[
                REPLY_TO_ADDRESS,
            ]
        )
    except Exception as e:
        print ('Failed to send message via SES')
        print (e.message)
        raise e

def handler(event,context):
    event_trigger = event['resources'][0]
    print ('event triggered by ' + event_trigger)
    if 'come_to_work' in event_trigger:
        for employee in EMPLOYEES:
            email = []
            email.append(employee[0])
            employee_first_name = employee[1]
            html_email, plaintext_email, subject = render_come_to_work_template(employee_first_name)
            send_email(html_email, plaintext_email, subject, email)
    elif 'daily_tasks' in event_trigger:
        for employee in EMPLOYEES:
            email = []
            email.append(employee[0])
            html_email, plaintext_email, subject = render_daily_tasks_template()
            send_email(html_email, plaintext_email, subject, email)
    elif 'pickup' in event_trigger:
        for client in CLIENTS:
            email = []
            email.append(client[0])
            client_first_name = client[1]
            pet_name = client[3]
            html_email, plaintext_email, subject = render_pickup_template(client_first_name, pet_name)
            send_email(html_email, plaintext_email, subject, email)
    else:
        return 'No template for this trigger!'

