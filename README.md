# Intro - Library Management System

<img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white"/> <img alt="Django" src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white"/>


The project aims and objectives that will be achieved after completion of this project. The
aims and objectives are as follows:
- Online book issue
- Request column for librarian for providing new books
- A separate column for digital library
- Student login page where students can find books issued by him/her and date of return.
- A search column to search availability of books
- A teacher login page where mentors can add any events being organized in the
college and important suggestions regarding books.
- Online notice board about the workshop
- Subscription for emails and newsletters (Advance Level task)

## Status
 - In api/views.py, Notice serializer 
   - for students allow POST request ( Do not allow modification of is_approved field ). Do not allow acces to modify, delete.
   - separate view for librarian to approve notices.
   - by deafult only approved notices to be put up on noticeboard


## Development - Do when working on deployment to Heroku

1. Install requirements from requirements.txt ( preferably setup a [virtual environment!](https://docs.python.org/3/library/venv.html))

2. Set environment variables ``` SECRET_KEY ``` and ``` DEBUG ``` to get your website up and running on a 'nix OS ( [guide for other OS](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) )
   
   ```bash
   $ export SECRET_KEY=yourKeyHere
   $ export DEBUG=True #for development, for production set False
   ```