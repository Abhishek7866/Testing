pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('AbhishekDocker')
        IMAGE_NAME = "dockerbatra69/apd-stock-app:v1"
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'AbhishekGit', url: 'https://github.com/Abhishek7866/Testing.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh 'docker push $IMAGE_NAME'
            }
        }

        stage('Deploy to Azure') {
            steps {
                sh 'az webapp config container set --name new-apd-app --resource-group apd-resource-group --docker-custom-image-name $IMAGE_NAME'
            }
        }
    }
}