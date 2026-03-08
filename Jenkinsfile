pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Checking out code...'
                checkout scm
            }
        }

        stage('Docker Test') {
            steps {
                echo '🐳 Testing Docker...'
                sh 'docker --version'
                sh 'docker compose version'
                sh 'docker run --rm hello-world'
            }
        }

        stage('Build Image') {
            steps {
                echo '🔨 Building Django image...'
                sh 'docker build -t django-app:latest .'
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running Django tests...'
                sh '''
                    docker run --rm \
                        -e DEBUG=True \
                        -e SECRET_KEY=test-secret-key \
                        django-app:latest \
                        python manage.py test
                '''
            }
        }

    }

    post {
        success {
            echo '✅ Pipeline passed!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
        always {
            echo '🧹 Cleaning up...'
            sh 'docker rmi django-app:latest || true'
        }
    }
}