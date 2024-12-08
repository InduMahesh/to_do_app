pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "todo-app"  // Name of the Docker image
        DOCKER_REGISTRY = "your-docker-registry" // Replace with your Docker registry (e.g., DockerHub or private registry)
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository...'
                checkout scm  // Automatically clones the repository specified in the Jenkins job
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh '''
                . venv/bin/activate
                pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                docker build -t $DOCKER_IMAGE .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                echo 'Pushing Docker image to registry...'
                sh '''
                docker tag $DOCKER_IMAGE $DOCKER_REGISTRY/$DOCKER_IMAGE
                docker push $DOCKER_REGISTRY/$DOCKER_IMAGE
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Deploying application...'
                sh '''
                docker run -d -p 3000:3000 --name todo-app $DOCKER_IMAGE
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh '''
            docker container rm -f todo-app || true
            docker image rm -f $DOCKER_IMAGE || true
            '''
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
