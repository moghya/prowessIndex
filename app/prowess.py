import csv
import os
from prowessIndex import *
from settings import APP_STATIC
from flask import Flask
from flask import render_template,request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/fillDetails',methods=['POST','GET'])
def makeItHappen():
     if request.method == 'POST':
        form_data = request.form
        courses = []
        try:
            with open(os.path.join(APP_STATIC, form_data['programme']+'.csv')) as f:
                lines = f.readlines()
                i = 0
                for line in lines:
                    if i>0:
                        line = line.split(',')
                        courses.append((line[0],line[1]))
                    i+=1
            data = {
                'programme':form_data['programme'],
                'courses':courses,
                'total_courses':i
            }
            return render_template("fillDetails.html",data = data)
        except:
            return 'Bad Request.....<a href="/">Start Over</a>'
     else:
         return 'Bad Request.....<a href="/">Start Over</a>'

@app.route('/prowessIndexReport',methods=['POST','GET'])
def prowessIndex():
    if request.method=="POST":
        try:
            form_data = request.form
            courses = []
            f = open(os.path.join(APP_STATIC, 'student_'+form_data['prn']+'.csv'),'w')
            f.write('course_id,course_name,grade\n')
            for key in form_data:
                if key!='prn' and key!='prowessIndex' and key!='programme':
                    line = key.split(':')[0]+','+key.split(':')[1]+','+form_data[key]+'\n'
                    courses.append((key.split(':')[0],key.split(':')[1],form_data[key]))
                    f.write(line)
            f.close()
            prowessIndex = getProwessIndex(form_data['programme'],form_data['prn'])
            with open(os.path.join(APP_STATIC, form_data['programme']+'PO.txt')) as f:
                lines = f.readlines()
                POs = []
                for line in lines:
                    POs.append((line.split('|')[0],str(line.split('|')[1]).strip(' \n ')))

            prowessIndexResult = []
            for i in range(0,len(prowessIndex)):
                prowessIndexResult.append((POs[i],prowessIndex[i]))
            data = {
                'prowessIndexResult' : prowessIndexResult,
                'prn':form_data['prn'],
                'programme':form_data['programme'],
                'courses':courses
            }
            return render_template('prowessIndexReport.html',data=data)
        except:
            return 'Bad Request.....<a href="/">Start Over</a>'
    else:

        programme  = request.args.get('prg')
        prn = request.args.get('prn')
        courses = []
        f = open(os.path.join(APP_STATIC, 'student_'+prn+'.csv'),'r')
        f.readline()
        lines = f.readlines()
        for line in lines:
            course = line.split(',')
            courses.append(course)
        f.close()
        prowessIndex = getProwessIndex(programme,prn)
        with open(os.path.join(APP_STATIC,programme+'PO.txt')) as f:
            lines = f.readlines()
            POs = []
            for line in lines:
                POs.append((line.split('|')[0],str(line.split('|')[1]).strip(' \n ')))

        prowessIndexResult = []
        for i in range(0,len(prowessIndex)):
            prowessIndexResult.append((POs[i],prowessIndex[i]))
        data = {
            'prowessIndexResult' : prowessIndexResult,
            'prn':prn,
            'programme':programme,
            'courses':courses
        }
        return render_template('prowessIndexReport.html',data=data)



if __name__ == '__main__':
    app.run()
