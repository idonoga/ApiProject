
pipeline {
    agent any
    
    stages {
        
        stage('flask-container-build') {
            steps{
                cleanWs()
                echo "Building flask container"
                sh """
                
                """
                
            }
        }
        stage('ngnix-container-build') {
            steps{
            sh """
                
                """
                
            }
        }
        stage('run-containers') {
            steps{
            sh """
                
                """
                
            }
        }
    }
}
