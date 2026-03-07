pipeline {
    
    agent any
    
    options {
        // This stops Jenkins from automatically cloning the repo at the start
        skipDefaultCheckout() 
    }
    
    parameters {
        // 1. Dropdown for branches
        choice(
            name: 'GIT_BRANCH', 
            choices: ['development', 'main'], 
            description: 'Select the branch to build'
        )
    }

    stages {
        stage('Checkout code'){
            steps {
                git branch: "${params.GIT_BRANCH}", url: 'https://github.com/subhash-devopslearner/cicd-with-django-app.git'
            }
        }

        stage('Running test'){
            agent { 
                docker {
                    image 'python:3.12-slim'
                    // IMPORTANT: This mounts the Git code into the container
                    reuseNode true 
                } 
            }
            
            steps{
                sh '''
                pip install --upgrade pip
                pip install -r requirements.txt
                python manage.py test
                '''
            }           
        }

        stage('Build Docker image'){
            // when {
            //     branch 'main'
            // }
            when {
            // This checks what YOU selected in the dropdown
            expression { params.GIT_BRANCH == 'main' }
            }
            
            steps{
                sh 'docker build -t cicd-django .'
            }
        }        
    }

    post {
        success {
            echo 'Pipeline successful.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}