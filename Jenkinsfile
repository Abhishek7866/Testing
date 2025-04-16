pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('AbhishekDocker')
        IMAGE_NAME = "dockerbatra69/apd-stock-app:v1"
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'AbhishekGit', branch: 'main', url: 'https://github.com/Abhishek7866/Testing.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                export PATH=/usr/local/bin:$PATH
                docker buildx create --use || true
                docker buildx build --platform linux/amd64 -t $IMAGE_NAME --push .
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                sh '''
                export PATH=/usr/local/bin:$PATH
                echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                export PATH=/usr/local/bin:$PATH
                docker push $IMAGE_NAME
                '''
            }
        }

        stage('Azure Login') {
            steps {
                withCredentials([string(credentialsId: 'AZURE_CREDENTIALS', variable: 'AZURE_JSON')]) {
                    sh '''
                    export PATH=/usr/local/bin:/opt/homebrew/bin:$PATH
                    echo "$AZURE_JSON" > azure_creds.json
                    az login --service-principal --username $(jq -r .clientId azure_creds.json) \
                             --password $(jq -r .clientSecret azure_creds.json) \
                             --tenant $(jq -r .tenantId azure_creds.json)
                    '''
                }
            }
        }

        stage('Deploy to Azure') {
            steps {
                sh '''
                export PATH=/usr/local/bin:/opt/homebrew/bin:$PATH
                az webapp config container set --name new-apd-app \
                  --resource-group apd-resource-group \
                  --container-image-name $IMAGE_NAME
                '''
            }
        }
    }
}
