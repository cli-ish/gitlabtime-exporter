# GitlabTime Exporter

Export all the time you spend on a project and all of its issues with a quick and easy-to-use Python script.

### Installation and Usage

```bash
git clone https://github.com/cli-ish/gitlabtime-exporter
cd gitlabtime-exporter
pip3 install -r requirements.txt
python3 export.py --gitlab-instance https://yourgitlab.com --project-name group/project --access-token xxxxx-XxXxXxXxXxXxXxXxXxXx
cat timesheet-*.csv
```

You can obtain the access token for Gitlab at https://yourgitlab.com/-/profile/personal_access_tokens

A sample output might look like the following:

```csv
Spend At,Spend At Clock,Project,Issue Id,Title,Time Spend,User,Summary
10.02.2023,12:59:17,group/project,#500,Ticket 3,0:20:00,User 3,test message 123
08.02.2023,13:59:17,group/project,#500,Ticket 3,1:00:00,User 2,Some example summary
01.02.2023,14:59:17,group/project,#400,Ticket 2,0:30:00,User 2,
01.02.2017,15:59:17,group/project,#120,Ticket 1,1:30:00,User 1,Test
```

### Note

In some edge cases where you have more than 100 spend commands in an issue, there is a possibility that not all of them will be returned,
I haven't tested this edge case yet. It is pretty unlikely to happen anyway. It could be fixed if the script takes these outputs into a list
and retrieve them later with a paging.
