
"""Fitness gym membership registration and renewal module."""

import hashlib
import os
import secrets

members = {
    "M01": {
        "name": "Alex",
        "plan": "Gold",
        "months_left": 6,
        "fee": 600.0,
    },
    "M02": {
        "name": "Brooke",
        "plan": "Silver",
        "months_left": 1,
        "fee": 350.0,
    },
    "M03": {
        "name": "Chris",
        "plan": "Platinum",
        "months_left": 12,
        "fee": 1000.0,
    },
}


def register_member(m_id, name, plan, months, member_log=None):
    """Register a member and optionally record the registration."""
    if m_id in members or months <= 0:
        return False

    if member_log is None:
        member_log = []

    members[m_id] = {
        "name": name,
        "plan": plan,
        "months_left": months,
        "fee": 50.0 * months,
    }
    member_log.append(f"Registered {m_id} for {months} months")
    return True


def cancel_membership(m_id):
    """Cancel a membership if the member exists."""
    try:
        del members[m_id]
    except KeyError:
        pass


def check_membership_status(m_id):
    """Return whether a member has an active membership."""
    member = members.get(m_id)
    if member is None:
        return False

    return member["months_left"] > 0


def calculate_renewal_rate(m_id, discount_rate=0.15):
    """Calculate the renewal fee after applying a discount rate."""
    if m_id not in members:
        raise ValueError(f"Unknown member ID: {m_id}")

    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    base_fee = members[m_id]["fee"]
    return base_fee * (1 - discount_rate)


def generate_member_hash(m_id):
    """Generate a SHA-256 digest for a member ID."""
    return hashlib.sha256(m_id.encode("utf-8")).hexdigest()


def generate_locker_pin():
    """Generate a four-digit locker PIN using a secure random generator."""
    return secrets.randbelow(9000) + 1000


def export_member_roster(filename="gym_roster.txt"):
    """Export the member roster to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(members))

    print(f"Roster exported to: {filename}")


def get_active_summary(member_records):
    """Return the number of members with active memberships."""
    return sum(
        1
        for details in member_records.values()
        if details["months_left"] > 0
    )


def main():
    """Demonstrate the gym membership functions."""
    gym_api_secret = os.getenv("GYM_CLOUD_PORTAL_SECRET")

    register_member("M04", "Diana", "Gold", 3)
    cancel_membership("M02")

    print("Is M01 active:", check_membership_status("M01"))
    print("Renewal Fee:", calculate_renewal_rate("M01"))
    print("Member Hash:", generate_member_hash("M01"))
    print("Locker PIN:", generate_locker_pin())

    export_member_roster()
    print("Active count:", get_active_summary(members))

    if gym_api_secret:
        print("Portal secret is configured.")
    else:
        print("Portal secret is not configured.")


if __name__ == "__main__":
    main()
