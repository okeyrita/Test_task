# WunderSchild Back End Developer Test Task

## Description

#### In this task we have any subproblems:
1. Implement algorithm to parse business data from a global business data registry.
2. Store information to a database (MongoDB).
3. Find algorithm that generates partially or fully the list of valid companies ID

#### Content of project.
1. The first project 'opencorporates' contain implementation for parsing business data from data registry and added this information to database _MongoDB_. This parser is asynchronous.
- This parser parse not all id_numbers because it is need too much time. There are we use list of 51 valid id_numbers for show that parser is work.
2. The second project 'checker' contain algorithm for checking ID is valid or not.
3. Some support files such as List_of_national_identifiers, test_task (file with text of task), national_identifiers, generate_id (code for generating id numbers) and other.

## Structure of Database

This project implement Database with name _database_. 
- Database consist of 5 collections with some fields:
### 1. __company_information__
  - __company_number__
  - native_company_number
  - status
  - jurisdiction
  - registered_address
  - previous_names
  - directors_officers
  - - name
  - - __link__
  - - position
  - - info
  - inactive_directors_officers
  - - name
  - - __link__
  - - position
  - - info
  - link

### 2. __latest_events__
  - __company_number__
  - date
  - event
  - link

### 3. __similarly_named_companies__
  - __company_number__
  - __name__
  - link

### 4. __director_information__
  - __link__
  - company
  - __name__
  - address
  - position
  - start_date
  - end_date
  
### 5. __similarly_named_officers__
  - __name__
  - link
  - position
  - company_name
  - company_link

These collections can be connected with bold fields.

This database can have not only German companies and officers, because of in the task says that "Similarly named officers (__information from this section, with link and names of the company form each link__)" . Then when we collect Similarly named officers (who can finds not only in the same country) we parse not only German companies and officers.

## Structure of company id_number

#### We can divide id_number to five separate parts.

For example use a valid id_number  __F1103R_HRA44021__:

1. F1103 part is associated with city of registration of this company. It is nationl identifier (XJustiz-ID). See all XJustiz-ID in file __List_of_national_identifiers.xlsx__ and list of these XJustiz-ID also contains in national_identifiers.txt
2. After this part can be R or V or nothing.
3. "_"
4. HRA is a type of registry. There are only 5 types of registers such as HRB, HRA, GnR, PR and VR.
5. The last number combination (in this example 44021) is an index number. This combination can contain 1 to 6 digits.
6. After this part also can be combination of 1 or 2 letters or nothing.

Remark: Then number of possible combinations is 157 * 3 * 5 * 10^6 * (26^2 +1) ≈ 16^11.
It is too much for checking.

Also valid id number can be loks like __P2507_P2511_HRB3455__:
- In this case one of national identifiers is German and second is identifiers of another country.a rough calculation of the value, number, quantity, or extent of something.
- Last information has the same structure.

#### Well, after this estimation we have some ways.

#### Way 1. Brute force (full solution)

We can check all of combinations and add to separate file only valid id.

We can calculate it in >=2 threads. But it is need too much time. 

#### Way 2. Estimate by upper bound (partial solution)

For id_numbers which we already have, we can estimate that special case , kind of F1103R_HRA44021. And F1103R_HRA is a static part , but 44021 is an index number. And if we have valid index number 44021 then there are all combinations F1103R_HRA with 1 to 44020.

Based on 51 id_numbers which we already have we can made an algorithm for calculating another id_numbers by upper bound.

This method immplements in file __estimate_by_upper_bound.py__ . Output stored in file __estimated_id.txt__
This file is too much for estimated_id file and this file stored in <https://yadi.sk/d/TE1_JbZA0HLnnA>
(For current 51 id we get 2,874,119 id, full count of commpanies at the moment of writing this file is 5,357,667. Then we found ≈ 50% of numbers).