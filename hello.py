from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

@app.route("/")
def hello():
  return render_template('index.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
  if request.method == 'POST':
    train_file = request.files['train_csv']
    test_file = request.files['test_csv']
    train_file.save(secure_filename(train_file.filename))
    test_file.save(secure_filename(test_file.filename))
    import pdb; pdb.set_trace()
    return 'files uploaded successfully'

if __name__ == '__main__':
  app.run(debug=True)