import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Load dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/car/car.data"
columns = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "class"]
data = pd.read_csv(url, names=columns, header=None)

# Preprocess dataset
data["buying"] = data["buying"].replace({"low": 0, "med": 1, "high": 2, "vhigh": 3})
data["maint"] = data["maint"].replace({"low": 0, "med": 1, "high": 2, "vhigh": 3})
data["doors"] = data["doors"].replace({"2": 0, "3": 1, "4": 2, "5more": 3})
data["persons"] = data["persons"].replace({"2": 0, "4": 1, "more": 2})
data["lug_boot"] = data["lug_boot"].replace({"small": 0, "med": 1, "big": 2})
data["safety"] = data["safety"].replace({"low": 0, "med": 1, "high": 2})
data["class"] = data["class"].replace({"unacc": 0, "acc": 1, "good": 2, "vgood": 3})

# Select relevant features and target
x = data[["maint", "doors", "lug_boot", "safety", "class"]]
y = data["buying"]

# Split dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y)

# Train machine learning model
model = DecisionTreeClassifier()
model.fit(x_train, y_train)

# Evaluate model on testing set
score = model.score(x_test, y_test)
print("Accuracy:", score)

# Use trained model to make a prediction on the input parameters
input_params = pd.DataFrame({"maint": [2], "doors": [2], "lug_boot": [2], "safety": [2], "class": [2]})
prediction = model.predict(input_params)
print("Prediction:", prediction)
