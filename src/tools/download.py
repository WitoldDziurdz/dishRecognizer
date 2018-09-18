
dishes = ['bigos', 'rosół', 'kopytka', 'schabowy', 'grochówka', 'pierogi', 'kapuniak', 'kompot', 'gulasz', 'pomidorowa']

for dish in dishes:
    os.makedirs(dish)
    cmd = "python temp.py -q " + dish + " -o " + dish
    print(cmd)
    os.system(cmd)