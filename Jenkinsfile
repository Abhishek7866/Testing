pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('AbhishekDocker')
        IMAGE_NAME = "dockerbatra69/apd-stock-app:v1"
        CUSTOM_PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    }

    stages {
        stage('Checkout') {
            steps {
                // Ensure Git is in PATH
                sh '''
                export PATH=$CUSTOM_PATH:$PATH
                git --version
                git clone https://github.com/Abhishek7866/Testing.git
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                export PATH=$CUSTOM_PATH:$PATH
                docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                sh '''
                export PATH=$CUSTOM_PATH:$PATH
                echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                export PATH=$CUSTOM_PATH:$PATH
                docker push $IMAGE_NAME
                '''
            }
        }

        stage('Deploy to Azure') {
            steps {
                sh '''
                export PATH=$CUSTOM_PATH:$PATH
                az webapp config container set --name new-apd-app --resource-group apd-resource-group --docker-custom-image-name $IMAGE_NAME
                '''
            }
        }
    }
}
