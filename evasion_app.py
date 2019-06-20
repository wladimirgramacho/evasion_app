from flask import Flask, render_template, request
from werkzeug import secure_filename
import model
import predict
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
    classifiers = train_classifiers()
    return classifiers

def train_classifiers():
  df1 = model.model1('train_file.csv')
  df2 = model.model2('train_file.csv')
  best_estimators1 = predict.predict(df1)
  best_estimators2 = predict.predict(df2)
  return best_estimators1.append(best_estimators2)

if __name__ == '__main__':
  app.debug = True
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)