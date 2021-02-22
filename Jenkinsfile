pipeline {
  agent any
  stages {
    stage('Initializing') {
      steps {
        echo 'Initializing pipeline'
      }
    }

    stage('Fetching EDRS Repo') {
      steps {
        echo 'sStarting to fetch'
        sh 'git clone https://github.com/HISMalawi/edrs_dc.git edrs_facility'
      }
    }

  }
}