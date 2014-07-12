# Mungy: a tool for data munging

Convert: Tabular data,
         list data

into data objects for programming

## Data conversion

convert this...

TH1 | TH2 | TH3 | TH4
----|-----|-----|-----
td1 | td2 | td3 | td4
----|-----|-----|-----
td5 | td6 | td7 | td8

...into this

data = {
    TH1: [td1, td5],
    TH2: [td2, td6],
    TH3: [td3, td7],
    TH4: [td4, td8]
}
