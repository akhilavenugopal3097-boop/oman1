#!/usr/bin/env python
import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oman.settings')  # CHANGE THIS to your project name
django.setup()

from oman_app.models import CreditPackage

def create_packages():
    print("📦 Creating credit packages...")
    print("-" * 50)
    
    # First, check if packages already exist
    if CreditPackage.objects.count() > 0:
        print(f"⚠️ Packages already exist! Found {CreditPackage.objects.count()} packages.")
        response = input("Do you want to delete existing packages and recreate? (yes/no): ")
        if response.lower() == 'yes':
            CreditPackage.objects.all().delete()
            print("✅ Deleted existing packages.")
        else:
            print("❌ Cancelled.")
            return
    
    # Define all packages
    packages = [
        # Listing Packages
        CreditPackage(
            name="5 Listings",
            package_type='listing',
            listing_credits=5,
            price_omr=Decimal('5.000'),
            validity_days=45,
            display_order=1,
            description="5 listing credits. Valid for 45 days.",
            features=["5 Ad Listings", "45 Days Validity", "Reusable Credits"]
        ),
        CreditPackage(
            name="10 Listings",
            package_type='listing',
            listing_credits=10,
            price_omr=Decimal('8.000'),
            validity_days=45,
            display_order=2,
            description="10 listing credits. Valid for 45 days.",
            features=["10 Ad Listings", "45 Days Validity", "Reusable Credits", "Save 20%"]
        ),
        CreditPackage(
            name="15 Listings",
            package_type='listing',
            listing_credits=15,
            price_omr=Decimal('13.000'),
            validity_days=45,
            display_order=3,
            description="15 listing credits. Valid for 45 days.",
            features=["15 Ad Listings", "45 Days Validity", "Reusable Credits", "Save 35%"]
        ),
        
        # Individual Boost
        CreditPackage(
            name="Boost - 7 Days",
            package_type='boost_individual',
            boost_days=7,
            boost_posts_count=1,
            price_omr=Decimal('8.000'),
            validity_days=365,
            display_order=4,
            description="Boost a single ad for 7 days.",
            features=["1 Ad Boosted", "7 Days Duration", "Premium Placement"]
        ),
        CreditPackage(
            name="Boost - 14 Days",
            package_type='boost_individual',
            boost_days=14,
            boost_posts_count=1,
            price_omr=Decimal('10.000'),
            validity_days=365,
            display_order=5,
            description="Boost a single ad for 14 days.",
            features=["1 Ad Boosted", "14 Days Duration", "Premium Placement", "Priority Visibility"]
        ),
        CreditPackage(
            name="Boost - 30 Days",
            package_type='boost_individual',
            boost_days=30,
            boost_posts_count=1,
            price_omr=Decimal('15.000'),
            validity_days=365,
            display_order=6,
            description="Boost a single ad for 30 days.",
            features=["1 Ad Boosted", "30 Days Duration", "Premium Placement", "Maximum Visibility"]
        ),
        
        # Bulk Boost - 7 Days
        CreditPackage(
            name="Bulk Boost - 5 Posts (7 Days)",
            package_type='boost_bulk',
            boost_days=7,
            boost_posts_count=5,
            price_omr=Decimal('30.000'),
            validity_days=365,
            is_bulk=True,
            display_order=7,
            description="Boost 5 ads for 7 days each.",
            features=["5 Ads Boosted", "7 Days Each", "Save 25%", "Best for Dealers"]
        ),
        CreditPackage(
            name="Bulk Boost - 10 Posts (7 Days)",
            package_type='boost_bulk',
            boost_days=7,
            boost_posts_count=10,
            price_omr=Decimal('55.000'),
            validity_days=365,
            is_bulk=True,
            display_order=8,
            description="Boost 10 ads for 7 days each.",
            features=["10 Ads Boosted", "7 Days Each", "Save 31%", "Best for Dealers"]
        ),
        
        # Bulk Boost - 14 Days
        CreditPackage(
            name="Bulk Boost - 5 Posts (14 Days)",
            package_type='boost_bulk',
            boost_days=14,
            boost_posts_count=5,
            price_omr=Decimal('40.000'),
            validity_days=365,
            is_bulk=True,
            display_order=9,
            description="Boost 5 ads for 14 days each.",
            features=["5 Ads Boosted", "14 Days Each", "Save 20%", "Best for Dealers"]
        ),
        CreditPackage(
            name="Bulk Boost - 10 Posts (14 Days)",
            package_type='boost_bulk',
            boost_days=14,
            boost_posts_count=10,
            price_omr=Decimal('75.000'),
            validity_days=365,
            is_bulk=True,
            display_order=10,
            description="Boost 10 ads for 14 days each.",
            features=["10 Ads Boosted", "14 Days Each", "Save 25%", "Best for Dealers"]
        ),
        
        # Business Package
        CreditPackage(
            name="Business Package",
            package_type='business',
            listing_credits=0,
            price_omr=Decimal('16.000'),
            validity_days=365,
            is_business=True,
            business_duration_days=365,
            display_order=11,
            description="Business package for professionals. 1 year validity.",
            features=[
                "Unlimited Listings",
                "Priority Support",
                "Featured Badge",
                "1 Free Boost (7 days)/month",
                "Analytics Dashboard",
                "Customizable Options"
            ]
        ),
    ]
    
    # Save all packages
    for package in packages:
        package.save()
        print(f"✅ Created: {package.name} - {package.price_omr} OMR")
    
    print("-" * 50)
    print(f"🎉 Success! Created {len(packages)} credit packages.")
    print("\n📊 Summary:")
    print(f"   - Listing Packages: 3")
    print(f"   - Individual Boosts: 3")
    print(f"   - Bulk Boosts (7 days): 2")
    print(f"   - Bulk Boosts (14 days): 2")
    print(f"   - Business Package: 1")

if __name__ == "__main__":
    create_packages()