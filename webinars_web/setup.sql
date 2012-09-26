DROP DATABASE IF EXISTS webinars;
DROP DATABASE IF EXISTS test_webinars;
CREATE DATABASE webinars CHARACTER SET UTF8;
CREATE DATABASE test_webinars CHARACTER SET UTF8;
USE webinars;

/* LOCAL */
CREATE USER 'webinars'@'localhost' IDENTIFIED BY '__SECRET__';
GRANT ALL ON webinars.* TO 'webinars'@'%';
GRANT ALL ON test_webinars.* TO 'webinars'@'%';
CREATE USER 'SUSR_Nagios'@'localhost' IDENTIFIED BY '__SECRET__';
GRANT SELECT ON webinars.* TO 'SUSR_Nagios'@'%';

/* QA or PROD */
CREATE USER 'webinars'@'%' IDENTIFIED BY '__SECRET__';
GRANT ALL ON webinars.* TO 'webinars'@'%';
CREATE USER 'SUSR_Nagios'@'%' IDENTIFIED BY '__SECRET__';
GRANT SELECT ON webinars.* TO 'SUSR_Nagios'@'%';


/* SearchService user QA or Prod */

CREATE USER 'webinars'@'%' IDENTIFIED BY '__SECRET__';
GRANT ALL ON SearchService.* TO 'webinars'@'%';



/* CLEAR OUT SEARCH SERVICE STUFF */
DELETE 
FROM SavedSearches 
WHERE portalId IN (28306,104860,41827,69769,69879,103343)
    AND (name LIKE 'Registered For % Webinar' 
        OR name LIKE 'Registered But Did Not Attend % Webinar' 
        OR name LIKE 'Attended % Webinar'
        OR name LIKE 'Webinar % Noshows' 
        OR name LIKE 'Webinar % Registrants'
        OR name LIKE 'Webinar Attendees For %'
        OR name LIKE 'Webinar Registrants For %'
        OR name LIKE 'Webinar Noshows For %');

DELETE
FROM FormFieldRollups
WHERE portalId IN (28306,104860,41827,69769,69879,103343)
    AND (label LIKE 'Attended "%"% Webinar?'
        OR label LIKE 'Registered For "%"% Webinar?'
        OR label LIKE 'Attended Any Webinar?'
        OR label LIKE 'Registered For Any Webinar?');

UPDATE webinars_event 
SET 
  _registered_criterium_guid=NULL,
  _attended_criterium_guid=NULL,
  _registered_saved_search_id=NULL,
  _attended_saved_search_id=NULL,
  _noshow_saved_search_id=NULL;

UPDATE webinars_hub
SET 
  _registered_any_criterium_guid=NULL,
  _attended_any_criterium_guid=NULL,
  _registered_any_saved_search_id=NULL,
  _attended_any_saved_search_id=NULL;
