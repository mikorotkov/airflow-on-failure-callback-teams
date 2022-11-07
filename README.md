# Summary

Function `send_ms_teams_notification` receives definitions for ["message card"](https://docs.microsoft.com/en-us/outlook/actionable-messages/message-card-reference) to be displayed in MS Teams

It then uses [pymsteams](https://github.com/rveachkc/pymsteams) PYPI package to construct this card based on parameters and send it to webhook url (defined separately for each channel in MS teams).

Function `send_notification_on_failure` receives context dictionary from the dag that calls the functions.

Context contains all the information about the dag and it's tasks. After that it calls `send_ms_teams_notification` function with relevant parameters

# Example usage in Airflow

```python
from modules.send_ms_teams_notification import send_notification_on_failure

default_args = {
    "owner": "me@example.com",
    "depends_on_past": True,
    "max_active_runs": 1,
    "wait_for_downstream": True,
    "start_date": schedule['start_date'],
    "on_failure_callback": send_notification_on_failure
}
```
- In first line we import the function `send_ms_teams_notification`. As evident from import path the script in contained in folder `./modules`
- In last line we use this script as callback in case the dag fails.
