"""make_eval.py: writes the evaluation sets eval/ to eval9/, size/ and size2/. No LLM, no GPU.

    python -m experiments.make_eval eval9      (only the sets named; all if none)

An evaluation set measures the formal check on specs that were NOT used to
develop the prompts. Each set is held-out until its results are read to
design something; from then on it is development data:

    eval/    written 2026-11-17. Held-out in E4 and E5; development data since.
    eval2/   written 2026-11-18. Held-out in E7; development data since.
    eval3/   written 2026-11-18. Held-out in E8; development data since.
    eval4/   written 2026-11-18. Held-out in E9; development data since.
    eval5/   written 2026-11-18. Held-out in E10; development data since.
    eval6/   written 2026-11-19. Held-out in E11; development data since.
    eval7/   written 2026-11-19, after E11. Held-out in E12; development data since.
    eval8/   written 2026-11-20, after E12 and T15. Held-out in E13; development
             data since.
    size/    written 2026-11-20 with eval8/: one spec of 30 requirements, to
             see what a larger document does. Not part of the eval8 numbers.
             Read in E13; development data since.
    size2/   written 2026-11-22: one spec of 100 requirements. Read in E14.
    eval9/   written 2026-11-23, after T19, before the parentheses repair of
             the facts vote. Same design as eval8/.

Each set has six small specs (new domains; half Kiro EARS, half OpenSpec), each
in several versions. The defects are planted by rule, so the expected answer is
known by construction:

    clean      nothing planted. Any reported conflict is a false alarm.
    direct     one requirement added that plainly contradicts an existing one
               (a blanket prohibition, or the opposite outcome on the same trigger).
    overlap    one requirement added whose condition can hold together with an
               existing one, with an incompatible outcome (an exception that
               nobody reconciled). The clash needs both conditions to line up.
    ambiguity  one requirement reworded so that it has two readings
               (eval2 and eval3 have two such versions per spec).
    gap        (eval8 on) one of two complementary requirements removed: "WHEN a
               container is inserted AND it is on the list" stays, "... AND it
               is not on the list" goes. Nothing then says what to do in that case.

eval3 to eval6 have one conflict version per spec, and two kinds of
ambiguity per spec, three specs per kind: a boundary, the scope of
"and"/"or", the scope of "only", the scope of "if". Their clean specs also
contain, as real specs do, events that could clash if they happened at the
same moment; eval4 adds counted events ("for the third time"); eval6 adds
conflicts whose WHEN part is a state ("WHEN the station is out of order").

Written per version: experiments/sets/<set>/<spec>_<version>/spec.md and expected.json with

    conflicts  groups of requirement numbers (position in the document) that
               must be reported as conflicts
    ambiguous  requirement numbers that must be flagged as ambiguous
    allowed    conflicts that are a fair consequence of a planted ambiguity:
               neither required nor counted as false alarms
    gaps       (gap versions) requirement numbers: a gap must be reported in
               which the event of that requirement happens
    covered    (clean versions, eval8 on) requirement numbers whose event has
               all its cases covered: a gap in which it happens is a false alarm
"""

import json
import sys
from pathlib import Path

# Each spec: format, intro text, the clean requirements, and its variants.
# A variant is (added, replaced or removed requirements, expected.json content).
# "add" appends a requirement; "replace" maps a requirement number to a new
# text; "remove" takes the requirement with that number out (eval8 on).
SPECS = {
    "library": {
        "format": "ears",
        "intro": "As a library member, I want to borrow and return books, so that I can read them at home.",
        "rules": [
            "WHEN a member requests to borrow a book AND the book is available AND the member has no unpaid fines, THE Library System SHALL lend the book to the member.",
            "WHEN a member requests to borrow a book AND the book is not available AND the member has no unpaid fines, THE Library System SHALL add the member to the waiting list for the book.",
            "WHEN a member requests to borrow a book AND the member has unpaid fines, THE Library System SHALL refuse the request.",
            "WHEN a member returns a book, THE Library System SHALL mark the book as available.",
            "WHEN a member returns a book more than 14 days after borrowing it, THE Library System SHALL add a fine to the member's account.",
        ],
        "variants": {
            "direct": ({"add": "THE Library System SHALL NOT add any member to a waiting list."},
                       {"conflicts": [[2, 6]]}),
            "overlap": ({"add": "WHILE a book is reserved for another member, THE Library System SHALL NOT lend the book."},
                        {"conflicts": [[1, 6]]}),
            "ambiguity": ({"replace": {5: "WHEN a member has had a book on loan for 14 days, THE Library System SHALL add a fine to the member's account."}},
                          {"ambiguous": [5]}),
        },
    },
    "parking": {
        "format": "openspec",
        "intro": "The parking garage lets cars in and out and makes sure every stay is paid.",
        "rules": [
            ("Entry", "Space available", "WHEN a car arrives at the entry AND a space is free THEN the system opens the entry barrier"),
            ("Entry", "Garage full", "WHEN a car arrives at the entry AND no space is free THEN the system keeps the entry barrier closed and shows FULL"),
            ("Exit", "Paid ticket", "WHEN a car arrives at the exit AND its ticket is paid THEN the system opens the exit barrier"),
            ("Exit", "Unpaid ticket", "WHEN a car arrives at the exit AND its ticket is not paid THEN the system keeps the exit barrier closed"),
            ("Payment", "Paying", "WHEN a driver pays a ticket THEN the system marks the ticket as paid"),
        ],
        "variants": {
            "direct": ({"add": ("Entry", "Manual entry only", "WHEN a car arrives at the entry THEN the system keeps the entry barrier closed until an attendant opens it")},
                       {"conflicts": [[1, 6]]}),
            "overlap": ({"add": ("Safety", "Fire alarm", "WHEN the fire alarm is active THEN the system opens the exit barrier")},
                        {"conflicts": [[4, 6]]}),
        },
    },
    "thermostat": {
        "format": "ears",
        "intro": "As a resident, I want the heating to keep my home comfortable without wasting energy.",
        "rules": [
            "WHEN the room temperature is below 19 degrees AND the heating mode is on AND no window is open, THE Thermostat SHALL turn the boiler on.",
            "WHEN the room temperature is above 22 degrees, THE Thermostat SHALL turn the boiler off.",
            "WHILE a window is open, THE Thermostat SHALL turn the boiler off.",
            "WHILE the heating mode is off, THE Thermostat SHALL turn the boiler off.",
            "WHEN the boiler reports a fault, THE Thermostat SHALL display a warning.",
        ],
        "variants": {
            "direct": ({"add": "WHEN the room temperature is below 19 degrees AND the heating mode is on AND no window is open, THE Thermostat SHALL keep the boiler off to save energy."},
                       {"conflicts": [[1, 6]]}),
            "overlap": ({"add": "WHEN the room temperature is below 5 degrees, THE Thermostat SHALL turn the boiler on."},
                        {"conflicts": [[3, 6], [4, 6]]}),
        },
    },
    "upload": {
        "format": "openspec",
        "intro": "Users upload documents to a shared folder that has a size limit.",
        "rules": [
            ("Upload", "Accepted file", "WHEN a user uploads a file AND the file is at most 10 MB AND the file type is allowed AND the folder has free space THEN the system stores the file"),
            ("Upload", "File too large", "WHEN a user uploads a file AND the file is larger than 10 MB THEN the system rejects the file and shows a size error"),
            ("Upload", "Type not allowed", "WHEN a user uploads a file AND the file type is not allowed THEN the system rejects the file and shows a type error"),
            ("Quota", "Folder full", "WHEN a user uploads a file AND the folder has no free space THEN the system rejects the file"),
            ("Notification", "Owner notified", "WHEN the system stores a file THEN the system notifies the folder owner"),
        ],
        "variants": {
            "direct": ({"add": ("Notification", "Silent uploads", "WHEN the system stores a file THEN the system does not notify anyone")},
                       {"conflicts": [[5, 6]]}),
            "overlap": ({"add": ("Administrators", "Administrator upload", "WHEN an administrator uploads a file THEN the system stores the file")},
                        {"conflicts": [[2, 6], [3, 6], [4, 6]]}),
        },
    },
    "booking": {
        "format": "ears",
        "intro": "As a patient, I want to book and cancel appointments online, so that I do not have to call the practice.",
        "rules": [
            "WHEN a patient requests an appointment AND the time slot is free, THE Booking System SHALL confirm the appointment.",
            "WHEN a patient requests an appointment AND the time slot is taken, THE Booking System SHALL offer the next free time slot.",
            "WHEN a patient cancels an appointment at least 24 hours before its start, THE Booking System SHALL cancel the appointment without a fee.",
            "WHEN a patient cancels an appointment less than 24 hours before its start, THE Booking System SHALL cancel the appointment and charge a late fee.",
            "WHEN an appointment is confirmed, THE Booking System SHALL send a confirmation message to the patient.",
        ],
        "variants": {
            "direct": ({"add": "THE Booking System SHALL NOT charge any fee to patients."},
                       {"conflicts": [[4, 6]]}),
            "overlap": ({"add": "WHILE a patient has three or more missed appointments, THE Booking System SHALL NOT confirm new appointments for the patient."},
                        {"conflicts": [[1, 6]]}),
            "ambiguity": ({"replace": {4: "WHEN a patient cancels an appointment within 24 hours of its start, THE Booking System SHALL cancel the appointment and charge a late fee."}},
                          {"ambiguous": [4], "allowed": [[3, 4]]}),
        },
    },
    "vending": {
        "format": "openspec",
        "intro": "The vending machine sells snacks for coins and gives change.",
        "rules": [
            ("Purchase", "Enough credit", "WHEN a customer selects a product AND the credit covers the price AND the product is in stock THEN the machine dispenses the product"),
            ("Purchase", "Not enough credit", "WHEN a customer selects a product AND the credit does not cover the price THEN the machine shows the missing amount"),
            ("Purchase", "Out of stock", "WHEN a customer selects a product AND the product is out of stock THEN the machine shows SOLD OUT"),
            ("Money back", "Cancel", "WHEN a customer presses the cancel button THEN the machine returns the inserted credit"),
            ("Money back", "Change", "WHEN the machine dispenses a product AND the credit exceeds the price THEN the machine returns the difference"),
        ],
        "variants": {
            "direct": ({"add": ("Exact amount only", None, "The machine SHALL never return money.")},
                       {"conflicts": [[4, 6], [5, 6]]}),
            "overlap": ({"add": ("Maintenance", "Service door open", "WHEN the service door is open THEN the machine does not dispense any product")},
                        {"conflicts": [[1, 6]]}),
            "ambiguity": ({"replace": {1: ("Purchase", "Enough credit", "WHEN a customer selects a product and the credit covers the price or the customer pays by card and the product is in stock THEN the machine dispenses the product")}},
                          {"ambiguous": [1]}),
        },
    },
}


# The second set (eval2), written on 2026-11-18. Every planted ambiguity was
# chosen so that both readings make sense in the domain: a reader would have
# to ask which one is meant.
SPECS2 = {
    "transfer": {
        "format": "ears",
        "intro": "As an account holder, I want to transfer money to other accounts, so that I can pay people.",
        "rules": [
            "WHEN the account holder submits a transfer AND the balance covers the amount AND the amount is at most the daily limit, THE Banking System SHALL execute the transfer.",
            "WHEN the account holder submits a transfer AND the balance does not cover the amount, THE Banking System SHALL reject the transfer and show an insufficient-funds message.",
            "WHEN the account holder submits a transfer AND the amount is above the daily limit, THE Banking System SHALL reject the transfer and show a limit message.",
            "WHEN a transfer is executed, THE Banking System SHALL send a receipt to the account holder.",
            "WHEN the account holder submits a transfer to a payee that was never used before, THE Banking System SHALL ask for a one-time code.",
        ],
        "variants": {
            "direct": ({"add": "WHEN a transfer is executed, THE Banking System SHALL NOT send any message to the account holder."},
                       {"conflicts": [[4, 6]]}),
            "overlap": ({"add": "WHILE the account is frozen, THE Banking System SHALL NOT execute any transfer."},
                        {"conflicts": [[1, 6]]}),
            # boundary: is an amount equal to the limit "within" it?
            "ambiguity1": ({"replace": {1: "WHEN the account holder submits a transfer AND the balance covers the amount AND the amount is within the daily limit, THE Banking System SHALL execute the transfer."}},
                           {"ambiguous": [1]}),
            # scope: (new payee and above 500) or abroad, or new payee and (above 500 or abroad)?
            "ambiguity2": ({"replace": {5: "WHEN the account holder submits a transfer AND the payee was never used before and the amount is above 500 euros or the transfer goes abroad, THE Banking System SHALL ask for a one-time code."}},
                           {"ambiguous": [5]}),
        },
    },
    "newsletter": {
        "format": "openspec",
        "intro": "Readers subscribe to a newsletter by email and can leave it at any time.",
        "rules": [
            ("Signup", "Valid address", "WHEN a visitor submits the signup form AND the email address is valid THEN the system sends a confirmation email to that address"),
            ("Signup", "Invalid address", "WHEN a visitor submits the signup form AND the email address is not valid THEN the system shows an error message"),
            ("Delivery", "New issue", "WHEN a new issue is published AND the subscription is active THEN the system sends the issue to the subscriber"),
            ("Leaving", "Unsubscribe link", "WHEN a subscriber clicks the unsubscribe link THEN the system deactivates the subscription"),
            ("Address change", "New address", "WHEN a subscriber changes the email address THEN the system sends a confirmation email to the new address"),
        ],
        "variants": {
            "direct": ({"add": ("Privacy", "No email before consent", "WHEN a visitor submits the signup form THEN the system sends no email before the visitor has given consent")},
                       {"conflicts": [[1, 6]]}),
            "overlap": ({"add": ("Delivery", "Bounced addresses", "WHEN an email address has bounced three times THEN the system sends nothing to that address")},
                        {"conflicts": [[3, 6]], "allowed": [[1, 6], [5, 6]]}),
            # "only": send to every active subscriber, or merely to no one else?
            "ambiguity1": ({"replace": {3: ("Delivery", "New issue", "WHEN a new issue is published THEN the system sends the issue only to active subscribers")}},
                           {"ambiguous": [3]}),
            # "if": does the condition cover both emails, or only the notice?
            "ambiguity2": ({"replace": {5: ("Address change", "New address", "WHEN a subscriber changes the email address THEN the system sends a confirmation email to the new address and a notice to the old address if the subscription is active")}},
                           {"ambiguous": [5]}),
        },
    },
    "discounts": {
        "format": "ears",
        "intro": "As a shop owner, I want prices to be adjusted automatically at checkout, so that customers pay what was promised.",
        "rules": [
            "WHEN a customer checks out AND the cart total is at least 100 euros, THE Shop System SHALL apply a 10 percent discount.",
            "WHEN a customer checks out AND the customer is a member, THE Shop System SHALL offer free shipping.",
            "WHEN a customer checks out AND the cart total is below 20 euros, THE Shop System SHALL add a small-order fee.",
            "WHEN a customer enters a valid voucher code at checkout, THE Shop System SHALL subtract the voucher value from the total.",
            "WHEN a customer enters an expired voucher code at checkout, THE Shop System SHALL show an expired-voucher message.",
        ],
        "variants": {
            # needs three rules: a member with a large cart
            "direct": ({"add": "WHEN a customer checks out, THE Shop System SHALL NOT combine a discount with free shipping."},
                       {"conflicts": [[1, 2, 6]], "allowed": [[2, 4, 6]]}),
            "overlap": ({"add": "WHILE a product in the cart is on sale, THE Shop System SHALL NOT apply any further discount."},
                        {"conflicts": [[1, 6]], "allowed": [[4, 6]]}),
            # boundary: is a total of exactly 20 euros "between 0 and 20"?
            "ambiguity1": ({"replace": {3: "WHEN a customer checks out AND the cart total is between 0 and 20 euros, THE Shop System SHALL add a small-order fee."}},
                           {"ambiguous": [3]}),
            # scope: member or (50 euros and domestic), or (member or 50 euros) and domestic?
            "ambiguity2": ({"replace": {2: "WHEN a customer checks out AND the customer is a member or the cart total is at least 50 euros and the delivery address is in the country, THE Shop System SHALL offer free shipping."}},
                           {"ambiguous": [2]}),
        },
    },
    "exam": {
        "format": "openspec",
        "intro": "Students take online exams with a time limit; the exams are graded automatically.",
        "rules": [
            ("Submission", "In time", "WHEN a student submits the exam AND the time limit has not passed THEN the system records the submission"),
            ("Submission", "Too late", "WHEN a student submits the exam AND the time limit has passed THEN the system rejects the submission"),
            ("Grading", "Pass", "WHEN a recorded submission is graded AND the score is at least 50 points THEN the system marks the exam as passed"),
            ("Grading", "Fail", "WHEN a recorded submission is graded AND the score is below 50 points THEN the system marks the exam as failed"),
            ("Retake", "Failed exam", "WHEN an exam is marked as failed THEN the system allows the student one retake"),
        ],
        "variants": {
            "direct": ({"add": ("Submission", "Grace period", "WHEN a student submits the exam after the time limit has passed THEN the system records the submission")},
                       {"conflicts": [[2, 6]]}),
            "overlap": ({"add": ("Retake", "Misconduct", "WHEN a student has been flagged for misconduct THEN the system allows no retake")},
                        {"conflicts": [[5, 6]]}),
            # boundary: are 40 and 50 points "between 40 and 50"?
            "ambiguity1": ({"replace": {4: ("Grading", "Borderline", "WHEN a recorded submission is graded AND the score is between 40 and 50 points THEN the system offers an oral re-examination")}},
                           {"ambiguous": [4], "allowed": [[3, 4]]}),
            # "if": is the score shown always, or only with a pass?
            "ambiguity2": ({"replace": {3: ("Grading", "Pass", "WHEN a recorded submission is graded THEN the system shows the score and marks the exam as passed if the score is at least 50 points")}},
                           {"ambiguous": [3]}),
        },
    },
    "pharmacy": {
        "format": "ears",
        "intro": "As a patient, I want to refill my prescriptions online, so that I do not run out of medicine.",
        "rules": [
            "WHEN a patient requests a refill AND the prescription has refills left AND the prescription has not expired, THE Pharmacy System SHALL prepare the refill.",
            "WHEN a patient requests a refill AND the prescription has no refills left, THE Pharmacy System SHALL send a renewal request to the doctor.",
            "WHEN a patient requests a refill AND the prescription has expired, THE Pharmacy System SHALL reject the request.",
            "WHEN a refill is prepared, THE Pharmacy System SHALL notify the patient that it is ready for pickup.",
            "WHEN a refill has been ready for 10 days or more AND it has not been picked up, THE Pharmacy System SHALL put the medicine back into stock.",
        ],
        "variants": {
            "direct": ({"add": "WHEN a patient requests a refill AND the prescription has expired, THE Pharmacy System SHALL prepare the refill and inform the doctor."},
                       {"conflicts": [[3, 6]]}),
            "overlap": ({"add": "WHILE the medicine is out of stock, THE Pharmacy System SHALL NOT prepare refills of it."},
                        {"conflicts": [[1, 6]]}),
            # "if": is the patient notified always, or only for controlled substances?
            "ambiguity1": ({"replace": {4: "WHEN a refill is prepared, THE Pharmacy System SHALL notify the patient and the doctor if the medicine is a controlled substance."}},
                           {"ambiguous": [4]}),
            # boundary: after exactly 10 days, or only after more than 10?
            "ambiguity2": ({"replace": {5: "WHEN a refill has not been picked up after 10 days, THE Pharmacy System SHALL put the medicine back into stock."}},
                           {"ambiguous": [5]}),
        },
    },
    "rental": {
        "format": "openspec",
        "intro": "Customers book rental cars online and return them at a branch.",
        "rules": [
            ("Booking", "Car available", "WHEN a customer books a car AND a car of the chosen class is free AND the customer has a valid driving licence THEN the system confirms the booking"),
            ("Booking", "No car of the class", "WHEN a customer books a car AND the customer has a valid driving licence AND no car of the chosen class is free THEN the system offers a car of a higher class"),
            ("Booking", "No licence", "WHEN a customer books a car AND the customer has no valid driving licence THEN the system rejects the booking"),
            ("Return", "Late return", "WHEN a car is returned more than 2 hours after the agreed time THEN the system charges one extra day"),
            ("Return", "Damage", "WHEN a car is returned with new damage THEN the system charges the repair costs to the customer"),
        ],
        "variants": {
            "direct": ({"add": ("Return", "Damage waiver", "WHEN a car is returned with new damage THEN the system does not charge any repair costs to the customer")},
                       {"conflicts": [[5, 6]]}),
            "overlap": ({"add": ("Return", "Grace period", "WHEN a car is returned less than 3 hours after the agreed time THEN the system charges nothing extra")},
                        {"conflicts": [[4, 6]], "allowed": [[5, 6]]}),
            # "only": must every booking with a licence be confirmed, or are others merely refused?
            "ambiguity1": ({"replace": {3: ("Booking", "Licence check", "WHEN a customer books a car THEN the system confirms bookings only for customers with a valid driving licence")}},
                           {"ambiguous": [3], "allowed": [[1, 3], [2, 3]]}),
            # scope: late or (other branch and no one-way booking), or (late or other branch) and no one-way booking?
            "ambiguity2": ({"replace": {4: ("Return", "Extra day", "WHEN a car is returned more than 2 hours after the agreed time or at another branch and the customer did not book a one-way rental THEN the system charges one extra day")}},
                           {"ambiguous": [4]}),
        },
    },
}

# The third set (eval3), written on 2026-11-18 before the ambiguity questions
# were changed and before conflicts needing two events at once were marked.
SPECS3 = {
    "helpdesk": {
        "format": "ears",
        "intro": "As a customer, I want my support tickets handled quickly, so that my problems get solved.",
        "rules": [
            "WHEN a customer submits a ticket, THE Helpdesk System SHALL assign the ticket to an available agent.",
            "WHEN an agent closes a ticket, THE Helpdesk System SHALL mark the ticket as closed and notify the customer.",
            "WHEN a customer replies to a closed ticket, THE Helpdesk System SHALL reopen the ticket.",
            "WHEN a ticket has had no agent reply for 48 hours or more, THE Helpdesk System SHALL escalate the ticket to a supervisor.",
            "WHEN a ticket is escalated, THE Helpdesk System SHALL notify the supervisor.",
        ],
        "variants": {
            "overlap": ({"add": "WHILE a ticket is marked as spam, THE Helpdesk System SHALL NOT assign the ticket to any agent."},
                        {"conflicts": [[1, 6]]}),
            # boundary: does a reply exactly at 48 hours count as "within"?
            "ambiguity1": ({"replace": {4: "WHEN a ticket has had no agent reply within 48 hours, THE Helpdesk System SHALL escalate the ticket to a supervisor."}},
                           {"kind": "boundary", "ambiguous": [4]}),
            # "if": is the customer notified always, or only for escalated tickets?
            "ambiguity2": ({"replace": {2: "WHEN an agent closes a ticket, THE Helpdesk System SHALL mark the ticket as closed and notify the customer if the ticket was escalated."}},
                           {"kind": "if", "ambiguous": [2]}),
        },
    },
    "doors": {
        "format": "openspec",
        "intro": "Office doors open with an employee badge and stay locked outside working hours.",
        "rules": [
            ("Badge", "Valid badge", "WHEN a badge is presented AND the badge is valid AND it is within working hours THEN the system unlocks the door"),
            ("Badge", "Invalid badge", "WHEN a badge is presented AND the badge is not valid THEN the system keeps the door locked and logs the attempt"),
            ("After hours", "Outside working hours", "WHEN a badge is presented AND it is outside working hours AND the badge holder is not a security guard THEN the system keeps the door locked"),
            ("Doors", "Door left open", "WHEN a door has been open for more than 60 seconds THEN the system sounds an alarm"),
            ("Reception", "Remote unlock", "WHEN the receptionist presses the remote button THEN the system unlocks the front door"),
        ],
        "variants": {
            "overlap": ({"add": ("Safety", "Fire alarm", "WHEN the fire alarm is active THEN the system unlocks all doors")},
                        {"conflicts": [[2, 6], [3, 6]]}),
            # scope: (outside hours or weekend) and not a guard, or outside hours or (weekend and not a guard)?
            "ambiguity1": ({"replace": {3: ("After hours", "Outside working hours", "WHEN a badge is presented AND it is outside working hours or a weekend and the badge holder is not a security guard THEN the system keeps the door locked")}},
                           {"kind": "and/or", "ambiguous": [3], "allowed": [[1, 3]]}),
            # "only": must every valid badge open the door, or are invalid ones merely refused?
            "ambiguity2": ({"replace": {1: ("Badge", "Valid badge", "WHEN a badge is presented AND it is within working hours THEN the system unlocks the door only for a valid badge")}},
                           {"kind": "only", "ambiguous": [1]}),
        },
    },
    "streaming": {
        "format": "ears",
        "intro": "As a parent, I want each profile of our streaming account to show suitable films, so that the children see what they may see.",
        "rules": [
            "WHEN an adult profile starts a film AND the subscription is active, THE Streaming Service SHALL play the film.",
            "WHEN a profile starts a film AND the subscription has expired, THE Streaming Service SHALL show the renewal page.",
            "WHEN a child profile starts a film AND the film is rated 16 or higher, THE Streaming Service SHALL block the film.",
            "WHEN a child profile starts a film AND the film is rated below 16 AND the subscription is active, THE Streaming Service SHALL play the film.",
            "WHEN a parent enters the correct PIN, THE Streaming Service SHALL unlock the child profile for one film.",
        ],
        "variants": {
            "direct": ({"add": "WHEN a child profile starts a film, THE Streaming Service SHALL play the film."},
                       {"conflicts": [[3, 6]]}),
            # "only": must every film below 16 be played, or are others merely not played?
            "ambiguity1": ({"replace": {4: "WHEN a child profile starts a film AND the subscription is active, THE Streaming Service SHALL play the film only if it is rated below 16."}},
                           {"kind": "only", "ambiguous": [4]}),
            # "if": is the profile unlocked always, or only for films rated 18?
            "ambiguity2": ({"replace": {5: "WHEN a parent enters the correct PIN, THE Streaming Service SHALL unlock the child profile and record the event if the film is rated 18."}},
                           {"kind": "if", "ambiguous": [5]}),
        },
    },
    "claims": {
        "format": "openspec",
        "intro": "Policy holders file insurance claims online; small claims are paid automatically.",
        "rules": [
            ("Filing", "Covered damage", "WHEN a policy holder files a claim AND the damage is covered by the policy THEN the system registers the claim"),
            ("Filing", "Damage not covered", "WHEN a policy holder files a claim AND the damage is not covered by the policy THEN the system rejects the claim and explains why"),
            ("Payment", "Small claim", "WHEN a registered claim is below 1000 euros AND it matches no fraud pattern THEN the system pays the claim automatically"),
            ("Payment", "Large claim", "WHEN a registered claim is 1000 euros or more AND it matches no fraud pattern THEN the system assigns the claim to an assessor"),
            ("Fraud", "Fraud suspicion", "WHEN a claim matches a fraud pattern THEN the system assigns the claim to the fraud team"),
        ],
        "variants": {
            "overlap": ({"add": ("Payment", "Unpaid premiums", "WHEN the policy has unpaid premiums THEN the system pays no claim")},
                        {"conflicts": [[3, 6]]}),
            # "if": is every small claim paid, or only those without a fraud pattern?
            "ambiguity1": ({"replace": {3: ("Payment", "Small claim", "WHEN a registered claim is below 1000 euros THEN the system pays the claim automatically and sends a receipt if the claim matches no fraud pattern")}},
                           {"kind": "if", "ambiguous": [3]}),
            # scope: not covered or (lapsed and late), or (not covered or lapsed) and late?
            "ambiguity2": ({"replace": {2: ("Filing", "Damage not covered", "WHEN a policy holder files a claim AND the damage is not covered or the policy has lapsed and the claim is filed late THEN the system rejects the claim and explains why")}},
                           {"kind": "and/or", "ambiguous": [2], "allowed": [[1, 2]]}),
        },
    },
    "gym": {
        "format": "ears",
        "intro": "As a gym member, I want to enter the gym and book classes with my card, so that I can train when I want.",
        "rules": [
            "WHEN a member scans the card AND the membership is active, THE Gym System SHALL open the entrance gate.",
            "WHEN a member scans the card AND the membership has expired, THE Gym System SHALL keep the gate closed and show a renewal message.",
            "WHEN a member books a class AND the class has free places, THE Gym System SHALL confirm the booking.",
            "WHEN a member books a class AND the class is full, THE Gym System SHALL put the member on the waiting list.",
            "WHEN a member cancels a booking at least 2 hours before the class, THE Gym System SHALL give the place to the first member on the waiting list.",
        ],
        "variants": {
            "direct": ({"add": "WHEN a member books a class, THE Gym System SHALL NOT put anyone on a waiting list."},
                       {"conflicts": [[4, 6]]}),
            # "only": must every booking with free places be confirmed, or are others merely refused?
            "ambiguity1": ({"replace": {3: "WHEN a member books a class, THE Gym System SHALL confirm the booking only if the class has free places."}},
                           {"kind": "only", "ambiguous": [3]}),
            # boundary: are 2 and 24 hours "between 2 and 24 hours"?
            "ambiguity2": ({"replace": {5: "WHEN a member cancels a booking between 2 and 24 hours before the class, THE Gym System SHALL give the place to the first member on the waiting list."}},
                           {"kind": "boundary", "ambiguous": [5]}),
        },
    },
    "moderation": {
        "format": "openspec",
        "intro": "Users post comments; comments that look offensive are reviewed by a moderator.",
        "rules": [
            ("Posting", "Clean comment", "WHEN a user posts a comment AND the comment contains no blocked word THEN the system publishes the comment"),
            ("Posting", "Blocked word", "WHEN a user posts a comment AND the comment contains a blocked word THEN the system holds the comment for review"),
            ("Reports", "Reported comment", "WHEN a comment receives its third report THEN the system hides the comment and queues it for review"),
            ("Review", "Approved", "WHEN a moderator approves a comment THEN the system publishes the comment"),
            ("Review", "Rejected", "WHEN a moderator rejects a comment THEN the system deletes the comment and notifies the author"),
        ],
        "variants": {
            "direct": ({"add": ("Review", "Quiet rejection", "WHEN a moderator rejects a comment THEN the system notifies nobody")},
                       {"conflicts": [[5, 6]]}),
            # scope: blocked word or (link and new user), or (blocked word or link) and new user?
            "ambiguity1": ({"replace": {2: ("Posting", "Blocked word", "WHEN a user posts a comment AND the comment contains a blocked word or a link and the user is new THEN the system holds the comment for review")}},
                           {"kind": "and/or", "ambiguous": [2], "allowed": [[1, 2]]}),
            # boundary: exactly three reports, or three or more?
            "ambiguity2": ({"replace": {3: ("Reports", "Reported comment", "WHEN a comment has been reported three times THEN the system hides the comment and queues it for review")}},
                           {"kind": "boundary", "ambiguous": [3]}),
        },
    },
}

# The fourth set (eval4), written on 2026-11-18 after E8 and before steps 17
# (events written as states) and 18 (a second reader) were designed. Like
# eval3, with events in every spec, and with counted events ("for the third
# time"), the kind that E8 showed being written as states.
SPECS4 = {
    "elevator": {
        "format": "ears",
        "intro": "As a building resident, I want the elevator to answer calls and to move safely, so that I can reach my floor.",
        "rules": [
            "WHEN a passenger presses a call button AND the elevator is idle, THE Elevator Controller SHALL close the doors and move the elevator to the calling floor.",
            "WHEN the door sensor detects an obstruction, THE Elevator Controller SHALL open the doors.",
            "WHEN a passenger presses the door-open button AND the elevator is stopped at a floor, THE Elevator Controller SHALL open the doors.",
            "WHEN a passenger presses the alarm button, THE Elevator Controller SHALL connect the cabin to the service line.",
            "WHEN the doors fail to close for the third time in a row, THE Elevator Controller SHALL take the elevator out of service and notify the maintenance team.",
        ],
        "variants": {
            "direct": ({"add": "WHEN the door sensor detects an obstruction, THE Elevator Controller SHALL keep the doors closed."},
                       {"conflicts": [[2, 6]]}),
            # "if": is the cabin always connected, or only when the power has failed?
            "ambiguity1": ({"replace": {4: "WHEN a passenger presses the alarm button, THE Elevator Controller SHALL connect the cabin to the service line and switch on the emergency light if the power has failed."}},
                           {"kind": "if", "ambiguous": [4]}),
            # scope: (idle or parked) and fire mode off, or idle or (parked and fire mode off)?
            "ambiguity2": ({"replace": {1: "WHEN a passenger presses a call button AND the elevator is idle or parked and the fire service mode is off, THE Elevator Controller SHALL close the doors and move the elevator to the calling floor."}},
                           {"kind": "and/or", "ambiguous": [1]}),
        },
    },
    "lockers": {
        "format": "openspec",
        "intro": "Couriers leave parcels in lockers; recipients open their compartment with a pickup code.",
        "rules": [
            ("Delivery", "Free compartment", "WHEN a courier scans a parcel AND a compartment of the right size is free THEN the system opens that compartment and sends a pickup code to the recipient"),
            ("Delivery", "Locker full", "WHEN a courier scans a parcel AND no compartment of the right size is free THEN the system shows the courier the nearest locker with space"),
            ("Pickup", "Correct code", "WHEN a recipient enters a correct pickup code THEN the system opens the compartment of the parcel"),
            ("Pickup", "Wrong code", "WHEN a recipient enters a wrong pickup code for the third time THEN the system locks the keypad for ten minutes and alerts the recipient"),
            ("Expiry", "Not collected", "WHEN a parcel has been in its compartment for more than 72 hours THEN the system sends a last reminder to the recipient"),
        ],
        "variants": {
            "overlap": ({"add": ("Maintenance", "Maintenance mode", "WHEN the locker is in maintenance mode THEN the system opens no compartment")},
                        {"conflicts": [[1, 6], [3, 6]]}),
            # boundary: is a parcel at exactly 72 hours "after 72 hours"?
            "ambiguity1": ({"replace": {5: ("Expiry", "Not collected", "WHEN a parcel is still in its compartment after 72 hours THEN the system sends a last reminder to the recipient")}},
                           {"kind": "boundary", "ambiguous": [5]}),
            # "only": must a correct code open the compartment, or is a wrong one merely refused?
            "ambiguity2": ({"replace": {3: ("Pickup", "Correct code", "WHEN a recipient enters a pickup code THEN the system opens the compartment of the parcel only if the code is correct")}},
                           {"kind": "only", "ambiguous": [3]}),
        },
    },
    "irrigation": {
        "format": "ears",
        "intro": "As a gardener, I want the garden watered automatically, so that the plants get enough water without waste.",
        "rules": [
            "WHEN the schedule starts a watering cycle AND the soil is dry AND no rain is forecast, THE Irrigation Controller SHALL open the water valve.",
            "WHEN the schedule starts a watering cycle AND rain is forecast, THE Irrigation Controller SHALL keep the water valve closed and log the skipped cycle.",
            "WHEN the flow sensor reports a leak, THE Irrigation Controller SHALL close the water valve and alert the gardener.",
            "WHEN the gardener presses the pause button, THE Irrigation Controller SHALL suspend the schedule for 24 hours.",
            "WHEN the soil sensor fails to answer for the third time in a row, THE Irrigation Controller SHALL switch to the fixed backup schedule.",
        ],
        "variants": {
            "direct": ({"add": "WHEN the flow sensor reports a leak, THE Irrigation Controller SHALL keep the water valve open."},
                       {"conflicts": [[3, 6]]}),
            # scope: (dry or hot) and no rain, or dry or (hot and no rain)?
            "ambiguity1": ({"replace": {1: "WHEN the schedule starts a watering cycle AND the soil is dry or the temperature is above 30 degrees and no rain is forecast, THE Irrigation Controller SHALL open the water valve."}},
                           {"kind": "and/or", "ambiguous": [1], "allowed": [[1, 2]]}),
            # "if": is the valve always closed, or only when notifications are on?
            "ambiguity2": ({"replace": {3: "WHEN the flow sensor reports a leak, THE Irrigation Controller SHALL close the water valve and alert the gardener if notifications are switched on."}},
                           {"kind": "if", "ambiguous": [3]}),
        },
    },
    "attendance": {
        "format": "openspec",
        "intro": "Students check in at school with a card; parents are told about absences.",
        "rules": [
            ("Check-in", "On time", "WHEN a student scans the card AND it is before 8:00 THEN the system records the student as present"),
            ("Check-in", "Late", "WHEN a student scans the card AND it is 8:00 or later THEN the system records the student as late"),
            ("Absence", "Missing student", "WHEN the first lesson ends AND a student has not scanned the card AND no illness has been reported for the student THEN the system records the student as absent and sends a message to the parents"),
            ("Absence", "Illness", "WHEN a parent reports an illness THEN the system records the student as excused"),
            ("Late arrivals", "Third late arrival", "WHEN a student is recorded as late for the third time in a term THEN the system asks the class teacher to call the parents"),
        ],
        "variants": {
            "overlap": ({"add": ("Trips", "School trip", "WHEN the class of a student is on a school trip THEN the system records no student of that class as absent")},
                        {"conflicts": [[3, 6]]}),
            # boundary: is a scan at exactly 8:00 "after 8:00"?
            "ambiguity1": ({"replace": {2: ("Check-in", "Late", "WHEN a student scans the card after 8:00 THEN the system records the student as late")}},
                           {"kind": "boundary", "ambiguous": [2]}),
            # "if": is the student always recorded absent, or only without an illness report?
            "ambiguity2": ({"replace": {3: ("Absence", "Missing student", "WHEN the first lesson ends AND a student has not scanned the card THEN the system records the student as absent and sends a message to the parents if no illness has been reported")}},
                           {"kind": "if", "ambiguous": [3], "allowed": [[3, 4]]}),
        },
    },
    "printing": {
        "format": "ears",
        "intro": "As an office worker, I want my print jobs handled reliably, so that I get my pages quickly.",
        "rules": [
            "WHEN a user sends a print job AND the printer is ready, THE Print Server SHALL add the job to the queue.",
            "WHEN a user sends a print job AND the printer is offline, THE Print Server SHALL hold the job and notify the user.",
            "WHEN a user sends a print job of more than 100 pages, THE Print Server SHALL show the user a warning about paper use.",
            "WHEN the printer runs out of paper, THE Print Server SHALL pause the queue and alert the office manager.",
            "WHEN the printer jams for the third time in one day, THE Print Server SHALL take the printer offline and call the service technician.",
        ],
        "variants": {
            "overlap": ({"add": "WHILE the page quota of a user is used up, THE Print Server SHALL NOT add jobs of that user to the queue."},
                        {"conflicts": [[1, 6]]}),
            # boundary: exactly three jams, or three or more?
            "ambiguity1": ({"replace": {5: "WHEN the printer has jammed three times in one day, THE Print Server SHALL take the printer offline and call the service technician."}},
                           {"kind": "boundary", "ambiguous": [5]}),
            # "only": must every job be queued when the printer is ready, or are others merely not queued?
            "ambiguity2": ({"replace": {1: "WHEN a user sends a print job, THE Print Server SHALL add the job to the queue only if the printer is ready."}},
                           {"kind": "only", "ambiguous": [1]}),
        },
    },
    "delivery": {
        "format": "openspec",
        "intro": "Customers order food from restaurants; couriers deliver the orders.",
        "rules": [
            ("Ordering", "Restaurant open", "WHEN a customer places an order AND the restaurant is open AND the address is inside the delivery area THEN the system sends the order to the restaurant"),
            ("Ordering", "Cannot deliver", "WHEN a customer places an order AND the restaurant is closed or the address is outside the delivery area THEN the system rejects the order and suggests other restaurants"),
            ("Dispatch", "Order ready", "WHEN the restaurant marks an order as ready THEN the system assigns the nearest free courier to the order"),
            ("Cancelling", "Customer cancels", "WHEN a customer cancels an order before the restaurant marks it as ready THEN the system refunds the customer and informs the restaurant"),
            ("Delivery", "Second failed attempt", "WHEN a courier fails to deliver an order for the second time THEN the system returns the order to the restaurant and notifies the customer"),
        ],
        "variants": {
            "direct": ({"add": ("Dispatch", "Collection only", "WHEN the restaurant marks an order as ready THEN the system assigns no courier to the order")},
                       {"conflicts": [[3, 6]]}),
            # "only": must every such order be sent, or are others merely not sent?
            "ambiguity1": ({"replace": {1: ("Ordering", "Restaurant open", "WHEN a customer places an order THEN the system sends the order to the restaurant only if the restaurant is open and the address is inside the delivery area")}},
                           {"kind": "only", "ambiguous": [1]}),
            # scope: (closed or outside) and not for pickup, or closed or (outside and not for pickup)?
            "ambiguity2": ({"replace": {2: ("Ordering", "Cannot deliver", "WHEN a customer places an order AND the restaurant is closed or the address is outside the delivery area and the order is not for pickup THEN the system rejects the order and suggests other restaurants")}},
                           {"kind": "and/or", "ambiguous": [2]}),
        },
    },
}

# The fifth set (eval5), written on 2026-11-18 after E9 and before steps 19
# (delete_property) and 20 (failures as events) were changed. Its clean specs
# have counted failures whose outcome clashes with another event's ("the PIN
# check fails for the third time": block; "the cardholder unblocks the card":
# unblock), which eval4 lacked; two conflicts are "remove" against "keep", the
# pattern of delete_property.
SPECS5 = {
    "cards": {
        "format": "ears",
        "intro": "As a cardholder, I want my bank card to work in shops and to be protected when something goes wrong, so that my money is safe.",
        "rules": [
            "WHEN a cardholder pays with the card AND the card is not blocked AND the account has enough funds, THE Card System SHALL approve the payment.",
            "WHEN a cardholder pays with the card AND the account does not have enough funds, THE Card System SHALL decline the payment.",
            "WHEN a PIN check fails for the third time in a row, THE Card System SHALL block the card.",
            "WHEN the cardholder unblocks the card in the banking app, THE Card System SHALL unblock the card.",
            "WHEN a payment is made abroad, THE Card System SHALL send a notification to the cardholder.",
        ],
        "variants": {
            "direct": ({"add": "WHEN a cardholder pays with the card AND the account has enough funds, THE Card System SHALL decline the payment."},
                       {"conflicts": [[1, 6]]}),
            # boundary: is a payment of exactly 500 euros "within the limit"?
            "ambiguity1": ({"replace": {1: "WHEN a cardholder pays with the card AND the card is not blocked AND the account has enough funds AND the payment is within the daily limit of 500 euros, THE Card System SHALL approve the payment."}},
                           {"kind": "boundary", "ambiguous": [1]}),
            # "only": must a confirmed request unblock the card, or are others merely refused?
            "ambiguity2": ({"replace": {4: "WHEN the cardholder asks to unblock the card in the banking app, THE Card System SHALL unblock the card only if the cardholder confirms with a fingerprint."}},
                           {"kind": "only", "ambiguous": [4]}),
        },
    },
    "messages": {
        "format": "openspec",
        "intro": "Members of a team chat send messages to channels.",
        "rules": [
            ("Sending", "Message sent", "WHEN a member sends a message THEN the system delivers the message to the channel"),
            ("Editing", "Message edited", "WHEN a member edits a message THEN the system shows the new text and marks the message as edited"),
            ("Deleting", "Message deleted", "WHEN a member deletes a message THEN the system removes the message"),
            ("Delivery", "Delivery failed", "WHEN the delivery of a message fails for the third time THEN the system marks the message as failed and stops retrying"),
            ("Delivery", "Manual retry", "WHEN a member presses retry on a failed message THEN the system tries again to deliver the message"),
        ],
        "variants": {
            "direct": ({"add": ("Records", None, "The system SHALL keep every message in the archive for five years.")},
                       {"conflicts": [[3, 6]]}),
            # "if": is the new text always shown, or only for messages older than one hour?
            "ambiguity1": ({"replace": {2: ("Editing", "Message edited", "WHEN a member edits a message THEN the system shows the new text and notifies the channel if the message is older than one hour")}},
                           {"kind": "if", "ambiguous": [2]}),
            # scope: (open or admin) and not muted, or open or (admin and not muted)?
            "ambiguity2": ({"replace": {1: ("Sending", "Message sent", "WHEN a member sends a message AND the channel is open or the member is an admin and the member is not muted THEN the system delivers the message to the channel")}},
                           {"kind": "and/or", "ambiguous": [1]}),
        },
    },
    "hotel": {
        "format": "ears",
        "intro": "As a hotel guest, I want to check in at a kiosk and open my room with a key card, so that I do not have to wait at the desk.",
        "rules": [
            "WHEN a guest scans a booking code at the kiosk AND the room is ready, THE Hotel System SHALL issue a key card for the room.",
            "WHEN a guest scans a booking code at the kiosk AND the room is not ready, THE Hotel System SHALL show the time at which the room will be ready.",
            "WHEN a key card is held to a door lock AND the card is valid for the room, THE Hotel System SHALL unlock the door.",
            "WHEN a key card is rejected by a door lock for the third time in a row, THE Hotel System SHALL alert the front desk.",
            "WHEN a guest checks out, THE Hotel System SHALL deactivate the guest's key cards.",
        ],
        "variants": {
            "overlap": ({"add": "WHILE a room is blocked for maintenance, THE Hotel System SHALL NOT issue key cards for the room."},
                        {"conflicts": [[1, 6]]}),
            # boundary: exactly three rejections, or three or more; and is 60 minutes "within an hour"?
            "ambiguity1": ({"replace": {4: "WHEN a key card is rejected by a door lock three times within an hour, THE Hotel System SHALL alert the front desk."}},
                           {"kind": "boundary", "ambiguous": [4]}),
            # "if": are the cards always deactivated, or only when the guest asked for the bill?
            "ambiguity2": ({"replace": {5: "WHEN a guest checks out, THE Hotel System SHALL deactivate the guest's key cards and send the bill by email if the guest asked for it."}},
                           {"kind": "if", "ambiguous": [5]}),
        },
    },
    "backup": {
        "format": "openspec",
        "intro": "A backup service copies the files of each laptop to a server every night.",
        "rules": [
            ("Nightly backup", "Laptop online", "WHEN the nightly backup starts AND the laptop is online THEN the system copies the changed files to the server"),
            ("Nightly backup", "Laptop offline", "WHEN the nightly backup starts AND the laptop is offline THEN the system skips the laptop and records the skip"),
            ("Failures", "Third failure", "WHEN the backup of a laptop fails for the third time in a row THEN the system marks the laptop as unprotected and emails its owner"),
            ("Failures", "Successful backup", "WHEN the backup of a laptop succeeds THEN the system marks the laptop as protected"),
            ("Retention", "Old copies", "WHEN a backup copy is older than one year THEN the system deletes the copy"),
        ],
        "variants": {
            "overlap": ({"add": ("Legal hold", "Legal hold", "WHEN a laptop is under legal hold THEN the system keeps every backup copy of the laptop")},
                        {"conflicts": [[5, 6]]}),
            # boundary: exactly one year, or one year or more?
            "ambiguity1": ({"replace": {5: ("Retention", "Old copies", "WHEN a backup copy has been stored for one year THEN the system deletes the copy")}},
                           {"kind": "boundary", "ambiguous": [5]}),
            # "only": must an online laptop be copied, or are offline ones merely skipped?
            "ambiguity2": ({"replace": {1: ("Nightly backup", "Laptop online", "WHEN the nightly backup starts THEN the system copies the changed files of a laptop to the server only if the laptop is online")}},
                           {"kind": "only", "ambiguous": [1]}),
        },
    },
    "oven": {
        "format": "ears",
        "intro": "As a cook, I want the oven to heat safely and to be controlled from my phone, so that I can cook without worry.",
        "rules": [
            "WHEN the cook starts a program AND the oven door is closed, THE Oven Controller SHALL heat the oven to the program temperature.",
            "WHEN the oven door is opened during a program, THE Oven Controller SHALL pause the heating.",
            "WHEN the temperature sensor fails to respond for the third time in a row, THE Oven Controller SHALL show an error and notify the cook.",
            "WHEN the cook presses boost in the phone app, THE Oven Controller SHALL switch the heating on at full power.",
            "WHEN the program time is over, THE Oven Controller SHALL sound a signal.",
        ],
        "variants": {
            "direct": ({"add": "WHEN the oven door is opened during a program, THE Oven Controller SHALL keep heating at the program temperature."},
                       {"conflicts": [[2, 6]]}),
            # scope: (closed and lock off) or phone, or closed and (lock off or phone)?
            "ambiguity1": ({"replace": {1: "WHEN the cook starts a program AND the oven door is closed and the child lock is off or the program was started from the phone app, THE Oven Controller SHALL heat the oven to the program temperature."}},
                           {"kind": "and/or", "ambiguous": [1], "allowed": [[1, 2]]}),
            # "if": is the heating always paused, or only when the light setting is on?
            "ambiguity2": ({"replace": {2: "WHEN the oven door is opened during a program, THE Oven Controller SHALL pause the heating and switch on the oven light if the light setting is on."}},
                           {"kind": "if", "ambiguous": [2]}),
        },
    },
    "polls": {
        "format": "openspec",
        "intro": "Members vote in online polls; the results are published when a poll closes.",
        "rules": [
            ("Voting", "Valid vote", "WHEN a member casts a vote AND the poll is open AND the member has not voted yet THEN the system counts the vote"),
            ("Voting", "Second vote", "WHEN a member casts a vote AND the member has already voted THEN the system rejects the vote"),
            ("Voting", "Late vote", "WHEN a member casts a vote AND the poll is closed THEN the system rejects the vote"),
            ("Closing", "Poll closed", "WHEN the organizer closes the poll THEN the system publishes the results"),
            ("Integrity", "Check failed", "WHEN the result check fails for the second time THEN the system hides the results and alerts the organizer"),
        ],
        "variants": {
            "overlap": ({"add": ("Membership", "Suspended member", "WHEN a member is suspended THEN the system counts no vote of the member")},
                        {"conflicts": [[1, 6]]}),
            # "only": must the results be published with ten voters, or are others merely not published?
            "ambiguity1": ({"replace": {4: ("Closing", "Poll closed", "WHEN the organizer closes the poll THEN the system publishes the results only if at least ten members voted")}},
                           {"kind": "only", "ambiguous": [4]}),
            # scope: (voted or closed) and not organizer, or voted or (closed and not organizer)?
            "ambiguity2": ({"replace": {2: ("Voting", "Second vote", "WHEN a member casts a vote AND the member has already voted or the poll is closed and the member is not the organizer THEN the system rejects the vote")}},
                           {"kind": "and/or", "ambiguous": [2]}),
        },
    },
}

# The sixth set (eval6), written on 2026-11-19 after E10 and before step 21
# (states read as events) was changed. Four of its planted conflicts pair a
# rule whose WHEN part is a state ("WHEN the station is out of order") with a
# rule that reacts to an event; one is "remove" against "keep" again.
SPECS6 = {
    "charging": {
        "format": "ears",
        "intro": "As an electric car driver, I want to charge at public stations with my app, so that I can pay without a card.",
        "rules": [
            "WHEN a driver plugs in a car AND the driver's account is active, THE Charging System SHALL start charging.",
            "WHEN a driver plugs in a car AND the driver's account is suspended, THE Charging System SHALL refuse to charge and show the reason on the display.",
            "WHEN the battery reaches the charge limit set by the driver, THE Charging System SHALL stop charging.",
            "WHEN the driver presses stop in the app, THE Charging System SHALL stop charging and unlock the cable.",
            "WHEN the station loses its network connection for the second time in an hour, THE Charging System SHALL switch to offline mode.",
        ],
        "variants": {
            "overlap": ({"add": "WHEN the station is out of order, THE Charging System SHALL NOT start charging."},
                        {"conflicts": [[1, 6]]}),
            # boundary: exactly twice, or twice or more; and is 60 minutes "within an hour"?
            "ambiguity1": ({"replace": {5: "WHEN the station loses its network connection twice within an hour, THE Charging System SHALL switch to offline mode."}},
                           {"kind": "boundary", "ambiguous": [5]}),
            # "only": does it cover the unlocking, or stopping and unlocking?
            "ambiguity2": ({"replace": {4: "WHEN the driver presses stop in the app, THE Charging System SHALL stop charging and unlock the cable only if the driver is next to the car."}},
                           {"kind": "only", "ambiguous": [4]}),
        },
    },
    "bikes": {
        "format": "openspec",
        "intro": "Riders rent bikes from docking stations with a phone app.",
        "rules": [
            ("Renting", "Bike available", "WHEN a rider scans a bike AND the rider has no unpaid rides THEN the system unlocks the bike"),
            ("Renting", "Unpaid rides", "WHEN a rider scans a bike AND the rider has an unpaid ride THEN the system keeps the bike locked and asks for payment"),
            ("Returning", "Bike docked", "WHEN a rider docks a bike THEN the system ends the ride and charges the rider"),
            ("Maintenance", "Fault report", "WHEN a bike is reported as broken for the second time THEN the system blocks the bike for rentals"),
            ("Maintenance", "Repair done", "WHEN a mechanic marks a bike as repaired THEN the system makes the bike available for rentals"),
        ],
        "variants": {
            "direct": ({"add": ("Promotions", "Free returns", "WHEN a rider docks a bike THEN the system charges the rider nothing")},
                       {"conflicts": [[3, 6]]}),
            # scope: (second report or brakes fail) and not under repair, or second report or (brakes fail and not under repair)?
            "ambiguity1": ({"replace": {4: ("Maintenance", "Fault report", "WHEN a bike is reported as broken for the second time or its brakes fail a check and it is not under repair THEN the system blocks the bike for rentals")}},
                           {"kind": "and/or", "ambiguous": [4]}),
            # "if": is the ride always ended, or only when it lasted more than 30 minutes?
            "ambiguity2": ({"replace": {3: ("Returning", "Bike docked", "WHEN a rider docks a bike THEN the system ends the ride and charges the rider if the ride lasted more than 30 minutes")}},
                           {"kind": "if", "ambiguous": [3]}),
        },
    },
    "tickets": {
        "format": "ears",
        "intro": "As a concert fan, I want to buy tickets online and enter the venue with my phone, so that I do not need paper tickets.",
        "rules": [
            "WHEN a fan buys a ticket AND seats are left, THE Ticket System SHALL issue an e-ticket.",
            "WHEN a fan buys a ticket AND no seats are left, THE Ticket System SHALL put the fan on the waiting list.",
            "WHEN a fan scans an e-ticket at the entrance AND the e-ticket is valid, THE Ticket System SHALL open the gate.",
            "WHEN a fan returns a ticket, THE Ticket System SHALL refund the price and offer the seat to the waiting list.",
            "WHEN an e-ticket is scanned for the third time in a minute, THE Ticket System SHALL alert security.",
        ],
        "variants": {
            "overlap": ({"add": "WHEN the venue is at full capacity, THE Ticket System SHALL keep the entrance gates closed."},
                        {"conflicts": [[3, 6]]}),
            # boundary: is a return exactly 48 hours before "up to 48 hours before"?
            "ambiguity1": ({"replace": {4: "WHEN a fan returns a ticket up to 48 hours before the concert, THE Ticket System SHALL refund the price and offer the seat to the waiting list."}},
                           {"kind": "boundary", "ambiguous": [4]}),
            # "if": is the e-ticket always issued, or only with the premium package?
            "ambiguity2": ({"replace": {1: "WHEN a fan buys a ticket AND seats are left, THE Ticket System SHALL issue an e-ticket and add a parking pass if the fan chose the premium package."}},
                           {"kind": "if", "ambiguous": [1]}),
        },
    },
    "warehouse": {
        "format": "openspec",
        "intro": "A warehouse system stores incoming goods and ships customer orders.",
        "rules": [
            ("Receiving", "Delivery accepted", "WHEN a truck delivers goods AND the goods match the purchase order THEN the system adds the goods to the stock"),
            ("Receiving", "Delivery refused", "WHEN a truck delivers goods AND the goods do not match the purchase order THEN the system refuses the delivery"),
            ("Shipping", "Order shipped", "WHEN a customer order is ready AND the shipping address is known THEN the system ships the order"),
            ("Stock", "Low stock", "WHEN the stock of an item falls below its minimum THEN the system orders more of the item"),
            ("Stock", "Count mismatch", "WHEN the stock count of an item differs from the records for the third time THEN the system blocks the item for shipping"),
        ],
        "variants": {
            "overlap": ({"add": ("Holidays", "Warehouse closed", "WHEN the warehouse is closed for a holiday THEN the system ships no orders")},
                        {"conflicts": [[3, 6]]}),
            # "only": must every ready order with an address be shipped, or are others merely held?
            "ambiguity1": ({"replace": {3: ("Shipping", "Order shipped", "WHEN a customer order is ready THEN the system ships the order only if the shipping address is known")}},
                           {"kind": "only", "ambiguous": [3]}),
            # scope: (mismatch or damaged) and not trusted, or mismatch or (damaged and not trusted)?
            "ambiguity2": ({"replace": {2: ("Receiving", "Delivery refused", "WHEN a truck delivers goods AND the goods do not match the purchase order or are damaged and the supplier is not trusted THEN the system refuses the delivery")}},
                           {"kind": "and/or", "ambiguous": [2], "allowed": [[1, 2]]}),
        },
    },
    "auctions": {
        "format": "ears",
        "intro": "As a seller, I want to auction items online, so that buyers can bid against each other.",
        "rules": [
            "WHEN a buyer places a bid AND the bid is higher than the current price AND the auction is running, THE Auction System SHALL accept the bid.",
            "WHEN a buyer places a bid AND the bid is not higher than the current price, THE Auction System SHALL reject the bid.",
            "WHEN the auction time runs out AND there is at least one bid, THE Auction System SHALL sell the item to the highest bidder.",
            "WHEN a seller withdraws an item, THE Auction System SHALL delete the listing and notify the bidders.",
            "WHEN a payment of a buyer fails for the second time, THE Auction System SHALL block the buyer from bidding.",
        ],
        "variants": {
            "direct": ({"add": "THE Auction System SHALL keep every listing for seven years for tax audits."},
                       {"conflicts": [[4, 6]]}),
            # "if": is the listing always deleted, or only when bids were placed?
            "ambiguity1": ({"replace": {4: "WHEN a seller withdraws an item, THE Auction System SHALL delete the listing and charge the seller a fee if bids were placed."}},
                           {"kind": "if", "ambiguous": [4]}),
            # "only": must the item be sold when the reserve is reached, or merely not otherwise?
            "ambiguity2": ({"replace": {3: "WHEN the auction time runs out, THE Auction System SHALL sell the item to the highest bidder only if the reserve price was reached."}},
                           {"kind": "only", "ambiguous": [3]}),
        },
    },
    "carwash": {
        "format": "openspec",
        "intro": "Customers pay at a terminal and drive their car through an automatic car wash.",
        "rules": [
            ("Payment", "Paid", "WHEN a customer pays at the terminal AND the wash is free THEN the system opens the entry gate"),
            ("Payment", "Busy", "WHEN a customer pays at the terminal AND another car is being washed THEN the system shows the waiting time"),
            ("Washing", "Start", "WHEN a car is in position AND the entry gate is closed THEN the system starts the selected program"),
            ("Safety", "Emergency stop", "WHEN someone presses the emergency button THEN the system stops all brushes and opens the exit gate"),
            ("Safety", "Sensor fault", "WHEN the position sensor fails for the third time in a day THEN the system closes the wash and calls a technician"),
        ],
        "variants": {
            "overlap": ({"add": ("Weather", "Frost", "WHEN the outside temperature is below zero THEN the system starts no program")},
                        {"conflicts": [[3, 6]]}),
            # boundary: exactly three failures, or three or more?
            "ambiguity1": ({"replace": {5: ("Safety", "Sensor fault", "WHEN the position sensor has failed three times in a day THEN the system closes the wash and calls a technician")}},
                           {"kind": "boundary", "ambiguous": [5]}),
            # scope: (free or subscription) and not too high, or free or (subscription and not too high)?
            "ambiguity2": ({"replace": {1: ("Payment", "Paid", "WHEN a customer pays at the terminal AND the wash is free or the customer has a subscription and the car is not too high THEN the system opens the entry gate")}},
                           {"kind": "and/or", "ambiguous": [1]}),
        },
    },
}

# Folder -> the specs written into it.
# The seventh set (eval7), written on 2026-11-19 after E11 and before steps 23
# ("remove" against "keep") and 24 (fewer flags from the second reader) were
# changed. Three planted conflicts are "remove" against "keep", each worded
# differently; two clean specs remove one thing and keep another, which must
# not clash.
SPECS7 = {
    "photos": {
        "format": "openspec",
        "intro": "Users upload photos to albums and share them with friends.",
        "rules": [
            ("Upload", "Photo uploaded", "WHEN a user uploads a photo AND the photo is smaller than 20 MB THEN the system adds the photo to the album"),
            ("Upload", "Photo too large", "WHEN a user uploads a photo AND the photo is 20 MB or larger THEN the system rejects the photo"),
            ("Sharing", "Album shared", "WHEN a user shares an album with a friend THEN the system sends the friend a link"),
            ("Deleting", "Photo deleted", "WHEN a user deletes a photo THEN the system erases the photo"),
            ("Logging", "Upload log", "WHEN a user uploads a photo THEN the system writes an entry to the upload log and keeps the entry for one year"),
        ],
        "variants": {
            "direct": ({"add": ("Legal", None, "The system SHALL keep every photo for two years.")},
                       {"conflicts": [[4, 6]]}),
            # "only": must the link be sent to friends with an account, or are others merely not sent one?
            "ambiguity1": ({"replace": {3: ("Sharing", "Album shared", "WHEN a user shares an album with a friend THEN the system sends the friend a link only if the friend has an account")}},
                           {"kind": "only", "ambiguous": [3]}),
            # boundary: is a photo of exactly 20 MB "up to 20 MB"?
            "ambiguity2": ({"replace": {1: ("Upload", "Photo uploaded", "WHEN a user uploads a photo of up to 20 MB THEN the system adds the photo to the album")}},
                           {"kind": "boundary", "ambiguous": [1], "allowed": [[1, 2]]}),
        },
    },
    "taxi": {
        "format": "ears",
        "intro": "As a passenger, I want to order a taxi from my phone, so that I get a ride quickly.",
        "rules": [
            "WHEN a passenger requests a ride AND a driver is nearby, THE Taxi System SHALL assign the nearest driver.",
            "WHEN a passenger requests a ride AND no driver is nearby, THE Taxi System SHALL tell the passenger the expected waiting time.",
            "WHEN a driver accepts a ride, THE Taxi System SHALL send the driver's position to the passenger.",
            "WHEN a passenger cancels a ride after the driver has arrived, THE Taxi System SHALL charge a cancellation fee.",
            "WHEN a ride ends, THE Taxi System SHALL charge the fare and ask the passenger for a rating.",
        ],
        "variants": {
            "overlap": ({"add": "WHILE a passenger has an unpaid fare, THE Taxi System SHALL NOT assign drivers to the passenger."},
                        {"conflicts": [[1, 6]]}),
            # "if": is the fare always charged, or only for rides longer than ten minutes?
            "ambiguity1": ({"replace": {5: "WHEN a ride ends, THE Taxi System SHALL charge the fare and ask the passenger for a rating if the ride took longer than ten minutes."}},
                           {"kind": "if", "ambiguous": [5]}),
            # scope: (arrived or five minutes) and not premium, or arrived or (five minutes and not premium)?
            "ambiguity2": ({"replace": {4: "WHEN a passenger cancels a ride after the driver has arrived or after five minutes and the passenger is not a premium member, THE Taxi System SHALL charge a cancellation fee."}},
                           {"kind": "and/or", "ambiguous": [4]}),
        },
    },
    "lab": {
        "format": "openspec",
        "intro": "A laboratory system tracks blood samples from arrival to result.",
        "rules": [
            ("Arrival", "Sample registered", "WHEN a sample arrives AND its label is readable THEN the system registers the sample"),
            ("Arrival", "Unreadable label", "WHEN a sample arrives AND its label is not readable THEN the system rejects the sample and asks for a new one"),
            ("Testing", "Result ready", "WHEN a test is finished THEN the system sends the result to the doctor"),
            ("Testing", "Critical value", "WHEN a test result is below 50 or above 300 THEN the system calls the doctor immediately"),
            ("Disposal", "Sample disposal", "WHEN a sample has been tested THEN the system disposes of the sample"),
        ],
        "variants": {
            "direct": ({"add": ("Archive", None, "The system SHALL keep every tested sample in the freezer for ten years.")},
                       {"conflicts": [[5, 6]]}),
            # boundary: are 50 and 300 inside "the normal range of 50 to 300"?
            "ambiguity1": ({"replace": {4: ("Testing", "Critical value", "WHEN a test result is outside the normal range of 50 to 300 THEN the system calls the doctor immediately")}},
                           {"kind": "boundary", "ambiguous": [4]}),
            # scope: (readable or barcode) and not damaged, or readable or (barcode and not damaged)?
            "ambiguity2": ({"replace": {1: ("Arrival", "Sample registered", "WHEN a sample arrives AND its label is readable or it has a barcode and it is not damaged THEN the system registers the sample")}},
                           {"kind": "and/or", "ambiguous": [1], "allowed": [[1, 2]]}),
        },
    },
    "canteen": {
        "format": "ears",
        "intro": "As a student, I want to pay for lunch with my card at the canteen, so that I do not need cash.",
        "rules": [
            "WHEN a student taps the card at the till AND the card balance covers the meal, THE Canteen System SHALL take the price from the balance.",
            "WHEN a student taps the card at the till AND the card balance does not cover the meal, THE Canteen System SHALL refuse the payment.",
            "WHEN a parent tops up a card, THE Canteen System SHALL add the amount to the card balance.",
            "WHEN the balance of a card falls below 5 euros, THE Canteen System SHALL send a reminder to the parent.",
            "WHEN a student leaves the school, THE Canteen System SHALL close the card account and keep the payment history for one year.",
        ],
        "variants": {
            "overlap": ({"add": "WHILE the canteen is closed for holidays, THE Canteen System SHALL refuse all payments."},
                        {"conflicts": [[1, 6]]}),
            # "if": is the amount always added, or only when it is above 50 euros?
            "ambiguity1": ({"replace": {3: "WHEN a parent tops up a card, THE Canteen System SHALL add the amount to the card balance and send a receipt if the amount is above 50 euros."}},
                           {"kind": "if", "ambiguous": [3]}),
            # "only": must a covered meal be paid, or are others merely refused?
            "ambiguity2": ({"replace": {1: "WHEN a student taps the card at the till, THE Canteen System SHALL take the price from the balance only if the balance covers the meal."}},
                           {"kind": "only", "ambiguous": [1]}),
        },
    },
    "skipass": {
        "format": "openspec",
        "intro": "Skiers pass the lift gates with a ski pass card.",
        "rules": [
            ("Gates", "Valid pass", "WHEN a skier holds a pass to a gate AND the pass is valid for today THEN the system opens the gate"),
            ("Gates", "Invalid pass", "WHEN a skier holds a pass to a gate AND the pass is not valid for today THEN the system keeps the gate closed"),
            ("Gates", "Pass sharing", "WHEN a pass is used at a second gate less than five minutes after the first THEN the system blocks the pass"),
            ("Lifts", "Wind", "WHEN the wind speed at a lift exceeds 80 km/h THEN the system stops the lift"),
            ("Accounts", "Pass lost", "WHEN a skier reports a pass as lost THEN the system deletes the pass and issues a new one"),
        ],
        "variants": {
            "direct": ({"add": ("Records", None, "The system SHALL keep every pass for the whole season.")},
                       {"conflicts": [[5, 6]]}),
            # boundary: are 60 and 80 km/h "between 60 and 80"?
            "ambiguity1": ({"replace": {4: ("Lifts", "Wind", "WHEN the wind speed at a lift is between 60 and 80 km/h THEN the system slows the lift down")}},
                           {"kind": "boundary", "ambiguous": [4]}),
            # "if": is the gate always opened, or only for season passes?
            "ambiguity2": ({"replace": {1: ("Gates", "Valid pass", "WHEN a skier holds a pass to a gate AND the pass is valid for today THEN the system opens the gate and shows the skier's photo if the pass is a season pass")}},
                           {"kind": "if", "ambiguous": [1]}),
        },
    },
    "fleet": {
        "format": "ears",
        "intro": "As an employee, I want to book company cars online, so that I can travel to customers.",
        "rules": [
            "WHEN an employee books a car AND a car is free for the requested day, THE Fleet System SHALL reserve the car.",
            "WHEN an employee books a car AND no car is free for the requested day, THE Fleet System SHALL put the booking on the waiting list.",
            "WHEN an employee returns a car, THE Fleet System SHALL record the mileage and mark the car as free.",
            "WHEN the mileage of a car passes its next service limit, THE Fleet System SHALL book the car for a service.",
            "WHEN an employee reports damage to a car, THE Fleet System SHALL mark the car as unavailable.",
        ],
        "variants": {
            "overlap": ({"add": "WHILE the driving licence of an employee is not verified, THE Fleet System SHALL NOT reserve cars for the employee."},
                        {"conflicts": [[1, 6]]}),
            # scope: (free or manager) and long trip, or free or (manager and long trip)?
            "ambiguity1": ({"replace": {1: "WHEN an employee books a car AND a car is free for the requested day or the employee is a manager and the trip is longer than 100 km, THE Fleet System SHALL reserve the car."}},
                           {"kind": "and/or", "ambiguous": [1], "allowed": [[1, 2]]}),
            # "only": must a confirmed damage make the car unavailable, or merely not otherwise?
            "ambiguity2": ({"replace": {5: "WHEN an employee reports damage to a car, THE Fleet System SHALL mark the car as unavailable only if a mechanic confirms the damage."}},
                           {"kind": "only", "ambiguous": [5]}),
        },
    },
}

# The eighth set (eval8), written on 2026-11-20 after E12 and T15 and before
# step 26 (gaps in which an event happens; conflicts searched only among rules
# that share symbols) was built. New in this set: every spec has a "gap"
# version, in which one of two complementary requirements is removed, so that
# gaps get an expected answer for the first time:
#     gaps     in the gap version: a gap must be reported in which the event
#              of this requirement happens (its other case is no longer covered)
#     covered  in the clean version: both cases of this requirement's event
#              are covered, so a gap in which that event happens is a false alarm
# One conflict is "remove" against "keep" (clinic); the others are a blanket
# prohibition, an opposite outcome on the same trigger, and three exceptions
# written as states.
SPECS8 = {
    "recycling": {
        "format": "openspec",
        "intro": "Customers return empty bottles and cans to a machine and get their deposit back.",
        "rules": [
            ("Returns", "Accepted container", "WHEN a customer inserts a container AND the barcode of the container is on the deposit list THEN the system adds the deposit to the customer's total"),
            ("Returns", "Unknown container", "WHEN a customer inserts a container AND the barcode of the container is not on the deposit list THEN the system gives the container back"),
            ("Payout", "Voucher", "WHEN a customer presses the finish button THEN the system prints a voucher for the total"),
            ("Payout", "Voucher redeemed", "WHEN a cashier scans a voucher AND the voucher has not been used THEN the system pays out the amount and marks the voucher as used"),
            ("Service", "Bin almost full", "WHEN the fill level of the bin for crushed containers exceeds 90 percent THEN the system notifies the store staff"),
        ],
        "variants": {
            "overlap": ({"add": ("Service", "Out of service", "WHEN the machine is out of service THEN the system adds no deposit to any total")},
                        {"conflicts": [[1, 6]]}),
            # boundary: at exactly 90 percent only, or from 90 percent on?
            "ambiguity1": ({"replace": {5: ("Service", "Bin almost full", "WHEN the bin for crushed containers is 90 percent full THEN the system notifies the store staff")}},
                           {"kind": "boundary", "ambiguous": [5]}),
            # "only": must an unused voucher be paid out, or are used ones merely refused?
            "ambiguity2": ({"replace": {4: ("Payout", "Voucher redeemed", "WHEN a cashier scans a voucher THEN the system pays out the amount and marks the voucher as used only if the voucher has not been used")}},
                           {"kind": "only", "ambiguous": [4]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "tolls": {
        "format": "ears",
        "intro": "As a driver, I want to pay the motorway toll at the gate, so that I can continue my trip.",
        "rules": [
            "WHEN a vehicle arrives at the gate AND the vehicle has a valid toll tag, THE Toll System SHALL open the barrier and charge the tag account.",
            "WHEN a vehicle arrives at the gate AND the vehicle has no valid toll tag, THE Toll System SHALL show the price and wait for payment.",
            "WHEN a driver pays the toll at the gate, THE Toll System SHALL open the barrier and print a receipt.",
            "WHEN a card payment is declined for the third time, THE Toll System SHALL call an attendant.",
            "WHEN a vehicle leaves the gate, THE Toll System SHALL close the barrier.",
        ],
        "variants": {
            "direct": ({"add": "THE Toll System SHALL NOT print any receipt."},
                       {"conflicts": [[3, 6]]}),
            # scope: (tag or pass) and lane not reserved, or tag or (pass and lane not reserved)?
            "ambiguity1": ({"replace": {1: "WHEN a vehicle arrives at the gate AND the vehicle has a valid toll tag or a monthly pass and the lane is not reserved for trucks, THE Toll System SHALL open the barrier and charge the tag account."}},
                           {"kind": "and/or", "ambiguous": [1], "allowed": [[1, 2]]}),
            # "if": is the barrier always opened, or only for card payments?
            "ambiguity2": ({"replace": {3: "WHEN a driver pays the toll at the gate, THE Toll System SHALL open the barrier and print a receipt if the payment is made by card."}},
                           {"kind": "if", "ambiguous": [3]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "laundry": {
        "format": "openspec",
        "intro": "Residents book and pay for the washing machines in the shared laundry room.",
        "rules": [
            ("Booking", "Free slot", "WHEN a resident books a time slot AND the slot is free THEN the system reserves the slot for the resident"),
            ("Booking", "Taken slot", "WHEN a resident books a time slot AND the slot is taken THEN the system offers the next free slot"),
            ("Washing", "Start", "WHEN a resident starts a machine THEN the system charges the price of the programme to the resident's account"),
            ("Booking", "Cancelling", "WHEN a resident cancels a booking more than one hour before the slot starts THEN the system frees the slot"),
            ("Booking", "No-show", "WHEN a resident misses a booked slot for the third time in a month THEN the system notifies the caretaker"),
        ],
        "variants": {
            "direct": ({"add": ("Booking", "Fixed bookings", "WHEN a resident cancels a booking more than one hour before the slot starts THEN the system keeps the slot reserved")},
                       {"conflicts": [[4, 6]]}),
            # boundary: exactly one hour before, or one hour or more?
            "ambiguity1": ({"replace": {4: ("Booking", "Cancelling", "WHEN a resident cancels a booking one hour before the slot starts THEN the system frees the slot")}},
                           {"kind": "boundary", "ambiguous": [4]}),
            # scope: (free or caretaker) and room open, or free or (caretaker and room open)?
            "ambiguity2": ({"replace": {1: ("Booking", "Free slot", "WHEN a resident books a time slot AND the slot is free or the resident is the caretaker and the laundry room is open THEN the system reserves the slot for the resident")}},
                           {"kind": "and/or", "ambiguous": [1], "allowed": [[1, 2]]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "clinic": {
        "format": "ears",
        "intro": "As a patient, I want to book and manage my appointments online, so that I do not have to phone the clinic.",
        "rules": [
            "WHEN a patient requests an appointment AND the doctor has a free slot on the requested day, THE Clinic System SHALL book the slot and send a confirmation.",
            "WHEN a patient requests an appointment AND the doctor has no free slot on the requested day, THE Clinic System SHALL offer the next free day.",
            "WHEN a patient cancels an appointment, THE Clinic System SHALL delete the appointment and free the slot.",
            "WHEN a patient misses an appointment for the second time in a year, THE Clinic System SHALL send the patient a warning letter.",
            "WHEN a doctor reports sick, THE Clinic System SHALL cancel the doctor's appointments for that day and notify the patients.",
        ],
        "variants": {
            "direct": ({"add": "THE Clinic System SHALL keep every appointment in the patient's record for five years."},
                       {"conflicts": [[3, 6]]}),
            # "only": must a free slot be booked, or are requests without one merely not booked?
            "ambiguity1": ({"replace": {1: "WHEN a patient requests an appointment, THE Clinic System SHALL book the slot and send a confirmation only if the doctor has a free slot on the requested day."}},
                           {"kind": "only", "ambiguous": [1]}),
            # "if": are the appointments always cancelled, or only without a replacement doctor?
            "ambiguity2": ({"replace": {5: "WHEN a doctor reports sick, THE Clinic System SHALL cancel the doctor's appointments for that day and notify the patients if no replacement doctor is available."}},
                           {"kind": "if", "ambiguous": [5]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "donations": {
        "format": "openspec",
        "intro": "Supporters give money to a charity online, once or every month.",
        "rules": [
            ("Giving", "Card accepted", "WHEN a supporter makes a donation AND the card payment succeeds THEN the system records the donation and sends a thank-you email"),
            ("Giving", "Card declined", "WHEN a supporter makes a donation AND the card payment fails THEN the system shows an error and records nothing"),
            ("Monthly giving", "Monthly charge", "WHEN the first day of a month begins AND a supporter has a monthly donation THEN the system charges the supporter's card"),
            ("Monthly giving", "Stop", "WHEN a supporter stops a monthly donation THEN the system ends the monthly donation and confirms by email"),
            ("Receipts", "Tax receipt", "WHEN a year ends THEN the system sends a tax receipt by post to every supporter who gave more than 100 euros in that year"),
        ],
        "variants": {
            "overlap": ({"add": ("Privacy", "Anonymous supporter", "WHEN a supporter has asked to stay anonymous THEN the system sends the supporter no email")},
                        {"conflicts": [[1, 6], [4, 6]]}),
            # scope: (monthly donation or pledge) and card not expired, or monthly donation or (pledge and card not expired)?
            "ambiguity1": ({"replace": {3: ("Monthly giving", "Monthly charge", "WHEN the first day of a month begins AND a supporter has a monthly donation or a pledge and the supporter's card has not expired THEN the system charges the supporter's card")}},
                           {"kind": "and/or", "ambiguous": [3]}),
            # "only": must a successful payment be recorded, or are failed ones merely not recorded?
            "ambiguity2": ({"replace": {1: ("Giving", "Card accepted", "WHEN a supporter makes a donation THEN the system records the donation and sends a thank-you email only if the card payment succeeds")}},
                           {"kind": "only", "ambiguous": [1]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "meters": {
        "format": "ears",
        "intro": "As a household customer, I want my electricity use read and billed automatically, so that I do not have to send readings.",
        "rules": [
            "WHEN a meter sends a reading AND the reading is not lower than the previous one, THE Metering System SHALL store the reading.",
            "WHEN a meter sends a reading AND the reading is lower than the previous one, THE Metering System SHALL reject the reading and flag the meter for inspection.",
            "WHEN a billing period ends, THE Metering System SHALL create a bill from the stored readings.",
            "WHEN a bill has been unpaid for more than 30 days, THE Metering System SHALL send a reminder to the customer.",
            "WHEN a meter fails to send a reading for the third time in a row, THE Metering System SHALL send a technician.",
        ],
        "variants": {
            "overlap": ({"add": "WHILE a customer is on a payment plan, THE Metering System SHALL NOT send reminders to the customer."},
                        {"conflicts": [[4, 6]]}),
            # boundary: on day 30 only, or from day 30 on?
            "ambiguity1": ({"replace": {4: "WHEN a bill has been unpaid for 30 days, THE Metering System SHALL send a reminder to the customer."}},
                           {"kind": "boundary", "ambiguous": [4]}),
            # "if": is the reading always rejected, or only when the difference is large?
            "ambiguity2": ({"replace": {2: "WHEN a meter sends a reading AND the reading is lower than the previous one, THE Metering System SHALL reject the reading and flag the meter for inspection if the difference is more than 10 kWh."}},
                           {"kind": "if", "ambiguous": [2]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
}

# A set of its own (size), written on 2026-11-20 together with eval8: one spec
# of 30 requirements. All specs so far have 4 to 6. It shows what a larger
# document does to the read step, to the solver stage and to the findings; it
# is not part of the eval8 numbers.
SPECS_SIZE = {
    "campsite": {
        "format": "ears",
        "intro": "As a camper, I want to book a pitch and use the services of the campsite with my booking card, so that my stay runs smoothly.",
        "rules": [
            "WHEN a camper requests a pitch AND a pitch of the requested size is free for all requested nights, THE Campsite System SHALL reserve the pitch.",
            "WHEN a camper requests a pitch AND no pitch of the requested size is free for all requested nights, THE Campsite System SHALL offer the nearest free dates.",
            "WHEN a camper pays the deposit for a reserved pitch, THE Campsite System SHALL confirm the booking by email.",
            "WHEN the deposit for a reserved pitch has been missing for more than 48 hours, THE Campsite System SHALL send the camper a reminder.",
            "WHEN a camper cancels a booking more than 14 days before arrival, THE Campsite System SHALL refund the deposit.",
            "WHEN a camper cancels a booking 14 days or less before arrival, THE Campsite System SHALL keep the deposit.",
            "WHEN a camper arrives AND the booking is confirmed, THE Campsite System SHALL issue a booking card and show the way to the pitch.",
            "WHEN a camper arrives AND the booking is not confirmed, THE Campsite System SHALL send the camper to the reception desk.",
            "WHEN a camper holds a booking card to the barrier AND the card is valid, THE Campsite System SHALL open the barrier.",
            "WHEN a camper holds a booking card to the barrier AND the card is not valid, THE Campsite System SHALL keep the barrier closed and show a message.",
            "WHEN a vehicle has passed the barrier, THE Campsite System SHALL close the barrier.",
            "WHEN a camper plugs a cable into the power post of the pitch AND the booking includes electricity, THE Campsite System SHALL switch on the power post.",
            "WHEN a camper plugs a cable into the power post of the pitch AND the booking does not include electricity, THE Campsite System SHALL keep the power post off and offer the electricity option.",
            "WHEN the power use of a pitch exceeds 10 amperes, THE Campsite System SHALL notify the camper and the site manager.",
            "WHEN a camper buys shower tokens, THE Campsite System SHALL add the tokens to the booking card.",
            "WHEN a camper holds a booking card to a shower AND the card has at least one token, THE Campsite System SHALL start the shower for five minutes and take one token.",
            "WHEN a camper holds a booking card to a shower AND the card has no token, THE Campsite System SHALL show the price of a token.",
            "WHEN a camper registers a dog, THE Campsite System SHALL add the dog fee to the bill.",
            "WHEN a camper orders bread for the next morning before 18:00, THE Campsite System SHALL add the order to the bakery list.",
            "WHEN a camper orders bread for the next morning at 18:00 or later, THE Campsite System SHALL refuse the order.",
            "WHEN a camper reports a fault on the pitch, THE Campsite System SHALL create a task for the maintenance team.",
            "WHEN a maintenance task has been open for more than 24 hours, THE Campsite System SHALL alert the site manager.",
            "WHEN a camper asks to extend the stay AND the pitch is free for the extra nights, THE Campsite System SHALL extend the booking.",
            "WHEN a camper asks to extend the stay AND the pitch is not free for the extra nights, THE Campsite System SHALL offer another pitch.",
            "WHEN the departure day of a booking begins, THE Campsite System SHALL send the bill to the camper.",
            "WHEN a camper pays the bill, THE Campsite System SHALL send a receipt and mark the booking as paid.",
            "WHEN a camper leaves the campsite AND the bill is paid, THE Campsite System SHALL cancel the booking card.",
            "WHEN a camper leaves the campsite AND the bill is not paid, THE Campsite System SHALL charge the open amount to the stored payment card.",
            "WHEN a booking card is reported lost, THE Campsite System SHALL cancel the card and issue a new one.",
            "WHEN a camper writes a review after the stay, THE Campsite System SHALL publish the review on the campsite page.",
        ],
        "variants": {
            "direct": ({"add": "THE Campsite System SHALL NOT publish any review."},
                       {"conflicts": [[30, 31]]}),
            "overlap": ({"add": "WHILE a storm warning is active, THE Campsite System SHALL keep all power posts switched off."},
                        {"conflicts": [[12, 31]]}),
            "gap": ({"remove": 8}, {"gaps": [7]}),
        },
        "covered": [1, 5, 7, 9, 12, 16, 19, 23, 27],
    },
}

# A second set for size (size2), written on 2026-11-22 before the run that
# tests the larger answer limit of the read step (READ_MAX_TOKENS 8192 ->
# 24576): one spec of 100 requirements, a ferry line. The read answer for 30
# requirements was about 4,000 to 5,000 tokens, so 100 requirements do not fit
# in 8192. The versions are those of `size`: clean, a direct conflict, an
# overlap conflict, a gap. The 20 events in "covered" have both of their cases
# written, so a gap for one of them on the clean spec is a false gap.
SPECS_SIZE2 = {
    "ferry": {
        "format": "ears",
        "intro": "As a passenger of the ferry line, I want to book crossings, bring my vehicle and my pet, and use the services on board, so that my journey runs smoothly.",
        "rules": [
            # booking (1-13)
            "WHEN a passenger requests a crossing AND seats are available on the chosen sailing, THE Ferry System SHALL reserve a seat for the passenger.",
            "WHEN a passenger requests a crossing AND seats are not available on the chosen sailing, THE Ferry System SHALL offer the next sailing with available seats.",
            "WHEN a passenger pays for a reserved seat, THE Ferry System SHALL send an e-ticket by email.",
            "WHEN a reserved seat has been unpaid for more than 30 minutes, THE Ferry System SHALL release the seat.",
            "WHEN a passenger cancels a ticket more than 24 hours before departure, THE Ferry System SHALL refund the full fare.",
            "WHEN a passenger cancels a ticket 24 hours or less before departure, THE Ferry System SHALL refund half of the fare.",
            "WHEN a passenger moves a ticket to another sailing AND seats are available on the new sailing, THE Ferry System SHALL change the ticket to the new sailing.",
            "WHEN a passenger moves a ticket to another sailing AND seats are not available on the new sailing, THE Ferry System SHALL leave the ticket on its sailing and show a message.",
            "WHEN a passenger asks for a printed ticket at the port office, THE Ferry System SHALL print the ticket.",
            "WHEN a passenger books a crossing for a child under 4 years, THE Ferry System SHALL issue a free child ticket.",
            "WHEN a group booking of more than 10 passengers is paid, THE Ferry System SHALL apply a group discount of 10 percent.",
            "WHEN a passenger enters a discount code AND the code is valid, THE Ferry System SHALL reduce the fare by the amount of the code.",
            "WHEN a passenger enters a discount code AND the code is not valid, THE Ferry System SHALL show an error message.",
            # vehicles (14-25)
            "WHEN a passenger adds a vehicle to a booking AND space is available on the car deck, THE Ferry System SHALL reserve a vehicle space.",
            "WHEN a passenger adds a vehicle to a booking AND space is not available on the car deck, THE Ferry System SHALL put the vehicle on the waiting list.",
            "WHEN a passenger adds a vehicle that is taller than 2 metres, THE Ferry System SHALL charge the high-vehicle fare.",
            "WHEN a vehicle arrives at the check-in lane AND its number plate matches a booking, THE Ferry System SHALL assign the vehicle to a boarding lane.",
            "WHEN a vehicle arrives at the check-in lane AND its number plate does not match a booking, THE Ferry System SHALL send the driver to the port office.",
            "WHEN a vehicle is assigned to a boarding lane, THE Ferry System SHALL print a lane card for the driver.",
            "WHEN a driver declares dangerous goods at check-in, THE Ferry System SHALL notify the officer of the watch.",
            "WHEN a booked vehicle has not checked in 30 minutes before departure, THE Ferry System SHALL release its vehicle space.",
            "WHEN a vehicle space is released AND a vehicle is on the waiting list, THE Ferry System SHALL offer the space to the first vehicle on the waiting list.",
            "WHEN a vehicle space is released AND no vehicle is on the waiting list, THE Ferry System SHALL return the space to open sale.",
            "WHEN loading of the car deck begins, THE Ferry System SHALL call the boarding lanes in the order of check-in.",
            "WHEN a vehicle is unloaded at the arrival port, THE Ferry System SHALL mark the vehicle booking as completed.",
            # foot passengers (26-33)
            "WHEN a passenger scans an e-ticket at the gate AND the ticket is valid for the next sailing, THE Ferry System SHALL open the gate.",
            "WHEN a passenger scans an e-ticket at the gate AND the ticket is not valid for the next sailing, THE Ferry System SHALL keep the gate closed and show the sailing the ticket is valid for.",
            "WHEN boarding of foot passengers begins, THE Ferry System SHALL announce the boarding in the terminal.",
            "WHEN boarding closes, THE Ferry System SHALL send the number of boarded passengers to the captain.",
            "WHEN boarding closes AND a ticket holder has not boarded, THE Ferry System SHALL mark the ticket as a no-show.",
            "WHEN a passenger requests boarding assistance while booking, THE Ferry System SHALL book a wheelchair escort for the sailing.",
            "WHEN a passenger with booked assistance arrives at the terminal, THE Ferry System SHALL notify the assistance team.",
            "WHEN a passenger with priority boarding arrives at the terminal, THE Ferry System SHALL direct the passenger to the priority lane.",
            # cabins (34-42)
            "WHEN a passenger books a cabin AND a cabin of the requested class is available, THE Ferry System SHALL reserve the cabin.",
            "WHEN a passenger books a cabin AND a cabin of the requested class is not available, THE Ferry System SHALL offer a cabin of another class.",
            "WHEN a passenger with a cabin booking boards the ship, THE Ferry System SHALL send the cabin number and the door code by text message.",
            "WHEN a passenger enters a door code at a cabin AND the code is correct, THE Ferry System SHALL unlock the cabin door.",
            "WHEN a passenger enters a door code at a cabin AND the code is not correct, THE Ferry System SHALL keep the cabin door locked.",
            "WHEN a passenger reports a fault in a cabin, THE Ferry System SHALL create a task for the housekeeping team.",
            "WHEN a housekeeping task has been open for more than 2 hours, THE Ferry System SHALL alert the purser.",
            "WHEN the ship is 30 minutes from the arrival port, THE Ferry System SHALL remind the cabin passengers to leave their cabins.",
            "WHEN a passenger orders a wake-up call, THE Ferry System SHALL ring the cabin phone at the requested time.",
            # restaurant and shop (43-56)
            "WHEN a passenger orders a meal in the restaurant AND the meal is in stock, THE Ferry System SHALL send the order to the kitchen.",
            "WHEN a passenger orders a meal in the restaurant AND the meal is not in stock, THE Ferry System SHALL show the dishes that are in stock.",
            "WHEN the kitchen marks an order as ready, THE Ferry System SHALL show the order number on the restaurant screen.",
            "WHEN a passenger reserves a restaurant table AND a table is free at the requested time, THE Ferry System SHALL confirm the reservation.",
            "WHEN a passenger reserves a restaurant table AND no table is free at the requested time, THE Ferry System SHALL offer the nearest time with a free table.",
            "WHEN a passenger charges a shop purchase to the cabin, THE Ferry System SHALL add the amount to the cabin bill.",
            "WHEN a passenger pays in the shop by bank card AND the payment is approved, THE Ferry System SHALL print a receipt.",
            "WHEN a passenger pays in the shop by bank card AND the payment is not approved, THE Ferry System SHALL cancel the sale and show a message.",
            "WHEN a passenger buys alcohol in the shop, THE Ferry System SHALL ask the cashier to check the passenger's age.",
            "WHEN the ship enters the waters of the arrival country, THE Ferry System SHALL switch the shop prices to the tax rate of the arrival country.",
            "WHEN the stock of a product in the shop falls below 5 units, THE Ferry System SHALL add the product to the restocking list.",
            "WHEN the shop closes, THE Ferry System SHALL send the day's sales to the head office.",
            "WHEN a passenger orders room service AND the passenger has a cabin, THE Ferry System SHALL deliver the order to the cabin.",
            "WHEN a passenger orders room service AND the passenger does not have a cabin, THE Ferry System SHALL refuse the order and suggest the restaurant.",
            # Wi-Fi and entertainment (57-65)
            "WHEN a passenger connects to the onboard Wi-Fi, THE Ferry System SHALL show the login page.",
            "WHEN a passenger buys a Wi-Fi pass, THE Ferry System SHALL send the pass code by text message.",
            "WHEN a passenger logs in to the Wi-Fi AND the passenger has a valid Wi-Fi pass, THE Ferry System SHALL give internet access until the end of the crossing.",
            "WHEN a passenger logs in to the Wi-Fi AND the passenger does not have a valid Wi-Fi pass, THE Ferry System SHALL offer a free 15-minute session.",
            "WHEN a passenger books a cinema seat AND seats are left for the film, THE Ferry System SHALL reserve the cinema seat.",
            "WHEN a passenger books a cinema seat AND no seats are left for the film, THE Ferry System SHALL show the next showing of the film.",
            "WHEN a film is 10 minutes from its start, THE Ferry System SHALL announce the film on the cabin screens.",
            "WHEN a parent registers a child for the kids' club, THE Ferry System SHALL give the parent a pager.",
            "WHEN the kids' club calls a parent, THE Ferry System SHALL make the parent's pager vibrate.",
            # pets (66-71)
            "WHEN a passenger adds a pet to a booking AND a kennel is available, THE Ferry System SHALL reserve a kennel.",
            "WHEN a passenger adds a pet to a booking AND a kennel is not available, THE Ferry System SHALL offer a pet-friendly cabin.",
            "WHEN a passenger adds a pet to a booking, THE Ferry System SHALL add the pet fee to the fare.",
            "WHEN a passenger with a pet checks in AND the pet's vaccination record is valid, THE Ferry System SHALL issue a pet tag.",
            "WHEN a passenger with a pet checks in AND the pet's vaccination record is not valid, THE Ferry System SHALL refuse the pet and notify the port office.",
            "WHEN the ship has docked at the arrival port, THE Ferry System SHALL tell the passengers with kennels that they can collect their pets.",
            # weather and delays (72-78)
            "WHEN the weather service issues a storm warning for a route, THE Ferry System SHALL notify the operations manager.",
            "WHEN the operator cancels a sailing, THE Ferry System SHALL notify all booked passengers by text message.",
            "WHEN the operator cancels a sailing, THE Ferry System SHALL offer every booked passenger a free rebooking or a full refund.",
            "WHEN a sailing is delayed by more than 60 minutes, THE Ferry System SHALL give each passenger a meal voucher.",
            "WHEN a sailing is delayed by more than 120 minutes, THE Ferry System SHALL give each passenger a travel voucher worth 25 percent of the fare.",
            "WHEN a delay of a sailing is announced, THE Ferry System SHALL update the departure board.",
            "WHEN a passenger asks for a delay certificate, THE Ferry System SHALL email a certificate that states the delay.",
            # accounts and loyalty (79-88)
            "WHEN a customer creates an account, THE Ferry System SHALL send a welcome email.",
            "WHEN a customer with an account completes a crossing, THE Ferry System SHALL add loyalty points for the fare paid.",
            "WHEN a customer completes the tenth crossing of a calendar year, THE Ferry System SHALL upgrade the customer to silver status.",
            "WHEN a silver customer books a crossing, THE Ferry System SHALL give the customer priority boarding.",
            "WHEN a customer pays with loyalty points AND the points cover the fare, THE Ferry System SHALL take the points and issue the ticket.",
            "WHEN a customer pays with loyalty points AND the points do not cover the fare, THE Ferry System SHALL ask the customer to pay the difference by card.",
            "WHEN a customer changes the email address of the account, THE Ferry System SHALL send a confirmation link to the new address.",
            "WHEN a customer enters a wrong password for the third time in a row, THE Ferry System SHALL lock the account for 15 minutes.",
            "WHEN a customer subscribes to the newsletter, THE Ferry System SHALL send a confirmation email.",
            "WHEN a customer unsubscribes from the newsletter, THE Ferry System SHALL confirm the unsubscription by email.",
            # lost property, safety, crew (89-96)
            "WHEN a crew member registers a found item, THE Ferry System SHALL record the description of the item and the sailing.",
            "WHEN a passenger reports a lost item AND a matching found item is registered, THE Ferry System SHALL tell the passenger where to collect it.",
            "WHEN a passenger reports a lost item AND no matching found item is registered, THE Ferry System SHALL record the report and send a reply within 3 days.",
            "WHEN a found item has been unclaimed for more than 90 days, THE Ferry System SHALL hand the item over to a charity.",
            "WHEN a crew member presses the man-overboard button, THE Ferry System SHALL sound the alarm on the bridge and record the ship's position.",
            "WHEN a fire detector raises an alarm, THE Ferry System SHALL show the location of the detector on the bridge panel.",
            "WHEN a crew member starts a shift, THE Ferry System SHALL record the start time.",
            "WHEN a crew member has worked more than 12 hours in one shift, THE Ferry System SHALL alert the chief officer.",
            # after the crossing (97-100)
            "WHEN the ship has docked at the arrival port, THE Ferry System SHALL announce that passengers may leave the ship.",
            "WHEN a passenger leaves the ship, THE Ferry System SHALL mark the ticket as used.",
            "WHEN a passenger asks for an invoice, THE Ferry System SHALL email an invoice with the company's tax number.",
            "WHEN a passenger writes a review after the crossing, THE Ferry System SHALL publish the review on the route page.",
        ],
        "variants": {
            "direct": ({"add": "THE Ferry System SHALL NOT print tickets."},
                       {"conflicts": [[9, 101]]}),
            "overlap": ({"add": "WHILE a security alert is active in the terminal, THE Ferry System SHALL keep all gates closed."},
                        {"conflicts": [[26, 101]]}),
            "gap": ({"remove": 18}, {"gaps": [17]}),
        },
        "covered": [1, 5, 7, 12, 14, 17, 22, 26, 34, 37, 43, 46, 49, 55, 59, 61, 66, 69, 83, 90],
    },
}

# Written on 2026-11-23, after T19 and before the parentheses repair of the
# facts vote. Same design as eval8: six new domains, three with a direct and
# three with an overlap conflict, each kind of ambiguity in three specs, and a
# gap version that removes the second of two complementary requirements.
SPECS9 = {
    "crossing": {
        "format": "ears",
        "intro": "As a road user, I want the level crossing to close while a train passes, so that I can cross the railway safely.",
        "rules": [
            "WHEN a train approaches the crossing AND the barriers are working, THE Crossing System SHALL lower the barriers and switch on the warning lights.",
            "WHEN a train approaches the crossing AND the barriers are not working, THE Crossing System SHALL tell the train driver to stop before the crossing.",
            "WHEN a train has passed the crossing, THE Crossing System SHALL raise the barriers and switch off the warning lights.",
            "WHEN a barrier fails to lower for the third time in a week, THE Crossing System SHALL report the crossing to maintenance.",
            "WHEN a vehicle has stood on the crossing for more than 20 seconds, THE Crossing System SHALL warn the signal box.",
        ],
        "variants": {
            "direct": ({"add": "WHEN a train has passed the crossing, THE Crossing System SHALL keep the barriers down."},
                       {"conflicts": [[3, 6]]}),
            # boundary: after exactly 20 seconds only, or from 20 seconds on?
            "ambiguity1": ({"replace": {5: "WHEN a vehicle has stood on the crossing for 20 seconds, THE Crossing System SHALL warn the signal box."}},
                           {"kind": "boundary", "ambiguous": [5]}),
            # "if": are the barriers always raised, or only when no other train comes?
            "ambiguity2": ({"replace": {3: "WHEN a train has passed the crossing, THE Crossing System SHALL raise the barriers and switch off the warning lights if no other train is approaching."}},
                           {"kind": "if", "ambiguous": [3]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "grants": {
        "format": "openspec",
        "intro": "Researchers apply online for small research grants.",
        "rules": [
            ("Applications", "Complete application", "WHEN a researcher submits an application AND all required documents are attached THEN the system sends the application to two reviewers"),
            ("Applications", "Incomplete application", "WHEN a researcher submits an application AND a required document is missing THEN the system returns the application to the researcher"),
            ("Decisions", "Funding", "WHEN the committee approves an application THEN the system transfers the first payment to the researcher's institution"),
            ("Reviews", "Late reviewer", "WHEN a reviewer misses the review deadline for the second time THEN the system removes the reviewer from the panel"),
            ("Reporting", "Final report", "WHEN a project ends THEN the system asks the researcher for a final report"),
        ],
        "variants": {
            "overlap": ({"add": ("Decisions", "Budget used up", "WHEN the grant budget of the year is used up THEN the system makes no payments")},
                        {"conflicts": [[3, 6]]}),
            # "only": must a complete application be sent, or are incomplete ones merely not sent?
            "ambiguity1": ({"replace": {1: ("Applications", "Complete application", "WHEN a researcher submits an application THEN the system sends the application to two reviewers only if all required documents are attached")}},
                           {"kind": "only", "ambiguous": [1]}),
            # scope: (researcher or institution) and budget allows, or researcher or (institution and budget allows)?
            "ambiguity2": ({"replace": {3: ("Decisions", "Funding", "WHEN the committee approves an application AND the researcher has signed the contract or the institution has signed it and the budget allows it THEN the system transfers the first payment to the researcher's institution")}},
                           {"kind": "and/or", "ambiguous": [3]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "shelter": {
        "format": "openspec",
        "intro": "People adopt cats and dogs from an animal shelter through its website.",
        "rules": [
            ("Adoption", "Home check passed", "WHEN a person applies to adopt an animal AND the person has passed the home check THEN the system reserves the animal for the person"),
            ("Adoption", "Home check not passed", "WHEN a person applies to adopt an animal AND the person has not passed the home check THEN the system rejects the application and tells the person why"),
            ("Adoption", "Handover", "WHEN the adoption fee is paid THEN the system marks the animal as adopted and removes it from the website"),
            ("Website", "Long stay", "WHEN an animal has been in the shelter for more than 90 days THEN the system features the animal on the home page"),
            ("Volunteers", "Missed shifts", "WHEN a volunteer misses a shift for the third time THEN the system informs the volunteer coordinator"),
        ],
        "variants": {
            "direct": ({"add": ("Records", None, "The system SHALL keep every adopted animal on the website.")},
                       {"conflicts": [[3, 6]]}),
            # boundary: on day 90 only, or from day 90 on?
            "ambiguity1": ({"replace": {4: ("Website", "Long stay", "WHEN an animal has been in the shelter for 90 days THEN the system features the animal on the home page")}},
                           {"kind": "boundary", "ambiguous": [4]}),
            # "if": is the animal always marked as adopted, or only when it is microchipped?
            "ambiguity2": ({"replace": {3: ("Adoption", "Handover", "WHEN the adoption fee is paid THEN the system marks the animal as adopted and removes it from the website if the animal is microchipped")}},
                           {"kind": "if", "ambiguous": [3]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "pool": {
        "format": "ears",
        "intro": "As a swimmer, I want to enter the public pool with my card, so that I do not have to queue at the till.",
        "rules": [
            "WHEN a swimmer holds a card at the entry gate AND the card has entries left, THE Pool System SHALL open the gate and deduct one entry.",
            "WHEN a swimmer holds a card at the entry gate AND the card has no entries left, THE Pool System SHALL keep the gate closed and show where to buy more entries.",
            "WHEN the water temperature drops below 24 degrees, THE Pool System SHALL alert the pool manager.",
            "WHEN a swimmer leaves through the exit gate, THE Pool System SHALL record the time of exit.",
            "WHEN a card is reported lost for the second time, THE Pool System SHALL block the card and charge a replacement fee.",
        ],
        "variants": {
            "overlap": ({"add": "WHILE the pool is closed for cleaning, THE Pool System SHALL keep the entry gate closed."},
                        {"conflicts": [[1, 6]]}),
            # scope: (entries left or season pass) and pool open, or entries left or (season pass and pool open)?
            "ambiguity1": ({"replace": {1: "WHEN a swimmer holds a card at the entry gate AND the card has entries left or the swimmer has a season pass and the pool is open, THE Pool System SHALL open the gate and deduct one entry."}},
                           {"kind": "and/or", "ambiguous": [1], "allowed": [[1, 2]]}),
            # "only": must a card with entries open the gate, or are cards without entries merely refused?
            "ambiguity2": ({"replace": {1: "WHEN a swimmer holds a card at the entry gate, THE Pool System SHALL open the gate and deduct one entry only if the card has entries left."}},
                           {"kind": "only", "ambiguous": [1]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "topup": {
        "format": "openspec",
        "intro": "Customers of a prepaid mobile network add credit to their phones.",
        "rules": [
            ("Top-up", "Payment accepted", "WHEN a customer buys credit AND the payment is accepted THEN the system adds the credit to the balance and sends a text message"),
            ("Top-up", "Payment refused", "WHEN a customer buys credit AND the payment is refused THEN the system leaves the balance unchanged and shows the reason"),
            ("Calls", "Low balance", "WHEN the balance falls below 2 euros THEN the system sends the customer a warning"),
            ("Calls", "Empty balance", "WHEN the balance reaches zero during a call THEN the system ends the call"),
            ("Security", "Wrong PIN", "WHEN a customer enters a wrong PIN for the third time THEN the system locks the account for 24 hours"),
        ],
        "variants": {
            "direct": ({"add": ("Calls", "Calls never cut", "WHEN the balance reaches zero during a call THEN the system lets the call continue")},
                       {"conflicts": [[4, 6]]}),
            # boundary: at exactly 2 euros only, or at 2 euros and below?
            "ambiguity1": ({"replace": {3: ("Calls", "Low balance", "WHEN the balance falls to 2 euros THEN the system sends the customer a warning")}},
                           {"kind": "boundary", "ambiguous": [3]}),
            # "only": must an accepted payment be added, or are refused ones merely not added?
            "ambiguity2": ({"replace": {1: ("Top-up", "Payment accepted", "WHEN a customer buys credit THEN the system adds the credit to the balance and sends a text message only if the payment is accepted")}},
                           {"kind": "only", "ambiguous": [1]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "kindergarten": {
        "format": "ears",
        "intro": "As a parent, I want the kindergarten to check who picks up my child, so that my child goes home only with people I trust.",
        "rules": [
            "WHEN an adult comes to pick up a child AND the adult is on the child's pick-up list, THE Kindergarten System SHALL let the child go and record the time.",
            "WHEN an adult comes to pick up a child AND the adult is not on the child's pick-up list, THE Kindergarten System SHALL keep the child inside and call the parents.",
            "WHEN a child is absent without notice, THE Kindergarten System SHALL send a text message to the parents.",
            "WHEN a parent arrives after closing time for the third time in a month, THE Kindergarten System SHALL charge a late fee.",
            "WHEN a child has a fever, THE Kindergarten System SHALL call the parents and move the child to the quiet room.",
        ],
        "variants": {
            "overlap": ({"add": "WHILE the parents have turned off notifications, THE Kindergarten System SHALL NOT send text messages to the parents."},
                        {"conflicts": [[3, 6]]}),
            # scope: (on the list or teacher) and parents agreed, or on the list or (teacher and parents agreed)?
            "ambiguity1": ({"replace": {1: "WHEN an adult comes to pick up a child AND the adult is on the child's pick-up list or the adult is a teacher and the parents have agreed by phone, THE Kindergarten System SHALL let the child go and record the time."}},
                           {"kind": "and/or", "ambiguous": [1], "allowed": [[1, 2]]}),
            # "if": are the parents always called, or only for a high fever?
            "ambiguity2": ({"replace": {5: "WHEN a child has a fever, THE Kindergarten System SHALL call the parents and move the child to the quiet room if the fever is above 39 degrees."}},
                           {"kind": "if", "ambiguous": [5]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
}

# Folder -> the specs written into it.
SETS = {"eval": SPECS, "eval2": SPECS2, "eval3": SPECS3, "eval4": SPECS4, "eval5": SPECS5,
        "eval6": SPECS6, "eval7": SPECS7, "eval8": SPECS8, "eval9": SPECS9,
        "size": SPECS_SIZE, "size2": SPECS_SIZE2}


def document(name: str, spec: dict, rules: list) -> str:
    """Write the requirements out in the spec's own format."""
    title = name.capitalize()
    if spec["format"] == "ears":  # Kiro style: a user story and labelled criteria
        label = name[0].upper()
        lines = [f"# Requirements: {title}", "", "## Requirement 1", "",
                 f"**User Story:** {spec['intro']}", "", "### Acceptance Criteria", ""]
        lines += [f"- {label}{number}: {text}" for number, text in enumerate(rules, start=1)]
        return "\n".join(lines) + "\n"
    # OpenSpec style: requirements with unlabelled scenarios
    lines = [f"# {title} Specification", "", "## Purpose", "", spec["intro"], "", "## Requirements"]
    previous = None
    for requirement, scenario, text in rules:
        if requirement != previous:
            lines += ["", f"### Requirement: {requirement}"]
            previous = requirement
        if scenario is None:  # a requirement stated as one sentence, without a scenario
            lines += ["", text]
            continue
        when, then = text.split(" THEN ")
        lines += ["", f"#### Scenario: {scenario}", ""]
        first, *others = when.removeprefix("WHEN ").split(" AND ")
        lines += [f"- **WHEN** {first}"] + [f"- **AND** {part}" for part in others]
        lines += [f"- **THEN** {then}"]
    return "\n".join(lines) + "\n"


def main() -> None:
    # Only the sets named on the command line (all if none), so that writing a
    # new set never rewrites an old one.
    for folder_name in sys.argv[1:] or SETS:
        specs = SETS[folder_name]
        root = Path("experiments/sets") / folder_name
        for name, spec in specs.items():
            # The clean version says which events have all their cases covered (eval8 on).
            clean = {"covered": spec["covered"]} if "covered" in spec else {}
            versions = {"clean": ({}, clean)} | spec["variants"]
            for version, (change, expected) in versions.items():
                rules = list(spec["rules"])
                for number, text in change.get("replace", {}).items():
                    rules[number - 1] = text
                if "add" in change:
                    rules.append(change["add"])
                if "remove" in change:
                    del rules[change["remove"] - 1]
                folder = root / f"{name}_{version}"
                folder.mkdir(parents=True, exist_ok=True)
                (folder / "spec.md").write_text(document(name, spec, rules), encoding="utf-8")
                expected = {"conflicts": [], "ambiguous": [], "allowed": [], **expected}
                (folder / "expected.json").write_text(json.dumps(expected) + "\n", encoding="utf-8")
        print(f"wrote {sum(1 + len(s['variants']) for s in specs.values())} specs to {root}/")


if __name__ == "__main__":
    main()
