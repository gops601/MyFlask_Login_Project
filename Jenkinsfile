pipeline {
    agent any

    environment {
        IMAGE_NAME = "gops601/flask-login-app"
        TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/gops601/MyFlask_Login_Project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${TAG}")
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh "docker stop flask-container || true"
                    sh "docker rm flask-container || true"
                    sh "docker run -d --name flask-container -p 5000:5000 ${IMAGE_NAME}:${TAG}"
                }
            }
        }
    }
}
