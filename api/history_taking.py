import json
import Database as DB
import Diferertial_diagnosis as DDX


with open('./Q_table_1.json', 'r') as openfile:
    Q_table = json.load(openfile)

db = DB.Database()
ddx = DDX.Differtial_diagnosis(db)
action = [s['id'] for s in db.sym]
max_action = 5

def get_used_action(record: dict):
    used_action = [cc['id'] for cc in record['cc']] \
        + [pi_p['id'] for pi_p in record['pi_p']]  \
        + [pi_n['id'] for pi_n in record['pi_n']] 
    return used_action

def get_max_Q(currented_state: str,  available_action: list):
    try:
        max_value = Q_table[currented_state][available_action[0]]
    except:
        max_value = 0
    max_id = available_action[0]

    for id in available_action:
        try:
            q_value = Q_table[currented_state][id]
        except:
            q_value = 0
        if q_value > max_value:
            max_value = q_value
            max_id = id
    return max_id

def get_question(record: dict):
    used_action = get_used_action(record)
    available_action = [id for id in action if id not in used_action]
    if  (len(available_action) == 0) :
        print("no question")
        return []
    
    if  (len(used_action) > max_action):
        print("max question")
        return []
    
    probable_disease = ddx.probable_disease(record)
    state = ">".join(probable_disease)
    print("state:" , state)
    if (len(state) <= 1):
        return []
    actionId = get_max_Q(state ,available_action)
    question = [ sym   for sym in db.sym if sym["id"] == actionId ] 
    return question

def find_index_item(items: list, id: int) -> int:
    for index, item in enumerate(items):
      if item['id'] == id:
        return index
    return -1

def display_disease(probable_disease: dict):
    disease_id = list(probable_disease.keys())
    result = []
    for d in disease_id[:5]:
      idx = find_index_item(db.dx, int(d))
      if id != -1:
        result.append(db.dx[idx]['t_name'])
    return result


def get_probaple_disease(record: dict):
    probable_disease = ddx.probable_disease(record)
    return  display_disease(probable_disease)

def get_cheif_complaint():
    summary = {}
    for record in db.mr:
        try:
            id = record['cc'][0]['id']
            if id in summary:
                summary[id] += 1
            else:
                summary[id] = 1
        except:
            pass
    sorted_summary = sorted(summary.items(), key=lambda kv: (kv[1], kv[0]) , reverse=True)
    cheif_complaint = []
    symptom = db.sym
    for arr in sorted_summary:
        index = find_index_item(symptom, arr[0])
        if index != -1:
            cheif_complaint.append(symptom[index])
    print('cc-amount: ', len(cheif_complaint))
    return cheif_complaint
