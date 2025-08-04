from flask import Flask,jsonify, request
import json
# import library and instance flask object
app = Flask(__name__)

#app configs
version = "v1"


def read_json_data(file_path:str) -> dict:
   with open(file_path, 'r') as f:
      return json.load(fp=f)


data = read_json_data('candidates.json')
print("File Loaded SuccessFully: ",len(data))


@app.route(f'/dep/api/{version}/get/province/<string:province>', methods=['GET'])
def get_province_data(province):
    # dict_body = request.get_json()
    # request.args
    filtered_candidates = []
    for candidates in data:
        filtered_candidates.extend(list(
           filter(
              lambda candidate: candidate["province"] == province, 
              candidates
                )))
    # for todo in todos:
    #     if todo['id'] == id:
    #         print(todo)
    return jsonify({"message":"Success","data":filtered_candidates}),200

@app.route(f'/dep/api/{version}/get/year/<string:year>', methods=['GET'])
def get_history_data(year):
    filtered_candidates = []
    province = None
    if request.args:
        province = request.args['province']
    
    for candidates in data:
        if province:
            filtered_candidates.extend(list(
            filter(
                lambda candidate: candidate["province"] == province 
                and candidate['year']==year, 
                candidates
                    )))
        else:
            filtered_candidates.extend(list(
            filter(
                lambda candidate: candidate['year']==year, 
                candidates
                    )))
    
    return jsonify({"message":"Success","data":filtered_candidates}),200

# api endpoint
@app.route('/get', methods=['GET', 'POST'])
def get_data():
   return "This is the ECP API portal for CDE Week2 Assignment!"


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)

