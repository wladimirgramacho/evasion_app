import course_codes
import semester_calculator
import pandas as pd

def first_semesters(df):
  # calculate semester
  df['Semester'] = df.apply(lambda x: semester_calculator.calculate(x['SemestreIngresso'], x['SemestreMateria']), axis=1)
  df = df[(df.Semester > 0) & (df.Semester <= 2)]

  # filter for courses of two first semesters
  df = df[df.CodigoMateria.isin(course_codes.COURSE_CODES)]
  return df


#
# This is the first model I'll be testing and the idea is
# to see how accurate we can get just with the info from
# the first two semesters and the number of  failed courses
# on those semesters
# Data: How many times they failed courses from 1st two semesters
#

def model1(csv_file):
  df = pd.read_csv(csv_file)
  df = first_semesters(df)
  print('1st model start')

  # discretize course grade
  df.Conceito = df.Conceito.replace(['SR', 'II', 'MI'], 1)
  df.Conceito = df.Conceito.replace(['SS', 'MS', 'MM', 'CC', 'DP', 'TR', 'TJ'], 0)

  df['CourseTerm'] = df.Semester.map(str) + '_' + df.CodigoMateria.map(str)

  # remove unnecessary columns
  df = df.drop(columns=['SemestreIngresso', 'SemestreMateria', 'CodigoMateria', 'Semester'])

  df = df.pivot_table(values='Conceito', index=[
                        'StudentId', 'StatusFinal'], columns='CourseTerm', aggfunc='sum', fill_value=0)
  df.columns.name = None
  df = df.reset_index()
  df.loc[df['1_114014'] != 0, '1_114626'] = df['1_114014']
  df.loc[df['1_114014'] != 0, '1_114634'] = df['1_114014']
  df.loc[df['2_114014'] != 0, '2_114626'] = df['2_114014']
  df.loc[df['2_114014'] != 0, '2_114634'] = df['2_114014']
  df.drop(columns=['1_114014', '2_114014'])
  print('1st model done')
  return df


#
# This is the second model, with the same idea that the first
# one with the actual grade.
# Data: Grades on the courses from 2 first semesters
#
def model2(csv_file):
  df = pd.read_csv(csv_file)
  df = first_semesters(df)
  print('2nd model start')

  df['CourseTerm'] = df.Semester.map(str) + '_' + df.CodigoMateria.map(str)
  # remove unnecessary columns
  df = df.drop(columns=['SemestreIngresso', 'SemestreMateria', 'CodigoMateria', 'Semester'])

  df = df.pivot_table(values='Conceito', index=[
                        'StudentId', 'StatusFinal'], columns='CourseTerm', aggfunc='last', fill_value='NC')
  df.columns.name = None
  df = df.reset_index()
  df.loc[df['1_114014'] != -1, '1_114626'] = df['1_114014']
  df.loc[df['1_114014'] != -1, '1_114634'] = df['1_114014']
  df.loc[df['2_114014'] != -1, '2_114626'] = df['2_114014']
  df.loc[df['2_114014'] != -1, '2_114634'] = df['2_114014']
  df.drop(columns=['1_114014', '2_114014'])

  # One hot encoding the grade column
  columns = df.columns.difference(['StatusFinal', 'StudentId']).tolist()
  for column in columns:
    one_hot = pd.get_dummies(df[column])
    df = df.drop(column,axis = 1)
    one_hot.columns = map(lambda x: column + '_' + x, one_hot.columns)
    df = df.join(one_hot)

  print('2nd model done')
  return df
