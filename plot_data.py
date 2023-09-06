import sys
import ast
import os
import pandas as pd
import matplotlib.pyplot as plt

# Check if the correct number of command-line arguments are provided
if len(sys.argv) != 2:
    print("Usage: python script.py input_filename")
    sys.exit(1)

# Get the input filename from the command line argument
txt_filename = sys.argv[1]

# Check if the input file exists
if not os.path.isfile(txt_filename):
    print(f"File '{txt_filename}' not found.")
    sys.exit(1)

# Create a directory for saving plots if it doesn't exist
os.makedirs("plots", exist_ok=True)

# Read data from the txt file and parse it as a list of floats
with open(txt_filename, 'r') as file:
    # Skip lines until the line that starts with '[' is found
    for line in file:
        if line.strip().startswith('['):
            data_line = line.strip()
            break
    else:
        print("No list data found in the file.")
        sys.exit(1)

data_list = ast.literal_eval(data_line)

# Extract the base name of the input file (without extension) for Excel and plot filenames
base_filename = os.path.splitext(os.path.basename(txt_filename))[0]
excel_filename = f"plots/{base_filename}.xlsx"
plot_filename = f"plots/{base_filename}.jpg"  # Change the extension to .jpg

# Create a DataFrame from the indexed data
indexed_data = pd.DataFrame({'Index': range(1, len(data_list) + 1), 'Value': data_list})

# Write the indexed data to an Excel file
indexed_data.to_excel(excel_filename, index=False)

print(f"{excel_filename} has been created")

# Read data from the Excel file
df = pd.read_excel(excel_filename)

# Extract the 'Index' and 'Value' columns
index = df['Index']
value = df['Value']

# Create a line plot
plt.plot(index, value, linestyle='-')
plt.xlabel('Line Number')
plt.ylabel('Time')
plt.title('Plot')
plt.grid(True)

# Annotate the last point on the plot
last_index = index.iloc[-1]
last_value = value.iloc[-1]
annotation_text = f'({last_index}, {last_value:.2f})'
plt.annotate(annotation_text, xy=(last_index, last_value), xytext=(last_index - 200, last_value + 0.02),
             arrowprops=dict(arrowstyle="->"))

# Increase the resolution (DPI) of the saved plot image
plt.savefig(plot_filename, format='jpg', dpi=2500)  # Specify the DPI value (e.g., 300)

print(f"Plot saved as {plot_filename}")

# Show the plot (optional)
plt.show()
