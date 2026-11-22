# Requirements analysis: ferry_direct

101 requirements analysed: 1 conflict(s), 6 gap(s), 2 ambiguity(ies), 3 scenario(s) to confirm.

## 1. Ambiguity: Ambiguity in seat release condition

Requirement F4 is ambiguous because it is unclear whether the system should release a seat based solely on the time elapsed since payment was due, or if the seat must also currently be in a reserved state. In the situation described, the seat is not reserved and has not been released, yet the unpaid time is 31 minutes. Under the first reading, the system would be required to release the seat because the time limit was exceeded, whereas under the second reading, the system would not release the seat because it is not currently reserved. Which did you mean?

- **A) Keep as-is:** Keep the requirement as written, meaning the system releases a seat whenever the unpaid time exceeds 30 minutes, regardless of whether the seat is currently marked as reserved.
- **B) Change:** Reword the requirement to explicitly state that the system shall release the seat only if the seat is currently reserved and has been unpaid for more than 30 minutes.

*Proven:* Requirement F4 has no single clear meaning. Shown both readings and the situation below, and asked whether the words decide between them, the answers were: 0 for reading 1, 8 for reading 2, 0 'either'.
Reading 1: If a reserved seat has remained unpaid for a duration exceeding 30 minutes, the system must release that seat. [in logic: (> seat_unpaid_minutes 30) => seat_released]
Reading 2: If a reserved seat has remained unpaid for more than 30 minutes, the system must release that seat. [in logic: (and seat_reserved (> seat_unpaid_minutes 30)) => seat_released]
The readings differ in this situation:
- FALSE: seat_released (The seat has been released.)
- FALSE: seat_reserved (A seat has been reserved for the passenger.)
- seat_unpaid_minutes = 31 (The number of minutes a reserved seat has been unpaid.)
Choosing reading 2 instead of reading 1 changes no conflict and no gap.

## 2. Ambiguity: Ambiguous vehicle release timing

Requirement F21 can be read in two different ways. The first reading says that if a vehicle has not checked in 30 minutes before departure, the system must release its vehicle space. The second reading says that if a vehicle space has been released and the vehicle has not checked in exactly 30 minutes before departure, the system must have released the space. Which did you mean?

- **A) Keep as-is:** Keep the requirement as written, meaning the system must release the vehicle space if the vehicle has not checked in 30 minutes before departure.
- **B) Change:** Rewrite the requirement to state that the system must release the vehicle space if the vehicle has not checked in 30 minutes before departure, removing the alternative interpretation.

*Proven:* Requirement F21 has no single clear meaning (independent translations split 4/1/1/1).
Reading 1: If a vehicle has not checked in 30 minutes before departure, the system must release its vehicle space. [in logic: (and (>= minutes_before_departure 30) (not vehicle_checked_in)) => vehicle_space_released]
Reading 2: If a vehicle space has been released and the booked vehicle has not checked in, the system must have released the vehicle space. [in logic: (and vehicle_space_released (not vehicle_checked_in) (= minutes_before_departure 30)) => true]
The readings differ in this situation:
- minutes_before_departure = 30 (The number of minutes before departure.)
- FALSE: vehicle_checked_in (The booked vehicle has checked in.)
- FALSE: vehicle_space_released (A vehicle space has been released.)
It was left out of the conflict and gap checks and should be rewritten.

## 3. Conflict: Ticket Printing Contradiction

The requirements contain a direct conflict regarding the printing of tickets. Requirement F9 states that the system must print a ticket when a passenger asks for one at the port office, while Requirement F101 states that the system must never print tickets. In the situation where a passenger asks for a printed ticket, the system is forced to both print the ticket and not print the ticket, which is impossible.

- **A) Keep as-is:** Keeping the requirements as written means the system is in a state of logical contradiction and cannot function correctly when a passenger requests a printed ticket.
- **B) Change:** Remove Requirement F9 or modify it to state that the system shall provide a digital alternative or direct the passenger to a self-service kiosk, thereby removing the obligation to print tickets that conflicts with Requirement F101.

*Proven:* Requirements F9, F101 cannot all be obeyed in this situation:
- TRUE: passenger_asks_for_printed_ticket (A passenger has asked for a printed ticket at the port office.)

## 4. Gap: Missing requirement for customer booking

The requirements do not specify what the system must do when a customer is booking a crossing. This gap appears in the situation where a customer is booking a crossing and no other triggering events or conditions are active.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for a customer booking a crossing, which could lead to unpredictable or missing functionality.
- **B) Change:** Add a requirement stating that when a customer books a crossing, the system shall process the booking and confirm it to the customer.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: boarding_closes (Boarding has closed.)
- FALSE: car_deck_loading_begins (Loading of the car deck has begun.)
- FALSE: crew_registers_found_item (A crew member has registered a found item.)
- FALSE: crew_starts_shift (A crew member has started a shift.)
- TRUE: customer_books_crossing (A customer is booking a crossing.)
- FALSE: customer_changes_email (A customer has changed the email address of the account.)
- FALSE: customer_completes_crossing (A customer with an account has completed a crossing.)
- FALSE: customer_creates_account (A customer has created an account.)
- FALSE: customer_enters_wrong_password (A customer has entered a wrong password.)
- FALSE: customer_is_silver (The customer has silver status.)
- FALSE: customer_pays_with_points (A customer is paying with loyalty points.)
- FALSE: customer_subscribes_newsletter (A customer has subscribed to the newsletter.)
- FALSE: customer_unsubscribes_newsletter (A customer has unsubscribed from the newsletter.)
- FALSE: delay_announced (A delay of a sailing has been announced.)
- FALSE: driver_declares_dangerous_goods (A driver has declared dangerous goods at check-in.)
- FALSE: fire_detector_alarm (A fire detector has raised an alarm.)
- FALSE: foot_passenger_boarding_begins (Boarding of foot passengers has begun.)
- found_item_unclaimed_days = 90 (The number of days a found item has been unclaimed.)
- group_passenger_count = 0 (The number of passengers in the group booking.)
- FALSE: kids_club_calls_parent (The kids' club has called a parent.)
- FALSE: kitchen_marks_order_ready (The kitchen has marked an order as ready.)
- FALSE: man_overboard_button_pressed (A crew member has pressed the man-overboard button.)
- minutes_from_arrival_port = 31 (The number of minutes the ship is from the arrival port.)
- minutes_from_film_start = 11 (The number of minutes from the film's start.)
- FALSE: operator_cancels_sailing (The operator has cancelled a sailing.)
- FALSE: parent_registers_child (A parent has registered a child for the kids' club.)
- FALSE: passenger_adds_pet (A passenger has added a pet to a booking.)
- FALSE: passenger_adds_vehicle (A passenger has added a vehicle to a booking.)
- FALSE: passenger_asks_for_delay_certificate (A passenger has asked for a delay certificate.)
- FALSE: passenger_asks_for_invoice (A passenger has asked for an invoice.)
- FALSE: passenger_asks_for_printed_ticket (A passenger has asked for a printed ticket at the port office.)
- FALSE: passenger_boards_ship (A passenger with a cabin booking has boarded the ship.)
- FALSE: passenger_books_cabin (A passenger is booking a cabin.)
- FALSE: passenger_books_cinema_seat (A passenger is booking a cinema seat.)
- FALSE: passenger_books_crossing (A passenger is booking a crossing.)
- FALSE: passenger_buys_alcohol (A passenger is buying alcohol in the shop.)
- FALSE: passenger_buys_wifi_pass (A passenger has bought a Wi-Fi pass.)
- FALSE: passenger_cancels_ticket (A passenger has cancelled a ticket.)
- FALSE: passenger_charges_to_cabin (A passenger has charged a shop purchase to the cabin.)
- FALSE: passenger_checks_in_pet (A passenger with a pet has checked in.)
- FALSE: passenger_connects_wifi (A passenger has connected to the onboard Wi-Fi.)
- FALSE: passenger_enters_discount_code (A passenger has entered a discount code.)
- FALSE: passenger_enters_door_code (A passenger has entered a door code at a cabin.)
- FALSE: passenger_has_booked_assistance (The passenger has booked assistance.)
- FALSE: passenger_has_priority_boarding (The passenger has priority boarding.)
- FALSE: passenger_leaves_ship (A passenger has left the ship.)
- FALSE: passenger_logs_in_wifi (A passenger has logged in to the Wi-Fi.)
- FALSE: passenger_moves_ticket (A passenger has moved a ticket to another sailing.)
- FALSE: passenger_orders_meal (A passenger has ordered a meal in the restaurant.)
- FALSE: passenger_orders_room_service (A passenger has ordered room service.)
- FALSE: passenger_orders_wake_up_call (A passenger has ordered a wake-up call.)
- FALSE: passenger_pays_by_card (A passenger is paying in the shop by bank card.)
- FALSE: passenger_pays_for_seat (A passenger has paid for a reserved seat.)
- FALSE: passenger_reports_fault (A passenger has reported a fault in a cabin.)
- FALSE: passenger_reports_lost_item (A passenger has reported a lost item.)
- FALSE: passenger_requests_assistance (A passenger has requested boarding assistance while booking.)
- FALSE: passenger_requests_crossing (A passenger has submitted a request to book a crossing.)
- FALSE: passenger_reserves_table (A passenger is reserving a restaurant table.)
- FALSE: passenger_scans_e_ticket (A passenger has scanned an e-ticket at the gate.)
- FALSE: passenger_writes_review (A passenger has written a review after the crossing.)
- product_stock_units = 5 (The stock of a product in the shop in units.)
- sailing_delay_minutes = 0 (The delay of a sailing in minutes.)
- seat_unpaid_minutes = 30 (The number of minutes a reserved seat has been unpaid.)
- shift_hours_worked = 12 (The number of hours a crew member has worked in one shift.)
- FALSE: ship_docked (The ship has docked at the arrival port.)
- FALSE: ship_enters_arrival_waters (The ship has entered the waters of the arrival country.)
- FALSE: shop_closes (The shop has closed.)
- FALSE: storm_warning_issued (The weather service has issued a storm warning for a route.)
- task_open_hours = 2 (The number of hours a housekeeping task has been open.)
- FALSE: vehicle_arrives_check_in (A vehicle has arrived at the check-in lane.)
- FALSE: vehicle_assigned_to_lane (The vehicle has been assigned to a boarding lane.)
- FALSE: vehicle_space_released (A vehicle space has been released.)
- FALSE: vehicle_unloaded (A vehicle has been unloaded at the arrival port.)

## 5. Gap: Missing rule for fourth wrong password

The requirements do not specify what the system must do when a customer enters a wrong password for the fourth time in a row. This gap appears in the situation where the customer has entered a wrong password and the count of consecutive wrong entries is 4, while no other triggering events are occurring.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for the fourth consecutive wrong password entry, leaving the account state and user feedback undefined.
- **B) Change:** Add a requirement stating that when a customer enters a wrong password for the fourth time in a row, the system shall keep the account locked or extend the lock duration.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: boarding_closes (Boarding has closed.)
- FALSE: car_deck_loading_begins (Loading of the car deck has begun.)
- consecutive_wrong_passwords = 4 (The number of consecutive wrong password entries.)
- FALSE: crew_registers_found_item (A crew member has registered a found item.)
- FALSE: crew_starts_shift (A crew member has started a shift.)
- FALSE: customer_changes_email (A customer has changed the email address of the account.)
- FALSE: customer_completes_crossing (A customer with an account has completed a crossing.)
- FALSE: customer_creates_account (A customer has created an account.)
- TRUE: customer_enters_wrong_password (A customer has entered a wrong password.)
- FALSE: customer_is_silver (The customer has silver status.)
- FALSE: customer_pays_with_points (A customer is paying with loyalty points.)
- FALSE: customer_subscribes_newsletter (A customer has subscribed to the newsletter.)
- FALSE: customer_unsubscribes_newsletter (A customer has unsubscribed from the newsletter.)
- FALSE: delay_announced (A delay of a sailing has been announced.)
- FALSE: driver_declares_dangerous_goods (A driver has declared dangerous goods at check-in.)
- FALSE: fire_detector_alarm (A fire detector has raised an alarm.)
- FALSE: foot_passenger_boarding_begins (Boarding of foot passengers has begun.)
- found_item_unclaimed_days = 90 (The number of days a found item has been unclaimed.)
- group_passenger_count = 0 (The number of passengers in the group booking.)
- FALSE: kids_club_calls_parent (The kids' club has called a parent.)
- FALSE: kitchen_marks_order_ready (The kitchen has marked an order as ready.)
- FALSE: man_overboard_button_pressed (A crew member has pressed the man-overboard button.)
- minutes_from_arrival_port = 31 (The number of minutes the ship is from the arrival port.)
- minutes_from_film_start = 11 (The number of minutes from the film's start.)
- FALSE: operator_cancels_sailing (The operator has cancelled a sailing.)
- FALSE: parent_registers_child (A parent has registered a child for the kids' club.)
- FALSE: passenger_adds_pet (A passenger has added a pet to a booking.)
- FALSE: passenger_adds_vehicle (A passenger has added a vehicle to a booking.)
- FALSE: passenger_asks_for_delay_certificate (A passenger has asked for a delay certificate.)
- FALSE: passenger_asks_for_invoice (A passenger has asked for an invoice.)
- FALSE: passenger_asks_for_printed_ticket (A passenger has asked for a printed ticket at the port office.)
- FALSE: passenger_boards_ship (A passenger with a cabin booking has boarded the ship.)
- FALSE: passenger_books_cabin (A passenger is booking a cabin.)
- FALSE: passenger_books_cinema_seat (A passenger is booking a cinema seat.)
- FALSE: passenger_books_crossing (A passenger is booking a crossing.)
- FALSE: passenger_buys_alcohol (A passenger is buying alcohol in the shop.)
- FALSE: passenger_buys_wifi_pass (A passenger has bought a Wi-Fi pass.)
- FALSE: passenger_cancels_ticket (A passenger has cancelled a ticket.)
- FALSE: passenger_charges_to_cabin (A passenger has charged a shop purchase to the cabin.)
- FALSE: passenger_checks_in_pet (A passenger with a pet has checked in.)
- FALSE: passenger_connects_wifi (A passenger has connected to the onboard Wi-Fi.)
- FALSE: passenger_enters_discount_code (A passenger has entered a discount code.)
- FALSE: passenger_enters_door_code (A passenger has entered a door code at a cabin.)
- FALSE: passenger_has_booked_assistance (The passenger has booked assistance.)
- FALSE: passenger_has_priority_boarding (The passenger has priority boarding.)
- FALSE: passenger_leaves_ship (A passenger has left the ship.)
- FALSE: passenger_logs_in_wifi (A passenger has logged in to the Wi-Fi.)
- FALSE: passenger_moves_ticket (A passenger has moved a ticket to another sailing.)
- FALSE: passenger_orders_meal (A passenger has ordered a meal in the restaurant.)
- FALSE: passenger_orders_room_service (A passenger has ordered room service.)
- FALSE: passenger_orders_wake_up_call (A passenger has ordered a wake-up call.)
- FALSE: passenger_pays_by_card (A passenger is paying in the shop by bank card.)
- FALSE: passenger_pays_for_seat (A passenger has paid for a reserved seat.)
- FALSE: passenger_reports_fault (A passenger has reported a fault in a cabin.)
- FALSE: passenger_reports_lost_item (A passenger has reported a lost item.)
- FALSE: passenger_requests_assistance (A passenger has requested boarding assistance while booking.)
- FALSE: passenger_requests_crossing (A passenger has submitted a request to book a crossing.)
- FALSE: passenger_reserves_table (A passenger is reserving a restaurant table.)
- FALSE: passenger_scans_e_ticket (A passenger has scanned an e-ticket at the gate.)
- FALSE: passenger_writes_review (A passenger has written a review after the crossing.)
- product_stock_units = 5 (The stock of a product in the shop in units.)
- sailing_delay_minutes = 0 (The delay of a sailing in minutes.)
- seat_unpaid_minutes = 30 (The number of minutes a reserved seat has been unpaid.)
- shift_hours_worked = 12 (The number of hours a crew member has worked in one shift.)
- FALSE: ship_docked (The ship has docked at the arrival port.)
- FALSE: ship_enters_arrival_waters (The ship has entered the waters of the arrival country.)
- FALSE: shop_closes (The shop has closed.)
- FALSE: storm_warning_issued (The weather service has issued a storm warning for a route.)
- task_open_hours = 2 (The number of hours a housekeeping task has been open.)
- FALSE: vehicle_arrives_check_in (A vehicle has arrived at the check-in lane.)
- FALSE: vehicle_assigned_to_lane (The vehicle has been assigned to a boarding lane.)
- FALSE: vehicle_space_released (A vehicle space has been released.)
- FALSE: vehicle_unloaded (A vehicle has been unloaded at the arrival port.)

## 6. Gap: Group discount threshold ambiguity

The requirements do not specify what the system must do when a group booking of exactly 10 passengers is paid. Requirement F11 states that a group discount is applied when a group booking of more than 10 passengers is paid, which implies that a group of exactly 10 passengers does not qualify for the discount. However, the term "group booking" is not explicitly defined by a minimum passenger count elsewhere, leaving it unclear if a booking of 10 is considered a group for other purposes or if the discount threshold is intended to be inclusive of 10.

- **A) Keep as-is:** Keeping the requirements as written means that a group booking of exactly 10 passengers will not receive the 10 percent group discount, as the condition "more than 10" is not met.
- **B) Change:** Change requirement F11 to state that the group discount is applied when a group booking of 10 or more passengers is paid.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: boarding_closes (Boarding has closed.)
- FALSE: car_deck_loading_begins (Loading of the car deck has begun.)
- FALSE: crew_registers_found_item (A crew member has registered a found item.)
- FALSE: crew_starts_shift (A crew member has started a shift.)
- FALSE: customer_changes_email (A customer has changed the email address of the account.)
- FALSE: customer_completes_crossing (A customer with an account has completed a crossing.)
- FALSE: customer_creates_account (A customer has created an account.)
- FALSE: customer_enters_wrong_password (A customer has entered a wrong password.)
- FALSE: customer_is_silver (The customer has silver status.)
- FALSE: customer_pays_with_points (A customer is paying with loyalty points.)
- FALSE: customer_subscribes_newsletter (A customer has subscribed to the newsletter.)
- FALSE: customer_unsubscribes_newsletter (A customer has unsubscribed from the newsletter.)
- FALSE: delay_announced (A delay of a sailing has been announced.)
- FALSE: driver_declares_dangerous_goods (A driver has declared dangerous goods at check-in.)
- FALSE: fire_detector_alarm (A fire detector has raised an alarm.)
- FALSE: foot_passenger_boarding_begins (Boarding of foot passengers has begun.)
- found_item_unclaimed_days = 90 (The number of days a found item has been unclaimed.)
- TRUE: group_booking_paid (A group booking has been paid.)
- group_passenger_count = 10 (The number of passengers in the group booking.)
- FALSE: kids_club_calls_parent (The kids' club has called a parent.)
- FALSE: kitchen_marks_order_ready (The kitchen has marked an order as ready.)
- FALSE: man_overboard_button_pressed (A crew member has pressed the man-overboard button.)
- minutes_from_arrival_port = 31 (The number of minutes the ship is from the arrival port.)
- minutes_from_film_start = 11 (The number of minutes from the film's start.)
- FALSE: operator_cancels_sailing (The operator has cancelled a sailing.)
- FALSE: parent_registers_child (A parent has registered a child for the kids' club.)
- FALSE: passenger_adds_pet (A passenger has added a pet to a booking.)
- FALSE: passenger_adds_vehicle (A passenger has added a vehicle to a booking.)
- FALSE: passenger_asks_for_delay_certificate (A passenger has asked for a delay certificate.)
- FALSE: passenger_asks_for_invoice (A passenger has asked for an invoice.)
- FALSE: passenger_asks_for_printed_ticket (A passenger has asked for a printed ticket at the port office.)
- FALSE: passenger_boards_ship (A passenger with a cabin booking has boarded the ship.)
- FALSE: passenger_books_cabin (A passenger is booking a cabin.)
- FALSE: passenger_books_cinema_seat (A passenger is booking a cinema seat.)
- FALSE: passenger_books_crossing (A passenger is booking a crossing.)
- FALSE: passenger_buys_alcohol (A passenger is buying alcohol in the shop.)
- FALSE: passenger_buys_wifi_pass (A passenger has bought a Wi-Fi pass.)
- FALSE: passenger_cancels_ticket (A passenger has cancelled a ticket.)
- FALSE: passenger_charges_to_cabin (A passenger has charged a shop purchase to the cabin.)
- FALSE: passenger_checks_in_pet (A passenger with a pet has checked in.)
- FALSE: passenger_connects_wifi (A passenger has connected to the onboard Wi-Fi.)
- FALSE: passenger_enters_discount_code (A passenger has entered a discount code.)
- FALSE: passenger_enters_door_code (A passenger has entered a door code at a cabin.)
- FALSE: passenger_has_booked_assistance (The passenger has booked assistance.)
- FALSE: passenger_has_priority_boarding (The passenger has priority boarding.)
- FALSE: passenger_leaves_ship (A passenger has left the ship.)
- FALSE: passenger_logs_in_wifi (A passenger has logged in to the Wi-Fi.)
- FALSE: passenger_moves_ticket (A passenger has moved a ticket to another sailing.)
- FALSE: passenger_orders_meal (A passenger has ordered a meal in the restaurant.)
- FALSE: passenger_orders_room_service (A passenger has ordered room service.)
- FALSE: passenger_orders_wake_up_call (A passenger has ordered a wake-up call.)
- FALSE: passenger_pays_by_card (A passenger is paying in the shop by bank card.)
- FALSE: passenger_pays_for_seat (A passenger has paid for a reserved seat.)
- FALSE: passenger_reports_fault (A passenger has reported a fault in a cabin.)
- FALSE: passenger_reports_lost_item (A passenger has reported a lost item.)
- FALSE: passenger_requests_assistance (A passenger has requested boarding assistance while booking.)
- FALSE: passenger_requests_crossing (A passenger has submitted a request to book a crossing.)
- FALSE: passenger_reserves_table (A passenger is reserving a restaurant table.)
- FALSE: passenger_scans_e_ticket (A passenger has scanned an e-ticket at the gate.)
- FALSE: passenger_writes_review (A passenger has written a review after the crossing.)
- product_stock_units = 5 (The stock of a product in the shop in units.)
- sailing_delay_minutes = 0 (The delay of a sailing in minutes.)
- seat_unpaid_minutes = 30 (The number of minutes a reserved seat has been unpaid.)
- shift_hours_worked = 12 (The number of hours a crew member has worked in one shift.)
- FALSE: ship_docked (The ship has docked at the arrival port.)
- FALSE: ship_enters_arrival_waters (The ship has entered the waters of the arrival country.)
- FALSE: shop_closes (The shop has closed.)
- FALSE: storm_warning_issued (The weather service has issued a storm warning for a route.)
- task_open_hours = 2 (The number of hours a housekeeping task has been open.)
- FALSE: vehicle_arrives_check_in (A vehicle has arrived at the check-in lane.)
- FALSE: vehicle_assigned_to_lane (The vehicle has been assigned to a boarding lane.)
- FALSE: vehicle_space_released (A vehicle space has been released.)
- FALSE: vehicle_unloaded (A vehicle has been unloaded at the arrival port.)

## 7. Gap: Unspecified behavior upon terminal arrival

The requirements do not specify what the system must do when a passenger arrives at the terminal, provided that no other triggering events or conditions are active. This gap appears in the situation where a passenger has arrived at the terminal, but boarding has not closed, no other passenger actions or system events have occurred, and all other specific conditions are false or at their neutral values.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined action to take when a passenger arrives at the terminal in the absence of other specific triggers.
- **B) Change:** Add a requirement stating that when a passenger arrives at the terminal, the system shall log the arrival time and update the passenger's status to 'present'.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: boarding_closes (Boarding has closed.)
- FALSE: car_deck_loading_begins (Loading of the car deck has begun.)
- FALSE: crew_registers_found_item (A crew member has registered a found item.)
- FALSE: crew_starts_shift (A crew member has started a shift.)
- FALSE: customer_changes_email (A customer has changed the email address of the account.)
- FALSE: customer_completes_crossing (A customer with an account has completed a crossing.)
- FALSE: customer_creates_account (A customer has created an account.)
- FALSE: customer_enters_wrong_password (A customer has entered a wrong password.)
- FALSE: customer_is_silver (The customer has silver status.)
- FALSE: customer_pays_with_points (A customer is paying with loyalty points.)
- FALSE: customer_subscribes_newsletter (A customer has subscribed to the newsletter.)
- FALSE: customer_unsubscribes_newsletter (A customer has unsubscribed from the newsletter.)
- FALSE: delay_announced (A delay of a sailing has been announced.)
- FALSE: driver_declares_dangerous_goods (A driver has declared dangerous goods at check-in.)
- FALSE: fire_detector_alarm (A fire detector has raised an alarm.)
- FALSE: foot_passenger_boarding_begins (Boarding of foot passengers has begun.)
- found_item_unclaimed_days = 90 (The number of days a found item has been unclaimed.)
- group_passenger_count = 0 (The number of passengers in the group booking.)
- FALSE: kids_club_calls_parent (The kids' club has called a parent.)
- FALSE: kitchen_marks_order_ready (The kitchen has marked an order as ready.)
- FALSE: man_overboard_button_pressed (A crew member has pressed the man-overboard button.)
- minutes_from_arrival_port = 31 (The number of minutes the ship is from the arrival port.)
- minutes_from_film_start = 11 (The number of minutes from the film's start.)
- FALSE: operator_cancels_sailing (The operator has cancelled a sailing.)
- FALSE: parent_registers_child (A parent has registered a child for the kids' club.)
- FALSE: passenger_adds_pet (A passenger has added a pet to a booking.)
- FALSE: passenger_adds_vehicle (A passenger has added a vehicle to a booking.)
- TRUE: passenger_arrives_terminal (A passenger has arrived at the terminal.)
- FALSE: passenger_asks_for_delay_certificate (A passenger has asked for a delay certificate.)
- FALSE: passenger_asks_for_invoice (A passenger has asked for an invoice.)
- FALSE: passenger_asks_for_printed_ticket (A passenger has asked for a printed ticket at the port office.)
- FALSE: passenger_boards_ship (A passenger with a cabin booking has boarded the ship.)
- FALSE: passenger_books_cabin (A passenger is booking a cabin.)
- FALSE: passenger_books_cinema_seat (A passenger is booking a cinema seat.)
- FALSE: passenger_books_crossing (A passenger is booking a crossing.)
- FALSE: passenger_buys_alcohol (A passenger is buying alcohol in the shop.)
- FALSE: passenger_buys_wifi_pass (A passenger has bought a Wi-Fi pass.)
- FALSE: passenger_cancels_ticket (A passenger has cancelled a ticket.)
- FALSE: passenger_charges_to_cabin (A passenger has charged a shop purchase to the cabin.)
- FALSE: passenger_checks_in_pet (A passenger with a pet has checked in.)
- FALSE: passenger_connects_wifi (A passenger has connected to the onboard Wi-Fi.)
- FALSE: passenger_enters_discount_code (A passenger has entered a discount code.)
- FALSE: passenger_enters_door_code (A passenger has entered a door code at a cabin.)
- FALSE: passenger_has_booked_assistance (The passenger has booked assistance.)
- FALSE: passenger_has_priority_boarding (The passenger has priority boarding.)
- FALSE: passenger_leaves_ship (A passenger has left the ship.)
- FALSE: passenger_logs_in_wifi (A passenger has logged in to the Wi-Fi.)
- FALSE: passenger_moves_ticket (A passenger has moved a ticket to another sailing.)
- FALSE: passenger_orders_meal (A passenger has ordered a meal in the restaurant.)
- FALSE: passenger_orders_room_service (A passenger has ordered room service.)
- FALSE: passenger_orders_wake_up_call (A passenger has ordered a wake-up call.)
- FALSE: passenger_pays_by_card (A passenger is paying in the shop by bank card.)
- FALSE: passenger_pays_for_seat (A passenger has paid for a reserved seat.)
- FALSE: passenger_reports_fault (A passenger has reported a fault in a cabin.)
- FALSE: passenger_reports_lost_item (A passenger has reported a lost item.)
- FALSE: passenger_requests_assistance (A passenger has requested boarding assistance while booking.)
- FALSE: passenger_requests_crossing (A passenger has submitted a request to book a crossing.)
- FALSE: passenger_reserves_table (A passenger is reserving a restaurant table.)
- FALSE: passenger_scans_e_ticket (A passenger has scanned an e-ticket at the gate.)
- FALSE: passenger_writes_review (A passenger has written a review after the crossing.)
- product_stock_units = 5 (The stock of a product in the shop in units.)
- sailing_delay_minutes = 0 (The delay of a sailing in minutes.)
- seat_unpaid_minutes = 30 (The number of minutes a reserved seat has been unpaid.)
- shift_hours_worked = 12 (The number of hours a crew member has worked in one shift.)
- FALSE: ship_docked (The ship has docked at the arrival port.)
- FALSE: ship_enters_arrival_waters (The ship has entered the waters of the arrival country.)
- FALSE: shop_closes (The shop has closed.)
- FALSE: storm_warning_issued (The weather service has issued a storm warning for a route.)
- task_open_hours = 2 (The number of hours a housekeeping task has been open.)
- FALSE: vehicle_arrives_check_in (A vehicle has arrived at the check-in lane.)
- FALSE: vehicle_assigned_to_lane (The vehicle has been assigned to a boarding lane.)
- FALSE: vehicle_space_released (A vehicle space has been released.)
- FALSE: vehicle_unloaded (A vehicle has been unloaded at the arrival port.)

## 8. Gap: Missing rule for booking a crossing without a request

The requirements do not specify what the system must do when a passenger is in the state of booking a crossing but has not actually submitted a request to book a crossing. This situation is a gap because F1 and F2 only trigger when a passenger requests a crossing, yet the system is described as being in a booking state without that request having occurred.

- **A) Keep as-is:** Keeping the requirements as written means the system has no defined behavior for a passenger who is in a booking state but has not submitted a crossing request.
- **B) Change:** Add a requirement stating that when a passenger is in a booking state but has not submitted a crossing request, the system shall prompt the passenger to submit a request or return to the main menu.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: boarding_closes (Boarding has closed.)
- FALSE: car_deck_loading_begins (Loading of the car deck has begun.)
- child_age_years = 4 (The age of the child in years.)
- FALSE: crew_registers_found_item (A crew member has registered a found item.)
- FALSE: crew_starts_shift (A crew member has started a shift.)
- FALSE: customer_changes_email (A customer has changed the email address of the account.)
- FALSE: customer_completes_crossing (A customer with an account has completed a crossing.)
- FALSE: customer_creates_account (A customer has created an account.)
- FALSE: customer_enters_wrong_password (A customer has entered a wrong password.)
- FALSE: customer_is_silver (The customer has silver status.)
- FALSE: customer_pays_with_points (A customer is paying with loyalty points.)
- FALSE: customer_subscribes_newsletter (A customer has subscribed to the newsletter.)
- FALSE: customer_unsubscribes_newsletter (A customer has unsubscribed from the newsletter.)
- FALSE: delay_announced (A delay of a sailing has been announced.)
- FALSE: driver_declares_dangerous_goods (A driver has declared dangerous goods at check-in.)
- FALSE: fire_detector_alarm (A fire detector has raised an alarm.)
- FALSE: foot_passenger_boarding_begins (Boarding of foot passengers has begun.)
- found_item_unclaimed_days = 90 (The number of days a found item has been unclaimed.)
- group_passenger_count = 0 (The number of passengers in the group booking.)
- FALSE: kids_club_calls_parent (The kids' club has called a parent.)
- FALSE: kitchen_marks_order_ready (The kitchen has marked an order as ready.)
- FALSE: man_overboard_button_pressed (A crew member has pressed the man-overboard button.)
- minutes_from_arrival_port = 31 (The number of minutes the ship is from the arrival port.)
- minutes_from_film_start = 11 (The number of minutes from the film's start.)
- FALSE: operator_cancels_sailing (The operator has cancelled a sailing.)
- FALSE: parent_registers_child (A parent has registered a child for the kids' club.)
- FALSE: passenger_adds_pet (A passenger has added a pet to a booking.)
- FALSE: passenger_adds_vehicle (A passenger has added a vehicle to a booking.)
- FALSE: passenger_asks_for_delay_certificate (A passenger has asked for a delay certificate.)
- FALSE: passenger_asks_for_invoice (A passenger has asked for an invoice.)
- FALSE: passenger_asks_for_printed_ticket (A passenger has asked for a printed ticket at the port office.)
- FALSE: passenger_boards_ship (A passenger with a cabin booking has boarded the ship.)
- FALSE: passenger_books_cabin (A passenger is booking a cabin.)
- FALSE: passenger_books_cinema_seat (A passenger is booking a cinema seat.)
- TRUE: passenger_books_crossing (A passenger is booking a crossing.)
- FALSE: passenger_buys_alcohol (A passenger is buying alcohol in the shop.)
- FALSE: passenger_buys_wifi_pass (A passenger has bought a Wi-Fi pass.)
- FALSE: passenger_cancels_ticket (A passenger has cancelled a ticket.)
- FALSE: passenger_charges_to_cabin (A passenger has charged a shop purchase to the cabin.)
- FALSE: passenger_checks_in_pet (A passenger with a pet has checked in.)
- FALSE: passenger_connects_wifi (A passenger has connected to the onboard Wi-Fi.)
- FALSE: passenger_enters_discount_code (A passenger has entered a discount code.)
- FALSE: passenger_enters_door_code (A passenger has entered a door code at a cabin.)
- FALSE: passenger_has_booked_assistance (The passenger has booked assistance.)
- FALSE: passenger_has_priority_boarding (The passenger has priority boarding.)
- FALSE: passenger_leaves_ship (A passenger has left the ship.)
- FALSE: passenger_logs_in_wifi (A passenger has logged in to the Wi-Fi.)
- FALSE: passenger_moves_ticket (A passenger has moved a ticket to another sailing.)
- FALSE: passenger_orders_meal (A passenger has ordered a meal in the restaurant.)
- FALSE: passenger_orders_room_service (A passenger has ordered room service.)
- FALSE: passenger_orders_wake_up_call (A passenger has ordered a wake-up call.)
- FALSE: passenger_pays_by_card (A passenger is paying in the shop by bank card.)
- FALSE: passenger_pays_for_seat (A passenger has paid for a reserved seat.)
- FALSE: passenger_reports_fault (A passenger has reported a fault in a cabin.)
- FALSE: passenger_reports_lost_item (A passenger has reported a lost item.)
- FALSE: passenger_requests_assistance (A passenger has requested boarding assistance while booking.)
- FALSE: passenger_requests_crossing (A passenger has submitted a request to book a crossing.)
- FALSE: passenger_reserves_table (A passenger is reserving a restaurant table.)
- FALSE: passenger_scans_e_ticket (A passenger has scanned an e-ticket at the gate.)
- FALSE: passenger_writes_review (A passenger has written a review after the crossing.)
- product_stock_units = 5 (The stock of a product in the shop in units.)
- sailing_delay_minutes = 0 (The delay of a sailing in minutes.)
- seat_unpaid_minutes = 30 (The number of minutes a reserved seat has been unpaid.)
- shift_hours_worked = 12 (The number of hours a crew member has worked in one shift.)
- FALSE: ship_docked (The ship has docked at the arrival port.)
- FALSE: ship_enters_arrival_waters (The ship has entered the waters of the arrival country.)
- FALSE: shop_closes (The shop has closed.)
- FALSE: storm_warning_issued (The weather service has issued a storm warning for a route.)
- task_open_hours = 2 (The number of hours a housekeeping task has been open.)
- FALSE: vehicle_arrives_check_in (A vehicle has arrived at the check-in lane.)
- FALSE: vehicle_assigned_to_lane (The vehicle has been assigned to a boarding lane.)
- FALSE: vehicle_space_released (A vehicle space has been released.)
- FALSE: vehicle_unloaded (A vehicle has been unloaded at the arrival port.)

## 9. Gap (no event happens): Idle System State

The requirements do not specify any action for the system when it is in a state where no triggering events are occurring and no conditions are met to initiate a process. This situation represents a period of inactivity where the system is simply waiting for the next user interaction or system event.

- **A) Keep as-is:** Keeping the requirements as written means the system will remain idle and perform no actions until a specific event or condition defined in the requirements occurs.
- **B) Change:** Add a requirement stating that the system shall maintain its current state and monitor for new events while no specific triggers are active.

*Proven:* No requirement says what the system must do in this situation:
- FALSE: boarding_closes (Boarding has closed.)
- FALSE: car_deck_loading_begins (Loading of the car deck has begun.)
- FALSE: crew_registers_found_item (A crew member has registered a found item.)
- FALSE: crew_starts_shift (A crew member has started a shift.)
- FALSE: customer_books_crossing (A customer is booking a crossing.)
- FALSE: customer_changes_email (A customer has changed the email address of the account.)
- FALSE: customer_completes_crossing (A customer with an account has completed a crossing.)
- FALSE: customer_creates_account (A customer has created an account.)
- FALSE: customer_enters_wrong_password (A customer has entered a wrong password.)
- FALSE: customer_pays_with_points (A customer is paying with loyalty points.)
- FALSE: customer_subscribes_newsletter (A customer has subscribed to the newsletter.)
- FALSE: customer_unsubscribes_newsletter (A customer has unsubscribed from the newsletter.)
- FALSE: delay_announced (A delay of a sailing has been announced.)
- FALSE: driver_declares_dangerous_goods (A driver has declared dangerous goods at check-in.)
- FALSE: fire_detector_alarm (A fire detector has raised an alarm.)
- FALSE: foot_passenger_boarding_begins (Boarding of foot passengers has begun.)
- found_item_unclaimed_days = 90 (The number of days a found item has been unclaimed.)
- FALSE: group_booking_paid (A group booking has been paid.)
- FALSE: kids_club_calls_parent (The kids' club has called a parent.)
- FALSE: kitchen_marks_order_ready (The kitchen has marked an order as ready.)
- FALSE: man_overboard_button_pressed (A crew member has pressed the man-overboard button.)
- minutes_from_arrival_port = 31 (The number of minutes the ship is from the arrival port.)
- minutes_from_film_start = 11 (The number of minutes from the film's start.)
- FALSE: operator_cancels_sailing (The operator has cancelled a sailing.)
- FALSE: parent_registers_child (A parent has registered a child for the kids' club.)
- FALSE: passenger_adds_pet (A passenger has added a pet to a booking.)
- FALSE: passenger_adds_vehicle (A passenger has added a vehicle to a booking.)
- FALSE: passenger_arrives_terminal (A passenger has arrived at the terminal.)
- FALSE: passenger_asks_for_delay_certificate (A passenger has asked for a delay certificate.)
- FALSE: passenger_asks_for_invoice (A passenger has asked for an invoice.)
- FALSE: passenger_asks_for_printed_ticket (A passenger has asked for a printed ticket at the port office.)
- FALSE: passenger_boards_ship (A passenger with a cabin booking has boarded the ship.)
- FALSE: passenger_books_cabin (A passenger is booking a cabin.)
- FALSE: passenger_books_cinema_seat (A passenger is booking a cinema seat.)
- FALSE: passenger_books_crossing (A passenger is booking a crossing.)
- FALSE: passenger_buys_alcohol (A passenger is buying alcohol in the shop.)
- FALSE: passenger_buys_wifi_pass (A passenger has bought a Wi-Fi pass.)
- FALSE: passenger_cancels_ticket (A passenger has cancelled a ticket.)
- FALSE: passenger_charges_to_cabin (A passenger has charged a shop purchase to the cabin.)
- FALSE: passenger_checks_in_pet (A passenger with a pet has checked in.)
- FALSE: passenger_connects_wifi (A passenger has connected to the onboard Wi-Fi.)
- FALSE: passenger_enters_discount_code (A passenger has entered a discount code.)
- FALSE: passenger_enters_door_code (A passenger has entered a door code at a cabin.)
- FALSE: passenger_leaves_ship (A passenger has left the ship.)
- FALSE: passenger_logs_in_wifi (A passenger has logged in to the Wi-Fi.)
- FALSE: passenger_moves_ticket (A passenger has moved a ticket to another sailing.)
- FALSE: passenger_orders_meal (A passenger has ordered a meal in the restaurant.)
- FALSE: passenger_orders_room_service (A passenger has ordered room service.)
- FALSE: passenger_orders_wake_up_call (A passenger has ordered a wake-up call.)
- FALSE: passenger_pays_by_card (A passenger is paying in the shop by bank card.)
- FALSE: passenger_pays_for_seat (A passenger has paid for a reserved seat.)
- FALSE: passenger_reports_fault (A passenger has reported a fault in a cabin.)
- FALSE: passenger_reports_lost_item (A passenger has reported a lost item.)
- FALSE: passenger_requests_assistance (A passenger has requested boarding assistance while booking.)
- FALSE: passenger_requests_crossing (A passenger has submitted a request to book a crossing.)
- FALSE: passenger_reserves_table (A passenger is reserving a restaurant table.)
- FALSE: passenger_scans_e_ticket (A passenger has scanned an e-ticket at the gate.)
- FALSE: passenger_writes_review (A passenger has written a review after the crossing.)
- product_stock_units = 5 (The stock of a product in the shop in units.)
- sailing_delay_minutes = 0 (The delay of a sailing in minutes.)
- seat_unpaid_minutes = 30 (The number of minutes a reserved seat has been unpaid.)
- shift_hours_worked = 12 (The number of hours a crew member has worked in one shift.)
- FALSE: ship_docked (The ship has docked at the arrival port.)
- FALSE: ship_enters_arrival_waters (The ship has entered the waters of the arrival country.)
- FALSE: shop_closes (The shop has closed.)
- FALSE: storm_warning_issued (The weather service has issued a storm warning for a route.)
- task_open_hours = 2 (The number of hours a housekeeping task has been open.)
- FALSE: vehicle_arrives_check_in (A vehicle has arrived at the check-in lane.)
- FALSE: vehicle_assigned_to_lane (The vehicle has been assigned to a boarding lane.)
- FALSE: vehicle_space_released (A vehicle space has been released.)
- FALSE: vehicle_unloaded (A vehicle has been unloaded at the arrival port.)
No event happens in this situation, so this may only mean that the system waits.

## 10. Scenario, allowed: Gate opens without valid scan

Requirement F26 states that the gate shall open only when a passenger scans an e-ticket that is valid for the next sailing. The proven behaviour shows the gate opening in a situation where neither a scan occurred nor was the ticket valid, which directly contradicts the security and access control purpose of the requirement. This allows unauthorized boarding, which is clearly against the goal of managing passenger access safely.

- **A) Keep as-is:** Keep the requirements, so the behaviour stays allowed.
- **B) Change:** Modify Requirement F26 to explicitly state that the gate shall remain closed unless a valid e-ticket scan for the next sailing is detected.

*Proven:* The requirements allow this behaviour:
- TRUE: gate_opened (The gate has been opened.)
- FALSE: passenger_scans_e_ticket (A passenger has scanned an e-ticket at the gate.)
- FALSE: ticket_valid_for_next_sailing (The ticket is valid for the next sailing.)
Requirement F26 does not apply in it, and yet what F26 demands is the case.

## 11. Scenario, allowed: Cabin door unlocked without code entry

The requirements state that a cabin door is only unlocked when a passenger enters the correct door code (F37). However, the system allows the door to be unlocked even when no passenger has entered a code and the code is not correct. This defeats the purpose of the door code security measure, as it allows unauthorized access to the cabin.

- **A) Keep as-is:** Keep the requirements, so the behaviour stays allowed.
- **B) Change:** Add a requirement that the cabin door SHALL remain locked unless a passenger enters the correct door code.

*Proven:* The requirements allow this behaviour:
- TRUE: cabin_door_unlocked (The cabin door has been unlocked.)
- FALSE: door_code_correct (The entered door code is correct.)
- FALSE: passenger_enters_door_code (A passenger has entered a door code at a cabin.)
Requirement F37 does not apply in it, and yet what F37 demands is the case.

## 12. Scenario, allowed: Pet fee charged without pet

Requirement F68 states that the pet fee is added to the fare when a passenger adds a pet to a booking. The logic solver proved that the requirements allow the pet fee to be added to the fare even when no pet has been added to the booking. This is clearly against the goal of the requirement, which is to charge the fee only when a pet is actually part of the booking.

- **A) Keep as-is:** Keep the requirements, so the behaviour of adding a pet fee without a pet remains allowed.
- **B) Change:** Change requirement F68 to explicitly state that the pet fee SHALL NOT be added to the fare unless a pet has been added to the booking.

*Proven:* The requirements allow this behaviour:
- FALSE: passenger_adds_pet (A passenger has added a pet to a booking.)
- TRUE: pet_fee_added (The pet fee has been added to the fare.)
Requirement F68 does not apply in it, and yet what F68 demands is the case.
