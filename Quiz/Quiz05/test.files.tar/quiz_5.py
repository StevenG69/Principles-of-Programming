# Written by Hongyin Zhou for COMP9021
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
import os
import math
file_path = os.path.join(os.getcwd(), 'cardio_train.csv')

def analyse(gender, age):
    with open(file_path, newline='') as csvfile:
        data = csv.DictReader(csvfile, delimiter=';')        
        
        filtered_data = [
            {'height': int(row['height']), 'weight': int(float(row['weight'])),
            'Systolic blood pressure': int(row['ap_hi']), 'Diastolic blood pressure': int(row['ap_lo']),
            'cholesterol': int(row['cholesterol']), 'glucose': int(row['gluc']),
            'smoking': int(row['smoke']), 'drinking': int(row['alco']), 'being active': int(row['active']),
            'cardio': int(row['cardio']), 'age': int(row['age']), 'gender': row['gender'],}

            for row in data
            if gender == ('F' if row['gender'] == '1' else 'M') and (age == (int(row['age']) - 1) // 365)
            and 150 <= int(row['height']) <= 200
            and 50 <= int(float(row['weight'])) <= 150
            and 80 <= int(row['ap_hi']) <= 200
            and 70 <= int(row['ap_lo']) <= 140
        ]
                      
        cardio_problem = [row for row in filtered_data if row['cardio'] == 1]
        no_cardio_problem = [row for row in filtered_data if row['cardio'] == 0]      

        def create_bins(attribute, data, num_bins):
            if not data:
                return defaultdict(int)

            min_value = min(row[attribute] for row in data)
            max_value = max(row[attribute] for row in data) + 0.1
            bin_width = (max_value - min_value) / num_bins

            bins = defaultdict(int)
            for row in data:
                value = row[attribute]
                bin_index = math.ceil((value - min_value) / bin_width)
                bin_index = int(min(max(bin_index, 1), num_bins))
                bins[bin_index] += 1

            return bins

        def categorize(attribute, data):            
            min_value = min(row[attribute] for row in data)
            max_value = max(row[attribute] for row in data)  
             
            category_width = 1
            num_categories = max(1, (max_value - min_value) // category_width + 1)
            categories = defaultdict(int)

            for row in data:
                value = row[attribute]
                category_index = int((value - min_value) // category_width)
                categories[category_index] += 1

            return categories

        cp_len = len(cardio_problem)
        ncp_len = len(no_cardio_problem)

        def calculate_ratio(cp_count, ncp_count):
            return float('inf') if cp_count > 0 and ncp_count == 0 else ((cp_count / cp_len) / (ncp_count / ncp_len) if ncp_count > 0 else 0)

        # Calculate ratios and categories
        attributes = ['height', 'weight', 'Systolic blood pressure', 'Diastolic blood pressure']
        ratios = []

        for attribute in attributes:
            cp_bins = create_bins(attribute, cardio_problem, 5)
            ncp_bins = create_bins(attribute, no_cardio_problem, 5)
            for i in range(1, 6):
                ratio = calculate_ratio(cp_bins[i], ncp_bins[i])
                if ratio > 1:
                    ratios.append((round(ratio, 4), f"{attribute.capitalize()} in category {i} (1 lowest, 5 highest)"))

        # Cholesterol and Glucose
        for attribute in ['cholesterol', 'glucose']:
            cp_counts = categorize(attribute, cardio_problem)
            ncp_counts = categorize(attribute, no_cardio_problem)
            for i in range(3):
                ratio = calculate_ratio(cp_counts[i], ncp_counts[i])
                if ratio > 1:
                    ratios.append((round(ratio, 4), f"{attribute.capitalize()} in category {i+1} (1 lowest, 3 highest)"))

        # Smoking/Drinking/Active ratios
        for attribute in ['smoking', 'drinking', 'being active']:
            cp_count = sum(1 for item in cardio_problem if item[attribute] == 1)
            ncp_count = sum(1 for item in no_cardio_problem if item[attribute] == 1)
            ratio = calculate_ratio(cp_count, ncp_count)
            ratio_i = calculate_ratio(cp_len - cp_count, ncp_len - ncp_count)

            if ratio > 1 and attribute == 'being active':
                ratios.append((round(ratio, 4), f'{attribute.capitalize()}'))
            if ratio > 1 and attribute != 'being active':
                ratios.append((round(ratio, 4), f'Not {attribute}'))   
            if ratio_i > 1 and attribute != 'being active':
                ratios.append((round(ratio_i, 4), f'{attribute.capitalize()}'))
            if ratio_i > 1 and attribute == 'being active':
                ratios.append((round(ratio_i, 4), f'Not {attribute}'))

        ratios.sort(reverse=True)

        print(f"The following might particularly contribute to cardio problems for {"males" if gender == 'M' else 'females'} aged {age}:")
        for ratio, description in ratios:
            print(f"   {ratio:.2f}: {description}")
