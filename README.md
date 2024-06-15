#### Instructions 

#1 Use adsbbulkimport.py or Bulkimporter3min.py for importing historical data under 'readsb-hist” - https://samples.adsbexchange.com/readsb-hist/yyyy/mm/dd
    -- adsbbulk impport will import ALL files approx 17,280 intervals of 5 seconds (roughly 84.375GB!!)
    -- bulkimporter3min will import JSON every 3 minutes approx 480 intervals (2.34GB)
    -- follow code, you will need to place your own download_dir & if required change base_url = 

#2 Use imput_compare_combined.py to join bulk import json & apply lat/log & alt filter. It will output a CSV with todays date 
    -- update local directory_path, output_directory, latitude_min, latitude_max, longitude_min, longitude_max, altitude_min, altitude_max 
    -- row 16, output file_path_name
    -- mash the run button... wait a minute & print will show total stat data total points, adsb, mlat etc 

NOTES ### You may need to install libraries - homebrew, beautifulsoup ### Just ask overlord Chatgpt for instructions to any errors
