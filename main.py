import csv

# Inside the loop after calculating the score

# Create data to be saved in CSV
data = []
data.append(["Question No.", "User Answer", "Correct Answer", "Correct?"])
for i in range(questions):
    data.append([i+1, myIndex[i], ans[i], grading[i]])

# Save data to CSV
with open('results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)