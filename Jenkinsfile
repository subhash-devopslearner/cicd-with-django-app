pipeline {
    agent any

    stages{
        stage('Code checkout'){
            steps{
                checkout scm
            }
        }

        stage('Build Django docker image'){
            steps{
                'docker build -t django_demo:latest .'
            }
        }
        stage('Run Postgres Container'){
            steps{
                sh'''
                docker network create test-network 
                docker run -d \
                -- name test-postgres \
                -- network test-network \
                -e POSTGRES_DB=testdb \
                -e POSTGES_USER=testuser \
                -e POSTGRES_PASSWORD=testpass \
                postgres:15

                sleep 5

                docker run 
                
                docker run --rm \
                -- name test-django \
                -- network test-network \
                -e DEBUG=true \
                -e SECRET_KEY=my-secret-key \
                -e DB_NAME=testdb \
                -e DB_USER=testuser \
                -e DB_PASSWORD=testpass \
                -e DB_HOST=test-postgres \
                -e DB_PORT=5432 \
                django_demo:latest \
                python manage.py test
                '''
            }
        }
    }
    post {
        success {
            echo 'Pipeline successful'
        }
        failure {
            echo 'Pipeline failed'
        }
        always {
            sh 'docker stop test-postgres || true'
            sh 'docker rm test-postgres || true'
            sh 'docker network rm test-network || true'
            sh 'docker rmi django_demo:latest || true'
        }
    }
}