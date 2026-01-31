## Process of getting temporary access keys for AWS to access S3
### 1. Use the s3-bucket-admin user which has permission to assume the role of s3-admin-role
export ACCOUNT_ID="164788107070"
export USER_NAME="s3-bucket-admin"
export ROLE_NAME="s3-admin-role"
export EXTERNAL_ID="test-external-id-1122"

### Select the profile

aws configure --profile s3-bucket-admin

### Assume the role

aws sts assume-role \
  --profile s3-bucket-admin \
  --role-arn "arn:aws:iam::164788107070:role/$ROLE_NAME" \
  --role-session-name "s3-bucket-admin-$(date +%s)" \
  --external-id "$EXTERNAL_ID" >> credential.json

CREDS_JSON="$(cat credential.json)"

export AWS_ACCESS_KEY_ID=$(echo "$CREDS_JSON" | jq -r '.Credentials.AccessKeyId')
export AWS_SECRET_ACCESS_KEY=$(echo "$CREDS_JSON" | jq -r '.Credentials.SecretAccessKey')
export AWS_SESSION_TOKEN=$(echo "$CREDS_JSON" | jq -r '.Credentials.SessionToken')

### Verify the assumed identity

aws sts get-caller-identity

## DVC configuraiton

### DVC configure remote S3 bucket for storing large files

- List remotes > dvc remote list
  output - s3remote_for_sd_data s3://psaw-data-lake-bucket-1    (default)
- dvc remote add -d s3remote_for_sd_data s3://dvc-stable-defusion-training-dataset

### DVC configure S3 Credentials
Just exporting AWS credential into environment variables is enough.
If not use the following commands.

- dvc remote modify --local mys3remote access_key_id 'ASIA...'
- dvc remote modify --local mys3remote secret_access_key '...'
- dvc remote modify --local mys3remote session_token '...'

or change the AWS profile

- dvc remote modify mys3remote profile your-aws-profile

### DVC change remote S3 URL
dvc remote modify s3remote_for_sd_data --unset endpoint
dvc remote modify s3remote_for_sd_data endpointurl s3://dvc-stable-defusion-training-dataset