import csv

def convert_to_csv(input_file, output_file):
    with open(input_file, 'r') as in_file, open(output_file, 'w', newline='') as out_file:
        reader = csv.reader(in_file, delimiter='|')
        writer = csv.writer(out_file)

        for row in reader:
            writer.writerow(row)

# Example usage
input_file = 'insurance.csv'  # Replace with the path to your pipe-separated input file
output_file = 'data.csv'  # Replace with the desired path for the output CSV file

convert_to_csv(input_file, output_file)
