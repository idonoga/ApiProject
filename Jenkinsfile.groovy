
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
        
        
        stage('users-mysql-container-build-and-run') {
            steps{
            sh """
                docker build -t users-mysql ./MySQLDocker/
                docker run -d -p 3306:3306 --name users-mysql -e MYSQL_ROOT_PASSWORD=password users-mysql
                """
                
            }
        }
        stage('flask-api-container-build-and-run') {
            steps{
            sh """
                docker build -t flask-api ./MyFlaskDocker/
                docker run -d --name flask-api -p 5000:5000 --link users-mysql flask-api
                sleep 5
                """ 
            }
        }
        
      
          stage('testing-api') {
            steps{
                script
                {
                    def STATUS = sh(script: "python3.7 test_api.py | grep 'succeeded'", returnStdout: true)
                    
                    
                   
                   
                }
            }
          }
    }
}
