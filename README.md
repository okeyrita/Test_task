# WunderSchild Back End Developer Test Task

## Description

#### In this task we have such subproblems:
1. Implement algorithm to parse business data from a global business data registry.
2. Store information to a database (MongoDB).
3. Find an algorithm that generates a partial of full list of valid IDs of the companies.

## Content of the project
1. The first project `opencorporates` contains implementation of the parser of business data from the data registry, which adds this information to the _MongoDB_ database. This parser is asynchronous.
  - This parser works with only a part of all available IDs, as it takes too much time to parse them all. 51 valid IDs are parsed to show, that the parser works.
2. The second project `checker` contains algorithm for checking if ID is valid or not.
3. Some support files:
  - `List_of_national_identifiers.xlsx`
  - `test_task.docx` - file with the text of the task
  - `national_identifiers.txt`
  - `brute_forse.py` - code for generating id numbers using way 1
  - `estimate_by_upper_bound.py` - code for generating id numbers using way 2
  - others

## Structure of Database

This project will create a database with the parsed data. It is called _database_ and consists of 5 collections with such fields:
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

These collections can be connected together with the fields, which are marked bold.

This database may have not only German companies and officers, because the task says: "Similarly named officers (__information from this section, with link and names of the company form each link__)". And similarly named officers may be from countries, other than Germany as well.

## Structure of company id_number

#### We can divide id_number to five separate parts.

For example, let's use a valid id_number  __F1103R_HRA44021__:

1. F1103 part is associated with city of registration of this company. It is nationl identifier (XJustiz-ID). See all XJustiz-ID in file `List_of_national_identifiers.xlsx` and list of these XJustiz-ID can also be found in `national_identifiers.txt`
2. After this part can be R or V or nothing.
3. "_"
4. HRA is a type of registry. There are only 5 types of registers such as HRB, HRA, GnR, PR and VR.
5. The last number combination (in this example 44021) is an index number. This combination can contain 1 to 6 digits.
6. This part is followed by a combination of 1 or 2 letters, or nothing.

Remark: number of possible combinations is 157 * 3 * 5 * 10^6 * (26^2 +1) ≈ 16^11.
It is too much for checking for now.

Another example of valid ID is __P2507_P2511_HRB3455__:
- In this case one of the national identifiers is Germany and second is and identifier of another country: a rough calculation of the value, number, quantity, or extent of something.
- Last part has the same structure.

## Generation of company_id number

#### Way 1. Brute force (full solution)

We can check all of combinations and add to separate file only valid id.

We can calculate it in >=2 threads. But it needs too much time.

This way described in brute_force.py

#### Way 2. Estimate by upper bound (partial solution)

For id_numbers which we already have, we can estimate a special case, such as __F1103R_HRA44021__. __F1103R_HRA__ is a static part, and 44021 is an index number. If we have valid index number 44021, then all combinations with __F1103R_HRA__ and numbers from 1 to 44020 are possible.

Based on 51 id_numbers, which we already have, we can make an algorithm for calculating another id_numbers by upper bound.

This method is implemented in file `estimate_by_upper_bound.py`. Output is stored in file `estimated_id.txt`. This file's size appeared to be too much for the Github (around 200 Mb), so it was stored by this [link](https://yadi.sk/d/TE1_JbZA0HLnnA). Given that for current 51 IDs we got 2,874,119 IDs and that full count of companies at the moment of writing this file is 5,357,667, we found ≈ 50% of numbers.

## How to run parser

```
sudo mongod

cd opencorporates/opencorporates/spiders

scrapy crawl opencorp
```

## Docker

How to run paser in a docker container.

```
docker run -it margarita9/test-task:0.5.0

mkdir /data && mkdir /data/db && mongod --fork --logpath /var/task/db_log.txt

cd opencorporates/opencorporates/spiders/

scrapy crawl opencorp

```


## MongoDB

When running of parser is done you can see your database.
Let's use these commands.

- Run mongo

```
mongo
```
- Show your databases
```
show dbs
```
- Open our database
``` 
use database
```
- Show list of collections
```
show collections 
```
After these commands we can content of one collection.
For example, show content of collection company_information
```
db.company_information.find()
```