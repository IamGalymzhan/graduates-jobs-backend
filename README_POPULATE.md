# Job Posts Population Script

This directory contains scripts to populate the Django application's database with realistic job posts in Kazakh language.

## Files

- `job_posts.json` - Contains 15 realistic job posts in Kazakh language
- `populate_jobs.py` - Script to populate the database with jobs from the JSON file
- `clean_jobs.py` - Script to clean up the created job posts and employer accounts

## How to Use

### Prerequisites

Make sure your Django application is properly set up with the following:

- Virtual environment activated (if applicable)
- Django installed
- Database migrations applied

### Populating the Database

To populate the database with the job posts from the JSON file, run:

```bash
python populate_jobs.py
```

This script will:

1. Create employer accounts for the jobs (if they don't already exist)
2. Create skill records for each job skill (if they don't already exist)
3. Create job posts with randomized creation dates (within the last 30 days)
4. Associate the jobs with employers and skills

### Cleaning the Database

If you need to remove all the created job posts and associated employer accounts, run:

```bash
python clean_jobs.py
```

This script will:

1. Delete all job posts from the database (including their applications through cascade)
2. Delete all employer accounts created by the populate script

## Notes

- The employer accounts are created with a default password of "password123" (this should be changed in production)
- The job posts have realistic salaries for 2025
- More than half of the job posts are IT-related
- Job posts have varied locations (Almaty, Astana) and job types (full-time, part-time, internship)

## Customization

If you want to modify the job posts:

1. Edit the `job_posts.json` file
2. Run the `clean_jobs.py` script to clean existing data
3. Run the `populate_jobs.py` script to add your updated data

## Employer Accounts

The script creates employer accounts with emails in the format:

- `hr@[domain].kz`

where domains are tech-related company names like "techkz", "astanadev", etc.
