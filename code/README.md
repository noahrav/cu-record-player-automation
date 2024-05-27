# Record Player map generation

This generates the .lmu map file for the record player. 

A LCF2XML exe is required. Cross-platform support is yet to be implemented.

## requirements

Python < 3, Pandas, Numpy

## Generate the map

```
git clone https://github.com/noahrav/cu-record-player-automation.git
cd cu-record-player-automation/code
python ./event_gen.py
```

Both Map0007.emu and Map0007.lmu files will be generated in the code/ folder.