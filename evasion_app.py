from flask import Flask, render_template, request
from werkzeug import secure_filename
import model
import classifiers
import os

app = Flask(__name__)

@app.route("/")
def evasion_app():
  return render_template('index.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
  if request.method == 'POST':
    train_file = request.files['train_csv']
    test_file = request.files['test_csv']
    train_file.save(secure_filename('train_file.csv'))
    test_file.save(secure_filename('test_file.csv'))
    estimators = train_classifiers()
    results = test(estimators)

    return render_template('results.html', results=results)

def train_classifiers():
  df = model.model2('train_file.csv')
  best_estimators = classifiers.train(df)
  return best_estimators

def test(estimators):
  test_df = model.model2('test_file.csv')
  feature_cols = test_df.columns.difference(['StatusFinal', 'StudentId'])
  features = test_df.loc[:, feature_cols] # we want all rows and the features columns

  predictions = []
  for estimator in estimators:
    predictions.append(estimator.predict(features))

  results = []
  for index, student in test_df.StudentId.items():
    results.append([student, predictions[0][index], predictions[1][index]])

  return results

if __name__ == '__main__':
  app.debug = True
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)