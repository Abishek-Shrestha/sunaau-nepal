from django.core.management.base import BaseCommand
from accounts.models import Municipality


class Command(BaseCommand):
    help = 'Seed Nepal municipalities data'

    def handle(self, *args, **kwargs):
        municipalities = [
            # Metropolitan Cities (6)
            ("Kathmandu Metropolitan City", "Kathmandu", "Bagmati"),
            ("Lalitpur Metropolitan City", "Lalitpur", "Bagmati"),
            ("Bharatpur Metropolitan City", "Chitwan", "Bagmati"),
            ("Pokhara Metropolitan City", "Kaski", "Gandaki"),
            ("Biratnagar Metropolitan City", "Morang", "Koshi"),
            ("Birgunj Metropolitan City", "Parsa", "Madhesh"),
            # Sub-Metropolitan Cities (11)
            ("Bhaktapur Municipality", "Bhaktapur", "Bagmati"),
            ("Kirtipur Municipality", "Kathmandu", "Bagmati"),
            ("Madhyapur Thimi Municipality", "Bhaktapur", "Bagmati"),
            ("Budhanilkantha Municipality", "Kathmandu", "Bagmati"),
            ("Tokha Municipality", "Kathmandu", "Bagmati"),
            ("Gokarneshwor Municipality", "Kathmandu", "Bagmati"),
            ("Kageshwori Manahara Municipality", "Kathmandu", "Bagmati"),
            ("Tarakeshwor Municipality", "Kathmandu", "Bagmati"),
            ("Chandragiri Municipality", "Kathmandu", "Bagmati"),
            ("Nagarjun Municipality", "Kathmandu", "Bagmati"),
            ("Shankharapur Municipality", "Kathmandu", "Bagmati"),
            # Gandaki Province
            ("Lekhnath Municipality", "Kaski", "Gandaki"),
            ("Waling Municipality", "Syangja", "Gandaki"),
            ("Baglung Municipality", "Baglung", "Gandaki"),
            ("Gorkha Municipality", "Gorkha", "Gandaki"),
            # Koshi Province
            ("Dharan Sub-Metropolitan City", "Sunsari", "Koshi"),
            ("Itahari Sub-Metropolitan City", "Sunsari", "Koshi"),
            ("Damak Municipality", "Jhapa", "Koshi"),
            ("Birtamod Municipality", "Jhapa", "Koshi"),
            ("Mechinagar Municipality", "Jhapa", "Koshi"),
            ("Ilam Municipality", "Ilam", "Koshi"),
            # Madhesh Province
            ("Janakpurdham Sub-Metropolitan City", "Dhanusha", "Madhesh"),
            ("Rajbiraj Municipality", "Saptari", "Madhesh"),
            ("Lahan Municipality", "Siraha", "Madhesh"),
            ("Jaleshwor Municipality", "Mahottari", "Madhesh"),
            # Lumbini Province
            ("Butwal Sub-Metropolitan City", "Rupandehi", "Lumbini"),
            ("Bhairahawa (Siddharthanagar)", "Rupandehi", "Lumbini"),
            ("Tansen Municipality", "Palpa", "Lumbini"),
            ("Tulsipur Sub-Metropolitan City", "Dang", "Lumbini"),
            ("Ghorahi Sub-Metropolitan City", "Dang", "Lumbini"),
            # Karnali Province
            ("Birendranagar Municipality", "Surkhet", "Karnali"),
            ("Jumla Municipality", "Jumla", "Karnali"),
            # Sudurpashchim Province
            ("Dhangadhi Sub-Metropolitan City", "Kailali", "Sudurpashchim"),
            ("Mahendranagar Municipality", "Kanchanpur", "Sudurpashchim"),
        ]

        created = 0
        for name, district, province in municipalities:
            obj, was_created = Municipality.objects.get_or_create(
                name=name,
                defaults={'district': district, 'province': province}
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f'✅ Done! {created} municipalities added.')
        )