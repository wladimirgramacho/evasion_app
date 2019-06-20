def calculate(entry_semester, course_semester):
  if is_summer_course(course_semester):
    course_semester += 1

  diff = course_semester - entry_semester

  if entry_semester % 2 != 0 :
    if diff >= 10 :
      result = semesters_between_years(diff)
    else:
      result = diff
  else:
    if diff % 10 == 0 :
      result = semesters_between_years(diff)
    else:
      result = diff // 5

  return result + 1

def is_summer_course(semester):
  return semester % 10 == 0

def semesters_between_years(diff):
  return (diff // 5) + (diff % 5)