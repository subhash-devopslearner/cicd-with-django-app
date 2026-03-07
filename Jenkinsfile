pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    docker-compose run --rm web python manage.py test
                '''
            }
        }

        stage('Build & Start Services') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }

        stage('Run Migrations') {
            steps {
                sh 'docker-compose exec -T web python manage.py migrate'
            }
        }

    }

    post {
        always {
            sh 'docker-compose down'
        }
    }
}