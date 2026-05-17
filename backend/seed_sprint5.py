"""
Sprint 5 seed data.

Run from the backend/ directory (with venv active):
    python seed_sprint5.py
"""

import random
import sys
from datetime import date, timedelta

import bcrypt
from sqlalchemy import text

from database import SessionLocal
from entities.user_profile import UserProfile
from entities.user_account import UserAccount
from entities.fra_activity import FRAActivity
from entities.fra_category import FRACategory
from entities.favourite import Favourite
from entities.donation import Donation


def main():
    db = SessionLocal()
    try:
        # ── 1. Ensure Donee profile exists ─────────────────────────────────────
        donee_profile = db.query(UserProfile).filter(UserProfile.profileName == "Donee").first()
        if not donee_profile:
            donee_profile = UserProfile(
                profileName="Donee",
                profileDescription="Donor who searches and donates to FRAs.",
                profileStatus="Active",
            )
            db.add(donee_profile)
            db.commit()
            db.refresh(donee_profile)
            print(f"  Created UserProfile: Donee (ID={donee_profile.profileID})")
        else:
            print(f"  UserProfile 'Donee' already exists (ID={donee_profile.profileID})")

        # ── 2. Create 3 Donee user accounts ────────────────────────────────────
        hashed = bcrypt.hashpw(b"DoneePass123!", bcrypt.gensalt()).decode()
        donee_ids = []
        for username, email in [
            ("donee1", "donee1@fundbridger.com"),
            ("donee2", "donee2@fundbridger.com"),
            ("donee3", "donee3@fundbridger.com"),
        ]:
            existing = db.query(UserAccount).filter(UserAccount.username == username).first()
            if existing:
                donee_ids.append(existing.userID)
                print(f"  UserAccount '{username}' already exists (ID={existing.userID})")
            else:
                user = UserAccount(
                    username=username,
                    email=email,
                    password=hashed,
                    accountStatus="Active",
                    profile_id=donee_profile.profileID,
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                donee_ids.append(user.userID)
                print(f"  Created UserAccount: {username} (ID={user.userID})")

        # ── 3. Ensure at least some FRAs exist ─────────────────────────────────
        fra_count = db.query(FRAActivity).filter(FRAActivity.fraStatus == "Active").count()
        if fra_count == 0:
            print("  No active FRAs found — inserting sample category and FRAs...")
            cat = db.query(FRACategory).first()
            if not cat:
                cat = FRACategory(
                    categoryName="General",
                    categoryDescription="General fundraising",
                    categoryStatus="Active",
                )
                db.add(cat)
                db.commit()
                db.refresh(cat)

            # Find any active user to be owner
            owner = db.query(UserAccount).filter(UserAccount.accountStatus == "Active").first()
            if not owner:
                print("  ERROR: No active user accounts found to be FRA owner.")
                sys.exit(1)

            for i in range(1, 6):
                fra = FRAActivity(
                    fraName=f"Sample FRA #{i}",
                    fraDescription=f"Sample fundraising activity {i}",
                    fraGoalAmount=round(random.uniform(1000, 10000), 2),
                    fraStartDate=date.today() - timedelta(days=30),
                    fraEndDate=date.today() + timedelta(days=180),
                    fraStatus="Active",
                    fraCategoryID=cat.categoryID,
                    fraOwnerID=owner.userID,
                )
                db.add(fra)
            db.commit()
            print("  Inserted 5 sample FRAs.")

        active_fras = db.query(FRAActivity).filter(FRAActivity.fraStatus == "Active").all()
        fra_ids = [f.fraID for f in active_fras]

        # ── 4. Seed 5 Favourite rows ────────────────────────────────────────────
        fav_count = 0
        used_pairs = set()
        for donee_id in donee_ids:
            for fra_id in random.sample(fra_ids, min(2, len(fra_ids))):
                if (donee_id, fra_id) in used_pairs:
                    continue
                existing = db.query(Favourite).filter(
                    Favourite.userID == donee_id,
                    Favourite.fraID  == fra_id,
                ).first()
                if not existing:
                    fav = Favourite(userID=donee_id, fraID=fra_id, savedDate=date.today())
                    db.add(fav)
                    used_pairs.add((donee_id, fra_id))
                    fav_count += 1
                if fav_count >= 5:
                    break
            if fav_count >= 5:
                break
        db.commit()
        print(f"  Inserted {fav_count} Favourite rows.")

        # ── 5. Seed 10 Donation rows ────────────────────────────────────────────
        statuses = ["Completed", "Completed", "Completed", "Completed", "Completed",
                    "Pending", "Pending", "Failed", "Completed", "Completed"]
        don_count = 0
        for i in range(10):
            don = Donation(
                donationAmount=round(random.uniform(10, 500), 2),
                donationDate=date.today() - timedelta(days=random.randint(0, 180)),
                donationStatus=statuses[i],
                fraID=random.choice(fra_ids),
                userID=random.choice(donee_ids),
            )
            db.add(don)
            don_count += 1
        db.commit()
        print(f"  Inserted {don_count} Donation rows.")

        print("\nSeed complete.")
    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
