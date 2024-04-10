# TA ASSIGNMENT - AUTOMATION PROJECT

## How to run the project

INPUT FILES:

- You need three files to run this software: TA_schedule.csv, class_schedule.csv and Instr_Pref.csv.
- These input files should be stored in the folder: **input_files**
- Run the main.ipynb file in jupyter notebook or any IDE (VS CODE) and then open the index.html file in any browser to view the assignments
- If you want to run it in a terminal by converting to python, use the following command:

```
jupyter nbconvert --to python nb.ipynb
```

You may have to install the python mistune package:

```
sudo pip install -U mistune
```

### Folder Details:

- **algorithms**: Contains the code for hungarian algorith - **hungarian.py**
- **assignment_output_files**: Contains the final assignments, unassigned courses and the cost breakdown
- **data**- This folder contains the code to change edgeweights, capacity limit, LAB - TA requirement limit, etc.

  - **capacity_cap.py**: To change the capacity limit for TAs
  - **edgeWeights.py**: To change edgeWeights
  - **getPseudoLabs**: To fetch the labs that are not marked as lab but have lab like TA requirement
  - **db_config.py**: To change the DB URL
  - **lab_ta_requirements.py**: This function returns a dictionary which maps labs to the number of sections 1 TA can handle
  - **timeSlotMapping**: Map Time slots (period: 11:10 to 12:25) to Letters

- **input_files** - This folder contains all the input files that we need to provide to the program
- **input_json** - Input files converted to JSON files
- **output_files** - All the files that are generated as the program runs: The final section data is in the sub-folder: **section_data**

- **scripts** - ALL the scripts can be found in this folder

  - **parse_ta_data.py**: CREATE TA_schedule.json from the input file TA_Schedule.csv
  - **parse_courses.py**: CREATE courses.json from the input file course Schdule
  - **parse_sections.py**: CREATE INITIAL SECTION DATA - This will again be parsed in various scripts to form the final section data
  - **parse_schedule.py**: CREATE schedules
  - **combined_view.py**: Combines the schedule information by merging all slots for the CRN
  - **parse_instructor_pref.py**: Creates the instructor preference data from the input CSV file
  - **create_final_sections.py**: This file creates the final data that we need for the hungarian algorithm and calls lab processing scripts to process lab data and then processes non-lab data and creates a final section.json file which is stored in **section_data** folder in **output_files** folder.
  - **process_labs.py**: Processes lab data which handles pseudo labs and TA requirements, capacity cap mapping and filtering the labs we don't need
  - **compute_conflict_matrix.py**: This file creates the conflict matrix between TA and final sections. IT also calls the conflict break down skeleton to create and store the breakdown
  - **create_conflict_breakdown_skeleton.py**: This script creates the conflict breakdown skeleton
  - **duplicateTAs.py**: This script will create another entry for all TAs that have been assigned to classes with 0.5 TA requirement to be assigned to another class
  - **incremental_TA_duplication.py**: After we allocated all TAs if there are any unassigned courses left then we run this script to fetch the next best TA to duplicate - TA with least enrollment in section they are TAing for (if they are only TAing for one class)

- **utils**: Contains all the utility files
  - **show_hungarian_assignments** - This file produces the assignment output and stores it in the **assignment_output** folder

### FOLDER STURCTURE:

    .
    ├── algorithms
    │ ├── hungarian.py
    ├── assignment_output_files
    ├── data
    │ ├── capacity_cap.py
    │ ├── daysMapping.py
    │ ├── db_config.py
    │ ├── edgeWeights.py
    │ ├── getPseudoLabs.py
    │ ├── lab_ta_requirements.py
    │ └── timeSlotMapping.py
    ├── db
    │ ├── connect.py
    │ ├── create_tables.py
    │ ├── insert_data.py
    │ └── models.py
    ├── input_files
    ├── input_json
    ├── output_files
    │ └── section_data
    ├── scripts
    │ ├── combined_view.py
    │ ├── compute_conflict_matrix.py
    │ ├── create_conflict_breakdown_skeleton.py
    │ ├── create_final_sections.py
    │ ├── duplicateTAs.py
    │ ├── incremental_TA_duplication.py
    │ ├── parse_courses.py
    │ ├── parse_instructor_pref.py
    │ ├── parse_schedule.py
    │ ├── parse_sections.py
    │ ├── parse_ta_data.py
    │ └── process_labs.py
    ├── temp # ignore
    ├── utils
    │ ├── convertCSVtoJSON.py
    │ ├── csvToDict.py
    │ ├── create_conflict_breakdown_skeleton.py
    │ ├── dictionaryToJsonFile.py
    │ ├── getCoursesTakenFromCrn.py
    │ ├── getTimeSlotsFromCRN.py
    │ ├── load_conflict_matrix.py
    │ └── show_hungarian_assignments.py
    ├── conflicts_view.html # Shows the conflict breakdown in browser (TA vs Sections)
    ├── index.html
    ├── main.ipynb # This file should be used to run all the scripts in one go
    └── README.md
