import Matplotlib.pyplot as plt

subjects = ['Math', 'Science', 'English', 'History']
marks = [85, 90, 78, 92]
plt.bar(subjects,marks,color='pink')
plt.title("Bar Chart")
plt.xlabel('subjects')
plt.ylabel('marks')
plt.show()
