# ActiveCollab

## Overview
This project aims to build a headless interaction with your active collab using Selenium WebDriver.


## Download stats
[![Downloads](https://static.pepy.tech/badge/ActiveCollab)](https://pepy.tech/project/ActiveCollab) <br>
[![Downloads](https://static.pepy.tech/badge/ActiveCollab/week)](https://pepy.tech/project/ActiveCollab) <br>
[![Downloads](https://static.pepy.tech/badge/ActiveCollab/month)](https://pepy.tech/project/ActiveCollab)


## Installation

```console
pip install ActiveCollab
```
whatsapp-auto officially supports Python 3.8+.

## Usage

### Default
```python
import ActiveCollab

host_url = 'host_url' # Active Collab hosted URL  

user_name = 'your_username_or_email' # Active Collab username or email

password = 'your_password' # Active Collab Password

ac = ActiveCollab.Connect(host_url,user_name,password)  # Login to Active Collab
```



### List all projects
```python
ac.list_projects()  # List out all project assigned to logged in user
```

### List all users
```python
ac.list_users()  # List out all users in your organization with id, name and email
```

### List Users in a Project
```python
ac.list_users_in_project(project_id)  # List out all users in the project (project_id)
```

### + Add User in a Project
```python
ac.add_user_in_project(project_id,user_name_or_user_email)  # Add user in provided project_id
```


### + Add Task in a Project
```python
ac.add_task_in_project(project_id,task_title,task_description,task_assignee)  # Add task in the provided project_id
```

### + Add Note in a Project
```python
ac.add_note_in_project(project_id,note_title,note_content)  # Add note in the provided project_id
```
