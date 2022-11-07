import pymsteams
import urllib.parse
#https://github.com/rveachkc/pymsteams

def send_ms_teams_notification (message="test",
                 subtitle="",
                 button_text="",
                 button_url="",
                 theme_color="ff0000",
                 webhook_url="INSERT_YOU_WEBHOOK_URL_HERE",
                 *args,
                 **kwargs):

    """
    Function send_ms_teams_notification receives definitions for "message card" to be displayed in MS Teams https://docs.microsoft.com/en-us/outlook/actionable-messages/message-card-reference . 
    It then uses pymsteams (https://github.com/rveachkc/pymsteams) package to construct this card based on parameters
    """


    # You must create the connectorcard object with the Microsoft Webhook URL
    myTeamsMessage = pymsteams.connectorcard(webhook_url)

    myTeamsMessage.color(theme_color)
    myTeamsMessage.summary(message)

    myMessageSection = pymsteams.cardsection()

    # Section definition:
    myMessageSection.activityTitle(message)
    myMessageSection.activitySubtitle(subtitle)
    myMessageSection.enableMarkdown()
    
    # Action definition
    myTeamsPotentialAction1 =pymsteams.potentialaction(_name="Add button")
    myTeamsPotentialAction1.addOpenURI(_name=button_text,_targets=[{"os": "default","uri":button_url}])


    # Add text to the message.
    #myTeamsMessage.text("This is a test")
    
    # Add your section to the connector card object before sending
    myTeamsMessage.addSection(myMessageSection)
    # Add your action to the connector card object before sending
    myTeamsMessage.addPotentialAction(myTeamsPotentialAction1)


    # send the message.
    myTeamsMessage.send()
    #myTeamsMessage.printme()




#send_ms_teams_notification(message='This is a test message',button_text='This is a test button',subtitle='Test subtitle', button_url='https://en.wikipedia.org/wiki/Trollface#/media/File:Trollface_non-free.png' )


def send_notification_on_failure(context):

    """
    receives context dictionary from the dag that calls the functions. Context contains all the information about the dag and it's tasks.
    After that it calls send_ms_teams_notification function with relevant parameters.
    """

    dag_id = context['dag_run'].dag_id

    task_id = context['task_instance'].task_id
    context['task_instance'].xcom_push(key=dag_id, value=True)
    execution_date=urllib.parse.quote(context['ts'])

    logs_url = "https://o7a017b6474bb2dc1p-tp.appspot.com/log?dag_id={}&task_id={}&execution_date={}".format(
         dag_id, task_id, execution_date) #log url is always the same with url parameters for dag-id, task_id and execution_date

    teams_notification = send_ms_teams_notification(
        task_id="msteams_notify_failure", trigger_rule="all_done",
        message="pipeline: `{}` has failed on task: `{}`".format(dag_id, task_id),
        button_text="View log in Airflow", button_url=logs_url,
        theme_color="FF0000")
    
    
    teams_notification.execute(context)