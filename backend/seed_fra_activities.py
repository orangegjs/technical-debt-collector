"""
Seed script: inserts 100 FRA activities into the database.

Constraints enforced at runtime:
  - fraCategoryID must reference an active FRA category (categoryStatus = "Active")
  - fraOwnerID must reference an active Fund Raiser account (accountStatus = "Active",
    role = "Fund Raiser")

Run from the backend/ directory:
    python seed_fra_activities.py
"""

import random
import sys
from datetime import date, timedelta

from sqlalchemy import text

from database import SessionLocal
from entities.fra_activity import FRAActivity
from entities.fra_category import FRACategory
from entities.user_account import UserAccount

CAMPAIGN_NAMES = [
    "Clean Water for All", "Books for Bright Minds", "Feed the Hungry",
    "Shelter from the Storm", "Medical Aid Mission", "Education First",
    "Trees for Tomorrow", "Hope Rebuilds", "Children's Safe Haven",
    "Community Health Drive", "Light Up Lives", "Voices for Change",
    "Fresh Start Initiative", "Empowering Women", "Youth Tech Program",
    "Disaster Relief Fund", "Animal Rescue Network", "Senior Care Support",
    "Mental Health Matters", "Green Energy Push", "Flood Recovery Aid",
    "Back to School Drive", "Rural Health Outreach", "Hunger-Free Campaign",
    "Sports for Youth", "Bridge to Employment", "Ocean Cleanup Project",
    "Literacy for Life", "Safe Homes Initiative", "Kindness in Action",
]

DESCRIPTIONS = [
    "Providing essential resources to underserved communities across the region.",
    "Raising funds to support families affected by natural disasters.",
    "Connecting donors with those who need immediate assistance.",
    "Building long-term solutions for sustainable community development.",
    "Empowering individuals through education and skill-building programs.",
    "Supporting local volunteers delivering aid to vulnerable populations.",
    "Creating safe spaces and opportunities for youth to thrive.",
    "Funding critical medical supplies for remote areas with limited access.",
    "Partnering with NGOs to deliver lasting change at the grassroots level.",
    "Mobilising community support to tackle poverty and inequality.",
]

STATUSES = ["Active"] * 7 + ["Suspended"] * 2 + ["Completed"] * 1


def main():
    db = SessionLocal()
    try:
        # Fetch active categories
        active_categories = (
            db.query(FRACategory)
            .filter(FRACategory.categoryStatus == "Active")
            .all()
        )
        if not active_categories:
            print("ERROR: No active FRA categories found. Add some categories first.")
            sys.exit(1)

        # Fetch active Fund Raiser accounts (role stored directly on user_account)
        active_fund_raisers = (
            db.query(UserAccount)
            .filter(
                UserAccount.accountStatus == "Active",
                text("user_account.role = 'Fund Raiser'"),
            )
            .all()
        )
        if not active_fund_raisers:
            print("ERROR: No active Fund Raiser accounts found. Create some first.")
            sys.exit(1)

        print(f"Found {len(active_categories)} active category/ies and "
              f"{len(active_fund_raisers)} active Fund Raiser(s). Seeding 100 FRAs...")

        category_ids = [c.categoryID for c in active_categories]
        owner_ids = [u.userID for u in active_fund_raisers]

        inserted = 0
        skipped = 0
        index = 1

        while inserted < 100:
            base = random.choice(CAMPAIGN_NAMES)
            fra_name = f"{base} #{index}"
            index += 1

            # Check uniqueness (fraName has a unique constraint)
            exists = db.query(FRAActivity).filter(FRAActivity.fraName == fra_name).first()
            if exists:
                skipped += 1
                continue

            start_offset = random.randint(-365, 180)
            start_date = date.today() + timedelta(days=start_offset)
            end_date = start_date + timedelta(days=random.randint(30, 365))

            fra = FRAActivity(
                fraName=fra_name,
                fraDescription=random.choice(DESCRIPTIONS),
                fraGoalAmount=round(random.uniform(500, 50000), 2),
                fraStartDate=start_date,
                fraEndDate=end_date,
                fraStatus=random.choice(STATUSES),
                fraCategoryID=random.choice(category_ids),
                fraOwnerID=random.choice(owner_ids),
            )
            db.add(fra)
            db.commit()
            inserted += 1
            print(f"  [{inserted}/100] Inserted: {fra_name}")

        print(f"\nDone. {inserted} FRA activities inserted, {skipped} name collision(s) skipped.")

    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
