import json
import requests
import csv
from pprint import pprint

urls = [
["https://api6.tplmaps.com/dawn_election_portal/assets/js/election_2008.js","2008"],
["https://api6.tplmaps.com/dawn_election_portal/assets/js/election_2013.js","2013"],
["https://api6.tplmaps.com/dawn_election_portal/assets/js/election_2018.js","2018"]
# ["https://api6.tplmaps.com/dawn_election_portal/assets/js/election_2024.js","2024"]
]

def create_json_from_url(urls):
    list_of_candidates = []
    try:
        for url,year in urls:
            
                print(url,year)
                response = requests.get(url).content.replace(b"'{",b"{")\
                .replace(b"'}",b"")\
                .replace(b"'",b'"')\
                .replace(b"/",b"")\
                
                check_index = response.find(b'=')
                response = response[check_index+1:]
                candidates = json.loads(response)
                print(f'No. of Candidates: {len(candidates)}, Year:{year}')

                # Manipulate the dictionary
                for candidate in candidates:
                    if 'geom' in candidate:  # Check if the key exists before attempting to delete
                        del candidate['geom']
                    candidate['year'] = year
                    print(candidate)
                list_of_candidates.append(candidates)
        return list_of_candidates
    except json.JSONDecodeError as e:
        print(f'JSON decoding error: {e}')
        print(response[388:391])
    
    except ConnectionError as e:
        print(f"Errors: {e}")
    
    except Exception as e:
        print(f"Errors: {e}")


def create_json_file(list_of_candidates):
    try:
        with open('candidates.json','w') as f:
            json.dump(list_of_candidates,fp=f)
    except Exception as e:
        print(e)

def create_csv_file(list_of_candidates):
    try:
        for data in list_of_candidates:
            headers = data[0].keys()
            with open('candidates.csv','a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    list_of_candidates = create_json_from_url(urls)
    print(f"No. of Total Candidates: {len(list_of_candidates)}")
    print("creating json file....")
    create_json_file(list_of_candidates=list_of_candidates)
    print("json created successfully!")
    print("creating csv file...")
    create_csv_file(list_of_candidates=list_of_candidates)
    print("created csv successfully!")
        


    # print(list_of_candidates[0])
