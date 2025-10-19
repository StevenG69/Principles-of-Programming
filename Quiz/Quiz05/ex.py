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

            if min_value == max_value:
                return {0: len(data)}
              
            category_width = 1
            num_categories = max(1, (max_value - min_value) // category_width + 1)
            categories = defaultdict(int)

            for row in data:
                value = row[attribute]
                category_index = int((value - min_value) // category_width)
                categories[category_index] += 1

            return categories

        def calculate_ratio(cp_count, ncp_count):
            return float('inf') if cp_count > 0 and ncp_count == 0 else ((cp_count / len(cardio_problem)) / (ncp_count / len(no_cardio_problem))  if ncp_count > 0 else 0)

        # Calculate ratios and categories
        attributes = ['height', 'weight', 'Systolic blood pressure', 'Diastolic blood pressure']
        ratios = []

        for attribute in attributes:
            cp_bins = create_bins(attribute, cardio_problem, 5)
            ncp_bins = create_bins(attribute, no_cardio_problem, 5)
            for i in range(1, 6):
                ratio = calculate_ratio(cp_bins[i], ncp_bins[i])
                if ratio > 1:
                    ratios.append((round(ratio, 2), f"{attribute.capitalize()} in category {i} (1 lowest, 5 highest)"))

        # Cholesterol and Glucose
        for attribute in ['cholesterol', 'glucose']:
            cp_counts = categorize(attribute, cardio_problem)
            ncp_counts = categorize(attribute, no_cardio_problem)
            for i in range(1, 4):
                ratio = calculate_ratio(cp_counts[i], ncp_counts[i])
                if ratio > 1:
                    ratios.append((round(ratio, 2), f"{attribute.capitalize()} in category {i+1} (1 lowest, 3 highest)"))

        # Smoking/Drinking/Active ratios
        for attribute in ['smoking', 'drinking', 'being active']:
            cp_count = sum(item[attribute] == 0 for item in cardio_problem)
            ncp_count = sum(item[attribute] == 0 for item in no_cardio_problem)
            ratio = calculate_ratio(cp_count, ncp_count)
            
            if ratio > 1 and attribute == 'being active' or ratio < 1 and attribute != 'being active':
                ratios.append((round(ratio, 2), f'Not {attribute}'))
            if ratio < 1 and attribute == 'being active' or ratio > 1 and attribute != 'being active':
                ratios.append((round(ratio, 2), f'{attribute.capitalize()}'))

        ratios.sort(reverse=True)

        print(f"The following might particularly contribute to cardio problems for {"males" if gender == 'M' else 'females'} aged {age}:")
        for ratio, description in ratios:
            print(f"   {ratio:.2f}: {description}")

# Example of calling the function
analyse('F', 43)
analyse('M', 58)