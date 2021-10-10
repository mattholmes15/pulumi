import pulumi
from pulumi_gcp import storage

# Create a GCP resource (Storage Bucket)
bucket = storage.Bucket('my-bucket',
    labels={'environment': "dev"})

# Export the DNS name of the bucket
pulumi.export('bucket_name',  bucket.url)