MUST ADD a creds.txt file locally to folder to run - 
text file should contain one line formatted:
username,password

To change environment being tested adjust active_url variable in tpp_test_scripts

--SELENIUM NOTES--
REQUIRES locally installed Chrome driver and adjustment of PATH variable accordingly
Qs: 
-switching logic on first two filters
-guardrails for dropdown_handler
-better readouts (label tests by test plan?)

drivers_test and providers_test Running OK locally 9/20/21 -gb
adapted to multi-file 


--TEST CAFE NOTES --
CMD to run test:
testcafe chrome transportation_providers.js --skip-js-errors

Currently hanging on click of AMERICAN LOGISTICS ADMIN button.