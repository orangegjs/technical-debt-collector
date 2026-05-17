from sqlalchemy.orm import Session
from entities.donation import Donation


class RetrieveDonationController:
    def retrieveDonation(self, db: Session, donationID: int):
        return Donation.retrieveDonation(db, donationID)
