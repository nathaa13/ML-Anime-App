pipeline {
  agent any
  
  stages{

    stage('Clone Repository') {
        /* Cloning the repository to our workspace */
        steps {
            checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/nathaa13/ML-Anime-App.git']])
        }
    }
        
    stage("Login to Docker hub"){
            steps {

              withCredentials([usernamePassword(credentialsId: 'animeapp', passwordVariable: 'dockerhub_pwd', usernameVariable: 'dockerhub_login')]) {
                
                bat 'docker login -u nathaaa13 -p nathaa3004'
              }  
            }
        }

    stage('Docker Build'){
      steps{

        bat 'docker-compose up --build -d'

        
      }
    }
    stage('Push'){
      steps{
        bat 'docker push nathaaa13/anime_app:latest'
      }
    } 
    stage('Test'){
      steps{
        echo 'Testing..'
        /* bat 'python app.py'  */
      }
    } 
    
    
   }

}
