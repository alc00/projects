
CREATE TABLE DM_99_CO_RENTAL_LISTING_SUMMARY_T
(
DTIME_INSERTED TEXT,
LISTING_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
LISTING_NAME TEXT,
RENTAL_PER_MONTH REAL,
RENTAL_PER_MONTH_PSF REAL,
CNT_BEDS REAL,
CNT_BATHS REAL,
SIZE_SQFT REAL,
LATITUDE REAL,
LONGITUDE REAL,
LISTING_LINK TEXT UNIQUE
)
;

DROP TABLE DM_99_CO_RENTAL_LISTING_SUMMARY_T;