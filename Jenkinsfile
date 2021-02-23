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
        echo 'Starting to fetch EDRS application from GitHub'
        echo 'Checking if edrs_facility folder already exists'
        sh '[ -d "edrs_facility" ] && echo "edrs_facility already cloned." || git clone https://github.com/HISMalawi/edrs_dc.git edrs_facility'
        echo 'Change directory to edrs_facility'
        sh 'cd $WORKSPACE/edrs_facility && git pull'
        echo 'All changes are up-to-date.'
      }
    }

    stage('Fetching') {
      parallel {
        stage('Fetching touchscreentoolkit') {
          steps {
            echo 'Changing directory to public'
            sh 'cd $WORKSPACE/edrs_facility/public'
            echo 'Checking if touchscreentoolkit already exists'
            sh '[ -d "touchscreentoolkit" ] && echo "touchscreentoolkit already cloned." || git clone https://github.com/HISMalawi/touchscreentoolkit.git'
            echo 'Changing directory to touchscreentoolkit'
            sh 'cd $WORKSPACE/edrs_facility/public/touchscreentoolkit && git pull'
            echo 'all changes up-to-date'
          }
        }

        stage('Fetching couchdb-dump') {
          steps {
            echo 'Changing directory to bin'
            sh 'cd $WORKSPACE/edrs_facility/bin'
            echo 'Checking if couchdb-dump already exists'
            sh '[ -d "couchdb-dump" ] && echo "couchdb-dump already cloned." || git clone https://github.com/danielebailo/couchdb-dump.git $WORKSPACE/edrs_facility/bin/couchdb-dump'
            echo 'Changing directory to couchdb-dump'
            sh 'chmod 777 couchdb-dump'
            sh 'cd $WORKSPACE/edrs_facility/bin/couchdb-dump'
            echo 'Renaming couchdb-dump.sh to couchdb-backup.sh'
            sh 'mv couchdb-dump.sh couchdb-backup.sh'
          }
        }

      }
    }

  }
}