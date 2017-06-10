import numpy as np
import pandas as pd
import os
from settings import APP_STATIC

def gradeToScore(grade):
    score = {
        'AA':10,
        'AB':9,
        'BB':8,
        'BC':7,
        'CC':6,
        'CD':5,
        'DD':4,
        'NIL':0

    }
    return score[grade]

def getProwessIndex(programme_name,student_prn):
    programme = pd.read_csv(os.path.join(APP_STATIC,programme_name+'.csv'))
    programme.sort_values('course_id',inplace=True)
    programme = programme.reset_index().drop(['index'],axis=1)
    student = pd.read_csv(os.path.join(APP_STATIC,'student_'+student_prn+'.csv'))
    student.sort_values('course_id',inplace=True)
    student = student.reset_index().drop(['index'],axis=1)
    student['score'] = student['grade'].apply(gradeToScore)
    applicablePO = programme.drop(['course_id','course_name'],axis=1)
    for i in range(0,len(applicablePO)):
        isApplicable = 0
        if student.loc[i]['score']!=0:
            isApplicable=1
        applicablePO.loc[i]*=isApplicable
    result = applicablePO.copy()
    for i in range(0,len(result)):
        result.loc[i]*=student.loc[i]['score']
    prowessIndex = result.sum()/applicablePO.sum()*10
    prowessIndex = prowessIndex.fillna(0)
    return list(prowessIndex)