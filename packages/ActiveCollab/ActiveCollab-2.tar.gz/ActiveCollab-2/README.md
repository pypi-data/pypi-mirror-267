# ActiveCollab

## Overview
This project aims to build a headless interaction with your active collab using Selenium WebDriver.


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

### List users in a project

```python
ac.list_users_in_project(project_id)  # List out all users in the project (project_id)
```

### add user in a project

```python
ac.add_user_in_project(project_id,user_name_or_user_email)  # Add user in provided project_id
```
