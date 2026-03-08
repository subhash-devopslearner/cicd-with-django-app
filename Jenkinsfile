pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Checking out code...'
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                echo '🔨 Building Django image...'
                sh 'docker build -t django_demo:latest .'
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running tests with SQLite...'
                sh '''
                    docker run --rm \
                        -e SECRET_KEY=test-secret-key \
                        -e DEBUG=True \
                        django_demo:latest \
                        python manage.py test --settings=cicddjango.settings_test
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo '🚀 Deploying with Docker Compose...'
                sh '''
                    # Copy .env from VM home directory
                    cp /var/lib/jenkins/.env .env

                    # Stop existing containers
                    docker-compose down

                    # Start all services
                    docker-compose up -d --build

                    # Wait for db to be healthy
                    echo "Waiting for database..."
                    sleep 10

                    # Run migrations
                    docker-compose exec -T web python manage.py migrate

                    # Collect static files
                    docker-compose exec -T web python manage.py collectstatic --noinput
                '''
            }
        }

    }

    post {
        success {
            echo '✅ Pipeline passed! App is live!'
        }
        failure {
            echo '❌ Pipeline failed!'
            sh 'docker-compose logs'
        }
        always {
            echo '🧹 Cleaning up unused images...'
            sh 'docker image prune -f'
        }
    }
}