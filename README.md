# florida-plates

Using Selenium and Python to check [vanity license plate availability](https://services.flhsmv.gov/MVCheckPersonalPlate/PlateInquiryView.aspx) in the state of Florida.

## Quickstart

1. Populate `dat/inputs.csv` with every plate you want to check, one per line.
2. Run `docker-compose up --abort-on-container-exit --build`
3. Check the results in `dat/outputs.csv`.

Sample output:
```
PLATE,LENGTH,AVAILABLE
GWAZI,5,False
YINZER,6,True
```

**NOTE:** Florida plates cannot be longer than 7 characters, and many specialty plate designs require 5 characters or fewer. The script will reject entries over 7 characters, but it does not perform further input validation.
