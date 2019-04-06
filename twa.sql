-- count active members
SELECT COUNT(*)
FROM members_twamembership m
         JOIN members_person p ON p.id = m.person_id
WHERE m.public = TRUE
  AND m.status = 10 -- MEMBERSHIP_STATUS_MEMBER
  AND p.public = TRUE
  AND p.is_active = TRUE
;

-- count active members with current payment
SELECT COUNT(*)
FROM members_twamembership m
         JOIN members_person p ON p.id = m.person_id
         JOIN members_twapayment y ON y.twa_id = m.id
WHERE m.public = TRUE
  AND m.status = 10 -- MEMBERSHIP_STATUS_MEMBER
  AND p.public = TRUE
  AND p.is_active = TRUE
  AND y.public = TRUE
  AND y.year = EXTRACT(YEAR FROM NOW())
;

-- find active members without payments
SELECT c.code          AS "COUNTRY",
       m.twa_id_number AS "TWA ID",
       p.firstname     AS "FIRSTNAME",
       p.lastname      AS "LASTNAME"
FROM members_twamembership m
         JOIN members_person p ON p.id = m.person_id
         JOIN members_country c ON m.twa_id_country_id = c.id
WHERE m.public = TRUE
  AND m.status = 10 -- MEMBERSHIP_STATUS_MEMBER
  AND c.public = TRUE
  AND p.public = TRUE
  AND p.is_active = TRUE
  AND NOT EXISTS(SELECT *
                 FROM members_twapayment y
                 WHERE y.public = TRUE
                   AND y.year = EXTRACT(YEAR FROM NOW())
                   AND y.twa_id = m.id)
ORDER BY c.code, p.firstname
;

-- check payments for empty years
SELECT *
FROM members_twapayment y
WHERE y.year IS NULL;

-- find twa IDs over 2000
SELECT c.code,
       m.twa_id_number,
       m.status,
       m.passport_date AS passport,
       p.firstname,
       p.lastname,
       d.name          AS dojo
FROM members_twamembership m
         JOIN members_person p ON p.id = m.person_id
         JOIN members_person_dojos pd ON pd.person_id = p.id
         JOIN members_dojo d ON d.id = pd.dojo_id
         JOIN members_country c ON m.twa_id_country_id = c.id
WHERE m.twa_id_number >= 2000
ORDER BY m.twa_id_number DESC NULLS LAST, m.last_modified DESC
;
