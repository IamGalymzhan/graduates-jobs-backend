import os
import json
import django
import random
from datetime import timedelta

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graduatesjobsbackend.settings")
django.setup()

# Import models after Django setup
from django.utils import timezone
from users.models import CustomUser, Skill
from jobs.models import JobPost

def create_employer_if_needed(company_name, domain):
    """Create an employer user if it doesn't exist"""
    # Generate a unique email based on company name
    email = f"hr@{domain}.kz".lower()
    
    # Check if employer exists
    employer = CustomUser.objects.filter(email=email).first()
    
    if not employer:
        # Create a new employer
        password = "password123"  # In production, use a secure random password
        employer = CustomUser.objects.create_user(
            email=email,
            password=password,
            full_name=f"HR Manager {company_name}",
            user_type="employer",
            company_name=company_name,
            company_website=f"https://www.{domain}.kz",
            company_description=f"{company_name} - это инновационная компания, работающая над передовыми технологиями в своей отрасли."
        )
        print(f"Created employer: {employer.email}")
    
    return employer

def get_or_create_skills(skill_names):
    """Get or create skills from the list of skill names"""
    skills = []
    for skill_name in skill_names:
        skill, created = Skill.objects.get_or_create(name=skill_name)
        skills.append(skill)
    return skills

def main():
    try:
        # Load job posts from JSON file
        with open('job_posts.json', 'r', encoding='utf-8') as f:
            job_posts_data = json.load(f)
        
        # Company domains for email generation
        company_domains = [
            "techkz", "astanadev", "almatyit", "qaztech", "digitalsteppe", 
            "innovationkz", "smarttech", "techtalent", "devkz", "itpro",
            "qazdev", "softwarelab", "techgiant", "aicompany", "cloudkz"
        ]
        
        # List of company names (one for each job post)
        company_names = [
            "TechKZ Solutions", "Astana Dev Group", "Almaty IT Services", "QazTech Systems",
            "Digital Steppe", "Innovation KZ", "SmartTech Kazakhstan", "Tech Talent KZ",
            "DevKZ", "IT Pro Kazakhstan", "QazDev", "Software Lab KZ", "Tech Giant KZ",
            "AI Company KZ", "CloudKZ Technologies"
        ]
        
        print("Starting job posts population...")
        
        # Randomize created_at dates within the last 30 days
        now = timezone.now()
        
        # Create job posts
        for i, job_data in enumerate(job_posts_data):
            # Create employer if needed (allocate companies sequentially)
            company_index = i % len(company_names)
            employer = create_employer_if_needed(company_names[company_index], company_domains[company_index])
            
            # Get or create skills
            skills = get_or_create_skills(job_data["skills"])
            
            # Random date within the last 30 days
            days_ago = random.randint(0, 30)
            created_at = now - timedelta(days=days_ago)
            
            # Create job post
            job_post = JobPost.objects.create(
                employer=employer,
                title=job_data["title"],
                description=job_data["description"],
                requirements=job_data["requirements"],
                salary=job_data["salary"],
                location=job_data["location"],
                job_type=job_data["job_type"],
                created_at=created_at
            )
            
            # Add skills to job post (many-to-many field)
            job_post.skills.set(skills)
            
            print(f"Created job post: {job_post.title}")
        
        print(f"Successfully created {len(job_posts_data)} job posts!")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 