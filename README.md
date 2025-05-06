# Plant Disease Detection

Một ứng dụng web AI/ML để phát hiện bệnh trên cây trồng từ hình ảnh lá. Dự án này sử dụng Flask, PyTorch, và Docker.

## Tính năng

- Phát hiện nhiều loại bệnh trên cây trồng thông qua hình ảnh lá
- Giao diện web thân thiện với người dùng
- Chatbot hỗ trợ thông tin về bệnh và cách điều trị
- Docker hóa để dễ dàng triển khai

## Công nghệ sử dụng

- **Backend**: Flask (Python)
- **ML/AI**: PyTorch
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Docker, Nginx

## Cách triển khai

Dự án được triển khai sử dụng Docker và Nginx làm reverse proxy.

## CI/CD

Dự án sử dụng GitHub Actions để tự động hóa quy trình CI/CD.

## ⭐Run Project in your Machine
* You must have **Python3.8** installed in your machine.
* Create a Python Virtual Environment & Activate Virtual Environment [Link](https://docs.python.org/3/tutorial/venv.html)
* Install all the dependencies using below command
    `pip install -r requirements.txt`
* Go to the `Flask Deployed App` folder.
* Download the pre-trained model file `plant_disease_model_1.pt` from [here](https://drive.google.com/drive/folders/1ewJWAiduGuld_9oGSrTuLumg9y62qS6A?usp=share_link)
* Add the downloaded file in `Flask Deployed App` folder.
* Run the Flask app using below command `python3 app.py`
* You can also use downloaded file in `Model` Section and play with it using Jupyter Notebook.

## ⭐Contribution ( Open Source )
* This Project is now open source.
* All the developers who are intrested they can contribute in this project.
* Yo can make UI better , make Deep learning model more powerful , add informative markdown file in section...
* If you will change Deep learning make sure you upload updated markdown file (.md) , .pdf and .ipynb in particular section.
* Make sure your code is working. It will not have any type or error.
* You have to fork this project then make a pull request after you testing will successful.
* How to make pull request : https://opensource.com/article/19/7/create-pull-request-github


## ⭐Testing Images

* If you do not have leaf images then you can use test images located in test_images folder
* Each image has its corresponding disease name, so you can verify whether the model is working perfectly or not

## ⭐Blog Link
<a href="https://medium.com/analytics-vidhya/plant-disease-detection-using-convolutional-neural-networks-and-pytorch-87c00c54c88f" target = "_blank">Plant Disease Detection Using Convolutional Neural Networks with PyTorch</a><br>

## ⭐Deployed App
<a href="https://plant-disease-detection-ai.herokuapp.com/" target = "_blank">Plant-Disease-Detection-AI</a><br>


## ⭐Snippet of Web App :
#### Main page
<img src = "demo_images/1.png" > <br>
#### AI Engine 
<img src = "demo_images/2.png"> <br>
#### Results Page 
<img src = "demo_images/3.png"> <br>
#### Supplements/Fertilizer  Store
<img src = "demo_images/4.JPG"> <br>
#### Contact Us 
<img src = "demo_images/5.png"> <br><br>
