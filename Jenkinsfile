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
                    docker compose -f docker-compose-staging.yml --env-file .env.staging down

                    # Start all services
                    docker compose -f docker-compose-staging.yml --env-file .env.staging up --build -d

                    # Wait for db to be healthy
                    # echo "Waiting for database..."
                    # sleep 10

                    echo "Waiting for database to be healthy..."
                    until docker compose -f docker-compose-staging.yml \
                        exec -T db pg_isready -U $DB_USER; do
                        echo "Still waiting..."
                        sleep 2
                    done
                    echo "Database ready! ✅"

                    # Run migrations                    
                    docker compose -f docker-compose-staging.yml --env-file .env.staging exec -T web python manage.py migrate


                    # Collect static files
                    docker compose -f docker-compose-staging.yml --env-file .env.staging exec -T web python manage.py collectstatic --noinput
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
                    docker compose -f docker-compose-production.yml --env-file .env.production down

                    # Start all services
                    docker compose -f docker-compose-production.yml --env-file .env.production up --build -d

                    # Wait for db to be healthy
                    echo "Waiting for database..."
                    sleep 10

                    # Run migrations
                    docker compose -f docker-compose-production.yml --env-file .env.production exec -T web python manage.py migrate

                    # Collect static files
                    docker compose -f docker-compose-production.yml --env-file .env.production exec -T web python manage.py collectstatic --noinput
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
            echo '❌ Pipeline failed! Check logs for details.'
            steps {
                if (env.GIT_BRANCH == 'origin/development') {
                    echo '📋 Staging logs:'
                    sh 'docker compose -f docker-compose-staging.yml logs --tail=50'
                } else if (env.GIT_BRANCH == 'origin/main') {
                    echo '📋 Production logs:'
                    sh 'docker compose -f docker-compose-production.yml logs --tail=50'
                }            
            }
        }
        always {
            echo '🧹 Cleaning up unused images...'
            sh 'rm -f .env.* || true' // Clean up .env files
            sh 'docker image prune -f || true' // Clean up dangling images
        }
    }    
}