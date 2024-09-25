import pulumi
import pulumi_aws as aws

# Get the stack name (dev or prod)
stack = pulumi.get_stack()

# Configuration specific to each environment (dev or prod)
config = pulumi.Config()
db_username = config.require("db_username")
db_password = config.require("db_password")

# Define different instance types for dev and prod
rds_instance_class = 'db.t2.micro' if stack == 'dev' else 'db.t3.medium'

# Create an RDS PostgreSQL instance
rds = aws.rds.Instance(f"crypto-price-db-{stack}",
    allocated_storage=20,
    engine="postgres",
    engine_version="12.3",
    instance_class=rds_instance_class,
    name=f"crypto_db_{stack}",
    username=db_username,
    password=db_password,
    skip_final_snapshot=True,
    publicly_accessible=True,
    vpc_security_group_ids=[]  # Update this with actual security group IDs
)

# Create a Lambda function
lambda_role = aws.iam.Role(f"lambdaRole-{stack}",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Effect": "Allow",
            "Sid": ""
        }]
    }"""
)

# Attach policy to allow Lambda to interact with RDS
lambda_policy = aws.iam.RolePolicy(f"lambdaS3Policy-{stack}",
    role=lambda_role.id,
    policy=rds.arn.apply(lambda arn: f"""{{
        "Version": "2012-10-17",
        "Statement": [
            {{
                "Effect": "Allow",
                "Action": [
                    "rds-db:connect"
                ],
                "Resource": "{arn}"
            }}
        ]
    }}""")
)

# Define the Lambda function that calls the API
lambda_function = aws.lambda_.Function(f"cryptoIngestionFunction-{stack}",
    runtime="python3.9",
    role=lambda_role.arn,
    handler="lambda_function.handler",
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./lambda")
    })
)

# Export the Lambda and RDS endpoints
pulumi.export("rds_endpoint", rds.endpoint)
pulumi.export("lambda_function_name", lambda_function.name)
