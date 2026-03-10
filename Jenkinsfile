pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Checking out code...'
                checkout scm                
            }
        }
        stage('Get Branch Info'){
            steps{
                echo '📥 Getting branch info...'
                echo "${env.GIT_BRANCH}"
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

        stage('Deploy to staging environment with Docker Compose') {
            when {
                expression { env.GIT_BRANCH == 'origin/development' }
            }
            steps {
                echo '🚀 Deploying with Docker Compose...'
                
                withCredentials([file(credentialsId: 'Django_ENV_STAGING', variable: 'DJANGO_ENV_STAGING')]) {
                       
                    sh '''
                    # Copy .env file from Jenkins credentials to workspace
                    cp $DJANGO_ENV_STAGING .env.staging                  

                    # Stop existing containers
                    # docker compose down

                    # Start all services
                    docker compose --env_file .env.staging -f docker-compose-staging.yml up --build

                    # Wait for db to be healthy
                    echo "Waiting for database..."
                    sleep 10

                    # Run migrations
                    docker compose exec -T web python manage.py migrate

                    # Collect static files
                    docker compose exec -T web python manage.py collectstatic --noinput
                    '''
                }
            }
                
        }
        
        stage('Deploy to production environment with Docker Compose') {
            when {
                expression { env.GIT_BRANCH == 'origin/main' }
            }
            steps {
                echo '🚀 Deploying with Docker Compose...'

                withCredentials([file(credentialsId: 'Django_ENV_PRODUCTION', variable: 'DJANGO_ENV_PRODUCTION')]) {
                       
                    sh '''
                    # Copy .env file from Jenkins credentials to workspace
                    cp $DJANGO_ENV_PRODUCTION .env.production              

                    # Stop existing containers
                    # docker compose down

                    # Start all services
                    docker compose --env_file .env.production -f docker-compose-production.yml up -d --build

                    # Wait for db to be healthy
                    echo "Waiting for database..."
                    sleep 10

                    # Run migrations
                    docker compose exec -T web python manage.py migrate

                    # Collect static files
                    docker compose exec -T web python manage.py collectstatic --noinput
                '''
                }
                
            }
        }

    }

    post {
        success {
            echo '✅ Pipeline passed! App is live!'
        }
        failure {
            echo '❌ Pipeline failed!'
            //sh 'docker compose logs'
        }
        always {
            echo '🧹 Cleaning up unused images...'
            sh 'rm -f .env.*'
            //sh 'docker image prune -f'
        }
    }
}