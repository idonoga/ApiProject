
pipeline {
    agent any
    
    stages {
        
        stage('Initializing-Workspace') {
            steps{
                echo "Starting the environment"
                cleanWs()
                
                sh """
                yum install -y docker git 
                git clone -b ${BRANCH_NAME} https://${GIT_USER}:${GIT_PASSWORD}@${GIT_REPO} .
                """
                script
                {
                    try
                    {
                        sh """
                        docker stop users-mysql
                        docker rm users-mysql
                        """
                    }
                    catch(Exception ex)
                    {
                        echo "sql container is not running"
                    }
                    
                    
                    try
                    {
                        sh """
                        docker stop flask-api
                        docker rm flask-api
                        """
                    }
                    catch(Exception ex)
                    {
                        echo "flask-api is not running"
                    }
                }
            }
        }
        
        
        stage('users-mysql-container-build') {
            steps{
            sh """
                docker build -t users-mysql ./MySQLDocker/
                docker run -d --name users-mysql -p 3306:3306 users-mysql
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
