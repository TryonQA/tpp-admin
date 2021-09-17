MUST ADD a creds.txt file locally to folder to run - 
text file should contain one line formatted:
username,password

--SELENIUM NOTES--
REQUIRES locally installed Chrome driver and adjustment of PATH variable accordingly
Qs: 
-switching logic on first four filters
-guardrails for dropdown handler
-better readouts (label tests by test plan?)

Running OK locally in IDE 9/17/21 -gb
MAIN starts line 1083


--TEST CAFE NOTES --
CMD to run test:
testcafe chrome transportation_providers.js --skip-js-errors

Currently hanging on click of AMERICAN LOGISTICS ADMIN button.