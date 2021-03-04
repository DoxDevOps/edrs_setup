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
        echo 'Giving all users access to the folder'
        sh 'chmod 777 $WORKSPACE/edrs_facility'
        echo 'Change directory to edrs_facility'
        sh 'cd $WORKSPACE/edrs_facility && git pull'
        echo 'Fetching tags'
        sh 'cd $WORKSPACE/edrs_facility && git fetch --tags -f'
        echo 'Checking out to latest tag'
        sh 'cd $WORKSPACE/edrs_facility && latestTag=$(git describe --tags `git rev-list --tags --max-count=1`) && git checkout $latesttag'
        sh 'cd $WORKSPACE/edrs_facility && git describe > HEAD'
      }
    }

    stage('Configuring EDRS') {
      parallel {
        stage('Fetching touchscreentoolkit') {
          steps {
            echo 'Checking if touchscreentoolkit already exists'
            sh '[ -d "$WORKSPACE/edrs_facility/public/touchscreentoolkit" ] && echo "touchscreentoolkit already cloned." || git clone https://github.com/HISMalawi/touchscreentoolkit.git $WORKSPACE/edrs_facility/public/touchscreentoolkit'
            echo 'Pulling to check for latest changes'
            sh 'cd $WORKSPACE/edrs_facility/public/touchscreentoolkit && git pull'
            echo 'all changes up-to-date'
          }
        }

        stage('Fetching couchdb-dump') {
          steps {
            echo 'Checking if couchdb-dump already exists'
            sh '[ -d "$WORKSPACE/edrs_facility/bin/couchdb-dump" ] && echo "couchdb-dump already cloned." || git clone https://github.com/danielebailo/couchdb-dump.git $WORKSPACE/edrs_facility/bin/couchdb-dump'
            echo 'Pulling to check latest changes'
            sh 'cd $WORKSPACE/edrs_facility/bin/couchdb-dump && git pull'
            echo 'Renaming couchdb-dump.sh to couchdb-backup.sh'
            sh '[ -f "$WORKSPACE/edrs_facility/bin/couchdb-dump/couchdb-backup.sh" ] && echo "couchdb-backup.sh already exists." || mv $WORKSPACE/edrs_facility/bin/couchdb-dump/couchdb-dump.sh $WORKSPACE/edrs_facility/bin/couchdb-dump/couchdb-backup.sh'
          }
        }

        stage('Copying .example files to .yml files') {
          steps {
            echo 'Changes taking place inside config folder'
            sh '[ -f "$WORKSPACE/edrs_facility/config/couchdb.yml" ] && echo "couchdb.yml already exists." || cp $WORKSPACE/edrs_facility/config/couchdb.yml.example $WORKSPACE/edrs_facility/config/couchdb.yml'
            echo 'Editing couchdb.yml file [replacing dc with facility]'
            sh 'sed -i \'s/dc/facility/\' $WORKSPACE/edrs_facility/config/couchdb.yml'
            sh '[ -f "$WORKSPACE/edrs_facility/config/database.yml" ] && echo "database.yml already exists." || cp $WORKSPACE/edrs_facility/config/database.yml.example $WORKSPACE/edrs_facility/config/database.yml'
            echo 'Editing database.yml file [replacing edrs_fc with edrs_fc'
            sh 'sed -i \'s/edrs_dc/edrs_fc/\' $WORKSPACE/edrs_facility/config/database.yml'
            sh '[ -f "$WORKSPACE/edrs_facility/config/db_mapping.yml" ] && echo "db_mapping.yml already exists." || cp $WORKSPACE/edrs_facility/config/db_mapping.yml.example $WORKSPACE/edrs_facility/config/db_mapping.yml'
            sh '[ -f "$WORKSPACE/edrs_facility/config/elasticsearchsetting.yml" ] && echo "elasticsearchsetting.yml already exists." || cp $WORKSPACE/edrs_facility/config/elasticsearchsetting.yml.example $WORKSPACE/edrs_facility/config/elasticsearchsetting.yml'
            sh '[ -f "$WORKSPACE/edrs_facility/config/secrets.yml" ] && echo "secrets.yml already exists." || cp $WORKSPACE/edrs_facility/config/secrets.yml.example $WORKSPACE/edrs_facility/config/secrets.yml'
            sh '[ -f "$WORKSPACE/edrs_facility/config/settings.yml" ] && echo "settings.yml already exists." || cp $WORKSPACE/edrs_facility/config/settings.yml.example $WORKSPACE/edrs_facility/config/settings.yml'
            echo 'Editing settings.yml'
            sh 'sed -i \'s/\\/home\\/usr\\/barcodes\\//\\/var\\/www\\/edrs_facility\\/config\\//; s/\\/home\\/usr\\/certificates\\//\\/var\\/www\\/edrs_facility\\/config\\//; s/\\/home\\/usr\\/dispatch\\//\\/var\\/www\\/edrs_facility\\/config\\//; s/\\/home\\/usr\\/qrcodes\\//\\/var\\/www\\/edrs_facility\\/config\\//\' $WORKSPACE/edrs_facility/config/settings.yml'
            sh '[ -f "$WORKSPACE/edrs_facility/config/sync_settings.yml" ] && echo "sync_settings.yml already exists." || cp $WORKSPACE/edrs_facility/config/sync_settings.yml.example $WORKSPACE/edrs_facility/config/sync_settings.yml'
          }
        }

      }
    }

    stage('Shipping to remote server') {
      steps {
        sh 'rsync -a $WORKSPACE/edrs_facility opsuser@10.44.0.52:/home/opsuser'
      }
    }

    stage('Remote Server Configuration') {
      steps {
        echo 'Editng District id and Facility Code'
        sh '''#OpsUser
ssh opsuser@10.44.0.52 "sed -i \'s/facility_code\\:/facility_code\\: 11111/; s/district_code\\:/district_code\\: DV1/\' /home/opsuser/edrs_facility/config/settings.yml"
'''
      }
    }

  }
}