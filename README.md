# NSERC Grant Awardees Scraper

## Description
* Downloads the Canadian Natural Sciences and Engineering Research Council (NSERC) website grant data using `requests` and `lxml`

## How it Works
* Each grant is hosted on https://www.nserc-crsng.gc.ca/ase-oro/Details-Detailles_eng.asp?id=XXXXX 
* Each grant has a unique ID, however due to deletions, IDs are not contiguous.
* `check_page_headers_exist()` first makes sure that the ID exist, and writes it to `working_ids_full.txt`
* The scraping code goes through `working_ids_full.txt` to visit each grant page using `requests`
* uses `lxml` to extract data from html
* Each grant is saved as a row in `results.csv` (not included on github)
* Includes `BROWSER_WAIT_TIME` to not overload the website.

## Sample output
| Index  	| Title                                                                 	| Competition Year 	| Fiscal Year 	| Project Lead Name     	| Institution          	| Department                                              	| Province    	| Award Amount 	| Installment 	| Program                               	| Selection Committee                 	| Research Subject                	| Area of Application                                  	| Co-Researchers   	| Partners    	| Award Summary 	|
|--------	|-----------------------------------------------------------------------	|------------------	|-------------	|-----------------------	|----------------------	|---------------------------------------------------------	|-------------	|--------------	|-------------	|---------------------------------------	|-------------------------------------	|---------------------------------	|------------------------------------------------------	|------------------	|-------------	|---------------	|
| 592611 	| Multidimensional signal processing for visual and multimedia services 	| 2013             	| 2016-2017   	| Dubois, Eric          	| University of Ottawa 	| Electrical Engineering and Computer Science , School of 	| Ontario     	| $24,000      	| 4 - 5       	| Discovery Grants Program - Individual 	| Electrical and Computer Engineering 	| Digital signal processing       	| Information, computer and communication technologies 	| No Co-Researcher 	| No Partners 	| [...]           	|
| 592612 	| Geodynamics of Geological Processes                                   	| 2012             	| 2016-2017   	| Beaumont, Christopher 	| Dalhousie University 	| Oceanography                                            	| Nova Scotia 	| $54,000      	| 5 - 5       	| Discovery Grants Program - Individual 	| Geosciences                         	| Structural geology andtectonics 	| Earth sciences                                       	| No Co-Researcher 	| No Partners 	| [...]           	|

## Impact
* Scraped __500,000 grants__ from the NSERC website
* Code used towards a peer-reviewed journal article analyzing the Canadian research and innovation ecosystem:
    * Veletanlić, E., Sá, C. Implementing the Innovation Agenda: A Study of Change at a Research Funding Agency. Minerva 58, 261–283 (2020). <https://doi.org/10.1007/s11024-020-09396-4>
