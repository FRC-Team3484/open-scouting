from django.core.management.base import BaseCommand, CommandError
from authentication.models import Profile, Settings
from django.contrib.auth import get_user_model
import getpass

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a default superuser, and a profile and settings object for that superuser"

    def handle(self, *args, **options):
        try:
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    "\nCreating a superuser with profile and settings object...\n"
                )
            )

            username = input("Username: ")
            email = input("Email: ")
            password = getpass.getpass("Password: ")
            confirm_password = getpass.getpass("Password (confirm): ")
            if password != confirm_password:
                raise CommandError("Passwords do not match")

            display_name = input("Profile display name: ")
            team_number = input("Profile team number: ")

            user = User.objects.create_superuser(username, email, password)
            Profile.objects.create(
                user=user, display_name=display_name, team_number=team_number
            )
            Settings.objects.create(user=user)

            self.stdout.write(self.style.SUCCESS("Successfully created superuser"))
        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR("\nOperation cancelled"))
