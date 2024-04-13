import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests

def CAE_generator(n_student = 100000, random_seed = 1):
    np.random.seed(random_seed)
    if (n_student < 1000 or n_student > 100000):
        raise Exception("n_student have to greater than 1000 and smaller than 100000!")
    p_top = 0.05
    p_bot = 0.95
    p = []
    temp_p = np.linspace(p_top, p_bot, 40)
    np.random.shuffle(temp_p)
    for i in range(40):
        p.append((i, temp_p[i]))
    temp_p = np.linspace(p_top, p_bot, 30)
    for i in range(30):
        p.append((i+40, temp_p[i]))
    temp_p = np.linspace(p_top, p_bot, 50)
    for i in range(50):
        p.append((i+70,temp_p[i]))
    p = sorted(p, key = lambda x : x[1], reverse=True)
    solutions = []
    answers = ['A', 'B', 'C', 'D']
    for i in range(120):
        solutions.append(answers[np.random.randint(0, 3)])
    results = np.full((n_student, 120), 'E')
    student_performances = list(map(int,np.random.normal(65, 11.1, n_student)))
    
    points = []
    point_per_question = []
    for question in range(120):
        point_per_question.append(np.log(p[question][1]/(1-p[question][1])))

    for student in range(n_student):
        student_perf = student_performances[student]
        points.append(0)
        for i, item in enumerate(p):
            remain = 120 - i
            _p = np.random.rand()
            if (remain <= student_perf):
                results[student, item[0]] = solutions[item[0]]
                points[-1]+=10 + point_per_question[item[0]]
                student_perf -= 1
            elif (_p <= 0.9 and student_perf > 0):
                results[student, item[0]] = solutions[item[0]]
                points[-1]+=10 + point_per_question[item[0]]
                student_perf -= 1
            else:
                results[student, item[0]] = solutions[item[0]]
                while (results[student, item[0]] == solutions[item[0]]):
                    results[student, item[0]] = answers[np.random.randint(0, 3)]
        points[-1] = np.round(points[-1], 2)

    # fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    # ax[0].hist(points, bins=30)
    # ax[1].boxplot(points)
    # fig.savefig("hist.png")
    # print(f'max : {max(point_per_question)} | min : {min(point_per_question)} | median : {np.median(point_per_question)}')
    # print(f'max : {max(points)} | min : {min(points)} | median : {np.median(points)}')
    # print(points)

    return results, solutions

def name_generator(n_student = 100000, random_seed = 1):
    np.random.seed(random_seed)
    data = ""
    response = requests.get("https://raw.githubusercontent.com/nprm1243/MaSSP-DS-2023/main/ProjectData/names.txt")
    data = response.text
    data = data.split('\r\n')
    return data[:n_student]

def CAE_data_generator(n_student = 100000, random_seed = 1):
    CAE_data, sols = CAE_generator(n_student, random_seed)
    names = name_generator(n_student, random_seed)
    df = pd.DataFrame(CAE_data)
    df.columns += 1
    df.insert(0, "Name", names)
    return df, sols

if __name__ == '__main__':
    table, sols = CAE_data_generator(5000, 2024)
    print(table.head(5))
    print(sols)