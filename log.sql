-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Shows the formatting of the database
.schema

-- Outputs all of the crime scene reports on July 28th 2021
-- which took place on Humprey Street
SELECT *
FROM crime_scene_reports
WHERE year = "2021"
AND month = "7"
AND day = "28"
AND street = "Humphrey Street";

------ RESULT:
---- Description of crime 1 in the database is:
-- Theft of the CS50 duck took place at 10:15am
-- at the Humphrey Street bakery. Interviews were
-- conducted today with three witnesses who were present
-- at the time – each of their interview transcripts
-- mentions the bakery.

---- Description of crime 2 in the database is:
-- Littering took place at 16:36. No known witnesses.

-- Gets the transcripts of the interviews
SELECT name, transcript
FROM interviews
WHERE year = "2021"
AND month = "7"
AND day = "28"
AND transcript LIKE "%bakery%";

------ RESULT:
---- Transscript of the interview of Ruth:
-- Sometime within ten minutes of the theft, I saw the
-- thief get into a car in the bakery parking lot and
-- drive away. If you have security footage from the bakery
-- parking lot, you might want to look for cars that left the
-- parking lot in that time frame.

---- Transscript of the interview of Eugene:
-- I don't know the thief's name, but it was someone I
-- recognized. Earlier this morning, before I arrived at
-- Emma's bakery, I was walking by the ATM on Leggett Street
-- and saw the thief there withdrawing some money.

---- Transscript of the interview of Raymond:
-- As the thief was leaving the bakery, they called
-- someone who talked to them for less than a minute.
-- In the call, I heard the thief say that they were
-- planning to take the earliest flight out of Fiftyville
-- tomorrow. The thief then asked the person on the other
-- end of the phone to purchase the flight ticket.

-- Gets the bakerys security footage of the timeframe
-- of ten minutes after the theft
SELECT activity, license_plate
FROM bakery_security_logs
WHERE year = "2021"
AND month = "7"
AND day = "28"
AND hour = "10"
AND minute >= "15"
AND minute <= "25";

---- RESULT:
-- +----------+---------------+
-- | activity | license_plate |
-- +----------+---------------+
-- | exit     | 5P2BI95       |
-- | exit     | 94KL13X       |
-- | exit     | 6P58WS2       |
-- | exit     | 4328GD8       |
-- | exit     | G412CB7       |
-- | exit     | L93JTIZ       |
-- | exit     | 322W7JE       |
-- | exit     | 0NTHK55       |
-- +----------+---------------+

-- Gets the names of the owners of the
-- cars leaving the parking lot in the timeframe
SELECT people.name
FROM people
INNER JOIN bakery_security_logs
ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = "2021"
AND bakery_security_logs.month = "7"
AND bakery_security_logs.day = "28"
AND bakery_security_logs.hour = "10"
AND bakery_security_logs.minute >= "15"
AND bakery_security_logs.minute <= "25";

---- RESULT:
-- +---------+
-- |  name   |
-- +---------+
-- | Vanessa |
-- | Bruce   |
-- | Barry   |
-- | Luca    |
-- | Sofia   |
-- | Iman    |
-- | Diana   |
-- | Kelsey  |
-- +---------+

-- Checks if there are any names who made an atm transaction
-- and whos car left the parking lot at the given time and date
SELECT people.name, atm_transactions.transaction_type, atm_transactions.amount
FROM people
INNER JOIN bank_accounts
ON people.id = bank_accounts.person_id
INNER JOIN atm_transactions
ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = "2021"
AND atm_transactions.month = "7"
AND atm_transactions.day = "28"
AND atm_transactions.atm_location = "Leggett Street"
AND people.id IN (
    SELECT people.id
    FROM people
    INNER JOIN bakery_security_logs
    ON bakery_security_logs.license_plate = people.license_plate
    WHERE bakery_security_logs.year = "2021"
    AND bakery_security_logs.month = "7"
    AND bakery_security_logs.day = "28"
    AND bakery_security_logs.hour = "10"
    AND bakery_security_logs.minute >= "15"
    AND bakery_security_logs.minute <= "25"
);

------ RESULT:
-- +-------+------------------+--------+
-- | name  | transaction_type | amount |
-- +-------+------------------+--------+
-- | Bruce | withdraw         | 50     |
-- | Diana | withdraw         | 35     |
-- | Iman  | withdraw         | 20     |
-- | Luca  | withdraw         | 48     |
-- +-------+------------------+--------+

-- Gets the caller and receiver of the phone
-- call which took place at 10:15 for less than a minute
SELECT phone_calls.caller, phone_calls.receiver
FROM phone_calls
WHERE phone_calls.year = "2021"
AND phone_calls.month = "7"
AND phone_calls.day = "28"
AND phone_calls.duration < 60;

-- Gets the name of the person who withdrawed money
-- at the atm, owns the car which left at the timestamp,
-- and called for less than a minute on the 28 July of 2021
SELECT people.name
FROM people
WHERE people.id IN (
    SELECT people.id
    FROM people
    INNER JOIN bank_accounts
    ON people.id = bank_accounts.person_id
    INNER JOIN atm_transactions
    ON bank_accounts.account_number = atm_transactions.account_number
    WHERE atm_transactions.year = "2021"
    AND atm_transactions.month = "7"
    AND atm_transactions.day = "28"
    AND atm_transactions.atm_location = "Leggett Street"
    AND people.id IN (
        SELECT people.id
        FROM people
        INNER JOIN bakery_security_logs
        ON bakery_security_logs.license_plate = people.license_plate
        WHERE bakery_security_logs.year = "2021"
        AND bakery_security_logs.month = "7"
        AND bakery_security_logs.day = "28"
        AND bakery_security_logs.hour = "10"
        AND bakery_security_logs.minute >= "15"
        AND bakery_security_logs.minute <= "25"
    )
)
AND people.id IN (
    SELECT people.id
    FROM people
    WHERE people.phone_number IN (
        SELECT phone_calls.caller
        FROM phone_calls
        WHERE phone_calls.year = "2021"
        AND phone_calls.month = "7"
        AND phone_calls.day = "28"
        AND phone_calls.duration < 60
    )
);

------ RESULT:
-- +-------+
-- | name  |
-- +-------+
-- | Diana |
-- | Bruce |
-- +-------+

-- Gets the flights id that leaves the earliest on
-- 29th July 2021 from fiftyville
SELECT id
FROM flights
WHERE year = "2021"
AND month = "7"
AND day = "29"
AND origin_airport_id IN (
    SELECT id
    FROM airports
    WHERE city = "Fiftyville"
)
ORDER BY hour, minute ASC
LIMIT 1;

---- RESULT: Flight id = 36

-- Gets the passengers on flight id = 36
SELECT name
FROM people
INNER JOIN passengers
ON people.passport_number = passengers.passport_number
WHERE passengers.flight_id = (
    SELECT id
    FROM flights
    WHERE year = "2021"
    AND month = "7"
    AND day = "29"
    AND origin_airport_id IN (
        SELECT id
        FROM airports
        WHERE city = "Fiftyville"
    )
    ORDER BY hour, minute ASC
    LIMIT 1
);

------ RESULT:
-- +--------+
-- |  name  |
-- +--------+
-- | Doris  |
-- | Sofia  |
-- | Bruce  |
-- | Edward |
-- | Kelsey |
-- | Taylor |
-- | Kenny  |
-- | Luca   |
-- +--------+


-- Gets the name of the person who withdrawed money
-- at the atm, owns the car which left at the timestamp,
-- and called for less than a minute on the 28 July of 2021
-- and is on the first flight out of Fiftyville on the 29th

SELECT name
FROM people
WHERE people.id IN (
    SELECT people.id
    FROM people
    WHERE people.id IN (
        SELECT people.id
        FROM people
        INNER JOIN bank_accounts
        ON people.id = bank_accounts.person_id
        INNER JOIN atm_transactions
        ON bank_accounts.account_number = atm_transactions.account_number
        WHERE atm_transactions.year = "2021"
        AND atm_transactions.month = "7"
        AND atm_transactions.day = "28"
        AND atm_transactions.atm_location = "Leggett Street"
        AND people.id IN (
            SELECT people.id
            FROM people
            INNER JOIN bakery_security_logs
            ON bakery_security_logs.license_plate = people.license_plate
            WHERE bakery_security_logs.year = "2021"
            AND bakery_security_logs.month = "7"
            AND bakery_security_logs.day = "28"
            AND bakery_security_logs.hour = "10"
            AND bakery_security_logs.minute >= "15"
            AND bakery_security_logs.minute <= "25"
        )
    )
    AND people.id IN (
        SELECT people.id
        FROM people
        WHERE people.phone_number IN (
            SELECT phone_calls.caller
            FROM phone_calls
            WHERE phone_calls.year = "2021"
            AND phone_calls.month = "7"
            AND phone_calls.day = "28"
            AND phone_calls.duration < 60
        )
    )
)
AND people.id IN (
    SELECT id
    FROM people
    INNER JOIN passengers
    ON people.passport_number = passengers.passport_number
    WHERE passengers.flight_id = (
        SELECT id
        FROM flights
        WHERE year = "2021"
        AND month = "7"
        AND day = "29"
        AND origin_airport_id IN (
            SELECT id
            FROM airports
            WHERE city = "Fiftyville"
        )
        ORDER BY hour, minute ASC
        LIMIT 1
    )
);

--- RESULT: Bruce
-- SO: Bruce is the thief

-- Gets the destination of the first flight out of Fifthyville on the 29th
SELECT city
FROM airports
WHERE airports.id IN (
    SELECT destination_airport_id
    FROM flights
    WHERE year = "2021"
    AND month = "7"
    AND day = "29"
    AND origin_airport_id IN (
        SELECT id
        FROM airports
        WHERE city = "Fiftyville"
    )
    ORDER BY hour, minute ASC
    LIMIT 1
);

-- Gets the accomplice's name by checking
-- whos the receiver of the phone call
SELECT name
FROM people
INNER JOIN phone_calls
ON people.phone_number = phone_calls.receiver
WHERE phone_calls.caller = (
    SELECT phone_number
    FROM people
    WHERE people.id IN (
        SELECT people.id
        FROM people
        WHERE people.id IN (
            SELECT people.id
            FROM people
            INNER JOIN bank_accounts
            ON people.id = bank_accounts.person_id
            INNER JOIN atm_transactions
            ON bank_accounts.account_number = atm_transactions.account_number
            WHERE atm_transactions.year = "2021"
            AND atm_transactions.month = "7"
            AND atm_transactions.day = "28"
            AND atm_transactions.atm_location = "Leggett Street"
            AND people.id IN (
                SELECT people.id
                FROM people
                INNER JOIN bakery_security_logs
                ON bakery_security_logs.license_plate = people.license_plate
                WHERE bakery_security_logs.year = "2021"
                AND bakery_security_logs.month = "7"
                AND bakery_security_logs.day = "28"
                AND bakery_security_logs.hour = "10"
                AND bakery_security_logs.minute >= "15"
                AND bakery_security_logs.minute <= "25"
            )
        )
        AND people.id IN (
            SELECT people.id
            FROM people
            WHERE people.phone_number IN (
                SELECT phone_calls.caller
                FROM phone_calls
                WHERE phone_calls.year = "2021"
                AND phone_calls.month = "7"
                AND phone_calls.day = "28"
                AND phone_calls.duration < 60
            )
        )
    )
    AND people.id IN (
        SELECT id
        FROM people
        INNER JOIN passengers
        ON people.passport_number = passengers.passport_number
        WHERE passengers.flight_id = (
            SELECT id
            FROM flights
            WHERE year = "2021"
            AND month = "7"
            AND day = "29"
            AND origin_airport_id IN (
                SELECT id
                FROM airports
                WHERE city = "Fiftyville"
            )
            ORDER BY hour, minute ASC
            LIMIT 1
        )
    )
)
AND phone_calls.year = "2021"
AND phone_calls.month = "7"
AND phone_calls.day = "28"
AND phone_calls.duration < 60;

-- RESULT: Robin
-- Which means Robin is the accomplice