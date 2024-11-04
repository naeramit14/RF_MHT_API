class Differtial_diagnosis:
  def __init__(self, db):
    self.mr = db.mr
    self.dx = db.dx
    self.accepted_score = 0.9
    self.mr_weight =  {'ph_ud': 0.1, 'pd': 0.1, 'cc': 0.1 , 'pi_p': 0.8, 'pi_n': -0.1}

  def find_index_item(self, items: list, id: int) -> int:
    for index, item in enumerate(items):
      if item['id'] == id:
        return index
    return -1

  def correlated_score(self, main: list, compare: list) -> float:
    n_compare = len(compare)
    if n_compare == 0:
      return 1.0
    score_per_n = (1.0 / n_compare) 
    total_score = 0.0
    for c_item in compare:
      m_index = self.find_index_item(main, int(c_item['id'])) 
      if (m_index != -1):
          total_score += score_per_n / 2
          detail_score = score_per_n / 2
          for k, v in c_item.items():
            if (k == 'id'):
              continue
            try:
              if (main[m_index][k] == 0) | (v == main[m_index][k]) | (v == 0 ):
                total_score += (detail_score / (len(c_item) - 1))
            except:
              pass
    return total_score

  def get_dicision_score(self, h_mr: dict, c_mr: dict ) -> float:
    total_score = 0.0
    for k, v in self.mr_weight.items():
      if (k == 'ph_ud') & ('ph_ud' in c_mr) & ('ph_ud' in h_mr):
        for item in c_mr['ph_ud']:
          if self.find_index_item(h_mr['ph_ud'], int(item['id'])) != -1:
            total_score += v
            break
      elif (k == 'pi_n') & ('pi_n' in c_mr) & ('pi_p' in h_mr):
        for item in c_mr['pi_n']:
          if self.find_index_item(h_mr['pi_p'], int(item['id'])) != -1:
            total_score += v
            break
      else:
        if (k not in c_mr):
          total_score += v
        if (k in c_mr) & (k in h_mr):
          total_score += self.correlated_score(h_mr[k], c_mr[k]) * v
    return total_score

  def sorted_probable_disease(self, disease_percent: dict) -> dict:
    sorted_probable_disease = {}
    sorted_percent = list((sorted(disease_percent.values(), reverse=True)))
    for current_percent in sorted_percent:
      sorted_id = sorted([id for id, percent in  disease_percent.items() if percent == current_percent])
      for id in sorted_id:
        sorted_probable_disease[str(id)] =  int(current_percent * 100)
    return sorted_probable_disease

  def probable_disease(self, c_mr: dict):
    disease_count = {}
    total_count = 0
    for index, h_mr in enumerate(self.mr):
      if self.get_dicision_score(h_mr, c_mr) >= self.accepted_score:
        total_count += 1
        if h_mr['dx'] in disease_count:
          disease_count[h_mr['dx']] += 1
        else:
          disease_count[h_mr['dx']] = 1
      disease_percent = { disease : round(count / total_count, 2) \
                       for disease, count in disease_count.items()}
      sorted_percent =  self.sorted_probable_disease(disease_percent)
    return sorted_percent