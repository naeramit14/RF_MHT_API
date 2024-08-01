import json

class Database:
  def __init__(self, test=False):
    if test:
      src = "./db_test.json"
    else:
      src = "./db.json"
    with open(src, 'r', encoding="utf8") as openfile:
      obj = json.load(openfile)
    self.dx = obj['dx']
    self.pd = obj['pd']
    self.sym = obj['sym']
    self.mr = obj['mr']