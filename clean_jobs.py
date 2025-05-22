import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graduatesjobsbackend.settings")
django.setup()

# Import models after Django setup
from users.models import CustomUser
from jobs.models import JobPost

def main():
    try:
        # Get all employer emails from our company domains
        company_domains = [
            "techkz", "astanadev", "almatyit", "qaztech", "digitalsteppe", 
            "innovationkz", "smarttech", "techtalent", "devkz", "itpro",
            "qazdev", "softwarelab", "techgiant", "aicompany", "cloudkz"
        ]
        
        # Delete all job posts (will cascade delete applications)
        deleted_posts, _ = JobPost.objects.all().delete()
        print(f"Deleted {deleted_posts} job posts and their applications")
        
        # Find and delete employers created by our script
        employers_to_delete = []
        for domain in company_domains:
            email = f"hr@{domain}.kz"
            employer = CustomUser.objects.filter(email=email).first()
            if employer:
                employers_to_delete.append(employer.id)
        
        if employers_to_delete:
            deleted_employers, _ = CustomUser.objects.filter(id__in=employers_to_delete).delete()
            print(f"Deleted {deleted_employers} employer accounts")
        else:
            print("No script-created employer accounts found")
            
        print("Database cleanup complete!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 