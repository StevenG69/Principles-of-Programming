# Written by Eric Martin for COMP9021
#
# Uses the file cardio_train.csv downloaded from
# https://www.kaggle.com/sulianova/cardiovascular-disease-dataset
#
# Implements a function analyse(gender, age)
# where gender is one of 'F' (for female) or 'M' (for male),
# and where age is any integer for which we have data in the file
# (nothing needs to be done if that is not the case).
#
# We assume that all years have 365 days;
# in particular, someone who is 365 days old is 0 year old,
# and someone who is 366 days old is 1 year old.
#
# We ignore records for which at least one of these conditions holds:
# - height < 150 or height > 200
# - weight < 50 or weight > 150
# - ap_hi < 80 or ap_hi > 200
# - ap_lo < 70 or ap_lo > 140
#
# For each of both classes "cardio problem" and "no cardio problem"
# (as given by the cardio attribute), we create 5 bins/categories for
# height, weight, ap_hi, ap_lo, of equal width,
# that span between smallest value and largest value
# for the attribute in the category.
# For instance, suppose that gender is 'F' and age is 48.
# - Suppose that for the category "cardio problem",
#   the shortest woman aged 48 is 150cm tall, and
#   the tallest woman aged 48 is 200cm tall.
#   Then each of the 5 categories for the class "cardio problem"
#   and for the attribute "height" spans 10cm.
# - Suppose that for the class "no cardio problem",
#   the shortest woman aged 48 is 158cm tall, and
#   the tallest woman aged 48 is 193cm tall.
#   Then each of the 5 categories for the class "no cardio problem"
#   and for the attribute "height" spans 7cm.
# To avoid boundary issues, add 0.1 to the maximum value
# (so with the previous example, the maximum heights would be
# considered to be 200.1 and 193.1, respectively).
# This applies to each of the 4 attributes height, weight,
# ap_hi and ap_lo.
#
# For each attribute and for each of its possible values,
# we compute the ratio of
# - the frequency of people under consideration with a "cardio problem"
#   having that value for that attribute, with
# - the frequency of people under consideration with "no cardio problem"
#   having that value for that attribute.
# Continuing the previous example:
# - Suppose that there are 100 woman aged 48
#   who have a "cardio problem" and 20 of those are at most 160cm tall.
# - Suppose that there are 150 woman aged 48
#   who have "no cardio problem" and 50 of those are at most 165cm tall.
# Then the ratio for the value "category 1" of the attribute "height"
# is 0.2 / 0.3...3...
#
# We keep only ratios that are strictly greater than 1 and order them
# from largest to smallest.
# A ratio might be infinite (see second sample test).
# In case two ratios are exactly the same, their order is determined
# by the order of the corresponding attributes in the csv file
# (first is height, last is being active or not), and in case the
# attributes are the same, their order is determined by the rank of
# the category (first is 1, last is 5; for booleans, False comes
# before True).
#
# We format ratios with 2 digits after the decimal point.
# After a ratio, the output is one of:
# - Height in category [1-5] (1 lowest, 5 highest)
# - Weight in category [1-5] (1 lowest, 5 highest)
# - Systolic blood pressure in category [1-5] (1 lowest, 5 highest)
# - Diastolic blood pressure in category [1-5] (1 lowest, 5 highest)
# - Cholesterol in category [1-3] (1 lowest, 3 highest)
# - Glucose in category [1-3] (1 lowest, 3 highest)
# - Smoking/Not smoking
# - Drinking/Not drinking
# - Not being active/Being active
#
# You are NOT allowed to use pandas. If you do, then your submission
# will NOT be assessed and you will score 0 to the quiz.

import csv
from collections import defaultdict


def analyse(gender, age):
    with open('cardio_train.csv') as file:
        next(file)
        csv_file = csv.reader(file, delimiter=';')
        data = defaultdict(list)
        for _, age_, gender_, height, weight, ap_hi, ap_lo, cholesterol,\
            gluc, smoke, alco, active, cardio in csv_file:
            age_ = (int(age_) - 1) // 365
            ap_hi = int(ap_hi)
            ap_lo = int(ap_lo)
            height = int(height)
            weight = round(float(weight))
            if gender == 'F' and gender_ == '2'\
               or gender == 'M' and gender_ == '1'\
               or age != age_\
               or ap_hi < 80 or ap_hi > 200\
               or ap_lo < 70 or ap_lo > 140\
               or height < 150 or height > 200\
               or weight < 50 or weight > 150:
                continue
            data[cardio == '1'].append([height, weight, ap_hi, ap_lo,
                                        int(cholesterol), int(gluc),
                                        smoke == '1', alco == '1',
                                        active != '1'
                                       ]
                                      )
    min_values = [None] * 4
    max_values = [None] * 4
    bin_spans = [None] * 4
    for cardio in data:
        for i in range(4):
            min_values[i] = min(record[i] for record in data[cardio])
            max_values[i] = max(record[i] for record in data[cardio]) + 0.1
            bin_spans[i] = (max_values[i] - min_values[i]) / 5
        for record in data[cardio]:
            for i in range(4):
                record[i] =\
                        int((record[i] - min_values[i]) // bin_spans[i]) + 1
    counts = {True: defaultdict(int), False: defaultdict(int)}
    class_nbs = {True: len(data[True]), False: len(data[False])}
    frequencies = {True: {}, False: {}}
    for cardio in data:
        for record in data[cardio]:
            for i in range(len(record)):
                counts[cardio][i, record[i]] += 1
        for attribute in counts[cardio]:
            frequencies[cardio][attribute] =\
                    counts[cardio][attribute] / class_nbs[cardio]
    ratios = {attribute: attribute in frequencies[False] and
                                 frequencies[True][attribute] /
                                         frequencies[False][attribute]
                         or float('inf')
                  for attribute in frequencies[True]
             }
    ratios = {attribute: ratio for (attribute, ratio) in sorted(ratios.items(),
                                                                key=lambda x:
                                                                          -x[1]
                                                               )
             }
    attributes = ['Height', 'Weight', 'Systolic blood pressure',
                  'Diastolic blood pressure', 'Cholesterol', 'Glucose',
                  'smoking', 'drinking', 'being active'
                 ]
    print('The following might particularly contribute to cardio problems '
          'for', gender == 'F' and 'females' or 'males', 'aged', age, end=':\n'
         )
    for attribute in ratios:
        if ratios[attribute] <= 1:
            break
        category, value = attribute
        if category < 4:
            print('  ', f'{ratios[attribute]:.2f}:', attributes[category],
                  'in category', value,'(1 lowest, 5 highest)'
                 )
        elif category < 6:
            print('  ', f'{ratios[attribute]:.2f}:', attributes[category],
                  'in category', value, '(1 lowest, 3 highest)'
                 )
        else:
            if value:
                print('  ', f'{ratios[attribute]:.2f}:', 
                      'Not', attributes[category]
                     )
            else:
                print('  ', f'{ratios[attribute]:.2f}:',
                      attributes[category].capitalize()
                     )