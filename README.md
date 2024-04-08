1. clone the repo: `git clone https://github.com/balilarder/account-password-api.git`
2. move to the directory: `cd account-password-api`
3. Build the image: `docker build -t <image_name> .`For example, `docker build -t myapp .` Or you can pull the image: `docker push balilarder/myapp:latest`
4. Run the container: `docker run --name <container_name> -p 80:80 <image_name>`
5. The container use 80 port to receive the response
6. Test the API:
(1) http://127.0.0.1:80/user [POST] to create a user

(2) http://127.0.0.1:80/login [POST] to verify the user and its password

(3) http://127.0.0.1:80/users [GET] to list all users

For more detail, please check `API_document.docx`