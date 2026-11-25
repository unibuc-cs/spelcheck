"""make_eval.py: writes the evaluation sets eval/ to eval15/, size/, size2/ and mixed/. No LLM, no GPU.

    python -m experiments.make_eval eval15     (only the sets named; all if none)

change_dev/ is development data for the change check: the OpenSpec-format
specs of eval9/ and eval10/ as projects with a change (see as_projects).

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
             the facts vote. Same design as eval8/. Held-out in E15;
             development data since.
    eval10/  written 2026-11-23, after E15, before the doubtful mark on gaps.
             Same design as eval8/, except that 3 of the 6 specs name the
             condition of their two complementary requirements with two words
             ("passes" / "fails") instead of one and its negation.
    eval12/  written 2026-11-24, after E17, before the questions about pairs of
             outcomes. Same design as eval8/, but every spec has a direct AND
             an overlap version, and all 12 planted conflicts say the opposite
             outcome in other words ("switch the heater on" / "cut the power
             to the heater"), two of them as a retention period ("delete the
             payslips" / "keep every payslip for ten years"). That is the kind
             of conflict the earlier sets missed.

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

eval11/ is of another kind (written 2026-11-24, after E16, before the check of
an OpenSpec change against the existing specs was built): six OpenSpec
projects. A project has the specs that exist (openspec/specs/<capability>/
spec.md, two or three files, six scenarios in all) and ONE change
(openspec/changes/<name>/, with a proposal.md and one delta file for each
capability it touches). Each project comes in five versions, which differ only
in the change:

    clean      the change adds a requirement that covers both of its cases
               (in three projects it also removes an unrelated requirement).
               Nothing may be reported about the change.
    direct     the change adds a requirement that plainly contradicts an
               existing scenario (three projects), or
    overlap    one whose condition can hold together with an existing
               scenario, with an incompatible outcome (the other three).
    modified   the change rewrites an existing requirement (a state: "WHEN a
               storm warning is in force"), so that it now clashes with a
               scenario in another spec file.
    gap        the change adds a requirement that covers one of two cases.
    narrowed   the change rewrites a requirement and drops one of its two
               complementary scenarios.

The planted conflicts negate the outcome of an existing scenario in its own
words ("opens the gate" / "does not open the gate"). The set is meant to test
the change check (the merge, and which findings belong to the change), not the
choice of symbols, whose limits the earlier sets measure.

Written per version: experiments/sets/eval11/<project>_<version>/openspec/...
and expected.json. A scenario is named there by "capability/requirement/
scenario", as it is after the change:

    conflicts  pairs of scenarios that must be reported as a conflict
    gaps       scenarios: a gap must be reported in which their event happens
    covered    (clean) the added scenarios, whose event has both cases
               covered: a gap in which it happens is a false alarm

eval13/ is of the same kind (written 2026-11-24, after E18, before a gap that
a removal opens was tied to the change): six more OpenSpec projects, with nine
existing scenarios each. Among them is one conflict that the specs have before
any change ("unlock the room door" / "do not unlock any room door"); no change
touches the two scenarios it is between. Six versions:

    clean      the change adds a requirement that covers both of its cases.
    modified   it rewrites a requirement so that it clashes with a scenario
               in another spec file (as in eval11).
    removed    it REMOVES the requirement that held one of two complementary
               cases; the other case is in a requirement of its own. A gap
               for their event must be reported as the change's.
    narrowed   it rewrites a requirement and drops one of its two
               complementary scenarios (as in eval11): the same gap.
    retired    it REMOVES the only requirement for an event. Nothing may be
               reported about the change: nobody reacts to that event now,
               by decision.
    sibling    it rewrites a requirement: one scenario gets a harmless
               addition, the other is word for word the same, and that one is
               part of the old conflict. Nothing may be reported about the
               change.

expected.json has, besides the keys above:

    old        the conflict that the specs had before the change. It must not
               be shown as the change's.
    nothing    true: no conflict and no gap may be reported about the change

eval14/ is of the same kind again (written 2026-11-24, after E19, before a
change could be checked without formalizing all the specs again): six more
OpenSpec projects with seven existing scenarios each, to be run in both ways,
the full one and the new one. Six versions:

    clean      the change adds a requirement that covers both of its cases.
    direct     it adds a requirement for the trigger of an existing scenario,
               with the opposite outcome said in other words ("switches the
               floodlights on" / "keeps the floodlights dark").
    overlap    it adds a requirement for a state, which forbids, in the same
               words, what a scenario in the other spec file demands.
    modified   it rewrites a requirement so that it clashes with a scenario
               in the other spec file (as in eval11 and eval13).
    gap        it adds a requirement that covers one of two cases.
    removed    it REMOVES the requirement that held one of two complementary
               cases (as in eval13).

The new way must give a new rule the symbols of the old ones, or no clash
with them can be seen; direct, overlap and modified test that.

eval15/ is of the same kind (written 2026-11-25, after E20, before the read
step of the new way is told when a listed event is the trigger of a rule):
six more OpenSpec projects with seven existing scenarios each, to be run the
full way and the new way (held-out in E21; development data since). In E20 the new way lost a conflict when it read a
rule about a state ("a person is younger than 17") next to the saved symbols:
it tied the rule to a saved event that the rule does not name ("a person
registers"). The changes of eval15 are aimed at that. Six versions. clean,
direct, modified and gap are as in eval14; removed is left out, because a
change that only removes gives the model nothing to read. The two new ones:

    property   the change adds a requirement for a state that is a quantity
               of the person or thing an existing event is about ("the bar
               tab of a player is above 60 euros", next to "a player asks for
               shoes"). It forbids, in the same words, what a scenario for
               that event demands.
    status     the same with a yes/no property ("a game is a practice game",
               next to "a player starts a game").

mixed/ (written 2026-11-25, after E21; no design change goes with it) is one
larger OpenSpec project, a city marathon: four spec files, 28 requirements,
39 scenarios, and ONE change that does everything the sets above do one at a
time (PROJECTS_MIXED says which part plants what):

    it adds       a requirement with both of its cases (nothing to report), one
                  for the trigger of an existing scenario with the opposite
                  outcome in other words (conflict), one for a state that
                  forbids what a scenario in another spec file demands
                  (conflict), and one with one of two cases (gap)
    it rewrites   a requirement so that it clashes with an existing scenario
                  (conflict), one with a harmless addition to one of its two
                  scenarios (nothing), and one that loses a scenario (gap)
    it removes    the requirement that held one of two cases (gap), and the
                  only requirement for an event (nothing)
    it renames    a requirement (nothing)

The specs also have one conflict from before the change ("old"), and a fourth
spec file that the change does not touch. Expected about the change: 3
conflicts and 3 gaps.
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

# Written on 2026-11-23, after E15 and before the doubtful mark on gaps. The
# design of eval8, except that 3 of the 6 specs (baggage, inspection,
# passports) name the condition of requirements 1 and 2 with two words
# ("within the weight limit" / "overweight"), the case that gave all false gaps
# so far; the other 3 use one condition and its negation.
SPECS10 = {
    "baggage": {
        "format": "ears",
        "intro": "As a passenger, I want to drop my bag at a machine, so that I do not have to queue at the check-in desk.",
        "rules": [
            "WHEN a passenger drops a bag at the machine AND the bag is within the weight limit, THE Baggage System SHALL accept the bag and print a bag tag.",
            "WHEN a passenger drops a bag at the machine AND the bag is overweight, THE Baggage System SHALL return the bag and show the fee for the extra weight.",
            "WHEN a passenger scans a boarding pass AND the flight closes in less than 40 minutes, THE Baggage System SHALL send the passenger to the service desk.",
            "WHEN the belt behind the machine jams for the third time in an hour, THE Baggage System SHALL call a technician.",
            "WHEN a passenger presses the help button, THE Baggage System SHALL call an agent to the machine.",
        ],
        "variants": {
            "overlap": ({"add": "WHILE the sorting hall is out of order, THE Baggage System SHALL NOT accept any bag."},
                        {"conflicts": [[1, 6]]}),
            # boundary: in exactly 40 minutes only, or in 40 minutes or less?
            "ambiguity1": ({"replace": {3: "WHEN a passenger scans a boarding pass AND the flight closes in 40 minutes, THE Baggage System SHALL send the passenger to the service desk."}},
                           {"kind": "boundary", "ambiguous": [3]}),
            # "if": is the bag always accepted, or only after online check-in?
            "ambiguity2": ({"replace": {1: "WHEN a passenger drops a bag at the machine AND the bag is within the weight limit, THE Baggage System SHALL accept the bag and print a bag tag if the passenger has checked in online."}},
                           {"kind": "if", "ambiguous": [1]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "allotments": {
        "format": "openspec",
        "intro": "Residents rent garden plots from the town's allotment association.",
        "rules": [
            ("Renting", "Plot available", "WHEN a resident applies for a plot AND a plot is available THEN the system assigns the plot to the resident and sends the contract"),
            ("Renting", "No plot available", "WHEN a resident applies for a plot AND no plot is available THEN the system puts the resident on the waiting list"),
            ("Fees", "Yearly fee", "WHEN the gardening year begins THEN the system sends every tenant an invoice for the yearly fee"),
            ("Upkeep", "Neglected plot", "WHEN an inspector reports a neglected plot for the third time THEN the system ends the tenant's contract"),
            ("Upkeep", "Broken tap", "WHEN a tenant reports a broken water tap THEN the system informs the caretaker"),
        ],
        "variants": {
            "direct": ({"add": ("Contracts", None, "The system SHALL never end a tenant's contract.")},
                       {"conflicts": [[4, 6]]}),
            # "only": must a plot be assigned when one is available, or are applicants merely refused without one?
            "ambiguity1": ({"replace": {1: ("Renting", "Plot available", "WHEN a resident applies for a plot THEN the system assigns the plot to the resident and sends the contract only if a plot is available")}},
                           {"kind": "only", "ambiguous": [1]}),
            # scope: (plot or shed) and not on the board, or plot or (shed and not on the board)?
            "ambiguity2": ({"replace": {3: ("Fees", "Yearly fee", "WHEN the gardening year begins AND a tenant has a plot or a shed and is not a member of the board THEN the system sends the tenant an invoice for the yearly fee")}},
                           {"kind": "and/or", "ambiguous": [3]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "inspection": {
        "format": "ears",
        "intro": "As a car owner, I want the yearly safety test of my car recorded online, so that I can prove that the car is roadworthy.",
        "rules": [
            "WHEN an inspector finishes a test AND the car passes the test, THE Inspection System SHALL issue a certificate and set the date of the next test.",
            "WHEN an inspector finishes a test AND the car fails the test, THE Inspection System SHALL list the defects and book a retest.",
            "WHEN a certificate expires, THE Inspection System SHALL send the owner a reminder.",
            "WHEN a car fails the test for the third time in a row, THE Inspection System SHALL report the car to the road authority.",
            "WHEN an owner pays the test fee, THE Inspection System SHALL send a receipt by email.",
        ],
        "variants": {
            "direct": ({"add": "WHEN an inspector finishes a test, THE Inspection System SHALL NOT issue a certificate."},
                       {"conflicts": [[1, 6]]}),
            # scope: (passes or minor defects) and brakes work, or passes or (minor defects and brakes work)?
            "ambiguity1": ({"replace": {1: "WHEN an inspector finishes a test AND the car passes the test or the defects are minor and the brakes work, THE Inspection System SHALL issue a certificate and set the date of the next test."}},
                           {"kind": "and/or", "ambiguous": [1], "allowed": [[1, 2]]}),
            # "if": is the retest always booked, or only when the owner asks?
            "ambiguity2": ({"replace": {2: "WHEN an inspector finishes a test AND the car fails the test, THE Inspection System SHALL list the defects and book a retest if the owner asks for one."}},
                           {"kind": "if", "ambiguous": [2]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "visitors": {
        "format": "openspec",
        "intro": "Visitors check in at the entrance of a hospital ward.",
        "rules": [
            ("Check-in", "Listed visitor", "WHEN a visitor checks in at a ward AND the visitor is on the patient's visitor list THEN the system opens the ward door and prints a visitor badge"),
            ("Check-in", "Unlisted visitor", "WHEN a visitor checks in at a ward AND the visitor is not on the patient's visitor list THEN the system keeps the ward door closed and calls a nurse"),
            ("Hours", "End of visiting time", "WHEN visiting time ends THEN the system reminds all visitors to leave"),
            ("Safety", "Badge not returned", "WHEN a visitor leaves without returning the badge for the second time THEN the system informs the ward manager"),
            ("Hours", "Long visit", "WHEN a visitor has stayed for more than 2 hours THEN the system asks the visitor to make room for others"),
        ],
        "variants": {
            "overlap": ({"add": ("Safety", "Isolation", "WHEN the patient is in isolation THEN the system keeps the ward door closed for visitors")},
                        {"conflicts": [[1, 6]]}),
            # boundary: after exactly 2 hours only, or from 2 hours on?
            "ambiguity1": ({"replace": {5: ("Hours", "Long visit", "WHEN a visitor has stayed for 2 hours THEN the system asks the visitor to make room for others")}},
                           {"kind": "boundary", "ambiguous": [5]}),
            # "only": must a listed visitor be let in, or are unlisted ones merely kept out?
            "ambiguity2": ({"replace": {1: ("Check-in", "Listed visitor", "WHEN a visitor checks in at a ward THEN the system opens the ward door and prints a visitor badge only if the visitor is on the patient's visitor list")}},
                           {"kind": "only", "ambiguous": [1]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "fuel": {
        "format": "ears",
        "intro": "As a driver, I want to pay at the fuel pump with my card, so that I do not have to go into the shop.",
        "rules": [
            "WHEN a driver inserts a card at the pump AND the card is authorised, THE Pump System SHALL unlock the nozzle and show the price per litre.",
            "WHEN a driver inserts a card at the pump AND the card is not authorised, THE Pump System SHALL keep the nozzle locked and return the card.",
            "WHEN a driver hangs up the nozzle, THE Pump System SHALL charge the card for the fuel taken and print a receipt.",
            "WHEN a card is refused for the third time in a row at the same pump, THE Pump System SHALL alert the shop staff.",
            "WHEN the fuel tank of the station holds less than 500 litres, THE Pump System SHALL order a delivery.",
        ],
        "variants": {
            "direct": ({"add": "WHEN a driver hangs up the nozzle, THE Pump System SHALL release the payment hold without charging the card."},
                       {"conflicts": [[3, 6]]}),
            # boundary: at exactly 500 litres only, or at 500 litres and below?
            "ambiguity1": ({"replace": {5: "WHEN the fuel tank of the station is down to 500 litres, THE Pump System SHALL order a delivery."}},
                           {"kind": "boundary", "ambiguous": [5]}),
            # "if": is the card always charged, or only when the driver asks for a receipt?
            "ambiguity2": ({"replace": {3: "WHEN a driver hangs up the nozzle, THE Pump System SHALL charge the card for the fuel taken and print a receipt if the driver asks for one."}},
                           {"kind": "if", "ambiguous": [3]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "passports": {
        "format": "openspec",
        "intro": "Citizens renew their passports online.",
        "rules": [
            ("Renewal", "Valid old passport", "WHEN a citizen applies for a new passport AND the old passport is still valid THEN the system accepts the application online"),
            ("Renewal", "Expired old passport", "WHEN a citizen applies for a new passport AND the old passport has expired THEN the system books an appointment at the passport office"),
            ("Payment", "Fee", "WHEN a citizen pays the passport fee THEN the system starts the production of the passport"),
            ("Delivery", "Ready", "WHEN a new passport is ready THEN the system sends the citizen a text message"),
            ("Security", "Lost passports", "WHEN a citizen reports a passport lost for the second time in five years THEN the system asks the citizen to come to the office in person"),
        ],
        "variants": {
            "overlap": ({"add": ("Security", "Travel ban", "WHEN a court has banned the citizen from travelling THEN the system blocks the production of any passport for the citizen")},
                        {"conflicts": [[3, 6]]}),
            # "only": must production start when the photo meets the rules, or is it merely held back otherwise?
            "ambiguity1": ({"replace": {3: ("Payment", "Fee", "WHEN a citizen pays the passport fee THEN the system starts the production of the passport only if the photo meets the rules")}},
                           {"kind": "only", "ambiguous": [3]}),
            # scope: (still valid or identity card) and abroad, or still valid or (identity card and abroad)?
            "ambiguity2": ({"replace": {1: ("Renewal", "Valid old passport", "WHEN a citizen applies for a new passport AND the old passport is still valid or the citizen has an identity card and lives abroad THEN the system accepts the application online")}},
                           {"kind": "and/or", "ambiguous": [1], "allowed": [[1, 2]]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
}

SPECS12 = {
    "beds": {
        "format": "ears",
        "intro": "As a ward nurse, I want beds assigned to arriving patients, so that nobody waits in the corridor.",
        "rules": [
            "WHEN a patient arrives on the ward AND a bed is free, THE Bed System SHALL assign a bed to the patient and inform the nurse.",
            "WHEN a patient arrives on the ward AND no bed is free, THE Bed System SHALL put the patient on the waiting list of the ward.",
            "WHEN a patient is discharged, THE Bed System SHALL release the patient's bed and mark it for cleaning.",
            "WHEN a bed is reported broken for the second time in a month, THE Bed System SHALL order a replacement.",
            "WHEN a bed has been marked for cleaning for more than 2 hours, THE Bed System SHALL alert the cleaning team.",
        ],
        "variants": {
            "direct": ({"add": "WHEN a patient is discharged, THE Bed System SHALL hold the patient's bed for 24 hours."},
                       {"conflicts": [[3, 6]]}),
            "overlap": ({"add": "WHILE the ward is under quarantine, THE Bed System SHALL give no bed to anyone."},
                        {"conflicts": [[1, 6]]}),
            # boundary: after exactly 2 hours only, or from 2 hours on?
            "ambiguity1": ({"replace": {5: "WHEN a bed has been marked for cleaning for 2 hours, THE Bed System SHALL alert the cleaning team."}},
                           {"kind": "boundary", "ambiguous": [5]}),
            # "only": must a bed be assigned when one is free, or are patients merely not placed without one?
            "ambiguity2": ({"replace": {1: "WHEN a patient arrives on the ward, THE Bed System SHALL assign a bed to the patient and inform the nurse only if a bed is free."}},
                           {"kind": "only", "ambiguous": [1]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "timesheets": {
        "format": "openspec",
        "intro": "Employees record their working hours, and their managers approve them.",
        "rules": [
            ("Submission", "Complete week", "WHEN an employee submits a timesheet AND every working day has an entry THEN the system sends the timesheet to the manager"),
            ("Submission", "Missing days", "WHEN an employee submits a timesheet AND a working day has no entry THEN the system returns the timesheet to the employee"),
            ("Approval", "Approved", "WHEN a manager approves a timesheet THEN the system locks the timesheet and passes the hours to payroll"),
            ("Reminders", "Third late timesheet", "WHEN an employee is late with the timesheet for the third time in a year THEN the system informs the department head"),
            ("Overtime", "Long week", "WHEN a timesheet has more than 48 hours in a week THEN the system asks the manager for a comment"),
        ],
        "variants": {
            "direct": ({"add": ("Corrections", "After approval", "WHEN a manager approves a timesheet THEN the system leaves the timesheet open for corrections by the employee")},
                       {"conflicts": [[3, 6]]}),
            "overlap": ({"add": ("Audits", "Under audit", "WHEN the department is under audit THEN the system withholds all timesheets from the managers")},
                        {"conflicts": [[1, 6]]}),
            # scope: (more than 48 hours or Sunday work) and under 18, or more than 48 hours or (Sunday work and under 18)?
            "ambiguity1": ({"replace": {5: ("Overtime", "Long week", "WHEN a timesheet has more than 48 hours in a week or work on a Sunday and the employee is under 18 THEN the system asks the manager for a comment")}},
                           {"kind": "and/or", "ambiguous": [5]}),
            # "if": is the timesheet always locked, or only for employees paid by the hour?
            "ambiguity2": ({"replace": {3: ("Approval", "Approved", "WHEN a manager approves a timesheet THEN the system locks the timesheet and passes the hours to payroll if the employee is paid by the hour")}},
                           {"kind": "if", "ambiguous": [3]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "aquarium": {
        "format": "ears",
        "intro": "As the keeper of a public aquarium, I want the tank controller to look after water and feeding, so that the fish stay healthy.",
        "rules": [
            "WHEN the feeding time comes AND the feeder is not empty, THE Tank Controller SHALL release a portion of food into the tank.",
            "WHEN the feeding time comes AND the feeder is empty, THE Tank Controller SHALL alert the keeper.",
            "WHEN the water temperature falls below 24 degrees, THE Tank Controller SHALL switch the heater on.",
            "WHEN the filter clogs for the third time in a week, THE Tank Controller SHALL ask for a new filter cartridge.",
            "WHEN the water level is more than 5 centimetres below the mark, THE Tank Controller SHALL open the refill valve.",
        ],
        "variants": {
            "direct": ({"add": "WHEN the water temperature falls below 24 degrees, THE Tank Controller SHALL cut the power to the heater."},
                       {"conflicts": [[3, 6]]}),
            "overlap": ({"add": "WHILE the tank is being treated with medicine, THE Tank Controller SHALL keep all food out of the tank."},
                        {"conflicts": [[1, 6]]}),
            # boundary: at exactly 5 centimetres only, or at 5 centimetres and more?
            "ambiguity1": ({"replace": {5: "WHEN the water level is 5 centimetres below the mark, THE Tank Controller SHALL open the refill valve."}},
                           {"kind": "boundary", "ambiguous": [5]}),
            # "only": must food be released when the feeder is not empty, or is it merely held back otherwise?
            "ambiguity2": ({"replace": {1: "WHEN the feeding time comes, THE Tank Controller SHALL release a portion of food into the tank only if the feeder is not empty."}},
                           {"kind": "only", "ambiguous": [1]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "cloakroom": {
        "format": "openspec",
        "intro": "Guests of a theatre leave their coats at the cloakroom and get them back with a token.",
        "rules": [
            ("Hand-in", "Hook free", "WHEN a guest hands in a coat AND a hook is free THEN the system assigns a hook and prints a token"),
            ("Hand-in", "Cloakroom full", "WHEN a guest hands in a coat AND no hook is free THEN the system sends the guest to the second cloakroom"),
            ("Return", "Token shown", "WHEN a guest shows a token THEN the system releases the coat to the guest and deletes the token record"),
            ("Lost tokens", "Second lost token", "WHEN a guest reports a lost token for the second time in a season THEN the system asks the guest for an identity card"),
            ("Left behind", "Unclaimed coat", "WHEN a coat has been on its hook for more than 30 days THEN the system adds the coat to the list of unclaimed coats"),
        ],
        "variants": {
            "direct": ({"add": ("Records", None, "The system SHALL keep every token record for two years.")},
                       {"conflicts": [[3, 6]]}),
            "overlap": ({"add": ("Performances", "Performance running", "WHEN a performance is running THEN the system holds back all coats")},
                        {"conflicts": [[3, 6]]}),
            # boundary: after exactly 30 days only, or from 30 days on?
            "ambiguity1": ({"replace": {5: ("Left behind", "Unclaimed coat", "WHEN a coat has been on its hook for 30 days THEN the system adds the coat to the list of unclaimed coats")}},
                           {"kind": "boundary", "ambiguous": [5]}),
            # "if": is the coat always released, or only when the fee is paid?
            "ambiguity2": ({"replace": {3: ("Return", "Token shown", "WHEN a guest shows a token THEN the system releases the coat to the guest and deletes the token record if the cloakroom fee is paid")}},
                           {"kind": "if", "ambiguous": [3]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "turbine": {
        "format": "ears",
        "intro": "As the operator of a wind farm, I want each turbine to protect itself, so that faults and bad weather do no damage.",
        "rules": [
            "WHEN an operator sends the start command AND the turbine has no open fault, THE Turbine Controller SHALL release the brake and start the rotor.",
            "WHEN an operator sends the start command AND the turbine has an open fault, THE Turbine Controller SHALL refuse the command and show the fault.",
            "WHEN the wind direction changes by more than 10 degrees, THE Turbine Controller SHALL turn the nacelle into the wind.",
            "WHEN the vibration sensor trips for the third time in a day, THE Turbine Controller SHALL call the maintenance crew.",
            "WHEN the gearbox oil is hotter than 90 degrees, THE Turbine Controller SHALL lower the power output.",
        ],
        "variants": {
            "direct": ({"add": "WHEN the wind direction changes by more than 10 degrees, THE Turbine Controller SHALL leave the nacelle where it is."},
                       {"conflicts": [[3, 6]]}),
            "overlap": ({"add": "WHILE ice is detected on the blades, THE Turbine Controller SHALL hold the rotor still."},
                        {"conflicts": [[1, 6]]}),
            # scope: (oil or generator hot) and full power, or oil hot or (generator hot and full power)?
            "ambiguity1": ({"replace": {5: "WHEN the gearbox oil is hotter than 90 degrees or the generator is hotter than 120 degrees and the turbine runs at full power, THE Turbine Controller SHALL lower the power output."}},
                           {"kind": "and/or", "ambiguous": [5]}),
            # "only": must the rotor start when there is no open fault, or is it merely kept still otherwise?
            "ambiguity2": ({"replace": {1: "WHEN an operator sends the start command, THE Turbine Controller SHALL release the brake and start the rotor only if the turbine has no open fault."}},
                           {"kind": "only", "ambiguous": [1]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
    "payroll": {
        "format": "openspec",
        "intro": "A company pays its employees every month and gives them their payslips online.",
        "rules": [
            ("Monthly pay", "Bank details known", "WHEN the pay run starts AND the bank details of an employee are known THEN the system transfers the salary and publishes the payslip"),
            ("Monthly pay", "Bank details missing", "WHEN the pay run starts AND the bank details of an employee are not known THEN the system informs the payroll clerk"),
            ("Leavers", "Employee leaves", "WHEN an employee leaves the company THEN the system closes the employee's account and deletes the employee's payslips"),
            ("Corrections", "Third correction", "WHEN the salary of an employee is corrected for the third time in a year THEN the system informs the head of finance"),
            ("Bonuses", "Large bonus", "WHEN a bonus is higher than 5000 euros THEN the system asks a director for approval"),
        ],
        "variants": {
            "direct": ({"add": ("Records", None, "The system SHALL keep every payslip for ten years.")},
                       {"conflicts": [[3, 6]]}),
            "overlap": ({"add": ("Monthly pay", "Unpaid leave", "WHEN an employee is on unpaid leave THEN the system pays the employee nothing")},
                        {"conflicts": [[1, 6]]}),
            # scope: (higher than 5000 or in shares) and a manager, or higher than 5000 or (in shares and a manager)?
            "ambiguity1": ({"replace": {5: ("Bonuses", "Large bonus", "WHEN a bonus is higher than 5000 euros or paid in shares and the employee is a manager THEN the system asks a director for approval")}},
                           {"kind": "and/or", "ambiguous": [5]}),
            # "if": is the salary always transferred, or only for employees with electronic payslips?
            "ambiguity2": ({"replace": {1: ("Monthly pay", "Bank details known", "WHEN the pay run starts AND the bank details of an employee are known THEN the system transfers the salary and publishes the payslip if the employee has asked for electronic payslips")}},
                           {"kind": "if", "ambiguous": [1]}),
            "gap": ({"remove": 2}, {"gaps": [1]}),
        },
        "covered": [1],
    },
}

# eval11: OpenSpec projects, each with one change (see the module docstring).
#   specs     capability -> (purpose, requirements): what exists before the change
#   changes   version -> the change: its folder name, the "why" of its
#             proposal, its delta (capability -> ADDED / MODIFIED / REMOVED,
#             and a purpose if the capability is new), and expected.json
# A requirement is (name, its SHALL sentence, [(scenario name, "WHEN ... THEN ...")]);
# a removed one is (name, reason, migration). "narrow" stands for a MODIFIED
# delta that keeps only the first scenario of that requirement; the gap it
# must give is filled in by write_projects.
PROJECTS11 = {
    "museum": {
        "specs": {
            "admission": ("Visitors buy day tickets and enter the museum through a gate.", [
                ("Ticket sale", "The system SHALL sell day tickets at the entrance.", [
                    ("Places left", "WHEN a visitor asks for a day ticket AND places are left for the day THEN the system sells the ticket and prints it"),
                    ("Sold out", "WHEN a visitor asks for a day ticket AND no places are left for the day THEN the system offers the visitor a ticket for the next day"),
                ]),
                ("Members", "The system SHALL let members in without a day ticket.", [
                    ("Member card", "WHEN a member scans a member card at the gate THEN the system opens the gate"),
                ]),
            ]),
            "programme": ("The museum offers guided tours and hosts private events.", [
                ("Guided tours", "The system SHALL take bookings for guided tours.", [
                    ("Tour booking", "WHEN a visitor books a guided tour THEN the system reserves a place on the tour and sends a confirmation"),
                ]),
                ("Private events", "The system SHALL announce private events.", [
                    ("Announcement", "WHEN a private event is taking place in the museum THEN the system shows a notice at the entrance"),
                ]),
                ("No-shows", "The system SHALL keep track of visitors who miss their tours.", [
                    ("Second missed tour", "WHEN a visitor misses a booked tour for the second time THEN the system asks the visitor to pay in advance for the next booking"),
                ]),
            ]),
        },
        "changes": {
            "clean": {
                "name": "add-audio-guides",
                "why": "Visitors keep asking for audio guides at the ticket desk.",
                "delta": {"audio-guides": {
                    "purpose": "The museum lends audio guides to visitors for the length of their visit.",
                    "ADDED": [("Lending", "The system SHALL lend audio guides to visitors.", [
                        ("Guide in stock", "WHEN a visitor asks for an audio guide AND an audio guide is in stock THEN the system hands out an audio guide and records the loan"),
                        ("None in stock", "WHEN a visitor asks for an audio guide AND no audio guide is in stock THEN the system offers the visitor the guide as a phone app"),
                    ])]}},
                "expected": {"covered": ["audio-guides/Lending/Guide in stock", "audio-guides/Lending/None in stock"]},
            },
            "direct": {
                "name": "add-interest-list",
                "why": "Tours are often booked by people who then do not come.",
                "delta": {"programme": {"ADDED": [("Interest list", "The system SHALL collect interest in a tour before places are given out.", [
                    ("Booking request", "WHEN a visitor books a guided tour THEN the system reserves no place on the tour and adds the visitor to the list of interested visitors"),
                ])]}},
                "expected": {"conflicts": [["programme/Guided tours/Tour booking", "programme/Interest list/Booking request"]]},
            },
            "modified": {
                "name": "close-gate-during-private-events",
                "why": "Members walked into private events.",
                "delta": {"programme": {"MODIFIED": [("Private events", "The system SHALL announce private events and keep other people out.", [
                    ("Announcement", "WHEN a private event is taking place in the museum THEN the system shows a notice at the entrance and does not open the gate for members"),
                ])]}},
                "expected": {"conflicts": [["programme/Private events/Announcement", "admission/Members/Member card"]]},
            },
            "gap": {
                "name": "add-school-groups",
                "why": "Schools visit in groups and should not queue for single tickets.",
                "delta": {"admission": {"ADDED": [("School groups", "The system SHALL admit a school group with one ticket.", [
                    ("Registered group", "WHEN a teacher arrives with a school group AND the group is registered THEN the system prints one group ticket"),
                ])]}},
                "expected": {"gaps": ["admission/School groups/Registered group"]},
            },
            "narrowed": {
                "name": "drop-next-day-offer",
                "why": "Tickets for the next day are now sold online only.",
                "narrow": ("admission", "Ticket sale"),
            },
        },
    },
    "coworking": {
        "specs": {
            "desks": ("Members book desks by the day and enter the building with a badge.", [
                ("Desk booking", "The system SHALL let members book a desk for a day.", [
                    ("Desk free", "WHEN a member books a desk for a day AND a desk is free on that day THEN the system confirms the booking and assigns a desk"),
                    ("No desk free", "WHEN a member books a desk for a day AND no desk is free on that day THEN the system puts the member on the waiting list for that day"),
                ]),
                ("Entrance", "The system SHALL let members into the building.", [
                    ("Badge at the entrance", "WHEN a member holds a badge to the reader at the entrance THEN the system unlocks the entrance door"),
                ]),
            ]),
            "building": ("Services of the building that all members share.", [
                ("Post", "The system SHALL tell members about their post.", [
                    ("Parcel arrives", "WHEN a parcel arrives for a member THEN the system sends the member a message"),
                ]),
                ("Cleaning", "The system SHALL announce the weekly deep cleaning.", [
                    ("Cleaning in progress", "WHEN the weekly deep cleaning is in progress THEN the system shows a notice on the screens"),
                ]),
                ("Printer", "The system SHALL keep the shared printer working.", [
                    ("Third paper jam", "WHEN the printer reports a paper jam for the third time in a day THEN the system calls the service company"),
                ]),
            ]),
        },
        "changes": {
            "clean": {
                "name": "add-guest-passes",
                "why": "Members bring guests, and nobody knows who is in the building.",
                "delta": {"building": {
                    "ADDED": [("Guests", "The system SHALL register guests at the reception.", [
                        ("Host present", "WHEN a guest arrives at the reception AND the host is in the building THEN the system prints a guest pass and informs the host"),
                        ("Host absent", "WHEN a guest arrives at the reception AND the host is not in the building THEN the system asks the guest to wait and calls the host"),
                    ])],
                    "REMOVED": [("Printer", "The printer is replaced by a leased one that the supplier monitors.", "None. The supplier's own service takes over.")]}},
                "expected": {"covered": ["building/Guests/Host present", "building/Guests/Host absent"]},
            },
            "overlap": {
                "name": "add-billing-holds",
                "why": "Some members book desks for months without paying.",
                "delta": {"billing": {
                    "purpose": "Invoices for memberships, and what happens when they are not paid.",
                    "ADDED": [("Overdue invoices", "The system SHALL limit members who have not paid.", [
                        ("Invoice overdue", "WHEN a member has an overdue invoice THEN the system does not confirm any booking of the member"),
                    ])]}},
                "expected": {"conflicts": [["desks/Desk booking/Desk free", "billing/Overdue invoices/Invoice overdue"]]},
            },
            "modified": {
                "name": "lock-door-during-cleaning",
                "why": "The cleaners were disturbed by members coming in.",
                "delta": {"building": {"MODIFIED": [("Cleaning", "The system SHALL announce the weekly deep cleaning and keep the building empty during it.", [
                    ("Cleaning in progress", "WHEN the weekly deep cleaning is in progress THEN the system shows a notice on the screens and does not unlock the entrance door"),
                ])]}},
                "expected": {"conflicts": [["building/Cleaning/Cleaning in progress", "desks/Entrance/Badge at the entrance"]]},
            },
            "gap": {
                "name": "add-meeting-rooms",
                "why": "Members want to book meeting rooms as they book desks.",
                "delta": {"desks": {"ADDED": [("Meeting rooms", "The system SHALL let members book meeting rooms by the hour.", [
                    ("Room free", "WHEN a member books a meeting room AND the room is free at that time THEN the system reserves the room and adds it to the member's calendar"),
                ])]}},
                "expected": {"gaps": ["desks/Meeting rooms/Room free"]},
            },
            "narrowed": {
                "name": "drop-desk-waiting-list",
                "why": "The waiting list for desks was hardly used.",
                "narrow": ("desks", "Desk booking"),
            },
        },
    },
    "marina": {
        "specs": {
            "berths": ("Visiting boats get a guest berth and pay for their stay.", [
                ("Guest berths", "The system SHALL give guest berths to visiting boats.", [
                    ("Berth free", "WHEN a skipper asks for a guest berth AND a guest berth is free THEN the system assigns the berth and shows its number"),
                    ("No berth free", "WHEN a skipper asks for a guest berth AND no guest berth is free THEN the system sends the skipper to the anchorage"),
                ]),
                ("Departure", "The system SHALL close the stay when a boat leaves.", [
                    ("Boat leaves", "WHEN a skipper reports the departure of the boat THEN the system frees the berth and sends the invoice for the stay"),
                ]),
            ]),
            "crane": ("Skippers book the boat crane of the harbour.", [
                ("Crane slots", "The system SHALL take bookings for the boat crane.", [
                    ("Crane booking", "WHEN a skipper books the crane THEN the system reserves a crane slot and sends the time to the skipper"),
                ]),
            ]),
            "harbour": ("The weather service and the shore power of the harbour.", [
                ("Weather", "The system SHALL pass on storm warnings.", [
                    ("Storm warning", "WHEN a storm warning is in force THEN the system shows the warning on the harbour screens"),
                ]),
                ("Shore power", "The system SHALL watch the shore power of the pontoons.", [
                    ("Third outage", "WHEN the shore power of a pontoon fails for the third time in a week THEN the system calls the electrician"),
                ]),
            ]),
        },
        "changes": {
            "clean": {
                "name": "add-pump-out-station",
                "why": "The harbour gets a station for waste water.",
                "delta": {"harbour": {"ADDED": [("Pump-out", "The system SHALL manage the pump-out station.", [
                    ("Station free", "WHEN a skipper asks for the pump-out station AND the station is free THEN the system unlocks the station for the boat"),
                    ("Station in use", "WHEN a skipper asks for the pump-out station AND the station is not free THEN the system adds the boat to the queue for the station"),
                ])]}},
                "expected": {"covered": ["harbour/Pump-out/Station free", "harbour/Pump-out/Station in use"]},
            },
            "direct": {
                "name": "keep-berths-of-season-guests",
                "why": "Season guests lose their berth every time they sail out for a day.",
                "delta": {"berths": {"ADDED": [("Season guests", "The system SHALL keep berths for boats that come back.", [
                    ("Day trip", "WHEN a skipper reports the departure of the boat THEN the system does not free the berth and keeps it for the boat's return"),
                ])]}},
                "expected": {"conflicts": [["berths/Departure/Boat leaves", "berths/Season guests/Day trip"]]},
            },
            "modified": {
                "name": "no-crane-in-storms",
                "why": "The crane must not work in strong wind.",
                "delta": {"harbour": {"MODIFIED": [("Weather", "The system SHALL pass on storm warnings and stop work that is unsafe in a storm.", [
                    ("Storm warning", "WHEN a storm warning is in force THEN the system shows the warning on the harbour screens and does not reserve any crane slot"),
                ])]}},
                "expected": {"conflicts": [["harbour/Weather/Storm warning", "crane/Crane slots/Crane booking"]]},
            },
            "gap": {
                "name": "add-winter-storage",
                "why": "Owners ask to leave their boats ashore over the winter.",
                "delta": {"berths": {"ADDED": [("Winter storage", "The system SHALL take requests for winter storage ashore.", [
                    ("Place ashore free", "WHEN an owner asks for winter storage AND a place ashore is free THEN the system reserves the place and sends the price"),
                ])]}},
                "expected": {"gaps": ["berths/Winter storage/Place ashore free"]},
            },
            "narrowed": {
                "name": "drop-anchorage-referral",
                "why": "The anchorage is closed for dredging.",
                "narrow": ("berths", "Guest berths"),
            },
        },
    },
    "cinema": {
        "specs": {
            "screenings": ("Customers buy seats for film screenings and enter the hall with their ticket.", [
                ("Seat sale", "The system SHALL sell seats for screenings.", [
                    ("Seats left", "WHEN a customer asks for a seat at a screening AND seats are left for the screening THEN the system sells the seat and shows its number"),
                    ("Sold out", "WHEN a customer asks for a seat at a screening AND no seats are left for the screening THEN the system offers the customer the next screening of the film"),
                ]),
                ("Admission", "The system SHALL check tickets at the hall door.", [
                    ("Ticket scan", "WHEN a customer scans a ticket at the hall door THEN the system lets the customer into the hall"),
                ]),
            ]),
            "operations": ("What the staff of the cinema is told and asked to do.", [
                ("Snack orders", "The system SHALL take snack orders from the seats.", [
                    ("Order from a seat", "WHEN a customer orders snacks from a seat THEN the system sends the order to the kiosk and charges the customer's card"),
                ]),
                ("Projector", "The system SHALL report projector trouble.", [
                    ("Projector fault", "WHEN the projector of a hall is out of order THEN the system informs the technician on duty"),
                ]),
                ("Cleaning", "The system SHALL react to complaints about dirty halls.", [
                    ("Third complaint", "WHEN customers complain about a dirty hall for the third time in a week THEN the system orders an extra cleaning"),
                ]),
            ]),
        },
        "changes": {
            "clean": {
                "name": "add-lost-property",
                "why": "Customers ask every day for things they left in a hall.",
                "delta": {"operations": {
                    "ADDED": [("Lost property", "The system SHALL answer questions about lost property.", [
                        ("Item found", "WHEN a customer asks about a lost item AND the item is in the lost property box THEN the system tells the customer where to collect the item"),
                        ("Item not found", "WHEN a customer asks about a lost item AND the item is not in the lost property box THEN the system records a search request"),
                    ])],
                    "REMOVED": [("Cleaning", "Every hall is now cleaned after every screening.", "None.")]}},
                "expected": {"covered": ["operations/Lost property/Item found", "operations/Lost property/Item not found"]},
            },
            "overlap": {
                "name": "enforce-age-ratings",
                "why": "The cinema was fined for letting children into a film rated 16.",
                "delta": {"screenings": {"ADDED": [("Age rating", "The system SHALL enforce the age rating of a film.", [
                    ("Under age", "WHEN the customer is younger than the age rating of the film THEN the system does not let the customer into the hall"),
                ])]}},
                "expected": {"conflicts": [["screenings/Admission/Ticket scan", "screenings/Age rating/Under age"]]},
            },
            "modified": {
                "name": "stop-sales-on-projector-fault",
                "why": "Seats were sold for a hall whose projector was broken.",
                "delta": {"operations": {"MODIFIED": [("Projector", "The system SHALL report projector trouble and stop the sale of seats.", [
                    ("Projector fault", "WHEN the projector of a hall is out of order THEN the system informs the technician on duty and does not sell any seat for that hall"),
                ])]}},
                "expected": {"conflicts": [["operations/Projector/Projector fault", "screenings/Seat sale/Seats left"]]},
            },
            "gap": {
                "name": "add-private-screenings",
                "why": "Schools ask for screenings of their own.",
                "delta": {"screenings": {"ADDED": [("Private screenings", "The system SHALL take requests for private screenings.", [
                    ("Hall free", "WHEN a school asks for a private screening AND a hall is free at that time THEN the system books the hall and sends an offer"),
                ])]}},
                "expected": {"gaps": ["screenings/Private screenings/Hall free"]},
            },
            "narrowed": {
                "name": "drop-next-screening-offer",
                "why": "Customers found the offer of another screening confusing.",
                "narrow": ("screenings", "Seat sale"),
            },
        },
    },
    "conference": {
        "specs": {
            "registration": ("People sign up for the conference and get their badge on arrival.", [
                ("Sign-up", "The system SHALL register participants.", [
                    ("Places left", "WHEN a person signs up for the conference AND places are left THEN the system registers the person and sends an invoice"),
                    ("Conference full", "WHEN a person signs up for the conference AND no places are left THEN the system adds the person to the waiting list"),
                ]),
                ("Badges", "The system SHALL hand out badges on arrival.", [
                    ("Arrival", "WHEN a participant arrives at the welcome desk THEN the system prints the participant's badge"),
                ]),
            ]),
            "sessions": ("The talks, their speakers and the questions of the audience.", [
                ("Questions", "The system SHALL collect questions for the speakers.", [
                    ("Question sent", "WHEN a participant sends a question during a talk THEN the system shows the question to the moderator"),
                ]),
                ("Slides", "The system SHALL watch the deadline for the slides.", [
                    ("Second missed deadline", "WHEN a speaker misses the deadline for the slides for the second time THEN the system informs the programme chair"),
                ]),
            ]),
            "payments": ("The invoices of the participants.", [
                ("Overdue invoices", "The system SHALL remind participants who have not paid.", [
                    ("Invoice overdue", "WHEN the invoice of a participant is overdue THEN the system sends the participant a reminder"),
                ]),
            ]),
        },
        "changes": {
            "clean": {
                "name": "add-workshops",
                "why": "The conference gets a day of workshops with few places each.",
                "delta": {"sessions": {"ADDED": [("Workshops", "The system SHALL take bookings for workshops.", [
                    ("Workshop has places", "WHEN a participant books a workshop AND the workshop has places left THEN the system adds the participant to the workshop"),
                    ("Workshop full", "WHEN a participant books a workshop AND the workshop has no places left THEN the system suggests another workshop at the same time"),
                ])]}},
                "expected": {"covered": ["sessions/Workshops/Workshop has places", "sessions/Workshops/Workshop full"]},
            },
            "direct": {
                "name": "go-paperless",
                "why": "The organisers want to avoid printed material.",
                "delta": {"registration": {"ADDED": [("Paperless arrival", "The system SHALL avoid printed material at the welcome desk.", [
                    ("Code on the phone", "WHEN a participant arrives at the welcome desk THEN the system prints no badge and shows a code on the participant's phone"),
                ])]}},
                "expected": {"conflicts": [["registration/Badges/Arrival", "registration/Paperless arrival/Code on the phone"]]},
            },
            "modified": {
                "name": "no-badge-without-payment",
                "why": "Some participants attended without ever paying.",
                "delta": {"payments": {"MODIFIED": [("Overdue invoices", "The system SHALL remind participants who have not paid and hold back their badge.", [
                    ("Invoice overdue", "WHEN the invoice of a participant is overdue THEN the system sends the participant a reminder and does not print the participant's badge"),
                ])]}},
                "expected": {"conflicts": [["payments/Overdue invoices/Invoice overdue", "registration/Badges/Arrival"]]},
            },
            "gap": {
                "name": "add-student-price",
                "why": "Students asked for a lower price.",
                "delta": {"registration": {"ADDED": [("Student price", "The system SHALL give students a lower price.", [
                    ("Valid student card", "WHEN a person asks for the student price AND the student card is valid THEN the system lowers the price on the invoice"),
                ])]}},
                "expected": {"gaps": ["registration/Student price/Valid student card"]},
            },
            "narrowed": {
                "name": "close-conference-waiting-list",
                "why": "Nobody on the waiting list ever got a place.",
                "narrow": ("registration", "Sign-up"),
            },
        },
    },
    "foodbank": {
        "specs": {
            "intake": ("Donors bring food, and volunteers check it and put it into the stock.", [
                ("Deliveries", "The system SHALL record the food that donors deliver.", [
                    ("Within date", "WHEN a donor delivers food AND the food is within its use-by date THEN the system adds the food to the stock and prints a receipt"),
                    ("Past date", "WHEN a donor delivers food AND the food is not within its use-by date THEN the system refuses the food and records the reason"),
                ]),
                ("Cold room", "The system SHALL find a place for chilled goods.", [
                    ("Chilled goods", "WHEN a volunteer scans chilled goods at the door THEN the system assigns a shelf in the cold room"),
                ]),
            ]),
            "counter": ("Households collect a food parcel at the counter once a week.", [
                ("Collection", "The system SHALL hand out food parcels at the counter.", [
                    ("Card scanned", "WHEN a client scans the household card at the counter THEN the system releases a food parcel for the household"),
                ]),
                ("Stock count", "The system SHALL announce the yearly stock count.", [
                    ("Count in progress", "WHEN the yearly stock count is in progress THEN the system shows a notice at the counter"),
                ]),
                ("Missed collections", "The system SHALL notice households that stop coming.", [
                    ("Third missed collection", "WHEN a household misses its collection for the third time in a row THEN the system informs the social worker"),
                ]),
            ]),
        },
        "changes": {
            "clean": {
                "name": "add-diet-parcels",
                "why": "Some clients cannot eat what is in the standard parcel.",
                "delta": {"counter": {
                    "ADDED": [("Diet parcels", "The system SHALL offer gluten-free parcels.", [
                        ("Parcel in stock", "WHEN a client asks for a gluten-free parcel AND a gluten-free parcel is in stock THEN the system hands out the gluten-free parcel"),
                        ("None in stock", "WHEN a client asks for a gluten-free parcel AND no gluten-free parcel is in stock THEN the system notes the request for the next week"),
                    ])],
                    "REMOVED": [("Missed collections", "The social workers now keep their own list.", "None.")]}},
                "expected": {"covered": ["counter/Diet parcels/Parcel in stock", "counter/Diet parcels/None in stock"]},
            },
            "overlap": {
                "name": "expire-registrations",
                "why": "Households that had moved away were still collecting parcels.",
                "delta": {"counter": {"ADDED": [("Registration", "The system SHALL keep the register of households up to date.", [
                    ("Registration expired", "WHEN the registration of a household has expired THEN the system does not release any food parcel for the household"),
                ])]}},
                "expected": {"conflicts": [["counter/Collection/Card scanned", "counter/Registration/Registration expired"]]},
            },
            "modified": {
                "name": "freeze-stock-during-count",
                "why": "Food that arrived during the count was counted twice.",
                "delta": {"counter": {"MODIFIED": [("Stock count", "The system SHALL announce the yearly stock count and keep the stock unchanged during it.", [
                    ("Count in progress", "WHEN the yearly stock count is in progress THEN the system shows a notice at the counter and does not add any food to the stock"),
                ])]}},
                "expected": {"conflicts": [["counter/Stock count/Count in progress", "intake/Deliveries/Within date"]]},
            },
            "gap": {
                "name": "add-shop-surplus",
                "why": "Shops offer food that they cannot sell any more.",
                "delta": {"intake": {"ADDED": [("Shop surplus", "The system SHALL collect surplus food from shops.", [
                    ("Van free", "WHEN a shop offers surplus food AND a van is free THEN the system plans a pick-up and confirms it to the shop"),
                ])]}},
                "expected": {"gaps": ["intake/Shop surplus/Van free"]},
            },
            "narrowed": {
                "name": "stop-recording-refused-food",
                "why": "Volunteers now turn away food past its date before it reaches the system.",
                "narrow": ("intake", "Deliveries"),
            },
        },
    },
}

# Folder -> the specs written into it.
SETS = {"eval": SPECS, "eval2": SPECS2, "eval3": SPECS3, "eval4": SPECS4, "eval5": SPECS5,
        "eval6": SPECS6, "eval7": SPECS7, "eval8": SPECS8, "eval9": SPECS9, "eval10": SPECS10,
        "eval12": SPECS12, "size": SPECS_SIZE, "size2": SPECS_SIZE2}


def _project13(capabilities: tuple, first, second, doors, pair, single, ban, notice, added, removal: dict) -> dict:
    """One eval13 project from its nine existing scenarios and what the changes say.

    capabilities  the names of its two spec files, with their purpose: ((name, purpose), (name, purpose))
    first, second two requirements with one scenario each: the two complementary cases of one event
    doors         a requirement with two complementary scenarios; its first one is in the old conflict
    pair          a requirement with two complementary scenarios (the "narrowed" change drops the second)
    single        the only requirement for its event (the "retired" change removes it)
    ban           a state requirement that forbids what the first scenario of `doors` demands: the old conflict
    notice        a state requirement, and the words that the "modified" change adds to it: it then
                  forbids what `first` demands
    added         the requirement that the "clean" change adds
    removal       the words for the changes: their names and reasons, and the reworded sibling scenario
    """
    (a, a_purpose), (b, b_purpose) = capabilities
    notice_requirement, notice_extra = notice

    def name(capability: str, requirement: tuple, scenario: int = 0) -> str:
        return f"{capability}/{requirement[0]}/{requirement[2][scenario][0]}"

    old = [[name(a, doors), name(b, ban)]]
    notice_name, notice_sentence, [(notice_scenario, notice_text)] = notice_requirement
    reworded = (doors[0], doors[1], [doors[2][0], (doors[2][1][0], doors[2][1][1] + removal["sibling_extra"])])
    changes = {
        "clean": {"name": removal["clean"][0], "why": removal["clean"][1],
                  "delta": {b: {"ADDED": [added]}},
                  "expected": {"covered": [name(b, added, 0), name(b, added, 1)], "nothing": True}},
        "modified": {"name": removal["modified"][0], "why": removal["modified"][1],
                     "delta": {b: {"MODIFIED": [(notice_name, notice_sentence,
                                                 [(notice_scenario, notice_text + notice_extra)])]}},
                     "expected": {"conflicts": [[name(b, notice_requirement), name(a, first)]]}},
        "removed": {"name": removal["removed"][0], "why": removal["removed"][1],
                    "delta": {a: {"REMOVED": [(second[0], removal["removed"][1], "None.")]}},
                    "expected": {"gaps": [name(a, first)]}},
        "narrowed": {"name": removal["narrowed"][0], "why": removal["narrowed"][1], "narrow": (b, pair[0])},
        "retired": {"name": removal["retired"][0], "why": removal["retired"][1],
                    "delta": {b: {"REMOVED": [(single[0], removal["retired"][1], "None.")]}},
                    "expected": {"nothing": True}},
        "sibling": {"name": removal["sibling"][0], "why": removal["sibling"][1],
                    "delta": {a: {"MODIFIED": [reworded]}},
                    "expected": {"nothing": True}},
    }
    return {"specs": {a: (a_purpose, [first, second, doors]), b: (b_purpose, [pair, single, ban, notice_requirement])},
            "old": old, "changes": changes}


PROJECTS13 = {
    "dorm": _project13(
        (("rooms", "Students move into a dormitory and open their rooms with a card."),
         ("house", "What the dormitory offers besides the rooms, and when it is closed.")),
        ("Move-in with deposit", "The system SHALL hand out a room when the deposit is paid.", [
            ("Deposit paid", "WHEN a student arrives to move in AND the deposit is paid THEN the system assigns a room and activates the student's card")]),
        ("Move-in without deposit", "The system SHALL hold back the room until the deposit is paid.", [
            ("Deposit not paid", "WHEN a student arrives to move in AND the deposit is not paid THEN the system sends the student to the housing office")]),
        ("Room doors", "The system SHALL control the room doors by card.", [
            ("Valid card", "WHEN a student holds the card to a room door AND the card is valid for that room THEN the system unlocks the room door"),
            ("Other card", "WHEN a student holds the card to a room door AND the card is not valid for that room THEN the system keeps the room door locked")]),
        ("Guests", "The system SHALL register overnight guests.", [
            ("Guest nights left", "WHEN a student registers an overnight guest AND the student has guest nights left THEN the system issues a guest pass"),
            ("No guest nights left", "WHEN a student registers an overnight guest AND the student has no guest nights left THEN the system refuses the registration")]),
        ("Bicycle cellar", "The system SHALL manage the bicycle cellar.", [
            ("Place in the cellar", "WHEN a student asks for a place in the bicycle cellar THEN the system assigns a stand and adds the student to the cellar list")]),
        ("Winter break", "The system SHALL close the house over the winter break.", [
            ("House closed", "WHEN the house is closed for the winter break THEN the system does not unlock any room door")]),
        (("Fire drills", "The system SHALL announce fire drills.", [
            ("Drill running", "WHEN a fire drill is running THEN the system shows a notice on the hall screens")]),
         " and does not assign any room"),
        ("Registered mail", "The system SHALL tell students about registered mail.", [
            ("Student in the house", "WHEN registered mail arrives for a student AND the student is in the house THEN the system informs the student at once"),
            ("Student away", "WHEN registered mail arrives for a student AND the student is not in the house THEN the system keeps the mail at the desk and sends an email")]),
        {"clean": ("add-registered-mail", "Registered letters were left lying at the desk for weeks."),
         "modified": ("no-move-in-during-drills", "A student moved in during a fire drill and was not counted."),
         "removed": ("drop-housing-office-referral", "The housing office has closed its counter."),
         "narrowed": ("drop-guest-refusal", "Refusals are now handled by the house tutors."),
         "retired": ("close-bicycle-cellar", "The bicycle cellar is turned into a storage room."),
         "sibling": ("record-door-attempts", "Security wants to know about attempts with a wrong card."),
         "sibling_extra": " and records the attempt"}),
    "courses": _project13(
        (("enrolment", "People enrol in the courses of a language school and pay for them."),
         ("school", "Lessons, certificates, and what the school announces.")),
        ("Enrolment with a test", "The system SHALL place people by their test result.", [
            ("Test taken", "WHEN a person enrols in a course AND the person has taken the placement test THEN the system assigns the person to a group and sends the timetable")]),
        ("Enrolment without a test", "The system SHALL ask new people to take the placement test.", [
            ("Test not taken", "WHEN a person enrols in a course AND the person has not taken the placement test THEN the system books a placement test for the person")]),
        ("Course fees", "The system SHALL collect the course fee.", [
            ("Card accepted", "WHEN a student pays the course fee AND the card is accepted THEN the system issues a receipt"),
            ("Card declined", "WHEN a student pays the course fee AND the card is not accepted THEN the system asks for another means of payment")]),
        ("Missed lessons", "The system SHALL handle lessons that a student cannot attend.", [
            ("Notice in time", "WHEN a student cancels a lesson AND the lesson is more than 24 hours away THEN the system offers a replacement lesson"),
            ("Late notice", "WHEN a student cancels a lesson AND the lesson is not more than 24 hours away THEN the system counts the lesson as taken")]),
        ("Certificates", "The system SHALL issue certificates.", [
            ("Course completed", "WHEN a student completes a course THEN the system issues a certificate of attendance")]),
        ("Audit", "The system SHALL freeze the books during an audit.", [
            ("Audit running", "WHEN the accounts of the school are being audited THEN the system does not issue any receipt")]),
        (("Teacher absence", "The system SHALL announce lessons that do not take place.", [
            ("Teacher ill", "WHEN a teacher is ill THEN the system shows the cancelled lessons in the app")]),
         " and does not assign anyone to a group"),
        ("Conversation club", "The system SHALL take sign-ups for the conversation club.", [
            ("Places left", "WHEN a student signs up for the conversation club AND places are left THEN the system adds the student to the club list"),
            ("Club full", "WHEN a student signs up for the conversation club AND no places are left THEN the system suggests the next club date")]),
        {"clean": ("add-conversation-club", "Students asked for a place to practise speaking."),
         "modified": ("no-new-groups-while-a-teacher-is-ill", "New students were put into groups that had no teacher."),
         "removed": ("drop-placement-test-booking", "Placement tests are now taken on the website before enrolment."),
         "narrowed": ("drop-late-notice-rule", "Counting a cancelled lesson as taken led to many complaints."),
         "retired": ("stop-certificates", "Certificates are issued by the examination board from now on."),
         "sibling": ("hold-place-after-declined-card", "Students lost their place when a card payment failed."),
         "sibling_extra": " and keeps the place for three days"}),
    "bloodbank": _project13(
        (("donors", "Donors check in to give blood and hear about their test results."),
         ("operations", "Orders of the hospitals, the fridges, and what the staff is told.")),
        ("Donors who may give", "The system SHALL admit donors who may give blood.", [
            ("Last donation long ago", "WHEN a donor checks in AND the last donation of the donor is more than 8 weeks ago THEN the system prints a donation form and calls the donor")]),
        ("Donors who must wait", "The system SHALL turn away donors who gave blood recently.", [
            ("Last donation recent", "WHEN a donor checks in AND the last donation of the donor is not more than 8 weeks ago THEN the system tells the donor the next possible date")]),
        ("Test results", "The system SHALL tell donors their test results.", [
            ("Normal result", "WHEN a test result arrives AND the result is normal THEN the system sends the donor a letter of thanks"),
            ("Abnormal result", "WHEN a test result arrives AND the result is not normal THEN the system asks the donor to call the doctor")]),
        ("Hospital orders", "The system SHALL serve the orders of the hospitals.", [
            ("In stock", "WHEN a hospital orders blood AND the blood group is in stock THEN the system reserves the units and prints a delivery note"),
            ("Not in stock", "WHEN a hospital orders blood AND the blood group is not in stock THEN the system asks the neighbouring blood bank")]),
        ("Fridges", "The system SHALL watch the fridges.", [
            ("Fridge too warm", "WHEN a fridge reports a temperature above 6 degrees THEN the system alerts the technician on duty")]),
        ("Postal strike", "The system SHALL hold back the post during a strike.", [
            ("Strike", "WHEN the postal service is on strike THEN the system does not send any letter")]),
        (("Stocktaking", "The system SHALL announce the stocktaking.", [
            ("Stocktaking running", "WHEN the stocktaking is running THEN the system shows a notice to the staff")]),
         " and does not print any donation form"),
        ("Donation drives", "The system SHALL plan donation drives at companies.", [
            ("Bus free", "WHEN a company asks for a donation drive AND the donation bus is free on that day THEN the system books the bus and confirms the date"),
            ("Bus not free", "WHEN a company asks for a donation drive AND the donation bus is not free on that day THEN the system offers the company another date")]),
        {"clean": ("add-donation-drives", "Companies ask for donation drives on their premises."),
         "modified": ("no-donations-during-stocktaking", "Donations taken during the stocktaking were counted twice."),
         "removed": ("drop-next-date-notice", "The donor app now shows the next possible date."),
         "narrowed": ("stop-asking-the-neighbours", "The neighbouring blood bank has closed."),
         "retired": ("retire-fridge-alarm", "The new fridges call the technician themselves."),
         "sibling": ("block-donors-with-abnormal-results", "A donor with an abnormal result came back and donated again."),
         "sibling_extra": " and blocks further donations"}),
    "permits": _project13(
        (("applications", "Builders apply for building permits and get a decision."),
         ("office", "Site visits, old files, and when the permit office holds back.")),
        ("Complete applications", "The system SHALL take in complete applications.", [
            ("All plans attached", "WHEN a builder submits an application AND all plans are attached THEN the system registers the application and assigns a case officer")]),
        ("Incomplete applications", "The system SHALL send back incomplete applications.", [
            ("Plans missing", "WHEN a builder submits an application AND not all plans are attached THEN the system returns the application to the builder")]),
        ("Decisions", "The system SHALL make decisions known.", [
            ("Permit granted", "WHEN a case officer decides an application AND the permit is granted THEN the system publishes the decision on the notice board"),
            ("Permit refused", "WHEN a case officer decides an application AND the permit is not granted THEN the system sends the reasons to the builder")]),
        ("Site visits", "The system SHALL plan site visits.", [
            ("Inspector available", "WHEN a case officer asks for a site visit AND an inspector is available that week THEN the system books the visit and informs the builder"),
            ("No inspector", "WHEN a case officer asks for a site visit AND no inspector is available that week THEN the system puts the visit on the waiting list")]),
        ("Old files", "The system SHALL fetch old files on request.", [
            ("File requested", "WHEN a citizen asks to see an old file THEN the system orders the file from the archive")]),
        ("Election silence", "The system SHALL publish nothing during an election campaign.", [
            ("Campaign running", "WHEN an election campaign is running THEN the system does not publish any decision on the notice board")]),
        (("Staff training", "The system SHALL announce days on which the office is closed for training.", [
            ("Office closed", "WHEN the office is closed for staff training THEN the system shows the closing on the website")]),
         " and does not register any application"),
        ("Objections", "The system SHALL take objections from neighbours.", [
            ("Period open", "WHEN a neighbour files an objection AND the objection period is open THEN the system adds the objection to the case"),
            ("Period over", "WHEN a neighbour files an objection AND the objection period is not open THEN the system rejects the objection and explains why")]),
        {"clean": ("add-objections", "Neighbours had no way to object online."),
         "modified": ("no-registration-on-training-days", "Applications that came in on training days got a wrong date."),
         "removed": ("drop-return-of-incomplete-applications", "Incomplete applications are now completed by phone."),
         "narrowed": ("drop-visit-waiting-list", "The waiting list for site visits was never looked at."),
         "retired": ("close-file-requests", "Old files are now public on the archive's own website."),
         "sibling": ("send-refusals-by-registered-mail", "Builders claimed they never got the reasons."),
         "sibling_extra": " by registered mail"}),
    "newsroom": _project13(
        (("articles", "Reporters hand in articles, and editors review and publish them."),
         ("desk", "Photos, corrections, and the state of the newsroom and its website.")),
        ("Articles with sources", "The system SHALL pass on articles that name their sources.", [
            ("Source list attached", "WHEN a reporter submits an article AND the article has a source list THEN the system sends the article to the editor on duty")]),
        ("Articles without sources", "The system SHALL send back articles that name no sources.", [
            ("No source list", "WHEN a reporter submits an article AND the article has no source list THEN the system returns the article to the reporter")]),
        ("Review", "The system SHALL act on the review of an editor.", [
            ("Approved", "WHEN an editor reviews an article AND the article is approved THEN the system publishes the article on the website"),
            ("Not approved", "WHEN an editor reviews an article AND the article is not approved THEN the system sends the notes of the editor to the reporter")]),
        ("Photos", "The system SHALL find photos for articles.", [
            ("Photo in the archive", "WHEN an editor asks for a photo AND a fitting photo is in the archive THEN the system attaches the photo to the article"),
            ("No photo in the archive", "WHEN an editor asks for a photo AND no fitting photo is in the archive THEN the system sends a request to the photo desk")]),
        ("Corrections", "The system SHALL follow up on errors that readers report.", [
            ("Error reported", "WHEN a reader reports an error in an article THEN the system opens a correction case for the article")]),
        ("Maintenance", "The system SHALL keep the website unchanged during maintenance.", [
            ("Maintenance mode", "WHEN the website is in maintenance mode THEN the system does not publish any article on the website")]),
        (("Night hours", "The system SHALL tell reporters whom to reach at night.", [
            ("No editor on duty", "WHEN no editor is on duty THEN the system shows the night contact to the reporters")]),
         " and does not send any article to the editor on duty"),
        ("Interview room", "The system SHALL plan the use of the interview room.", [
            ("Room free", "WHEN a reporter asks for the interview room AND the room is free at that time THEN the system books the room for the reporter"),
            ("Room not free", "WHEN a reporter asks for the interview room AND the room is not free at that time THEN the system offers the reporter the next free hour")]),
        {"clean": ("add-interview-room", "Two interviews were planned in the same room at the same time."),
         "modified": ("hold-articles-at-night", "Articles sent at night were lost in an empty inbox."),
         "removed": ("drop-return-of-unsourced-articles", "Source lists are now enforced by the editor program itself."),
         "narrowed": ("drop-photo-desk-requests", "The photo desk has been merged into the archive."),
         "retired": ("retire-reader-corrections", "Corrections are handled by the reader editor's own tool."),
         "sibling": ("back-to-draft-after-review", "Rejected articles stayed in the review queue."),
         "sibling_extra": " and sets the article back to draft"}),
    "makerspace": _project13(
        (("machines", "Members of a makerspace use machines and buy material."),
         ("space", "Hand tools, visitors, and what happens in the rooms.")),
        ("Trained members", "The system SHALL let trained members use the machines.", [
            ("Training done", "WHEN a member logs in at a machine AND the member has completed the training for that machine THEN the system switches the machine on and starts the timer")]),
        ("Untrained members", "The system SHALL keep untrained members off the machines.", [
            ("Training missing", "WHEN a member logs in at a machine AND the member has not completed the training for that machine THEN the system shows the next training dates")]),
        ("Material", "The system SHALL sell material to members.", [
            ("Credit sufficient", "WHEN a member takes material from the store AND the credit of the member covers the price THEN the system books the price to the account of the member"),
            ("Credit too low", "WHEN a member takes material from the store AND the credit of the member does not cover the price THEN the system asks the member to top up the account")]),
        ("Tool loans", "The system SHALL lend hand tools.", [
            ("Tool on the shelf", "WHEN a member asks to borrow a tool AND the tool is on the shelf THEN the system records the loan and shows the return date"),
            ("Tool lent out", "WHEN a member asks to borrow a tool AND the tool is not on the shelf THEN the system adds the member to the queue for the tool")]),
        ("Tours", "The system SHALL arrange tours for visitors.", [
            ("Tour request", "WHEN a visitor asks for a tour THEN the system proposes a date with a volunteer")]),
        ("Year-end closing", "The system SHALL keep the accounts unchanged while the year is closed.", [
            ("Accounts being closed", "WHEN the accounts of the year are being closed THEN the system does not book anything to the account of any member")]),
        (("Safety inspection", "The system SHALL announce the yearly safety inspection.", [
            ("Inspection running", "WHEN the yearly safety inspection is running THEN the system shows a notice at the entrance")]),
         " and does not switch any machine on"),
        ("Open evenings", "The system SHALL take sign-ups for open evenings.", [
            ("Places left", "WHEN a guest signs up for an open evening AND places are left THEN the system confirms the place by email"),
            ("Evening full", "WHEN a guest signs up for an open evening AND no places are left THEN the system offers the guest the next open evening")]),
        {"clean": ("add-open-evenings", "Guests turned up at open evenings that were already full."),
         "modified": ("no-machines-during-inspection", "The inspector found a machine running during the inspection."),
         "removed": ("drop-training-dates-screen", "Training dates are now printed on a poster next to each machine."),
         "narrowed": ("drop-tool-queue", "Nobody answered the messages of the tool queue."),
         "retired": ("stop-tours", "There are no volunteers left to give tours."),
         "sibling": ("return-material-when-credit-is-low", "Material taken without credit was never paid for."),
         "sibling_extra": " and puts the material back on the stock list"}),
}


def _project14(capabilities: tuple, first, second, event, pair, counted, notice, added, direct, overlap, gap,
               names: dict) -> dict:
    """One eval14 project from its seven existing scenarios and what the changes add.

    capabilities  the names of its two spec files, with their purpose
    first, second two requirements with one scenario each: the two complementary cases of one event
    event         a requirement with one scenario: an event and what the system then does
    pair          a requirement with two complementary scenarios
    counted       a requirement about something that happens for the n-th time
    notice        a state requirement, and the words that the "modified" change adds to it: it then
                  forbids what `first` demands
    added         the requirement that the "clean" change adds, with both of its cases
    direct        a requirement for the trigger of `event`, with the opposite outcome in other words
    overlap       a state requirement that forbids what the first scenario of `pair` demands
    gap           a requirement with one of two cases
    names         for each change: the name of its folder and the "why" of its proposal
    """
    (a, a_purpose), (b, b_purpose) = capabilities
    (notice_name, notice_sentence, [(notice_scenario, notice_text)]), notice_extra = notice

    def name(capability: str, requirement: tuple, scenario: int = 0) -> str:
        return f"{capability}/{requirement[0]}/{requirement[2][scenario][0]}"

    def change(version: str, delta: dict, expected: dict) -> dict:
        return {"name": names[version][0], "why": names[version][1], "delta": delta, "expected": expected}

    changes = {
        "clean": change("clean", {b: {"ADDED": [added]}},
                        {"covered": [name(b, added, 0), name(b, added, 1)], "nothing": True}),
        "direct": change("direct", {a: {"ADDED": [direct]}},
                         {"conflicts": [[name(a, event), name(a, direct)]]}),
        "overlap": change("overlap", {a: {"ADDED": [overlap]}},
                          {"conflicts": [[name(b, pair), name(a, overlap)]]}),
        "modified": change("modified", {b: {"MODIFIED": [(notice_name, notice_sentence,
                                                           [(notice_scenario, notice_text + notice_extra)])]}},
                           {"conflicts": [[f"{b}/{notice_name}/{notice_scenario}", name(a, first)]]}),
        "gap": change("gap", {b: {"ADDED": [gap]}}, {"gaps": [name(b, gap)]}),
        "removed": change("removed", {a: {"REMOVED": [(second[0], names["removed"][1], "None.")]}},
                          {"gaps": [name(a, first)]}),
    }
    return {"specs": {a: (a_purpose, [first, second, event]),
                      b: (b_purpose, [pair, counted, (notice_name, notice_sentence, [(notice_scenario, notice_text)])])},
            "changes": changes}


PROJECTS14 = {
    "tennis": _project14(
        (("courts", "Members of a tennis club book courts and play on them."),
         ("club", "Guests, members who do not turn up, and tournaments.")),
        ("Booking a free court", "The system SHALL give a free court to the member who asks for it.", [
            ("Court free", "WHEN a member books a court AND the court is free at that hour THEN the system reserves the court for the member")]),
        ("Booking a taken court", "The system SHALL offer another hour when a court is taken.", [
            ("Court taken", "WHEN a member books a court AND the court is not free at that hour THEN the system shows the member the next free hour")]),
        ("Floodlights", "The system SHALL light the courts for evening play.", [
            ("Evening match", "WHEN a member starts a match after sunset THEN the system switches the floodlights on")]),
        ("Guests", "The system SHALL handle the guests of members.", [
            ("Guest fee paid", "WHEN a member brings a guest AND the guest fee is paid THEN the system prints a guest ticket"),
            ("Guest fee not paid", "WHEN a member brings a guest AND the guest fee is not paid THEN the system asks for the guest fee")]),
        ("No-shows", "The system SHALL act on members who do not turn up.", [
            ("Third no-show", "WHEN a member misses a booked court for the third time in a season THEN the system blocks the bookings of the member for a week")]),
        (("Tournaments", "The system SHALL announce tournaments.", [
            ("Tournament day", "WHEN a tournament is being played THEN the system shows the schedule at the entrance")]),
         " and does not reserve any court for members"),
        ("Ball machine", "The system SHALL lend the ball machine to members.", [
            ("Machine free", "WHEN a member asks for the ball machine AND the machine is free THEN the system hands out the key of the machine"),
            ("Machine in use", "WHEN a member asks for the ball machine AND the machine is not free THEN the system puts the member on the list for the machine")]),
        ("Energy saving", "The system SHALL save electricity in the evening.", [
            ("Lights out", "WHEN a member starts a match after sunset THEN the system keeps the floodlights dark")]),
        ("Unpaid dues", "The system SHALL limit members who have not paid their dues.", [
            ("Dues unpaid", "WHEN the dues of a member are unpaid THEN the system does not print any guest ticket")]),
        ("Coaching", "The system SHALL take bookings for coaching hours.", [
            ("Coach free", "WHEN a member asks for a coaching hour AND a coach is free THEN the system books the hour and informs the coach")]),
        {"clean": ("add-ball-machine", "The club has bought a ball machine."),
         "direct": ("save-electricity", "The electricity bill of the club has doubled."),
         "overlap": ("limit-members-with-unpaid-dues", "Members who had not paid kept bringing guests."),
         "modified": ("no-member-bookings-on-tournament-days", "Members booked courts that the tournament needed."),
         "gap": ("add-coaching", "The club has hired two coaches."),
         "removed": ("drop-next-free-hour", "The new calendar shows the free hours by itself.")}),
    "brewery": _project14(
        (("brewing", "Brewers start batches, and the tanks are watched while the beer ferments."),
         ("sales", "Orders of the shops, complaints, and what the brewers are told.")),
        ("Starting a batch with malt", "The system SHALL start a batch when the malt is there.", [
            ("Malt in stock", "WHEN a brewer starts a batch AND the malt for the recipe is in stock THEN the system reserves a tank and prints the brew sheet")]),
        ("Starting a batch without malt", "The system SHALL get the malt that a batch needs.", [
            ("Malt missing", "WHEN a brewer starts a batch AND the malt for the recipe is not in stock THEN the system orders the malt from the supplier")]),
        ("Fermentation", "The system SHALL watch the temperature of the tanks.", [
            ("Tank too warm", "WHEN the temperature of a tank rises above 22 degrees THEN the system opens the cooling valve of the tank")]),
        ("Shop orders", "The system SHALL serve the orders of the shops.", [
            ("Beer in stock", "WHEN a shop orders beer AND the beer is in stock THEN the system prints a delivery note"),
            ("Beer not in stock", "WHEN a shop orders beer AND the beer is not in stock THEN the system tells the shop the next bottling date")]),
        ("Complaints", "The system SHALL act on complaints about a batch.", [
            ("Third complaint", "WHEN a shop complains about a batch for the third time THEN the system recalls the batch")]),
        (("Cleaning", "The system SHALL announce the cleaning of the brewhouse.", [
            ("Cleaning day", "WHEN the brewhouse is being cleaned THEN the system shows a notice to the brewers")]),
         " and does not reserve any tank"),
        ("Tastings", "The system SHALL take bookings for tastings.", [
            ("Places left", "WHEN a visitor books a tasting AND places are left THEN the system confirms the tasting by email"),
            ("Tasting full", "WHEN a visitor books a tasting AND no places are left THEN the system offers the visitor the next tasting")]),
        ("Warm fermentation", "The system SHALL let some beers ferment warm.", [
            ("Warm tank", "WHEN the temperature of a tank rises above 22 degrees THEN the system shuts off the cooling of the tank")]),
        ("Recalls", "The system SHALL stop deliveries during a recall.", [
            ("Recall running", "WHEN a recall is running THEN the system does not print any delivery note")]),
        ("Kegs", "The system SHALL rent kegs to customers.", [
            ("Keg available", "WHEN a customer asks for a keg AND a keg is available THEN the system books the keg and prints the deposit slip")]),
        {"clean": ("add-tastings", "Visitors ask for tastings at the brewery."),
         "direct": ("allow-warm-fermentation", "The new summer ale has to ferment warm."),
         "overlap": ("stop-deliveries-during-recalls", "Beer from a recalled batch was delivered to a shop."),
         "modified": ("no-new-batches-on-cleaning-days", "A batch was started in a tank that was being cleaned."),
         "gap": ("add-keg-rental", "Customers ask for kegs for their parties."),
         "removed": ("drop-automatic-malt-orders", "The malt is now ordered by the head brewer by phone.")}),
    "musicschool": _project14(
        (("lessons", "Pupils of a music school take lessons and practise in the rooms of the school."),
         ("school", "Instruments on loan, absences, and school concerts.")),
        ("Lessons with a free teacher", "The system SHALL book a lesson when a teacher is free.", [
            ("Teacher free", "WHEN a pupil asks for a lesson AND a teacher of the instrument is free THEN the system books the lesson and informs the teacher")]),
        ("Lessons without a free teacher", "The system SHALL keep a waiting list for lessons.", [
            ("No teacher free", "WHEN a pupil asks for a lesson AND no teacher of the instrument is free THEN the system puts the pupil on the waiting list")]),
        ("Practice rooms", "The system SHALL open the practice rooms to pupils.", [
            ("Pupil card", "WHEN a pupil holds the card to a practice room THEN the system unlocks the practice room")]),
        ("Instrument loans", "The system SHALL lend instruments to pupils.", [
            ("Instrument on the shelf", "WHEN a pupil asks to borrow an instrument AND the instrument is on the shelf THEN the system records the loan"),
            ("Instrument lent out", "WHEN a pupil asks to borrow an instrument AND the instrument is not on the shelf THEN the system reserves the instrument for the pupil")]),
        ("Absences", "The system SHALL tell the parents about missed lessons.", [
            ("Third absence", "WHEN a pupil misses a lesson for the third time in a term THEN the system informs the parents")]),
        (("Concerts", "The system SHALL announce school concerts.", [
            ("Concert evening", "WHEN a school concert is taking place THEN the system shows the programme in the hall")]),
         " and does not book any lesson"),
        ("Sheet music", "The system SHALL sell sheet music to pupils.", [
            ("Copy in stock", "WHEN a pupil orders sheet music AND a copy is in stock THEN the system puts the copy aside for the pupil"),
            ("No copy in stock", "WHEN a pupil orders sheet music AND no copy is in stock THEN the system orders a copy from the publisher")]),
        ("Supervised practice", "The system SHALL let pupils practise only when a teacher is present.", [
            ("Card at the door", "WHEN a pupil holds the card to a practice room THEN the system keeps the practice room shut")]),
        ("Unpaid fees", "The system SHALL limit pupils whose fees are not paid.", [
            ("Fees unpaid", "WHEN the fees of a pupil are unpaid THEN the system does not record any loan")]),
        ("Grade exams", "The system SHALL enter pupils for grade exams.", [
            ("Teacher agrees", "WHEN a pupil signs up for a grade exam AND the teacher agrees THEN the system enters the pupil for the exam")]),
        {"clean": ("add-sheet-music", "Pupils buy their sheet music at the school."),
         "direct": ("supervise-practice", "An instrument was damaged in a practice room."),
         "overlap": ("limit-pupils-with-unpaid-fees", "Instruments were lent to pupils who had not paid their fees."),
         "modified": ("no-lessons-during-concerts", "Lessons were booked into the hall on a concert evening."),
         "gap": ("add-grade-exams", "The school now enters pupils for grade exams."),
         "removed": ("drop-lesson-waiting-list", "The waiting list for lessons is now kept by the secretary.")}),
    "drivingschool": _project14(
        (("driving", "Learners of a driving school book lessons and take the theory test."),
         ("office", "Registration, cancellations, and the days on which the cars are serviced.")),
        ("Lessons with a free car", "The system SHALL book a lesson when a car is free.", [
            ("Car free", "WHEN a learner books a driving lesson AND a car is free at that time THEN the system books the lesson and assigns a car")]),
        ("Lessons without a free car", "The system SHALL offer another time when no car is free.", [
            ("No car free", "WHEN a learner books a driving lesson AND no car is free at that time THEN the system offers the learner another time")]),
        ("Theory test", "The system SHALL record the result of the theory test.", [
            ("Test passed", "WHEN a learner passes the theory test THEN the system opens the booking of road lessons for the learner")]),
        ("Registration", "The system SHALL register new learners.", [
            ("Eye test valid", "WHEN a person registers as a learner AND the eye test of the person is valid THEN the system creates a learner file"),
            ("Eye test not valid", "WHEN a person registers as a learner AND the eye test of the person is not valid THEN the system asks for a new eye test")]),
        ("Late cancellations", "The system SHALL act on lessons that are cancelled late.", [
            ("Third late cancellation", "WHEN a learner cancels a lesson late for the third time THEN the system charges the learner for the lesson")]),
        (("Car service", "The system SHALL announce the days on which the cars are serviced.", [
            ("Service day", "WHEN the cars are being serviced THEN the system shows the service day in the calendar")]),
         " and does not book any lesson"),
        ("Road exams", "The system SHALL book road exams at the test centre.", [
            ("Slot at the test centre", "WHEN an instructor asks for a road exam AND the test centre has a slot THEN the system books the exam and informs the learner"),
            ("No slot", "WHEN an instructor asks for a road exam AND the test centre has no slot THEN the system puts the learner on the list for the next date")]),
        ("Waiting period", "The system SHALL make learners wait after the theory test.", [
            ("After the theory test", "WHEN a learner passes the theory test THEN the system keeps road lessons closed for the learner")]),
        ("Age limit", "The system SHALL respect the legal age for learners.", [
            ("Too young", "WHEN a person is younger than 17 THEN the system does not create any learner file")]),
        ("Refresher courses", "The system SHALL take bookings for refresher courses.", [
            ("Licence held", "WHEN a driver asks for a refresher course AND the driver holds a licence THEN the system books the course")]),
        {"clean": ("add-road-exams", "Road exams were booked by phone and often forgotten."),
         "direct": ("add-waiting-period", "The insurer asks for a waiting period after the theory test."),
         "overlap": ("respect-age-limit", "A fifteen-year-old was registered as a learner."),
         "modified": ("no-lessons-on-service-days", "Lessons were booked on a day when all cars were at the garage."),
         "gap": ("add-refresher-courses", "Older drivers ask for refresher courses."),
         "removed": ("drop-other-time-offer", "Learners now see the free times in the app.")}),
    "climbing": _project14(
        (("entry", "Climbers check in at a climbing hall and hand back rental gear."),
         ("hall", "Courses, fall reports, and the setting of new routes.")),
        ("Entry with a safety check", "The system SHALL let in climbers who have passed the safety check.", [
            ("Check passed", "WHEN a climber checks in AND the climber has passed the safety check THEN the system opens the turnstile and counts the visit")]),
        ("Entry without a safety check", "The system SHALL send new climbers to an instructor.", [
            ("Check missing", "WHEN a climber checks in AND the climber has not passed the safety check THEN the system sends the climber to the instructor")]),
        ("Rental gear", "The system SHALL take back rental gear.", [
            ("Gear handed back", "WHEN a climber hands back rental gear THEN the system releases the deposit")]),
        ("Courses", "The system SHALL take sign-ups for courses.", [
            ("Places left", "WHEN a climber signs up for a course AND places are left THEN the system adds the climber to the course"),
            ("Course full", "WHEN a climber signs up for a course AND no places are left THEN the system suggests the next course")]),
        ("Fall reports", "The system SHALL act on falls that are reported.", [
            ("Second fall report", "WHEN a route gets a fall report for the second time in a week THEN the system closes the route for inspection")]),
        (("Route setting", "The system SHALL announce the setting of new routes.", [
            ("Setting in progress", "WHEN routes are being set in the hall THEN the system shows the closed walls on the screen")]),
         " and does not open the turnstile"),
        ("Birthday parties", "The system SHALL take bookings for birthday parties.", [
            ("Room free", "WHEN a parent books a birthday party AND the party room is free on that day THEN the system reserves the room and sends the price"),
            ("Room not free", "WHEN a parent books a birthday party AND the party room is not free on that day THEN the system offers the parent another day")]),
        ("Damaged gear", "The system SHALL check rental gear before the deposit goes back.", [
            ("Gear check", "WHEN a climber hands back rental gear THEN the system holds the deposit back")]),
        ("Expired memberships", "The system SHALL limit climbers whose membership has expired.", [
            ("Membership expired", "WHEN the membership of a climber has expired THEN the system does not add the climber to any course")]),
        ("Private coaching", "The system SHALL take bookings for private coaching.", [
            ("Coach available", "WHEN a climber asks for private coaching AND a coach is available THEN the system books the coach")]),
        {"clean": ("add-birthday-parties", "Parents ask for birthday parties in the hall."),
         "direct": ("check-gear-before-refund", "Damaged gear came back and the deposit was already paid out."),
         "overlap": ("limit-expired-memberships", "Climbers with an expired membership filled the courses."),
         "modified": ("close-entry-during-route-setting", "Climbers walked under the lift while routes were being set."),
         "gap": ("add-private-coaching", "Climbers ask for hours with a coach of their own."),
         "removed": ("drop-instructor-referral", "The safety check is now done online before the first visit.")}),
    "florist": _project14(
        (("bouquets", "Customers of a flower shop order bouquets, which the workshop makes."),
         ("shop", "Loyalty cards, complaints, and the arrival of fresh flowers.")),
        ("Bouquets with flowers in stock", "The system SHALL pass on orders that can be made.", [
            ("Flowers in stock", "WHEN a customer orders a bouquet AND the flowers are in stock THEN the system sends the order to the workshop")]),
        ("Bouquets without flowers in stock", "The system SHALL propose something else when flowers are missing.", [
            ("Flowers missing", "WHEN a customer orders a bouquet AND the flowers are not in stock THEN the system proposes a similar bouquet")]),
        ("Finished bouquets", "The system SHALL get finished bouquets to the customers.", [
            ("Bouquet ready", "WHEN the workshop finishes a bouquet THEN the system hands the bouquet to the driver")]),
        ("Loyalty cards", "The system SHALL reward regular customers.", [
            ("Card full", "WHEN a customer shows a loyalty card AND the card is full THEN the system gives the customer a free bouquet"),
            ("Card not full", "WHEN a customer shows a loyalty card AND the card is not full THEN the system adds a stamp to the card")]),
        ("Complaints", "The system SHALL act on complaints about wilted flowers.", [
            ("Third complaint", "WHEN a customer complains about wilted flowers for the third time THEN the system informs the owner")]),
        (("Fresh flowers", "The system SHALL announce the arrival of fresh flowers.", [
            ("Truck unloading", "WHEN the flower truck is being unloaded THEN the system shows a notice at the counter")]),
         " and does not send any order to the workshop"),
        ("Wedding consultations", "The system SHALL take bookings for wedding consultations.", [
            ("Florist free", "WHEN a couple asks for a consultation AND a florist is free that week THEN the system books the consultation"),
            ("No florist free", "WHEN a couple asks for a consultation AND no florist is free that week THEN the system offers the couple the following week")]),
        ("Pick-up", "The system SHALL keep bouquets for customers who fetch them.", [
            ("Bouquet kept", "WHEN the workshop finishes a bouquet THEN the system keeps the bouquet in the cold room")]),
        ("Busy weeks", "The system SHALL give nothing away in the busiest weeks.", [
            ("Week before Mother's Day", "WHEN it is the week before Mother's Day THEN the system does not give any customer a free bouquet")]),
        ("Subscriptions", "The system SHALL take orders for a weekly bouquet.", [
            ("Address in the delivery area", "WHEN a customer asks for a weekly bouquet AND the address is in the delivery area THEN the system starts the subscription")]),
        {"clean": ("add-wedding-consultations", "Couples ask for an hour with a florist before their wedding."),
         "direct": ("keep-bouquets-for-pick-up", "Many customers want to fetch their bouquet themselves."),
         "overlap": ("no-free-bouquets-in-busy-weeks", "Free bouquets were handed out in the busiest week of the year."),
         "modified": ("no-orders-during-unloading", "Orders came into the workshop while everyone was unloading the truck."),
         "gap": ("add-subscriptions", "Customers ask for a fresh bouquet every week."),
         "removed": ("drop-similar-bouquet-proposals", "Customers did not like the bouquets that were proposed instead.")}),
}


def _project15(capabilities: tuple, first, second, event, pair, counted, notice, added, direct, prop, status, gap,
               names: dict) -> dict:
    """One eval15 project: the seven existing scenarios of _project14, and six changes.

    Everything is as in _project14, except that there is no "removed" change,
    and the "overlap" change is replaced by two:

    prop      (the "property" change) a state requirement about a quantity of
              the person or thing that the event of `pair` is about. It
              forbids what the first scenario of `pair` demands
    status    a state requirement about a yes/no property of the person or
              thing that the event of `event` is about. It forbids what
              `event` demands
    """
    (a, _), (b, _) = capabilities
    project = _project14(capabilities, first, second, event, pair, counted, notice, added, direct, prop, gap,
                         {**names, "overlap": names["property"], "removed": ("unused", "")})
    changes = project["changes"]
    changes["property"] = changes.pop("overlap")
    del changes["removed"]
    changes["status"] = {
        "name": names["status"][0], "why": names["status"][1], "delta": {b: {"ADDED": [status]}},
        "expected": {"conflicts": [[f"{a}/{event[0]}/{event[2][0][0]}", f"{b}/{status[0]}/{status[2][0][0]}"]]}}
    return project


PROJECTS15 = {
    "bakery": _project15(
        (("orders", "Customers order cakes at a bakery, and the bakers bake."),
         ("counter", "Collection at the counter, regular customers, and notices.")),
        ("Order with oven time", "The system SHALL accept an order when the ovens have time for it.", [
            ("Oven time free", "WHEN a customer orders a cake AND the ovens have free time on that day THEN the system confirms the order to the customer")]),
        ("Order without oven time", "The system SHALL offer another day when the ovens are full.", [
            ("Ovens full", "WHEN a customer orders a cake AND the ovens have no free time on that day THEN the system offers the customer the next free day")]),
        ("Fresh bread", "The system SHALL announce fresh bread.", [
            ("Bread out of the oven", "WHEN a baker takes a batch of bread out of the oven THEN the system rings the shop bell")]),
        ("Collection", "The system SHALL hand out orders at the counter.", [
            ("Order paid", "WHEN a customer collects an order AND the order is paid THEN the system prints a collection slip"),
            ("Order not paid", "WHEN a customer collects an order AND the order is not paid THEN the system asks for the payment")]),
        ("Uncollected orders", "The system SHALL act on customers who do not collect their orders.", [
            ("Third uncollected order", "WHEN a customer fails to collect an order for the third time THEN the system asks the customer to pay in advance")]),
        (("Stocktaking", "The system SHALL announce stocktaking.", [
            ("Stocktaking day", "WHEN the bakery is taking stock THEN the system shows a notice in the shop window")]),
         " and does not confirm any order"),
        ("Loyalty cards", "The system SHALL reward regular customers.", [
            ("Card full", "WHEN a customer shows a loyalty card AND the card is full THEN the system gives the customer a free loaf"),
            ("Card not full", "WHEN a customer shows a loyalty card AND the card is not full THEN the system adds a stamp to the card")]),
        ("Quiet mornings", "The system SHALL keep the shop quiet in the early morning.", [
            ("No bell", "WHEN a baker takes a batch of bread out of the oven THEN the system keeps the shop bell silent")]),
        ("Large orders", "The system SHALL limit what is handed out at the counter.", [
            ("Too many items", "WHEN an order has more than 40 items THEN the system does not print any collection slip")]),
        ("Wholesale", "The system SHALL treat the batches for wholesale customers apart.", [
            ("Wholesale batch", "WHEN a batch of bread is baked for a wholesale customer THEN the system does not ring the shop bell")]),
        ("Baking courses", "The system SHALL take bookings for baking courses.", [
            ("Place free", "WHEN a customer asks for a place in a baking course AND a place is free THEN the system books the place and sends the recipe list")]),
        {"clean": ("add-loyalty-cards", "The bakery wants to reward its regular customers."),
         "direct": ("quiet-early-mornings", "Neighbours complained about the bell at five in the morning."),
         "property": ("limit-large-orders", "Large orders blocked the counter at rush hour."),
         "status": ("no-bell-for-wholesale", "Customers queued for bread that was not for sale."),
         "modified": ("no-orders-during-stocktaking", "Orders taken during stocktaking could not be baked."),
         "gap": ("add-baking-courses", "The bakery starts baking courses.")}),
    "observatory": _project15(
        (("visits", "Visitors book and attend evenings at a public observatory."),
         ("dome", "Telescope time, cancellations, and notices.")),
        ("Booking an evening with places", "The system SHALL give a place to the visitor who books an evening.", [
            ("Places left", "WHEN a visitor books an evening AND the evening has places left THEN the system reserves a place for the visitor")]),
        ("Booking a full evening", "The system SHALL offer another evening when one is full.", [
            ("Evening full", "WHEN a visitor books an evening AND the evening has no places left THEN the system offers the visitor the next evening")]),
        ("Dome roof", "The system SHALL prepare the dome for observing.", [
            ("Observing starts", "WHEN a guide starts an observing session THEN the system opens the dome roof")]),
        ("Telescope time", "The system SHALL give telescope time to visitors.", [
            ("Telescope free", "WHEN a visitor asks for telescope time AND the telescope is free THEN the system unlocks the telescope controls"),
            ("Telescope in use", "WHEN a visitor asks for telescope time AND the telescope is not free THEN the system puts the visitor on the telescope list")]),
        ("Late cancellations", "The system SHALL act on visitors who cancel late.", [
            ("Second late cancellation", "WHEN a visitor cancels an evening on the same day for the second time THEN the system asks the visitor for a deposit")]),
        (("Mirror cleaning", "The system SHALL announce the cleaning of the mirror.", [
            ("Mirror being cleaned", "WHEN the telescope mirror is being cleaned THEN the system shows a notice at the entrance")]),
         " and does not reserve any place for visitors"),
        ("Star maps", "The system SHALL lend star maps to visitors.", [
            ("Map on the shelf", "WHEN a visitor asks for a star map AND a map is on the shelf THEN the system lends the map to the visitor"),
            ("No map on the shelf", "WHEN a visitor asks for a star map AND no map is on the shelf THEN the system sends the map to the visitor by email")]),
        ("Bad weather", "The system SHALL protect the telescope from rain.", [
            ("Roof stays shut", "WHEN a guide starts an observing session THEN the system keeps the dome roof closed")]),
        ("Introduction evenings", "The system SHALL protect the telescope from misuse.", [
            ("Too few introductions", "WHEN a visitor has attended fewer than 2 introduction evenings THEN the system does not unlock the telescope controls")]),
        ("Indoor sessions", "The system SHALL run the sessions about the sun indoors.", [
            ("Session in the lecture room", "WHEN an observing session is held in the lecture room THEN the system does not open the dome roof")]),
        ("School visits", "The system SHALL take bookings from schools.", [
            ("Guide free", "WHEN a teacher asks for a school visit AND a guide is free on that day THEN the system books the visit and informs the guide")]),
        {"clean": ("add-star-maps", "Visitors asked for star maps to take home."),
         "direct": ("keep-roof-shut", "Rain got into the dome twice this year."),
         "property": ("telescope-after-two-introductions", "Beginners moved the telescope out of alignment."),
         "status": ("indoor-sessions", "The sessions about the sun are held in the lecture room."),
         "modified": ("no-bookings-during-mirror-cleaning", "Evenings were booked while the telescope could not be used."),
         "gap": ("add-school-visits", "Schools asked for visits in the morning.")}),
    "bowling": _project15(
        (("lanes", "Players get a lane at a bowling alley and play."),
         ("bar", "Shoes, fouls, the league, and notices.")),
        ("Asking for a free lane", "The system SHALL give a free lane to the player who asks for one.", [
            ("Lane free", "WHEN a player asks for a lane AND a lane is free THEN the system assigns the lane to the player")]),
        ("Asking when all lanes are taken", "The system SHALL let players wait for a lane.", [
            ("No lane free", "WHEN a player asks for a lane AND no lane is free THEN the system gives the player a pager")]),
        ("Scoreboard", "The system SHALL show the score of a game.", [
            ("Game starts", "WHEN a player starts a game THEN the system switches the lane screen on")]),
        ("Shoe hire", "The system SHALL hire out shoes.", [
            ("Shoes in stock", "WHEN a player asks for shoes AND shoes of the size are in stock THEN the system hands out a pair of shoes"),
            ("Shoes out of stock", "WHEN a player asks for shoes AND shoes of the size are not in stock THEN the system offers the player shoe covers")]),
        ("Fouls", "The system SHALL act on fouls.", [
            ("Third foul", "WHEN a player steps over the foul line for the third time in a game THEN the system ends the game of the player")]),
        (("League nights", "The system SHALL announce league nights.", [
            ("League night", "WHEN a league match is being played THEN the system shows the league table above the bar")]),
         " and does not assign any lane to players"),
        ("Bumpers", "The system SHALL help children to play.", [
            ("Bumper lane free", "WHEN a player asks for bumpers AND a lane with bumpers is free THEN the system raises the bumpers of the lane"),
            ("No bumper lane free", "WHEN a player asks for bumpers AND no lane with bumpers is free THEN the system offers the player a ramp")]),
        ("Screen saving", "The system SHALL spare the lane screens.", [
            ("Screen off", "WHEN a player starts a game THEN the system leaves the lane screen dark")]),
        ("Open tabs", "The system SHALL limit players who owe money.", [
            ("Tab too high", "WHEN the bar tab of a player is above 60 euros THEN the system does not hand out any pair of shoes")]),
        ("Practice games", "The system SHALL run practice games without a score.", [
            ("Practice game", "WHEN a game is a practice game THEN the system does not switch the lane screen on")]),
        ("Lockers", "The system SHALL rent lockers to players.", [
            ("Locker free", "WHEN a player asks for a locker AND a locker is free THEN the system gives the player the locker code")]),
        {"clean": ("add-bumpers", "Families asked for bumpers."),
         "direct": ("spare-the-screens", "The lane screens burn in."),
         "property": ("limit-open-tabs", "Players left without paying their tab."),
         "status": ("practice-games-without-screen", "Practice games do not need a scoreboard."),
         "modified": ("no-lanes-on-league-nights", "Players took lanes that the league needed."),
         "gap": ("add-lockers", "The alley has installed lockers.")}),
    "tailor": _project15(
        (("fittings", "Customers of a tailor book fittings, and the tailors work on garments."),
         ("workshop", "Collection, missed fittings, and notices.")),
        ("Fitting with a free tailor", "The system SHALL book a fitting when a tailor is free.", [
            ("Tailor free", "WHEN a customer asks for a fitting AND a tailor is free THEN the system books the fitting for the customer")]),
        ("Fitting without a free tailor", "The system SHALL offer another day when no tailor is free.", [
            ("No tailor free", "WHEN a customer asks for a fitting AND no tailor is free THEN the system offers the customer the next free day")]),
        ("Pressing", "The system SHALL keep the air of the workshop clean.", [
            ("Pressing starts", "WHEN a tailor starts the steam press THEN the system switches the extractor fan on")]),
        ("Collection", "The system SHALL hand out finished garments.", [
            ("Alteration paid", "WHEN a customer collects a garment AND the alteration is paid THEN the system prints a release note"),
            ("Alteration not paid", "WHEN a customer collects a garment AND the alteration is not paid THEN the system shows the amount due")]),
        ("Missed fittings", "The system SHALL act on customers who miss fittings.", [
            ("Second missed fitting", "WHEN a customer misses a fitting for the second time THEN the system asks the customer for a deposit")]),
        (("Holidays", "The system SHALL announce the holidays of the shop.", [
            ("Shop on holiday", "WHEN the shop is on holiday THEN the system shows the opening date on the door")]),
         " and does not book any fitting"),
        ("Fabric samples", "The system SHALL send fabric samples to customers.", [
            ("Sample in stock", "WHEN a customer asks for a fabric sample AND the sample is in stock THEN the system posts the sample to the customer"),
            ("Sample out of stock", "WHEN a customer asks for a fabric sample AND the sample is not in stock THEN the system orders the sample from the mill")]),
        ("Quiet workshop", "The system SHALL keep the workshop quiet.", [
            ("Fan off", "WHEN a tailor starts the steam press THEN the system keeps the extractor fan off")]),
        ("Storage time", "The system SHALL hold back garments that were left for long.", [
            ("Left too long", "WHEN a garment has been in storage for more than 90 days THEN the system does not print any release note")]),
        ("Cold pressing", "The system SHALL save energy when no steam is made.", [
            ("Cold mode", "WHEN the steam press is in cold mode THEN the system does not switch the extractor fan on")]),
        ("Home visits", "The system SHALL take bookings for fittings at home.", [
            ("Customer in the city", "WHEN a customer asks for a home visit AND the customer lives in the city THEN the system books the visit and prints the route")]),
        {"clean": ("add-fabric-samples", "Customers want to feel a fabric before they order."),
         "direct": ("keep-the-workshop-quiet", "The fan is too loud for the fitting room next door."),
         "property": ("hold-back-garments-left-too-long", "Garments left for months have to be checked by the owner first."),
         "status": ("cold-pressing", "The new press has a mode without steam."),
         "modified": ("no-fittings-during-holidays", "Fittings were booked for days on which the shop was closed."),
         "gap": ("add-home-visits", "Customers asked for fittings at home.")}),
    "airfield": _project15(
        (("launches", "Pilots of a gliding club launch and land gliders."),
         ("hangar", "Club gliders, hard landings, and notices.")),
        ("Launch with a free winch", "The system SHALL let a pilot launch when the winch is free.", [
            ("Winch free", "WHEN a pilot asks for a launch AND the winch is free THEN the system clears the pilot for launch")]),
        ("Launch with a busy winch", "The system SHALL let pilots wait for the winch.", [
            ("Winch busy", "WHEN a pilot asks for a launch AND the winch is not free THEN the system adds the pilot to the launch list")]),
        ("Access road", "The system SHALL keep the access road clear for landing gliders.", [
            ("Glider on approach", "WHEN a glider reports its approach THEN the system lowers the barrier on the access road")]),
        ("Club gliders", "The system SHALL give club gliders to pilots.", [
            ("Glider airworthy", "WHEN a pilot asks for a club glider AND the glider is airworthy THEN the system hands out the logbook of the glider"),
            ("Glider not airworthy", "WHEN a pilot asks for a club glider AND the glider is not airworthy THEN the system offers the pilot another glider")]),
        ("Hard landings", "The system SHALL act on hard landings.", [
            ("Third hard landing", "WHEN a pilot makes a hard landing for the third time in a season THEN the system books a check flight for the pilot")]),
        (("Air shows", "The system SHALL announce air shows.", [
            ("Air show", "WHEN an air show is taking place THEN the system shows the programme at the clubhouse")]),
         " and does not clear any pilot for launch"),
        ("Parachutes", "The system SHALL give parachutes to pilots.", [
            ("Parachute packed", "WHEN a pilot asks for a parachute AND a packed parachute is on the shelf THEN the system assigns the parachute to the pilot"),
            ("No parachute packed", "WHEN a pilot asks for a parachute AND no packed parachute is on the shelf THEN the system calls the parachute packer")]),
        ("Open road", "The system SHALL keep the access road open for the farmers.", [
            ("Barrier up", "WHEN a glider reports its approach THEN the system keeps the barrier on the access road raised")]),
        ("Solo hours", "The system SHALL give club gliders to experienced pilots only.", [
            ("Too few solo hours", "WHEN a pilot has fewer than 10 hours of solo flight THEN the system does not hand out any logbook")]),
        ("Training circuits", "The system SHALL treat training circuits apart.", [
            ("Training circuit", "WHEN a glider is on a training circuit THEN the system does not lower the barrier on the access road")]),
        ("Guest flights", "The system SHALL take bookings for guest flights.", [
            ("Instructor free", "WHEN a guest asks for a flight AND an instructor is free THEN the system books the flight and prints the waiver")]),
        {"clean": ("add-parachutes", "The club has bought parachutes."),
         "direct": ("keep-the-road-open", "Farmers complained about waiting at the barrier."),
         "property": ("solo-hours-for-club-gliders", "The insurer asks for a minimum of solo hours."),
         "status": ("training-circuits", "Training circuits do not cross the access road."),
         "modified": ("no-launches-during-air-shows", "Launches got in the way of the air show."),
         "gap": ("add-guest-flights", "The club offers flights to guests.")}),
    "escaperoom": _project15(
        (("games", "Teams book escape rooms and play in them."),
         ("lobby", "Hints, broken props, and notices.")),
        ("Booking a free room", "The system SHALL take the booking of a free room.", [
            ("Room free", "WHEN a team books a room AND the room is free at that hour THEN the system sends the team a booking code")]),
        ("Booking a taken room", "The system SHALL show other hours when a room is taken.", [
            ("Room taken", "WHEN a team books a room AND the room is not free at that hour THEN the system shows the team the free hours")]),
        ("Game start", "The system SHALL start the game when the team is inside.", [
            ("Team enters", "WHEN a team enters a room THEN the system locks the room door")]),
        ("Hints", "The system SHALL give hints to teams.", [
            ("Hints left", "WHEN a team asks for a hint AND the team has hints left THEN the system shows a hint on the room screen"),
            ("No hints left", "WHEN a team asks for a hint AND the team has no hints left THEN the system adds two minutes to the time of the team")]),
        ("Broken props", "The system SHALL act on teams that break props.", [
            ("Second broken prop", "WHEN a team breaks a prop for the second time THEN the system ends the game of the team")]),
        (("Rebuilding", "The system SHALL announce the rebuilding of the rooms.", [
            ("Rooms being rebuilt", "WHEN the rooms are being rebuilt THEN the system shows the opening date in the lobby")]),
         " and does not send any booking code"),
        ("Team photos", "The system SHALL give teams a photo of their game.", [
            ("Printer ready", "WHEN a team asks for a team photo AND the photo printer is ready THEN the system prints the photo"),
            ("Printer not ready", "WHEN a team asks for a team photo AND the photo printer is not ready THEN the system sends the photo by email")]),
        ("Fire safety", "The system SHALL keep the escape routes open.", [
            ("Door unlocked", "WHEN a team enters a room THEN the system keeps the room door unlocked")]),
        ("Fair play", "The system SHALL keep the high scores fair.", [
            ("Late in the game", "WHEN a team has less than 5 minutes left THEN the system does not show any hint on the room screen")]),
        ("Children", "The system SHALL not lock children in.", [
            ("Team with a child", "WHEN a team has a child among its players THEN the system does not lock the room door")]),
        ("Vouchers", "The system SHALL take vouchers as payment.", [
            ("Voucher valid", "WHEN a team pays with a voucher AND the voucher is valid THEN the system marks the booking as paid")]),
        {"clean": ("add-team-photos", "Teams asked for a photo after the game."),
         "direct": ("keep-doors-unlocked", "The fire inspector asked for unlocked doors."),
         "property": ("no-hints-in-the-last-minutes", "Late hints made the high scores unfair."),
         "status": ("do-not-lock-children-in", "Parents complained that their children were locked in."),
         "modified": ("no-bookings-during-rebuilding", "Bookings were taken for rooms that did not exist yet."),
         "gap": ("add-vouchers", "The lobby sells gift vouchers.")}),
}


def _marathon() -> dict:
    """The project of mixed/: a city marathon, and one change that does several things at once."""
    places = ("Registration with places left", "The system SHALL register a runner while places are left.", [
        ("Places left", "WHEN a runner registers AND places are left THEN the system confirms the registration and assigns a bib number")])
    full = ("Registration when full", "The system SHALL keep a waiting list when the race is full.", [
        ("No places left", "WHEN a runner registers AND no places are left THEN the system puts the runner on the waiting list")])
    payment = ("Payment", "The system SHALL take the entry fee.", [
        ("Payment accepted", "WHEN a runner pays the entry fee AND the payment is accepted THEN the system sends the runner a receipt"),
        ("Payment not accepted", "WHEN a runner pays the entry fee AND the payment is not accepted THEN the system asks for another payment method")])
    withdrawal = ("Withdrawal", "The system SHALL let runners withdraw.", [
        ("Runner withdraws", "WHEN a runner withdraws from the race THEN the system refunds the entry fee")])
    transfers = ("Transfers", "The system SHALL let a runner pass the registration on.", [
        ("Registration transferred", "WHEN a runner transfers the registration to another runner THEN the system sends the new runner a confirmation")])
    bibs = ("Bib collection", "The system SHALL hand out bibs before the race.", [
        ("Cleared to start", "WHEN a runner collects the bib AND the runner is cleared to start THEN the system hands out the bib and the timing chip"),
        ("Not cleared to start", "WHEN a runner collects the bib AND the runner is not cleared to start THEN the system sends the runner to the medical desk")])
    waves = ("Start waves", "The system SHALL start the runners in waves.", [
        ("Runner in the wave", "WHEN a start wave is called AND the runner belongs to the wave THEN the system opens the start gate for the runner"),
        ("Runner in another wave", "WHEN a start wave is called AND the runner does not belong to the wave THEN the system shows the runner the right wave")])
    heat_text = "WHEN a heat warning is in force THEN the system shows the warning at the start area"
    heat = ("Heat warning", "The system SHALL warn the runners of heat.", [("Warning in force", heat_text)])
    finish = ("Finish times", "The system SHALL publish the times of the runners.", [
        ("Runner finishes", "WHEN a runner crosses the finish line THEN the system publishes the finish time of the runner")])
    protests = ("Protests", "The system SHALL hold back results that are under protest.", [
        ("Protest open", "WHEN a protest against a result is open THEN the system does not publish any finish time")])
    final = "WHEN a runner asks for a certificate AND the result of the runner is final THEN the system sends the certificate by email"
    not_final = ("Result not final", "WHEN a runner asks for a certificate AND the result of the runner is not final THEN the system tells the runner the date of the final results")
    certificates = ("Certificates", "The system SHALL send certificates to runners.", [("Result final", final), not_final])

    # What the change adds.
    charity = ("Charity places", "The system SHALL offer places that are sold through a charity.", [
        ("Charity place free", "WHEN a runner asks for a charity place AND the charity has places left THEN the system reserves a charity place for the runner"),
        ("Charity full", "WHEN a runner asks for a charity place AND the charity has no places left THEN the system proposes another charity to the runner")])
    no_refund = ("No refunds", "The system SHALL keep the fees of runners who withdraw.", [
        ("Fee kept", "WHEN a runner withdraws from the race THEN the system keeps the entry fee")])
    unpaid = ("Unpaid fees", "The system SHALL hold back the bibs of runners who have not paid.", [
        ("Fee unpaid", "WHEN the entry fee of a runner is unpaid THEN the system does not hand out any bib")])
    pacers = ("Pacers", "The system SHALL give runners a pacer for their target time.", [
        ("Pacer free", "WHEN a runner asks for a pacer AND a pacer for the target time is free THEN the system assigns the pacer to the runner")])

    specs = {
        "registration": ("Runners register for a city marathon and pay the entry fee.", [
            places, full,
            ("Medical certificate", "The system SHALL check the medical certificate of a runner.", [
                ("Certificate valid", "WHEN a runner uploads a medical certificate AND the certificate is valid THEN the system marks the runner as cleared to start"),
                ("Certificate not valid", "WHEN a runner uploads a medical certificate AND the certificate is not valid THEN the system asks the runner for a new certificate")]),
            payment, withdrawal,
            ("Payment deadline", "The system SHALL act on runners who do not pay in time.", [
                ("Second missed deadline", "WHEN a runner misses the payment deadline for the second time THEN the system cancels the registration of the runner")]),
            transfers,
            ("Club discount", "The system SHALL give a discount to the members of running clubs.", [
                ("Club member", "WHEN a runner is a member of a running club THEN the system applies the club discount to the entry fee")])]),
        "race-day": ("The start, the course and the finish on the day of the race.", [
            bibs, waves,
            ("Checkpoints", "The system SHALL time the runners on the course.", [
                ("Checkpoint passed", "WHEN a runner passes a checkpoint THEN the system records the split time of the runner")]),
            ("Cut-off", "The system SHALL close the checkpoints in time.", [
                ("Cut-off time passed", "WHEN the cut-off time of a checkpoint has passed THEN the system closes the checkpoint")]),
            heat,
            ("Drop-outs", "The system SHALL look after runners who drop out.", [
                ("Runner injured", "WHEN a runner drops out AND the runner is injured THEN the system calls the medical team"),
                ("Runner not injured", "WHEN a runner drops out AND the runner is not injured THEN the system sends the sweep bus")]),
            ("Lost chips", "The system SHALL act on lost timing chips.", [
                ("Second lost chip", "WHEN a runner loses a timing chip for the second time THEN the system charges the runner for the chip")])]),
        "results": ("Times, rankings and certificates after the race.", [
            finish, protests, certificates,
            ("Age groups", "The system SHALL rank the runners.", [
                ("Results final", "WHEN the results of the race are final THEN the system ranks the runners in their age groups")]),
            ("Disqualification", "The system SHALL act on the warnings of the referees.", [
                ("Third warning", "WHEN a runner receives a warning from a referee for the third time THEN the system disqualifies the runner")]),
            ("Photos", "The system SHALL give runners their finish photo.", [
                ("Photo available", "WHEN a runner asks for the finish photo AND the photo is available THEN the system sends the runner a link to the photo"),
                ("Photo not available", "WHEN a runner asks for the finish photo AND the photo is not available THEN the system tells the runner when the photos will be ready")]),
            ("Records", "The system SHALL announce records.", [
                ("Course record", "WHEN the finish time of a runner is below the course record THEN the system announces a new course record")]),
            ("Corrections", "The system SHALL tell runners when their time is corrected.", [
                ("Time corrected", "WHEN a referee corrects a finish time THEN the system informs the runner of the new time")])]),
        "volunteers": ("Volunteers sign up for shifts and work at the race.", [
            ("Sign-up", "The system SHALL assign volunteers to shifts.", [
                ("Shift has places", "WHEN a volunteer signs up for a shift AND the shift has places left THEN the system assigns the volunteer to the shift"),
                ("Shift full", "WHEN a volunteer signs up for a shift AND the shift has no places left THEN the system offers the volunteer another shift")]),
            ("Check-in", "The system SHALL check volunteers in.", [
                ("Shift today", "WHEN a volunteer checks in AND the volunteer has a shift on that day THEN the system prints the volunteer badge"),
                ("No shift today", "WHEN a volunteer checks in AND the volunteer has no shift on that day THEN the system shows the volunteer the date of the next shift")]),
            ("No-shows", "The system SHALL act on volunteers who do not turn up.", [
                ("Second missed shift", "WHEN a volunteer misses a shift for the second time THEN the system removes the volunteer from the remaining shifts")]),
            ("Meals", "The system SHALL feed the volunteers.", [
                ("Shift finished", "WHEN a volunteer finishes a shift THEN the system issues a meal voucher")]),
            ("Briefing", "The system SHALL guide volunteers to their briefing.", [
                ("Briefing started", "WHEN the briefing of a shift has started THEN the system shows the briefing room on the volunteer screens")]),
            ("T-shirts", "The system SHALL give every volunteer a T-shirt.", [
                ("Size in stock", "WHEN a volunteer asks for a T-shirt AND the size is in stock THEN the system hands out the T-shirt"),
                ("Size not in stock", "WHEN a volunteer asks for a T-shirt AND the size is not in stock THEN the system notes the size for the next delivery")])]),
    }

    def name(capability: str, requirement: tuple, scenario: int = 0) -> str:
        return f"{capability}/{requirement[0]}/{requirement[2][scenario][0]}"

    delta = {
        "registration": {
            "ADDED": [charity,      # both cases: nothing to report
                      no_refund,    # conflict with `withdrawal`: the same trigger, "refunds" / "keeps"
                      unpaid],      # conflict with the first scenario of `bibs`, in the other spec file
            "MODIFIED": [(payment[0], payment[1], payment[2][:1])],   # loses "Payment not accepted": a gap
            "REMOVED": [(full[0], "The waiting list was never used.", "None."),            # a gap: registers, no places left
                        (transfers[0], "Registrations are personal from now on.", "None.")],  # the only rule for its event: nothing
        },
        "race-day": {
            "ADDED": [pacers],      # one of two cases: a gap
            # conflict with the first scenario of `waves`
            "MODIFIED": [(heat[0], heat[1], [("Warning in force", heat_text + " and does not open any start gate")])],
        },
        "results": {
            # a harmless addition to one scenario, the other word for word the same: nothing
            "MODIFIED": [(certificates[0], certificates[1], [("Result final", final + " and adds the split times"), not_final])],
            "RENAMED": [("Corrections", "Time corrections")],   # nothing
        },
    }
    expected = {
        "conflicts": [[name("registration", withdrawal), name("registration", no_refund)],
                      [name("race-day", bibs), name("registration", unpaid)],
                      [name("race-day", heat), name("race-day", waves)]],
        # A planted gap is named by a scenario that stays and reacts to the event of the gap.
        "gaps": [name("race-day", pacers), name("registration", payment), name("registration", places)],
        "covered": [name("registration", charity, 0), name("registration", charity, 1)],
    }
    return {"specs": specs, "old": [[name("results", finish), name("results", protests)]],
            "changes": {"mixed": {"name": "rules-for-next-season",
                                  "why": "The organisers went through the rules after this year's race.",
                                  "delta": delta, "expected": expected}}}


PROJECTS_MIXED = {"marathon": _marathon()}


def as_projects(specs: dict) -> dict:
    """Old OpenSpec-format specs as projects with a change: development data for the change check.

    The clean spec is what exists, in one spec file. Each planted version
    becomes one change, a MODIFIED requirement in all cases: with one more
    scenario (direct, overlap), with a scenario reworded (ambiguity), or with
    one scenario fewer (gap). The old sets have no SHALL sentence under a
    requirement's header, so a plain one is written. Versions that add a
    requirement without a scenario are left out.
    """
    projects = {}
    for name, spec in specs.items():
        if spec["format"] != "openspec":
            continue

        def requirements(rules: list) -> dict:
            """Requirement name -> (name, SHALL sentence, its scenarios), in the order of first use."""
            grouped = {}
            for requirement, scenario, text in rules:
                grouped.setdefault(requirement, (requirement, f"The system SHALL handle {requirement.lower()}.", []))
                grouped[requirement][2].append((scenario, text))
            return grouped

        changes = {}
        for version, (change, expected) in spec["variants"].items():
            if "add" in change and change["add"][1] is None:
                continue
            # The rules after the change, as main() makes them for the old sets.
            rules = list(spec["rules"])
            for number, rule in change.get("replace", {}).items():
                rules[number - 1] = rule
            if "add" in change:
                rules.append(change["add"])
            if "remove" in change:
                del rules[change["remove"] - 1]
            before, after = requirements(spec["rules"]), requirements(rules)
            names = [f"{name}/{requirement}/{scenario}" for requirement, scenario, _ in rules]
            changes[version] = {
                "name": f"{name}-{version}",
                "why": f"Development case: the '{version}' version of the spec '{name}', as a change.",
                "delta": {name: {"MODIFIED": [after[key] for key in after if after[key] != before[key]]}},
                # Requirement numbers (positions after the change) become scenario names.
                "expected": {key: [[names[n - 1] for n in item] if isinstance(item, list) else names[item - 1]
                                   for item in value] if isinstance(value, list) else value
                             for key, value in expected.items()},
            }
        projects[name] = {"specs": {name: (spec["intro"], list(requirements(spec["rules"]).values()))},
                          "changes": changes}
    return projects


# Folder -> the OpenSpec projects written into it, each with one change.
# change_dev is made from eval9 and eval10, which have been read (E15, E16).
PROJECT_SETS = {"eval11": PROJECTS11, "eval13": PROJECTS13, "eval14": PROJECTS14, "eval15": PROJECTS15,
                "mixed": PROJECTS_MIXED,
                "change_dev": as_projects({**SPECS9, **SPECS10})}


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
        lines += [""] + scenario_lines(scenario, text)
    return "\n".join(lines) + "\n"


def scenario_lines(scenario: str, text: str) -> list[str]:
    """One OpenSpec scenario, from "WHEN a AND b THEN c": a header and one bullet for each part."""
    when, then = text.split(" THEN ")
    first, *others = when.removeprefix("WHEN ").split(" AND ")
    return ([f"#### Scenario: {scenario}", "", f"- **WHEN** {first}"]
            + [f"- **AND** {part}" for part in others] + [f"- **THEN** {then}"])


def requirement_lines(requirement: tuple) -> list[str]:
    """One OpenSpec requirement: its header, its SHALL sentence and its scenarios."""
    name, sentence, scenarios = requirement
    lines = [f"### Requirement: {name}", "", sentence, ""]
    for scenario, text in scenarios:
        lines += scenario_lines(scenario, text) + [""]
    return lines


def write_projects(root: Path, projects: dict) -> int:
    """Write every version of every project (see PROJECTS11); return how many were written.

    A version folder holds the project as OpenSpec lays it out:

        openspec/specs/<capability>/spec.md                    what exists
        openspec/changes/<name>/proposal.md                    why the change is made
        openspec/changes/<name>/specs/<capability>/spec.md     the delta
    """
    written = 0
    for project_name, project in projects.items():
        for version, change in project["changes"].items():
            delta, expected = change.get("delta"), change.get("expected")
            if "narrow" in change:  # MODIFIED: the requirement with its first scenario only
                capability, wanted = change["narrow"]
                name, sentence, scenarios = next(requirement for requirement in project["specs"][capability][1]
                                                 if requirement[0] == wanted)
                delta = {capability: {"MODIFIED": [(name, sentence, scenarios[:1])]}}
                expected = {"gaps": [f"{capability}/{name}/{scenarios[0][0]}"]}
            folder = root / f"{project_name}_{version}"
            for capability, (purpose, requirements) in project["specs"].items():
                lines = [f"# {capability} Specification", "", "## Purpose", "", purpose, "", "## Requirements", ""]
                for requirement in requirements:
                    lines += requirement_lines(requirement)
                _write(folder / "openspec" / "specs" / capability / "spec.md", lines)
            change_folder = folder / "openspec" / "changes" / change["name"]
            _write(change_folder / "proposal.md",
                   ["## Why", "", change["why"], "", "## What Changes", ""]
                   + [f"- `{capability}`: {', '.join(f'{kind} {requirement[0]}' for kind in ('ADDED', 'MODIFIED', 'REMOVED', 'RENAMED') for requirement in parts.get(kind, []))}"
                      for capability, parts in delta.items()])
            for capability, parts in delta.items():
                lines = ["## Purpose", "", parts["purpose"], ""] if "purpose" in parts else []
                for kind in ("ADDED", "MODIFIED"):
                    if kind in parts:
                        lines += [f"## {kind} Requirements", ""]
                        for requirement in parts[kind]:
                            lines += requirement_lines(requirement)
                if "RENAMED" in parts:
                    lines += ["## RENAMED Requirements", ""]
                    for old, new in parts["RENAMED"]:
                        lines += [f"- FROM: `### Requirement: {old}`", f"- TO: `### Requirement: {new}`", ""]
                if "REMOVED" in parts:
                    lines += ["## REMOVED Requirements", ""]
                    for name, reason, migration in parts["REMOVED"]:
                        lines += [f"### Requirement: {name}", "", f"**Reason**: {reason}", "", f"**Migration**: {migration}", ""]
                _write(change_folder / "specs" / capability / "spec.md", lines)
            if "old" in project:  # a conflict that the specs have before any change (eval13)
                expected = {**expected, "old": project["old"]}
            (folder / "expected.json").write_text(
                json.dumps({"conflicts": [], "gaps": [], "covered": [], **expected}) + "\n", encoding="utf-8")
            written += 1
    return written


def _write(path: Path, lines: list[str]) -> None:
    """Write `lines` as a text file that ends with exactly one newline; make its folders."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")


def main() -> None:
    # Only the sets named on the command line (all if none), so that writing a
    # new set never rewrites an old one.
    for folder_name in sys.argv[1:] or [*SETS, *PROJECT_SETS]:
        if folder_name in PROJECT_SETS:
            root = Path("experiments/sets") / folder_name
            print(f"wrote {write_projects(root, PROJECT_SETS[folder_name])} projects to {root}/")
            continue
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
