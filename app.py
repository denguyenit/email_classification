from flask import Flask, request, render_template
import pickle
from preprocessing_data import find_body_email
from preprocessing_data import clean_special_paragraph
from preprocessing_data import pre_processing

app = Flask(__name__)
model = pickle.load(open('linearsvc.pkl', 'rb'))
svd = pickle.load(open('svd.pkl', 'rb'))
vect = pickle.load(open('vect.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    string_features = [str(x) for x in request.form.values()]
    
    subject = string_features[0]
    subject = clean_special_paragraph(subject)
    subject = pre_processing(subject)

    content = string_features[1]
    content = find_body_email(content)
    content = clean_special_paragraph(content)
    content = pre_processing(content)

    final_text = " ".join([subject, content])

    tdifvector = vect.transform([final_text])
    tsvd = svd.transform(tdifvector)
    result = model.predict(tsvd)

    output = ""
    if result == 0:
        output = "Service Request"
    elif result ==1:
        output = "Incident"

    return render_template('index.html', prediction_text='Type email: {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)