# AI20S - HW0
# Student ID                :B06902102
# English Name              :Fernando Lopez
# Chinese Name (optional)   :羅費南


# Import packages here
import numpy as np
from sklearn.linear_model import LinearRegression


class Predictor:
    def __init__(self, dataset_path='salary_data.csv'):
        self.test = 0
        self.dataset_data, self.dataset_target = self.read_csv(dataset_path)
        self.model = self.train()

    @staticmethod
    def read_csv(file_path='salary_data.csv'):
        # Implement your CSV file reading here
        # returns data, target
        # Both outputs should be in numpy array format with type np.float64
        # You may reshape the array if necessary
        f = open(file_path, 'r')
        reading = np.genfromtxt(file_path,delimiter=',',dtype=np.float64,skip_header=1)
        data = (reading[:,0]).reshape((-1,1))
        target = (reading[:,1].reshape((-1,1)))
        f.close()
        return data, target

    def train(self):
        # returns sklearn's fitted LinearRegression model
        # Remember to pass self.dataset_data and self.dataset_target as its parameters
        return LinearRegression().fit(self.dataset_data, self.dataset_target)

    def predict(self, x):
        # returns model's prediction given x as input
        predict_model = self.train()
        return predict_model.predict(x)

    def write_prediction(self, x, write_path='prediction.txt'):
        # opens a file using write_path with a writeable access
        # write all the outputs from the model's prediction to the file
        # You must write the output line by line instead of writing its numpy array or list object
        # This method does not return anything
        f = open(write_path, 'w')
        prediction = self.predict(x)
        rounded_p = np.around(prediction, 2)
        for i in rounded_p:
            print(i, file = f)
        f.close()
        return


if __name__ == '__main__':
    # You may test your program here
    # Anything residing in this block will not be graded
    print("Good luck!")
    p = Predictor()
    test_x = np.zeros(5).reshape(-1,1)
    for i in range(0,5):
        test_x[i][0] = (i+2)*2
    #print(p.predict(test_x))
    #print(p.train(p))
    p.write_prediction(test_x)
